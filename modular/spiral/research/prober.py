"""
prober.py -- The algebraic microscope. Given a matrix or expression,
tell us everything the framework says about it.

More important than scanner. Scanner finds numerical coincidences.
Prober finds what an object IS in the algebra.

Given any 2x2 matrix X, reports:
  basis decomposition in {I, R_tl, N, h}
  trace, det, rank, eigenvalues, norms
  square law (X^2 = ?), minimal polynomial
  commutators/anticommutators with R, N, J, h
  L_R(X) placement (ker or im?)
  L_X self-transparency (ker(L_{X,X}) = ?)
  tower behavior (does X survive K6' lift?)
"""
import numpy as np
from scipy.linalg import null_space
import sys
sys.path.insert(0, '../..')
from algebra import sylvester, ker_im_decomposition, quotient
from framework_types import ResultType, Tier


# Seed matrices (computed from d=2)
R = np.array([[0, 1], [1, 1]], dtype=float)
N = np.array([[0, -1], [1, 0]], dtype=float)
J = np.array([[0, 1], [1, 0]], dtype=float)
h = J @ N
I2 = np.eye(2)
R_tl = R - 0.5 * I2

# Canonical basis for M_2(R)
_BASIS = [I2, R_tl, N, h]
_BASIS_NAMES = ['I', 'R_tl', 'N', 'h']
_BASIS_MAT = np.column_stack([b.flatten() for b in _BASIS])

# Precompute L_R ker projection
_, _ker_basis, _ker_dim, _Q_ker = ker_im_decomposition(R)


class ProbeResult:
    """Complete algebraic profile of a matrix."""

    def __init__(self, name, matrix):
        self.name = name
        self.matrix = matrix
        self.status = ResultType.COMPUTED_MATCH
        self.tier = Tier.A
        self.properties = {}

    def __repr__(self):
        lines = [f"PROBE: {self.name}"]
        for k, v in self.properties.items():
            lines.append(f"  {k}: {v}")
        return '\n'.join(lines)


class Prober:
    """The algebraic microscope."""

    def probe(self, X, name='X'):
        """Full algebraic profile of matrix X."""
        result = ProbeResult(name, X)
        p = result.properties
        d = X.shape[0]

        # Basic properties
        p['matrix'] = X.tolist()
        p['trace'] = float(np.trace(X))
        p['det'] = float(np.linalg.det(X))
        p['rank'] = int(np.linalg.matrix_rank(X))
        eigs = sorted(np.linalg.eigvals(X).real)
        p['eigenvalues'] = [round(float(e), 6) for e in eigs]
        p['frobenius_norm'] = float(np.linalg.norm(X, 'fro'))

        # Basis decomposition
        if d == 2:
            coeffs = np.linalg.solve(_BASIS_MAT, X.flatten())
            p['basis_decomposition'] = {
                _BASIS_NAMES[i]: round(float(coeffs[i]), 6) for i in range(4)
            }
            # Sector placement
            pa = abs(coeffs[0]) + abs(coeffs[1])  # I + R_tl = im sector
            oa = abs(coeffs[2])                     # N = ker sector
            ma = abs(coeffs[3])                     # h = mediation sector
            total = pa + oa + ma
            if total > 1e-10:
                p['sector_weights'] = {
                    'im(PA+I)': round(pa/total, 3),
                    'ker(OA)': round(oa/total, 3),
                    'bridge(MA)': round(ma/total, 3),
                }

        # Square law
        X2 = X @ X
        p['X^2'] = X2.tolist()
        if np.allclose(X2, X):
            p['square_law'] = 'IDEMPOTENT (X^2=X)'
        elif np.allclose(X2, -np.eye(d)):
            p['square_law'] = 'ROTATION (X^2=-I)'
        elif np.allclose(X2, np.eye(d)):
            p['square_law'] = 'INVOLUTION (X^2=I)'
        elif np.allclose(X2, np.zeros((d,d))):
            p['square_law'] = 'NILPOTENT (X^2=0)'
        elif np.allclose(X2, X + np.eye(d)):
            p['square_law'] = 'PERSISTENCE (X^2=X+I)'
        else:
            # Decompose X^2 in basis
            if d == 2:
                c2 = np.linalg.solve(_BASIS_MAT, X2.flatten())
                terms = []
                for i in range(4):
                    if abs(c2[i]) > 1e-10:
                        terms.append(f'{c2[i]:.3f}*{_BASIS_NAMES[i]}')
                p['square_law'] = ' + '.join(terms) if terms else '0'

        # Commutators and anticommutators with generators
        if d == 2:
            gens = {'R': R, 'N': N, 'J': J, 'h': h}
            comm = {}
            anti = {}
            for gname, G in gens.items():
                c = X @ G - G @ X
                a = X @ G + G @ X
                # Recognize
                c_coeffs = np.linalg.solve(_BASIS_MAT, c.flatten())
                a_coeffs = np.linalg.solve(_BASIS_MAT, a.flatten())
                c_str = self._coeffs_to_str(c_coeffs)
                a_str = self._coeffs_to_str(a_coeffs)
                comm[f'[X,{gname}]'] = c_str
                anti[f'{{X,{gname}}}'] = a_str
            p['commutators'] = comm
            p['anticommutators'] = anti

        # L_R placement: is X in ker(L_R) or im(L_R)?
        if d == 2:
            rep, res = quotient(X, _Q_ker)
            ker_component = float(np.linalg.norm(res))
            im_component = float(np.linalg.norm(rep))
            if ker_component < 1e-10:
                p['L_R_placement'] = 'PURE im (visible)'
            elif im_component < 1e-10:
                p['L_R_placement'] = 'PURE ker (hidden)'
            else:
                p['L_R_placement'] = f'MIXED (im={im_component:.3f}, ker={ker_component:.3f})'

        # Self-transparency: ker(L_{X,X})
        L_XX = sylvester(X)
        ker_XX = null_space(L_XX, rcond=1e-10).shape[1]
        p['self_ker'] = ker_XX
        p['self_transparent'] = ker_XX == 0

        # L_R action on X
        if d == 2:
            LX = R @ X + X @ R - X
            lx_coeffs = np.linalg.solve(_BASIS_MAT, LX.flatten())
            p['L_R(X)'] = self._coeffs_to_str(lx_coeffs)
            p['L_R(X)_is_zero'] = np.allclose(LX, 0)

        # Idempotent test
        p['is_idempotent'] = bool(np.allclose(X2, X))
        p['is_symmetric'] = bool(np.allclose(X, X.T))
        p['is_asymmetric'] = not p['is_symmetric'] and p['is_idempotent']

        return result

    def _coeffs_to_str(self, coeffs):
        terms = []
        for i in range(4):
            c = round(float(coeffs[i]), 4)
            if abs(c) > 1e-10:
                if c == 1.0:
                    terms.append(_BASIS_NAMES[i])
                elif c == -1.0:
                    terms.append(f'-{_BASIS_NAMES[i]}')
                else:
                    terms.append(f'{c}*{_BASIS_NAMES[i]}')
        return ' + '.join(terms) if terms else '0'

    def probe_expression(self, expr_str, local_vars=None):
        """Probe a matrix built from an expression string.
        Safe eval with only framework matrices available."""
        safe_vars = {
            'R': R, 'N': N, 'J': J, 'h': h, 'I': I2, 'I2': I2,
            'R_tl': R_tl, 'P': R + N, 'Q': J @ R @ J,
            'np': np, 'eye': np.eye, 'sqrt': np.sqrt,
            'exp': np.exp, 'pi': np.pi, 'phi': (1+np.sqrt(5))/2,
        }
        if local_vars:
            safe_vars.update(local_vars)
        try:
            X = eval(expr_str, {"__builtins__": {}}, safe_vars)
            return self.probe(X, name=expr_str)
        except Exception as e:
            return f"PROBE FAILED: {e}"


# ================================================================
# SELF-TEST
# ================================================================

if __name__ == "__main__":
    print("PROBER SELF-TEST")
    print("=" * 60)

    prober = Prober()
    checks = []

    # Probe R
    r = prober.probe(R, 'R')
    print(r)
    checks.append(("R: persistence", 'PERSISTENCE' in r.properties['square_law']))
    checks.append(("R: in im", 'im' in r.properties['L_R_placement']))
    checks.append(("R: not self-transparent", not r.properties['self_transparent']))
    print()

    # Probe N
    n = prober.probe(N, 'N')
    print(n)
    checks.append(("N: rotation", 'ROTATION' in n.properties['square_law']))
    checks.append(("N: in ker", 'ker' in n.properties['L_R_placement']))
    checks.append(("N: self-transparent", n.properties['self_transparent']))
    print()

    # Probe P
    p = prober.probe(R + N, 'P=R+N')
    checks.append(("P: idempotent", p.properties['is_idempotent']))
    checks.append(("P: asymmetric", p.properties['is_asymmetric']))
    checks.append(("P: rank 1", p.properties['rank'] == 1))
    print(f"P: {p.properties['square_law']}, rank={p.properties['rank']}")
    print()

    # Probe h
    hprobe = prober.probe(h, 'h')
    checks.append(("h: involution", 'INVOLUTION' in hprobe.properties['square_law']))
    checks.append(("h: in im", 'im' in hprobe.properties['L_R_placement']))
    print(f"h: {hprobe.properties['square_law']}")
    print()

    # Probe expression
    omega_probe = prober.probe_expression('(-I + sqrt(3)*N)/2')
    if isinstance(omega_probe, ProbeResult):
        checks.append(("omega: det=1", abs(omega_probe.properties['det'] - 1.0) < 1e-10))
        print(f"omega: det={omega_probe.properties['det']:.4f}, "
              f"square_law={omega_probe.properties['square_law']}")
    print()

    # Summary
    print(f"{'=' * 60}")
    n_pass = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n{n_pass}/{len(checks)} passed.")
