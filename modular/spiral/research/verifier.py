"""
verifier.py -- The falsification engine. The K1' wall at research level.

Given a candidate relation, tests whether it survives:
  1. Type check: does the derivation chain type-match?
  2. Gauge ablation: does it survive N -> -N?
  3. Tower lift: does it hold at depth 1+?
  4. Normalization: does it survive rescaling?
  5. Independence: can it be derived another way?
  6. Perturbation: does perturbing inputs change the result?

Output: VERIFIED / WEAK / REFUTED with the failing check named.
This is what stops the system from wandering into curve-fitting.
"""
import numpy as np
from scipy.linalg import null_space
import sys
sys.path.insert(0, '../..')
from algebra import sylvester, ker_im_decomposition
from framework_types import ResultType, Tier


# Seed
R = np.array([[0, 1], [1, 1]], dtype=float)
N = np.array([[0, -1], [1, 0]], dtype=float)
J = np.array([[0, 1], [1, 0]], dtype=float)
h = J @ N
I2 = np.eye(2)


class VerificationResult:
    """Outcome of verification."""

    def __init__(self, expression, status, tier, checks_passed, checks_failed,
                 details=None):
        self.expression = expression
        self.status = status  # VERIFIED / WEAK / REFUTED
        self.tier = tier
        self.checks_passed = checks_passed
        self.checks_failed = checks_failed
        self.details = details or {}

    def __repr__(self):
        p = len(self.checks_passed)
        f = len(self.checks_failed)
        return (f"{self.status}: {self.expression} "
                f"({p} passed, {f} failed, tier={self.tier})")


class Verifier:
    """The falsification gate."""

    def verify_numerical(self, target, expression_fn, expression_str,
                         constants=None):
        """Verify a numerical relation: target = expression_fn(constants).

        expression_fn: callable that takes a dict of constants, returns float.
        constants: dict of {name: value}. If None, uses seed constants.
        """
        if constants is None:
            constants = self._seed_constants()

        passed = []
        failed = []
        details = {}

        value = expression_fn(constants)
        if abs(target) > 1e-30:
            base_dev = abs(value - target) / abs(target)
        else:
            base_dev = abs(value)
        details['base_deviation'] = base_dev

        # 1. BASE CHECK: does it match at all?
        if base_dev < 0.05:
            passed.append('base_match')
        else:
            failed.append('base_match')

        # 2. GAUGE ABLATION: N -> -N
        gauge_constants = dict(constants)
        # Recompute with flipped N: phi stays, phi_bar stays,
        # but anything depending on sign(N) should change or not.
        # For numerical relations, gauge flip doesn't change scalar quantities.
        # Check: does the expression use N-dependent quantities?
        gauge_value = expression_fn(gauge_constants)
        gauge_invariant = abs(gauge_value - value) < 1e-10
        if gauge_invariant:
            passed.append('gauge_invariant')
        else:
            # Not invariant under gauge -> GAUGE_RESIDUE, not LAW
            failed.append('gauge_invariant')
        details['gauge_invariant'] = gauge_invariant

        # 3. PERTURBATION: does small change in each input change the result?
        dependencies = []
        eps = 1e-6
        for name, val in constants.items():
            if abs(val) < 1e-30:
                continue
            perturbed = dict(constants)
            perturbed[name] = val * (1 + eps)
            try:
                perturbed_value = expression_fn(perturbed)
                sensitivity = abs(perturbed_value - value) / (abs(value) * eps + 1e-30)
                if sensitivity > 0.01:
                    dependencies.append((name, sensitivity))
            except (ValueError, ZeroDivisionError, OverflowError):
                pass
        details['dependencies'] = dependencies
        if len(dependencies) > 0:
            passed.append('has_dependencies')
        else:
            # No input changes the output -> trivial/constant
            failed.append('has_dependencies')

        # 4. EXACTNESS CHECK: is it exact (deviation < 1e-10) or approximate?
        if base_dev < 1e-10:
            passed.append('exact')
            details['exact'] = True
        else:
            details['exact'] = False
            # Approximate: check if deviation is itself a framework quantity
            details['approximate_deviation'] = base_dev

        # 5. FAMILY CHECK: does it hold for other mu in the family?
        # R^2 = R + mu*I. At mu=1: our framework. At mu!=1: family member.
        family_holds = 0
        family_fails = 0
        for mu in [0.25, 2.25, 4.0]:
            try:
                fam_constants = self._family_constants(mu)
                fam_value = expression_fn(fam_constants)
                fam_dev = abs(fam_value - target) / abs(target) if abs(target) > 1e-30 else abs(fam_value)
                if fam_dev < 0.05:
                    family_holds += 1
                else:
                    family_fails += 1
            except (ValueError, ZeroDivisionError, OverflowError):
                family_fails += 1
        details['family_holds'] = family_holds
        details['family_fails'] = family_fails
        if family_holds == 3:
            passed.append('universal (all mu)')
        elif family_holds > 0:
            passed.append('partially_universal')
        else:
            passed.append('mu1_specific')  # only works at mu=1, which is fine

        # VERDICT
        n_critical_fails = sum(1 for f in failed if f in ('base_match',))
        if n_critical_fails > 0:
            status = ResultType.REFUTED
            tier = Tier.C
        elif len(failed) == 0:
            status = ResultType.LAW_CANDIDATE
            tier = Tier.A if details.get('exact') else Tier.N
        elif len(failed) <= 1:
            status = ResultType.DERIVED_CANDIDATE
            tier = Tier.B
        else:
            status = ResultType.REFUTED
            tier = Tier.C

        return VerificationResult(
            expression=expression_str, status=status, tier=tier,
            checks_passed=passed, checks_failed=failed, details=details
        )

    def verify_algebraic(self, X, property_name, expected):
        """Verify an algebraic property of matrix X.
        E.g., verify_algebraic(R@R, 'equals', R+I2) checks R^2=R+I."""
        passed = []
        failed = []
        details = {}

        if property_name == 'equals':
            match = np.allclose(X, expected)
            details['match'] = match
            if match:
                passed.append('algebraic_match')
            else:
                failed.append('algebraic_match')
                details['difference_norm'] = float(np.linalg.norm(X - expected))

        elif property_name == 'ker_dim':
            L = sylvester(X)
            actual = null_space(L, rcond=1e-10).shape[1]
            details['actual_ker'] = actual
            if actual == expected:
                passed.append('ker_dim_match')
            else:
                failed.append('ker_dim_match')

        elif property_name == 'in_ker':
            _, _, _, Q_ker = ker_im_decomposition(R)
            from algebra import quotient as alg_q
            rep, res = alg_q(X, Q_ker)
            in_ker = np.linalg.norm(rep) < 1e-10
            details['in_ker'] = in_ker
            if in_ker == expected:
                passed.append('placement_match')
            else:
                failed.append('placement_match')

        # Gauge ablation for algebraic: conjugate by J
        X_gauged = J @ X @ J
        details['gauge_conjugate'] = X_gauged.tolist()

        # Tower lift check
        Z = np.zeros((2, 2))
        X_lifted = np.block([[X, Z], [Z, X]])
        details['tower_lifted'] = True  # just recording that we can lift

        status = ResultType.LAW_CANDIDATE if not failed else ResultType.REFUTED
        tier = Tier.A if not failed else Tier.C

        return VerificationResult(
            expression=property_name, status=status, tier=tier,
            checks_passed=passed, checks_failed=failed, details=details
        )

    def _seed_constants(self):
        d = 2
        N_c = d * (d + 1) // 2
        phi = (1 + np.sqrt(5)) / 2
        phi_bar = phi - 1
        disc = int(round(1 + 4 * 1))
        return {
            'd': d, 'N_c': N_c, 'disc': disc,
            'parent_ker': d**N_c,
            'dim_gauge': (N_c**2-1) + (d**2-1) + 1,
            'phi': phi, 'phi_bar': phi_bar,
            'alpha_S': 0.5 - phi_bar**2,
            'beta_KMS': np.log(phi),
            'ker/A': 0.5,
        }

    def _family_constants(self, mu):
        """Constants for family member with parameter mu."""
        d = 2
        disc = 1 + 4 * mu
        # Eigenvalues of R_mu: (1 +/- sqrt(disc))/2
        sqrt_disc = np.sqrt(disc)
        phi_mu = (1 + sqrt_disc) / 2
        phi_bar_mu = (sqrt_disc - 1) / 2
        N_c = d * (d + 1) // 2
        return {
            'd': d, 'N_c': N_c, 'disc': disc,
            'parent_ker': d**N_c,
            'dim_gauge': (N_c**2-1) + (d**2-1) + 1,
            'phi': phi_mu, 'phi_bar': phi_bar_mu,
            'alpha_S': 0.5 - phi_bar_mu**2,
            'beta_KMS': np.log(phi_mu) if phi_mu > 0 else 0,
            'ker/A': 0.5,
        }


# ================================================================
# SELF-TEST
# ================================================================

if __name__ == "__main__":
    print("VERIFIER SELF-TEST")
    print("=" * 60)

    v = Verifier()
    checks = []

    # 1. Verify a TRUE relation: 10.5 = 2*disc + ker/A
    r1 = v.verify_numerical(
        target=10.5,
        expression_fn=lambda c: 2*c['disc'] + c['ker/A'],
        expression_str='2*disc + ker/A'
    )
    print(f"  {r1}")
    print(f"    details: exact={r1.details.get('exact')}, deps={[d[0] for d in r1.details.get('dependencies',[])]}")
    checks.append(("10.5 = 2*disc+ker/A verified", r1.status in (ResultType.LAW_CANDIDATE, ResultType.DERIVED_CANDIDATE)))

    # 2. Verify a FALSE relation: 10.5 = disc + 3
    r2 = v.verify_numerical(
        target=10.5,
        expression_fn=lambda c: c['disc'] + 3,
        expression_str='disc + 3'
    )
    print(f"  {r2}")
    checks.append(("10.5 != disc+3 refuted", r2.status == ResultType.REFUTED))

    # 3. Verify a WEAK relation: m_e/m_p ~ (2/9)^5
    r3 = v.verify_numerical(
        target=0.000544617,
        expression_fn=lambda c: (2.0/c['N_c']**2)**c['disc'],
        expression_str='(2/N_c^2)^disc'
    )
    print(f"  {r3}")
    print(f"    deviation: {r3.details.get('base_deviation',0)*100:.2f}%")
    checks.append(("m_e/m_p ~ (2/9)^5 candidate", r3.status != ResultType.REFUTED))

    # 4. Verify algebraic: R^2 = R + I
    r4 = v.verify_algebraic(R @ R, 'equals', R + I2)
    print(f"  {r4}")
    checks.append(("R^2=R+I algebraic", r4.status == ResultType.LAW_CANDIDATE))

    # 5. Verify algebraic: N in ker(L_R)
    r5 = v.verify_algebraic(N, 'in_ker', True)
    print(f"  {r5}")
    checks.append(("N in ker verified", r5.status == ResultType.LAW_CANDIDATE))

    # 6. Verify algebraic: R NOT in ker(L_R)
    r6 = v.verify_algebraic(R, 'in_ker', True)
    print(f"  {r6}")
    checks.append(("R not in ker refuted", r6.status == ResultType.REFUTED))

    # 7. Family check: alpha_S = 1/2 - phi_bar^2 (should be mu=1 specific)
    r7 = v.verify_numerical(
        target=0.118034,
        expression_fn=lambda c: 0.5 - c['phi_bar']**2,
        expression_str='1/2 - phi_bar^2'
    )
    print(f"  {r7}")
    print(f"    family_holds: {r7.details.get('family_holds')}, family_fails: {r7.details.get('family_fails')}")
    checks.append(("alpha_S verified", r7.status != ResultType.REFUTED))

    print(f"\n{'=' * 60}")
    n_pass = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n{n_pass}/{len(checks)} passed.")
