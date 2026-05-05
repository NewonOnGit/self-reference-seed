"""
operations.py -- Every legal framework operation as a callable.

Each operation takes framework objects, produces results, and declares
what edge type it would create. The edge discoverer uses these to
grow the knowledge graph autonomously.

ARCHITECTURE: L9 (cortex). The framework's instruction set for self-research.
"""
import numpy as np
from scipy.linalg import null_space
import sys
sys.path.insert(0, '../..')
from algebra import sylvester, ker_im_decomposition, quotient
from framework_types import EdgeType

# Seed matrices
R = np.array([[0, 1], [1, 1]], dtype=float)
N = np.array([[0, -1], [1, 0]], dtype=float)
J = np.array([[0, 1], [1, 0]], dtype=float)
h = J @ N
I2 = np.eye(2)
R_tl = R - 0.5 * I2

# Canonical basis
_BASIS = [I2, R_tl, N, h]
_BASIS_NAMES = ['I', 'R_tl', 'N', 'h']
_BASIS_MAT = np.column_stack([b.flatten() for b in _BASIS])

# Precompute
_, _ker_basis, _, _Q_ker = ker_im_decomposition(R)


class OpResult:
    """Result of applying a framework operation."""
    def __init__(self, name, value, edge_type, description='', inputs=None):
        self.name = name
        self.value = value              # scalar, matrix, or array
        self.edge_type = edge_type
        self.description = description
        self.inputs = inputs or []      # names of inputs used
        self.is_scalar = isinstance(value, (int, float, np.floating))
        self.is_matrix = isinstance(value, np.ndarray) and value.ndim == 2

    def __repr__(self):
        if self.is_scalar:
            return f"Op({self.name}={self.value:.6g}, {self.edge_type})"
        elif self.is_matrix:
            return f"Op({self.name}, {self.value.shape} matrix, {self.edge_type})"
        else:
            return f"Op({self.name}, {type(self.value).__name__}, {self.edge_type})"


# ================================================================
# SCALAR OPERATIONS (matrix -> number)
# ================================================================

def op_trace(X, name='X'):
    return OpResult(f'tr({name})', float(np.trace(X)),
                    EdgeType.COMPUTED_BY, f'trace of {name}', [name])

def op_det(X, name='X'):
    return OpResult(f'det({name})', float(np.linalg.det(X)),
                    EdgeType.COMPUTED_BY, f'determinant of {name}', [name])

def op_norm_sq(X, name='X'):
    return OpResult(f'||{name}||^2', float(np.linalg.norm(X, 'fro')**2),
                    EdgeType.COMPUTED_BY, f'Frobenius norm squared', [name])

def op_rank(X, name='X'):
    return OpResult(f'rank({name})', int(np.linalg.matrix_rank(X)),
                    EdgeType.COMPUTED_BY, f'rank', [name])

def op_eigenvalues(X, name='X'):
    eigs = sorted(np.linalg.eigvals(X).real)
    return OpResult(f'eigs({name})', eigs,
                    EdgeType.COMPUTED_BY, f'eigenvalues', [name])

def op_max_eigenvalue(X, name='X'):
    return OpResult(f'max_eig({name})', float(max(np.abs(np.linalg.eigvals(X).real))),
                    EdgeType.COMPUTED_BY, f'max absolute eigenvalue', [name])

def op_disc(X, name='X'):
    tr = np.trace(X)
    det = np.linalg.det(X)
    return OpResult(f'disc({name})', float(tr**2 - 4*det),
                    EdgeType.OPERATION_PRODUCES, f'discriminant', [name])


# ================================================================
# MATRIX OPERATIONS (matrix -> matrix)
# ================================================================

def op_square(X, name='X'):
    return OpResult(f'{name}^2', X @ X,
                    EdgeType.OPERATION_PRODUCES, f'matrix square', [name])

def op_sylvester(X, name='X'):
    """L_{X,X} as a d^2 x d^2 matrix."""
    return OpResult(f'L_{{{name}}}', sylvester(X),
                    EdgeType.OPERATION_PRODUCES, f'Sylvester self-action', [name])

def op_L_action(X, s=None, name='X', s_name='R'):
    """L_{s,s}(X) = sX + Xs - X."""
    if s is None:
        s = R
    result = s @ X + X @ s - X
    return OpResult(f'L_{{{s_name}}}({name})', result,
                    EdgeType.OPERATION_PRODUCES, f'Sylvester action', [s_name, name])

def op_quotient_im(X, name='X'):
    """Project X onto im(L_R)."""
    rep, res = quotient(X, _Q_ker)
    return OpResult(f'im({name})', rep,
                    EdgeType.OPERATION_PRODUCES, f'im-projection', [name])

def op_quotient_ker(X, name='X'):
    """Project X onto ker(L_R)."""
    rep, res = quotient(X, _Q_ker)
    return OpResult(f'ker({name})', res,
                    EdgeType.OPERATION_PRODUCES, f'ker-projection', [name])

def op_commutator(A, B, a_name='A', b_name='B'):
    return OpResult(f'[{a_name},{b_name}]', A @ B - B @ A,
                    EdgeType.OPERATION_PRODUCES, f'commutator', [a_name, b_name])

def op_anticommutator(A, B, a_name='A', b_name='B'):
    return OpResult(f'{{{a_name},{b_name}}}', A @ B + B @ A,
                    EdgeType.OPERATION_PRODUCES, f'anticommutator', [a_name, b_name])

def op_product(A, B, a_name='A', b_name='B'):
    return OpResult(f'{a_name}*{b_name}', A @ B,
                    EdgeType.OPERATION_PRODUCES, f'matrix product', [a_name, b_name])

def op_conjugate(X, name='X'):
    """J-conjugation (gauge flip)."""
    return OpResult(f'J{name}J', J @ X @ J,
                    EdgeType.OPERATION_PRODUCES, f'gauge conjugation', [name, 'J'])

def op_transpose(X, name='X'):
    return OpResult(f'{name}^T', X.T,
                    EdgeType.OPERATION_PRODUCES, f'transpose', [name])


# ================================================================
# STRUCTURAL OPERATIONS (matrix -> structural info)
# ================================================================

def op_ker_dim(X, name='X'):
    """Dimension of ker(L_{X,X})."""
    L = sylvester(X)
    k = null_space(L, rcond=1e-10).shape[1]
    return OpResult(f'ker_dim(L_{{{name}}})', k,
                    EdgeType.COMPUTED_BY, f'kernel dimension', [name])

def op_self_transparent(X, name='X'):
    """Is ker(L_{X,X}) = 0?"""
    L = sylvester(X)
    k = null_space(L, rcond=1e-10).shape[1]
    return OpResult(f'transparent({name})', k == 0,
                    EdgeType.COMPUTED_BY, f'self-transparency', [name])

def op_basis_decompose(X, name='X'):
    """Decompose X in {I, R_tl, N, h} basis."""
    if X.shape != (2, 2):
        return OpResult(f'basis({name})', None, EdgeType.COMPUTED_BY, 'wrong size')
    coeffs = np.linalg.solve(_BASIS_MAT, X.flatten())
    return OpResult(f'basis({name})',
                    {_BASIS_NAMES[i]: round(float(coeffs[i]), 6) for i in range(4)},
                    EdgeType.COMPUTED_BY, f'canonical decomposition', [name])

def op_in_ker(X, name='X'):
    """Is X in ker(L_R)?"""
    rep, res = quotient(X, _Q_ker)
    return OpResult(f'{name}_in_ker', np.linalg.norm(rep) < 1e-10,
                    EdgeType.COMPUTED_BY, f'ker membership', [name])

def op_in_im(X, name='X'):
    """Is X in im(L_R)?"""
    rep, res = quotient(X, _Q_ker)
    return OpResult(f'{name}_in_im', np.linalg.norm(res) < 1e-10,
                    EdgeType.COMPUTED_BY, f'im membership', [name])


# ================================================================
# K6' TOWER OPERATION
# ================================================================

def op_k6_lift(s, Nk, Jk, name='s'):
    """K6' tower ascent."""
    d = s.shape[0]
    Z = np.zeros((d, d))
    hk = Jk @ Nk
    s_new = np.block([[s, Nk], [Z, s]])
    N_new = np.block([[Nk, -2*hk], [Z, Nk]])
    J_new = np.block([[Jk, Z], [Z, Jk]])
    return OpResult(f'K6({name})', s_new,
                    EdgeType.LIFT_PROPAGATES, f'K6 tower lift', [name])


# ================================================================
# ALL OPERATIONS REGISTRY
# ================================================================

# Single-matrix operations (matrix -> scalar or matrix)
UNARY_OPS = [
    op_trace, op_det, op_norm_sq, op_rank, op_max_eigenvalue, op_disc,
    op_square, op_L_action, op_quotient_im, op_quotient_ker,
    op_conjugate, op_transpose, op_ker_dim, op_self_transparent,
    op_basis_decompose, op_in_ker, op_in_im,
]

# Two-matrix operations
BINARY_OPS = [
    op_commutator, op_anticommutator, op_product,
]

# Named framework matrices for binary operations
FRAMEWORK_MATRICES = {
    'R': R, 'N': N, 'J': J, 'h': h, 'I': I2, 'R_tl': R_tl, 'P': R+N,
}


def apply_all_unary(X, name='X'):
    """Apply all unary operations to X. Returns list of OpResult."""
    results = []
    for op in UNARY_OPS:
        try:
            r = op(X, name)
            if r.value is not None:
                results.append(r)
        except Exception:
            pass
    return results


def apply_all_binary(X, name='X'):
    """Apply all binary operations between X and framework matrices."""
    results = []
    for op in BINARY_OPS:
        for fw_name, fw_mat in FRAMEWORK_MATRICES.items():
            if fw_name == name:
                continue
            try:
                r = op(X, fw_mat, name, fw_name)
                if r.value is not None:
                    results.append(r)
            except Exception:
                pass
    return results


# ================================================================
# PROBER (merged from prober.py — the algebraic microscope)
# ================================================================

class ProbeResult:
    """Complete algebraic profile of a matrix."""
    def __init__(self, name, matrix, properties=None):
        self.name = name
        self.matrix = matrix
        self.properties = properties or {}
        self.status = 'COMPUTED_MATCH'
        self.tier = 'A'

    def __repr__(self):
        lines = [f"PROBE: {self.name}"]
        for k, v in self.properties.items():
            lines.append(f"  {k}: {v}")
        return '\n'.join(lines)


def probe(X, name='X'):
    """Full algebraic profile of matrix X using all operations."""
    p = {}
    d = X.shape[0]

    # Apply all unary operations
    for r in apply_all_unary(X, name):
        p[r.name] = r.value

    # Square law classification
    X2 = X @ X
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
        if d == 2:
            c2 = np.linalg.solve(_BASIS_MAT, X2.flatten())
            terms = [f'{c2[i]:.3f}*{_BASIS_NAMES[i]}' for i in range(4) if abs(c2[i]) > 1e-10]
            p['square_law'] = ' + '.join(terms) if terms else '0'

    # Commutators with generators
    if d == 2:
        for gn, G in FRAMEWORK_MATRICES.items():
            if gn == name:
                continue
            c = X @ G - G @ X
            a = X @ G + G @ X
            c_coeffs = np.linalg.solve(_BASIS_MAT, c.flatten())
            a_coeffs = np.linalg.solve(_BASIS_MAT, a.flatten())
            c_terms = [f'{c_coeffs[i]:.3f}*{_BASIS_NAMES[i]}' for i in range(4) if abs(c_coeffs[i]) > 1e-10]
            a_terms = [f'{a_coeffs[i]:.3f}*{_BASIS_NAMES[i]}' for i in range(4) if abs(a_coeffs[i]) > 1e-10]
            p[f'[{name},{gn}]'] = ' + '.join(c_terms) if c_terms else '0'
            p[f'{{{name},{gn}}}'] = ' + '.join(a_terms) if a_terms else '0'

    # Key identities
    p['is_idempotent'] = bool(np.allclose(X2, X))
    p['is_symmetric'] = bool(np.allclose(X, X.T))

    return ProbeResult(name, X, p)


def probe_expression(expr_str):
    """Probe a matrix built from an expression string."""
    safe_vars = {
        'R': R, 'N': N, 'J': J, 'h': h, 'I': I2, 'I2': I2,
        'R_tl': R_tl, 'P': R + N, 'Q': J @ R @ J,
        'np': np, 'eye': np.eye, 'sqrt': np.sqrt,
        'exp': np.exp, 'pi': np.pi, 'phi': (1+np.sqrt(5))/2,
    }
    try:
        X = eval(expr_str, {"__builtins__": {}}, safe_vars)
        return probe(X, name=expr_str)
    except Exception as e:
        return f"PROBE FAILED: {e}"


# ================================================================
# SELF-TEST
# ================================================================

if __name__ == "__main__":
    print("OPERATIONS + PROBER SELF-TEST")
    print("=" * 55)

    checks = []

    # Test unary ops on R
    unary = apply_all_unary(R, 'R')
    print(f"  Unary ops on R: {len(unary)} results")
    for r in unary:
        if r.is_scalar:
            print(f"    {r}")
    checks.append(("unary ops on R", len(unary) > 10))

    # Check specific values
    tr_r = next(r for r in unary if 'tr' in r.name)
    checks.append(("tr(R) = 1", abs(tr_r.value - 1.0) < 1e-10))

    det_r = next(r for r in unary if 'det' in r.name)
    checks.append(("det(R) = -1", abs(det_r.value + 1.0) < 1e-10))

    disc_r = next(r for r in unary if 'disc' in r.name)
    checks.append(("disc(R) = 5", abs(disc_r.value - 5.0) < 1e-10))

    ker_r = next(r for r in unary if 'ker_dim' in r.name)
    checks.append(("ker_dim(L_R) = 2", ker_r.value == 2))

    transp_r = next(r for r in unary if 'transparent' in r.name)
    checks.append(("R not self-transparent", transp_r.value == False))

    # Test binary ops
    binary = apply_all_binary(R, 'R')
    print(f"\n  Binary ops on R: {len(binary)} results")
    checks.append(("binary ops on R", len(binary) > 5))

    # Test on N
    unary_n = apply_all_unary(N, 'N')
    transp_n = next(r for r in unary_n if 'transparent' in r.name)
    checks.append(("N self-transparent", transp_n.value == True))

    in_ker_n = next(r for r in unary_n if 'in_ker' in r.name)
    checks.append(("N in ker", in_ker_n.value == True))

    # Edge types
    checks.append(("trace is COMPUTED_BY", tr_r.edge_type == EdgeType.COMPUTED_BY))
    checks.append(("disc is OPERATION_PRODUCES", disc_r.edge_type == EdgeType.OPERATION_PRODUCES))

    print(f"\n{'=' * 55}")
    n_pass = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n{n_pass}/{len(checks)} passed.")
    print(f"\n{len(UNARY_OPS)} unary + {len(BINARY_OPS)} binary operations registered.")
    print(f"Each returns: result + edge_type + dependencies.")
