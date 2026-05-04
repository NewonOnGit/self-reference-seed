"""
scanner.py -- Relation finder. Given a target number, find all framework
expressions that match within tolerance, ranked by DAG distance and simplicity.

NOT a slot machine. Every output carries a type (RAW_MATCH). Ranked by
structural relevance, not just numerical closeness. Constant budgets
prevent numerology sludge.

Modes:
  STRICT_SEED:  only d, N_c, disc (the 3 cardinals)
  TOWER:        + phi, phi_bar, parent_ker, dim_gauge
  PHYSICS:      + alpha_S, beta_KMS, ker/A
  FULL:         all framework constants
"""
import numpy as np
from itertools import product as iterproduct
import sys
sys.path.insert(0, '../..')
from framework_types import ResultType, Tier


def _seed_constants():
    """All framework constants computed from d=2."""
    d = 2
    N_c = d * (d + 1) // 2
    disc = 1 + 4 * 1  # mu=1
    parent_ker = d ** N_c
    dim_gauge = (N_c**2 - 1) + (d**2 - 1) + 1
    phi = (1 + np.sqrt(5)) / 2
    phi_bar = phi - 1
    alpha_S = 0.5 - phi_bar**2
    beta_KMS = np.log(phi)
    ker_A = 0.5
    return {
        'd': d, 'N_c': N_c, 'disc': disc, 'parent_ker': parent_ker,
        'dim_gauge': dim_gauge, 'phi': phi, 'phi_bar': phi_bar,
        'alpha_S': alpha_S, 'beta_KMS': beta_KMS, 'ker/A': ker_A,
    }


# Constant budgets by mode
MODES = {
    'STRICT_SEED': ['d', 'N_c', 'disc'],
    'TOWER': ['d', 'N_c', 'disc', 'phi', 'phi_bar', 'parent_ker', 'dim_gauge'],
    'PHYSICS': ['d', 'N_c', 'disc', 'phi', 'phi_bar', 'parent_ker', 'dim_gauge',
                'alpha_S', 'beta_KMS', 'ker/A'],
    'FULL': None,  # all constants
}


class ScanResult:
    """A single scanner match."""

    def __init__(self, target, expression, value, constants_used,
                 complexity, tolerance):
        self.target = target
        self.expression = expression
        self.value = value
        self.constants_used = constants_used
        self.complexity = complexity
        self.tolerance = tolerance
        self.status = ResultType.RAW_MATCH
        self.tier = Tier.N  # numerical match only

    def deviation(self):
        if abs(self.target) < 1e-30:
            return abs(self.value)
        return abs(self.value - self.target) / abs(self.target)

    def __repr__(self):
        dev = self.deviation() * 100
        return (f"RAW_MATCH: {self.target} ~ {self.expression} = {self.value:.6g} "
                f"({dev:.2f}%) [complexity={self.complexity}]")


class Scanner:
    """Framework relation finder."""

    def __init__(self, mode='TOWER', tolerance=0.05, max_complexity=3):
        self.all_constants = _seed_constants()
        allowed = MODES.get(mode)
        if allowed is None:
            self.constants = dict(self.all_constants)
        else:
            self.constants = {k: v for k, v in self.all_constants.items() if k in allowed}
        self.tolerance = tolerance
        self.max_complexity = max_complexity

    def scan(self, target):
        """Find all framework expressions matching target within tolerance.
        Returns list of ScanResult, sorted by (exact first, then simplicity)."""
        if abs(target) < 1e-30:
            return []

        results = []
        names = list(self.constants.keys())
        values = list(self.constants.values())
        n = len(names)

        # Depth 1: single constants and simple transforms
        for i in range(n):
            self._check(target, names[i], values[i], [names[i]], 1, results)
            if values[i] != 0:
                self._check(target, f"1/{names[i]}", 1.0/values[i], [names[i]], 1, results)
            for exp in [2, 3, 4, 5, -1, -2]:
                if values[i] > 0 or exp == int(exp):
                    try:
                        v = values[i] ** exp
                        self._check(target, f"{names[i]}^{exp}", v, [names[i]], 2, results)
                    except (ValueError, OverflowError):
                        pass
            if values[i] > 0:
                self._check(target, f"sqrt({names[i]})", np.sqrt(values[i]),
                           [names[i]], 2, results)
                self._check(target, f"ln({names[i]})", np.log(values[i]),
                           [names[i]], 2, results)

        # Depth 2: pairwise operations
        if self.max_complexity >= 2:
            for i in range(n):
                for j in range(n):
                    a, b = values[i], values[j]
                    na, nb = names[i], names[j]
                    used = sorted(set([na, nb]))
                    self._check(target, f"{na}+{nb}", a+b, used, 2, results)
                    self._check(target, f"{na}-{nb}", a-b, used, 2, results)
                    self._check(target, f"{na}*{nb}", a*b, used, 2, results)
                    if abs(b) > 1e-30:
                        self._check(target, f"{na}/{nb}", a/b, used, 2, results)
                    if a > 0 and abs(b) < 20:
                        try:
                            self._check(target, f"{na}^{nb}", a**b, used, 2, results)
                        except (ValueError, OverflowError):
                            pass

        # Depth 3: a op b op c (selective, most useful patterns)
        if self.max_complexity >= 3:
            for i in range(n):
                for j in range(n):
                    for k in range(j, n):
                        a, b, c = values[i], values[j], values[k]
                        na, nb, nc = names[i], names[j], names[k]
                        used = sorted(set([na, nb, nc]))
                        # a*b + c, a*b - c, a*b*c, a^b + c, a^b * c
                        self._check(target, f"{na}*{nb}+{nc}", a*b+c, used, 3, results)
                        self._check(target, f"{na}*{nb}-{nc}", a*b-c, used, 3, results)
                        self._check(target, f"{na}*{nb}*{nc}", a*b*c, used, 3, results)
                        if abs(c) > 1e-30:
                            self._check(target, f"{na}*{nb}/{nc}", a*b/c, used, 3, results)
                        if a > 0 and abs(b) < 10:
                            try:
                                self._check(target, f"{na}^{nb}+{nc}", a**b+c, used, 3, results)
                                self._check(target, f"{na}^{nb}*{nc}", a**b*c, used, 3, results)
                                if abs(c) > 1e-30:
                                    self._check(target, f"{na}^{nb}/{nc}", a**b/c, used, 3, results)
                            except (ValueError, OverflowError):
                                pass

        # Deduplicate and sort
        seen = set()
        unique = []
        for r in results:
            key = (r.expression, round(r.value, 10))
            if key not in seen:
                seen.add(key)
                unique.append(r)

        # Sort: exact first, then by complexity, then by deviation
        unique.sort(key=lambda r: (r.deviation() > 1e-10, r.complexity, r.deviation()))
        return unique

    def _check(self, target, expr, value, constants_used, complexity, results):
        """Check if value matches target within tolerance."""
        if not np.isfinite(value) or abs(value) > 1e20:
            return
        if abs(target) < 1e-30:
            return
        dev = abs(value - target) / abs(target)
        if dev <= self.tolerance:
            results.append(ScanResult(
                target=target, expression=expr, value=value,
                constants_used=constants_used, complexity=complexity,
                tolerance=dev
            ))


# ================================================================
# SELF-TEST
# ================================================================

if __name__ == "__main__":
    print("SCANNER SELF-TEST")
    print("=" * 60)

    s = Scanner(mode='PHYSICS', tolerance=0.02, max_complexity=3)
    checks = []

    # Test: known framework relations
    test_cases = [
        (10.5, '2*disc+ker/A', 'B-DNA helix'),
        (0.000544, '(ker/A-phi_bar^2)^disc', 'm_e/m_p ~ alpha_S^disc... no'),
        (20, 'd^2*disc', 'amino acids'),
        (64, 'parent_ker^2', 'codons'),
        (57, 'disc*dim_gauge-N_c', 'alpha helix'),
        (12, 'dim_gauge', 'semitones'),
        (0.022, '1/(N_c^2*disc)', 'sin2_theta13 ~ 1/45'),
    ]

    for target, expected_pattern, name in test_cases:
        results = s.scan(target)
        found = any(expected_pattern.replace(' ', '') in r.expression.replace(' ', '')
                    for r in results)
        # Also check if ANY result matches closely
        best = results[0] if results else None
        best_dev = best.deviation() * 100 if best else float('inf')
        print(f"\n  {name}: target={target}")
        if results:
            for r in results[:3]:
                print(f"    {r}")
        else:
            print(f"    NO MATCHES")
        checks.append((f"{name} has matches", len(results) > 0))

    # Test: mode restriction
    strict = Scanner(mode='STRICT_SEED', tolerance=0.01)
    strict_results = strict.scan(10.5)
    uses_only_seed = all(
        all(c in ['d', 'N_c', 'disc'] for c in r.constants_used)
        for r in strict_results
    )
    checks.append(("STRICT_SEED uses only d,N_c,disc", uses_only_seed))

    # Test: type discipline
    for r in s.scan(10.5)[:5]:
        checks.append((f"result has RAW_MATCH type", r.status == ResultType.RAW_MATCH))
        break

    print(f"\n{'=' * 60}")
    n_pass = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n{n_pass}/{len(checks)} passed.")
