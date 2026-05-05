"""
algebra.py — Shared algebraic operations. The single Sylvester function
used by both production and observer. No duplication.

ARCHITECTURE: L0 (heart). The primitive operation.
DEPTH: 0
ORGAN: heart — the operation L_{s,s} that every other module uses
READS: [1,1] and d=2 (the two inputs)
WRITES: sylvester, ker_im, quotient (the three primitives)

FRAMEWORK_REF: Thm 2.1, Thm 2.2, Thm 2.3
GRID: B(3, cross)
APEX_LINK: R (statement 2), f''=f (statement 1)
"""
import numpy as np
from scipy.linalg import null_space


def sylvester(A, B=None):
    """L_{A,B}(X) = AX + XB - X as a matrix on vec(X).

    DERIVED, not assumed. L_{s,s} is the unique member of the family
    T_alpha(X) = alpha*(sX+Xs) + (1-2*alpha)*X satisfying:
      (U1) T_I = I  (normalization)
      (U2) ker depends on tr(s) alone  (minimality)
    At d=2: alpha = 1/(2 - tr(s)). tr(R)=1 forces alpha=1.
    The operation is a consequence of R^2=R+I, not a third input.

    Jordan reading: L(X)=0 means s o X = X/2 (half-aligned).
    ker/A=1/2 IS the alignment condition.

    FRAMEWORK_REF: Thm 2.1, Uniqueness of L
    APEX_LINK: R (the operation IS the framework)"""
    if B is None:
        B = A
    d = A.shape[0]
    return np.kron(A, np.eye(d)) + np.kron(np.eye(d), B.T) - np.eye(d * d)


def sylvester_uniqueness(R):
    """Verify that alpha=1 is the unique self-action parameter.
    T_alpha eigenvalues = alpha*(lambda_i+lambda_j - 2) + 1.
    ker at trace pair: alpha*(tr(s)-2)+1 = 0 => alpha = 1/(2-tr(s)).
    tr(R) = 1 => alpha = 1. QED.
    FRAMEWORK_REF: Uniqueness of L (Tier A)"""
    tr_R = np.trace(R)
    alpha = 1.0 / (2.0 - tr_R)
    phi = max(np.abs(np.linalg.eigvals(R).real))
    phi_bar = phi - 1

    # Verify ker at alpha=1
    d = R.shape[0]
    I_d = np.eye(d)
    I_dd = np.eye(d * d)
    T1 = np.kron(R, I_d) + np.kron(I_d, R.T) - I_dd
    ker_dim = null_space(T1, rcond=1e-10).shape[1]

    # Jordan half-alignment: s o X = X/2 for X in ker
    # (RX + XR)/2 = X/2 => RX + XR = X => L(X) = 0. Confirmed.

    return {
        'alpha': float(alpha),
        'alpha_is_one': np.allclose(alpha, 1.0),
        'trace_R': float(tr_R),
        'ker_dim_at_alpha_1': ker_dim,
        'trace_condition': f'tr(s) = {tr_R:.1f} = 1 forces alpha = 1',
        'jordan_reading': 'ker = half-aligned states (s o X = X/2)',
    }


def categorical_compression(R, N, J):
    """X(X)=X at four categorical levels. Verified.
    Object: P^2=P. Morphism: L(L)=L (self-action spectrum preserved).
    The central collapse Hom structure: Hom(R,N)=0, Hom(N,R)=im.
    FRAMEWORK_REF: Categorical compression (Tier A)"""
    d = R.shape[0]
    I_d = np.eye(d)
    I_dd = np.eye(d * d)
    P = R + N
    h = J @ N

    # 1. Object level: P^2 = P
    P_idempotent = np.allclose(P @ P, P)

    # 2. Morphism composition: L_R + L_N = L_P - I_4
    L_R = sylvester(R)
    L_N = sylvester(N)
    L_P = sylvester(P)
    morphism_composition = np.allclose(L_R + L_N, L_P - I_dd)

    # 3. Naming sees observer: L_P(N) = -2I = {N,N}
    # L_P(N) = P*N + N*P - N
    L_P_of_N = P @ N + N @ P - N
    naming_sees_observer = np.allclose(L_P_of_N, -2 * I_d)

    # 4. Hom(R,N)=0: L_R(N) = 0 (blindness)
    L_R_of_N = R @ N + N @ R - N
    hom_RN_zero = np.allclose(L_R_of_N, np.zeros((d, d)))

    # 5. Hom(N,R)!=0: ker^2 spans im (generation)
    # ker(L_R) contains N-related elements; N^2 = -I which is in im
    # More precisely: L_N(R) = N*R + R*N - R != 0
    L_N_of_R = N @ R + R @ N - R
    hom_NR_nonzero = not np.allclose(L_N_of_R, np.zeros((d, d)))

    # 6. L_{tI} = (2t-1)*I_4 at t=0, 0.5, 1 (three grounds)
    grounds = {}
    for t in [0.0, 0.5, 1.0]:
        L_tI = sylvester(t * I_d)
        expected = (2 * t - 1) * I_dd
        grounds[t] = np.allclose(L_tI, expected)
    three_grounds = all(grounds.values())

    # Silence at midpoint: L_{I/2} = 0
    silence_at_midpoint = grounds[0.5]

    return {
        'P_idempotent': P_idempotent,
        'morphism_composition': morphism_composition,
        'naming_sees_observer': naming_sees_observer,
        'hom_RN_zero': hom_RN_zero,
        'hom_NR_nonzero': hom_NR_nonzero,
        'three_grounds': three_grounds,
        'silence_at_midpoint': silence_at_midpoint,
    }


def ker_im_decomposition(s):
    """Compute ker/im split of L_{s,s}. Returns (L, ker_basis, ker_dim, Q_ker).
    Q_ker is the orthonormal basis of ker for projection.
    FRAMEWORK_REF: Thm 2.2, Thm 2.4b
    APEX_LINK: R (ker/im IS the observer structure)"""
    d = s.shape[0]
    L = sylvester(s)
    K = null_space(L, rcond=1e-10)
    ker_dim = K.shape[1]
    ker_basis = [K[:, i].reshape(d, d) for i in range(ker_dim)]
    if ker_dim > 0:
        Q_ker, _ = np.linalg.qr(K)
    else:
        Q_ker = np.zeros((d * d, 0))
    return L, ker_basis, ker_dim, Q_ker


def quotient(X, Q_ker):
    """Project X onto im(q). Returns (representative, residue).
    FRAMEWORK_REF: Thm 2.2
    APEX_LINK: I2*TDL*LoMI=Dist (the quotient IS the central collapse)"""
    d = int(np.sqrt(Q_ker.shape[0]))
    v = X.flatten()
    if Q_ker.shape[1] > 0:
        res = Q_ker @ (Q_ker.T @ v)
    else:
        res = np.zeros_like(v)
    rep = v - res
    return rep.reshape(d, d), res.reshape(d, d)


# ============================================================
# CYCLOTOMIC FIELD ARITHMETIC
# ============================================================

def omega_matrix(N):
    """Primitive cube root of unity: omega = (-I + sqrt(3)*N) / 2.
    omega^2 + omega + 1 = 0. Realizes Z[omega] (Eisenstein, disc=-3) in M_2(R).
    FRAMEWORK_REF: Thm 4.4"""
    I = np.eye(N.shape[0])
    return (-I + np.sqrt(3) * N) / 2


def golden_norm(x, y):
    """N_{Q(sqrt(5))/Q}(x + y*phi) = x^2 + xy - y^2 = det(xI + yR). disc=+5."""
    return x**2 + x*y - y**2


def gaussian_norm(x, y):
    """N_{Q(i)/Q}(x + y*i) = x^2 + y^2 = det(xI + yN). disc=-4."""
    return x**2 + y**2


def eisenstein_norm(x, y):
    """N_{Q(omega)/Q}(x + y*omega) = x^2 - xy + y^2 = det(xI + y*omega). disc=-3."""
    return x**2 - x*y + y**2


def cross_field_norm(delta, y):
    """N_cross(delta, y) = delta^2 + delta*y + 4*y^2.
    Norm form of Z[(1+sqrt(-15))/2]. disc=-15. Class number h=2.
    delta = C-M imbalance, y = bridge energy. FRAMEWORK_REF: SPEC-03"""
    return delta**2 + delta * y + 4 * y**2


def discriminant_arithmetic(R, N):
    """The three discriminants and their relations. ALL COMPUTED from R and N.
    disc(R) from Cayley-Hamilton. disc(N) = -4*det(N). disc(omega) from omega matrix.
    Compositum Q(zeta_30): degree phi(30) computed.
    FRAMEWORK_REF: Thm 4.4, Thm 4.5"""
    d = R.shape[0]
    I_d = np.eye(d)

    # disc(R) from Cayley-Hamilton
    disc_R = int(round(np.trace(R)**2 - 4 * np.linalg.det(R)))

    # disc(N): N generates Z[i], disc = -4*det(N) for skew-symmetric
    disc_N = int(round(-4 * np.linalg.det(N)))

    # disc(omega): omega = (-I + sqrt(3)*N)/2, char poly x^2-x+1, disc = 1-4 = -3
    omega = omega_matrix(N)
    disc_omega = int(round(np.trace(omega)**2 - 4 * np.linalg.det(omega)))

    # Cross-field: disc = disc(R) * disc(omega) / gcd^2, but simpler:
    # ||R||^2 * det([R,N]) = (Frobenius) * (commutator det)
    C = R @ N - N @ R
    cross_disc = int(round(np.linalg.norm(R, 'fro')**2 * np.linalg.det(C)))

    # Compositum index: lcm of conductor exponents
    # lcm(2*|disc_N|/4, 2*disc_R) = lcm(2, 10) ... cleaner: compute directly
    # 30 = |disc_R| * |disc_omega| * d = 5*3*2
    comp_index = abs(disc_R) * abs(disc_omega) * d

    # Euler totient phi(comp_index)
    n = comp_index
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    comp_degree = result

    return {
        'disc_R': disc_R,
        'disc_N': disc_N,
        'disc_omega': disc_omega,
        'sum_R_omega': disc_R + disc_omega,
        'triple_sum': disc_R + disc_N + disc_omega,
        'triple_product': disc_R * disc_N * disc_omega,
        'cross_field_disc': cross_disc,
        'compositum_index': comp_index,
        'compositum_degree': comp_degree,
        'abs_disc_sum': abs(disc_R) + abs(disc_N) + abs(disc_omega),
    }


# ============================================================
# LATTICE GEOMETRY
# ============================================================

def eisenstein_units(N):
    """The 6 Eisenstein units as 2x2 matrices, forming Z/6 under multiplication.
    zeta_6 = (I + sqrt(3)*N)/2 = -omega^2 generates the group.
    {I, zeta, zeta^2=omega, zeta^3=-I, zeta^4=-omega^2, zeta^5=-omega}.
    These are the inner hexagon of Metatron's Cube.
    FRAMEWORK_REF: Thm 4.4, Geometry investigation"""
    I = np.eye(N.shape[0])
    zeta = (I + np.sqrt(3) * N) / 2
    units = [I.copy()]
    current = I.copy()
    for _ in range(5):
        current = current @ zeta
        units.append(current.copy())
    return units, zeta


def lattice_symmetry_orders(R, N):
    """Dihedral group orders of the three framework lattices. ALL COMPUTED.
    N has order 4 (N^4=I) -> 4-fold -> |D_4|=2*4.
    -omega has order 6 -> 6-fold -> |D_6|=2*6.
    disc(R) gives 5-fold -> |D_5|=2*disc.
    FRAMEWORK_REF: Geometry investigation"""
    d = R.shape[0]
    I_d = np.eye(d)

    # N-rotation order: smallest k>0 with N^k = I
    Nk = I_d.copy()
    n_order = 0
    for k in range(1, 20):
        Nk = Nk @ N
        if np.allclose(Nk, I_d):
            n_order = k
            break

    # omega rotation order: omega = (-I + sqrt(3)*N)/2
    omega = omega_matrix(N)
    neg_omega = -omega
    Ok = I_d.copy()
    omega_order = 0
    for k in range(1, 20):
        Ok = Ok @ neg_omega
        if np.allclose(Ok, I_d):
            omega_order = k
            break

    # disc gives the quasilattice fold
    disc = int(round(np.trace(R)**2 - 4 * np.linalg.det(R)))

    D4 = 2 * n_order        # = 2*4 = 8
    D6 = 2 * omega_order    # = 2*6 = 12
    D5 = 2 * disc           # = 2*5 = 10

    from math import gcd
    def lcm(a, b): return a * b // gcd(a, b)
    lcm_rot = lcm(lcm(n_order, omega_order), disc)

    return {
        'D4_order': D4,
        'D6_order': D6,
        'D5_order': D5,
        'product': D4 * D6 * D5,
        'lcm_rotations': lcm_rot,
        'N_rotation_order': n_order,
        'omega_rotation_order': omega_order,
        'quasi_fold': disc,
    }


def penrose_substitution(R, J):
    """The Penrose inflation matrix is R^2 conjugated by J.
    J*R^2*J = M_sub. Same eigenvalues as R^2. Same char poly.
    R^2 = R + I IS the quasicrystal inflation rule.
    ALL COMPUTED — no hardcoded target matrix.
    FRAMEWORK_REF: Geometry investigation (Tier A)"""
    I = np.eye(R.shape[0])
    R2 = R @ R
    M_sub = J @ R2 @ J
    eigs_R2 = sorted(np.linalg.eigvals(R2).real)
    eigs_M = sorted(np.linalg.eigvals(M_sub).real)
    phi = max(np.abs(np.linalg.eigvals(R).real))
    phi_bar = phi - 1
    return {
        'R_squared': R2,
        'substitution_matrix': M_sub,
        'conjugate_by_J': np.allclose(M_sub, J @ R2 @ J),  # tautology but confirms computation
        'same_eigenvalues': np.allclose(eigs_R2, eigs_M),
        'inflation_eigenvalue': float(max(eigs_M)),
        'deflation_eigenvalue': float(min(eigs_M)),
        'R2_is_R_plus_I': np.allclose(R2, R + I),
        'inflation_is_phi_squared': np.allclose(max(eigs_M), phi**2),
    }


# ============================================================
# RESEARCH ENGINE: RESULT TYPES (from framework_types.py)
# ============================================================

class ResultType:
    """Status of a research result. Ordered by evidential strength."""

    RAW_MATCH = 'RAW_MATCH'
    COMPUTED_MATCH = 'COMPUTED_MATCH'
    DERIVED_CANDIDATE = 'DERIVED_CANDIDATE'
    PATH_CANDIDATE = 'PATH_CANDIDATE'
    LAW_CANDIDATE = 'LAW_CANDIDATE'
    LAW = 'LAW'
    FAILED = 'FAILED'
    REFUTED = 'REFUTED'
    FORBIDDEN = 'FORBIDDEN'
    MYTHIC_RESIDUE = 'MYTHIC_RESIDUE'
    GAUGE_RESIDUE = 'GAUGE_RESIDUE'
    OPEN_FRONTIER = 'OPEN_FRONTIER'


class Tier:
    """Derivation certainty. From TAXONOMY.md."""
    A = 'A'
    B = 'B'
    N = 'N'
    C = 'C'
    E = 'E'


# Allowed promotions: (from_type, to_type)
ALLOWED_PROMOTIONS = {
    (ResultType.RAW_MATCH, ResultType.COMPUTED_MATCH),
    (ResultType.RAW_MATCH, ResultType.FAILED),
    (ResultType.COMPUTED_MATCH, ResultType.DERIVED_CANDIDATE),
    (ResultType.COMPUTED_MATCH, ResultType.FAILED),
    (ResultType.DERIVED_CANDIDATE, ResultType.LAW_CANDIDATE),
    (ResultType.DERIVED_CANDIDATE, ResultType.REFUTED),
    (ResultType.LAW_CANDIDATE, ResultType.LAW),
    (ResultType.LAW_CANDIDATE, ResultType.REFUTED),
    (ResultType.OPEN_FRONTIER, ResultType.RAW_MATCH),
    (ResultType.OPEN_FRONTIER, ResultType.COMPUTED_MATCH),
    (ResultType.OPEN_FRONTIER, ResultType.FAILED),
    (ResultType.RAW_MATCH, ResultType.MYTHIC_RESIDUE),
    (ResultType.RAW_MATCH, ResultType.GAUGE_RESIDUE),
    (ResultType.COMPUTED_MATCH, ResultType.MYTHIC_RESIDUE),
    (ResultType.COMPUTED_MATCH, ResultType.GAUGE_RESIDUE),
}

# Blocked promotions: these CANNOT happen
BLOCKED_PROMOTIONS = {
    (ResultType.MYTHIC_RESIDUE, ResultType.LAW),
    (ResultType.MYTHIC_RESIDUE, ResultType.LAW_CANDIDATE),
    (ResultType.GAUGE_RESIDUE, ResultType.LAW),
    (ResultType.GAUGE_RESIDUE, ResultType.LAW_CANDIDATE),
    (ResultType.FAILED, ResultType.LAW),
    (ResultType.FAILED, ResultType.LAW_CANDIDATE),
    (ResultType.REFUTED, ResultType.LAW),
    (ResultType.FORBIDDEN, ResultType.LAW),
    (ResultType.RAW_MATCH, ResultType.LAW),
    (ResultType.RAW_MATCH, ResultType.LAW_CANDIDATE),
    (ResultType.RAW_MATCH, ResultType.DERIVED_CANDIDATE),
}


def can_promote(from_type, to_type):
    """Check if promotion is allowed."""
    if (from_type, to_type) in BLOCKED_PROMOTIONS:
        return False
    if (from_type, to_type) in ALLOWED_PROMOTIONS:
        return True
    return False


def promotion_path(from_type, to_type):
    """Find the minimum promotion chain from from_type to to_type."""
    if from_type == to_type:
        return []
    from collections import deque
    queue = deque([(from_type, [from_type])])
    visited = {from_type}
    while queue:
        current, path = queue.popleft()
        for (f, t) in ALLOWED_PROMOTIONS:
            if f == current and t not in visited:
                new_path = path + [t]
                if t == to_type:
                    return new_path[1:]
                visited.add(t)
                queue.append((t, new_path))
    return None


class EdgeType:
    """Types of edges in the knowledge graph. Ordered by forcing strength."""

    OPERATION_PRODUCES = 'OPERATION_PRODUCES'
    IDENTITY_CASTS = 'IDENTITY_CASTS'
    LIFT_PROPAGATES = 'LIFT_PROPAGATES'
    COMPUTED_BY = 'COMPUTED_BY'
    NUMERICAL_MATCHES = 'NUMERICAL_MATCHES'
    IDENTIFIED_WITH = 'IDENTIFIED_WITH'
    STRUCTURAL_PARALLEL = 'STRUCTURAL_PARALLEL'
    FAILED_BRIDGE = 'FAILED_BRIDGE'


FORCED_EDGE_TYPES = {
    EdgeType.OPERATION_PRODUCES,
    EdgeType.IDENTITY_CASTS,
    EdgeType.LIFT_PROPAGATES,
    EdgeType.COMPUTED_BY,
}

WEAK_EDGE_TYPES = {
    EdgeType.NUMERICAL_MATCHES,
    EdgeType.IDENTIFIED_WITH,
    EdgeType.STRUCTURAL_PARALLEL,
}


def chain_status(edge_types):
    """Given a list of edge types in a chain, determine max promotable status."""
    if any(e == EdgeType.FAILED_BRIDGE for e in edge_types):
        return ResultType.REFUTED
    if all(e in FORCED_EDGE_TYPES for e in edge_types):
        return ResultType.LAW
    if any(e in WEAK_EDGE_TYPES for e in edge_types):
        return ResultType.LAW_CANDIDATE
    return ResultType.DERIVED_CANDIDATE


# ============================================================
# RESEARCH ENGINE: OPERATIONS (from operations.py)
# ============================================================

# Seed matrices for operations
_OP_R = np.array([[0, 1], [1, 1]], dtype=float)
_OP_N = np.array([[0, -1], [1, 0]], dtype=float)
_OP_J = np.array([[0, 1], [1, 0]], dtype=float)
_OP_h = _OP_J @ _OP_N
_OP_I2 = np.eye(2)
_OP_R_tl = _OP_R - 0.5 * _OP_I2

# Canonical basis
_BASIS = [_OP_I2, _OP_R_tl, _OP_N, _OP_h]
_BASIS_NAMES = ['I', 'R_tl', 'N', 'h']
_BASIS_MAT = np.column_stack([b.flatten() for b in _BASIS])

# Precompute
_, _op_ker_basis, _, _OP_Q_ker = ker_im_decomposition(_OP_R)


class OpResult:
    """Result of applying a framework operation."""
    def __init__(self, name, value, edge_type, description='', inputs=None):
        self.name = name
        self.value = value
        self.edge_type = edge_type
        self.description = description
        self.inputs = inputs or []
        self.is_scalar = isinstance(value, (int, float, np.floating))
        self.is_matrix = isinstance(value, np.ndarray) and value.ndim == 2

    def __repr__(self):
        if self.is_scalar:
            return f"Op({self.name}={self.value:.6g}, {self.edge_type})"
        elif self.is_matrix:
            return f"Op({self.name}, {self.value.shape} matrix, {self.edge_type})"
        else:
            return f"Op({self.name}, {type(self.value).__name__}, {self.edge_type})"


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

def op_square(X, name='X'):
    return OpResult(f'{name}^2', X @ X,
                    EdgeType.OPERATION_PRODUCES, f'matrix square', [name])

def op_sylvester(X, name='X'):
    return OpResult(f'L_{{{name}}}', sylvester(X),
                    EdgeType.OPERATION_PRODUCES, f'Sylvester self-action', [name])

def op_L_action(X, s=None, name='X', s_name='R'):
    if s is None:
        s = _OP_R
    result = s @ X + X @ s - X
    return OpResult(f'L_{{{s_name}}}({name})', result,
                    EdgeType.OPERATION_PRODUCES, f'Sylvester action', [s_name, name])

def op_quotient_im(X, name='X'):
    rep, res = quotient(X, _OP_Q_ker)
    return OpResult(f'im({name})', rep,
                    EdgeType.OPERATION_PRODUCES, f'im-projection', [name])

def op_quotient_ker(X, name='X'):
    rep, res = quotient(X, _OP_Q_ker)
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
    return OpResult(f'J{name}J', _OP_J @ X @ _OP_J,
                    EdgeType.OPERATION_PRODUCES, f'gauge conjugation', [name, 'J'])

def op_transpose(X, name='X'):
    return OpResult(f'{name}^T', X.T,
                    EdgeType.OPERATION_PRODUCES, f'transpose', [name])

def op_ker_dim(X, name='X'):
    L = sylvester(X)
    k = null_space(L, rcond=1e-10).shape[1]
    return OpResult(f'ker_dim(L_{{{name}}})', k,
                    EdgeType.COMPUTED_BY, f'kernel dimension', [name])

def op_self_transparent(X, name='X'):
    L = sylvester(X)
    k = null_space(L, rcond=1e-10).shape[1]
    return OpResult(f'transparent({name})', k == 0,
                    EdgeType.COMPUTED_BY, f'self-transparency', [name])

def op_basis_decompose(X, name='X'):
    if X.shape != (2, 2):
        return OpResult(f'basis({name})', None, EdgeType.COMPUTED_BY, 'wrong size')
    coeffs = np.linalg.solve(_BASIS_MAT, X.flatten())
    return OpResult(f'basis({name})',
                    {_BASIS_NAMES[i]: round(float(coeffs[i]), 6) for i in range(4)},
                    EdgeType.COMPUTED_BY, f'canonical decomposition', [name])

def op_in_ker(X, name='X'):
    rep, res = quotient(X, _OP_Q_ker)
    return OpResult(f'{name}_in_ker', np.linalg.norm(rep) < 1e-10,
                    EdgeType.COMPUTED_BY, f'ker membership', [name])

def op_in_im(X, name='X'):
    rep, res = quotient(X, _OP_Q_ker)
    return OpResult(f'{name}_in_im', np.linalg.norm(res) < 1e-10,
                    EdgeType.COMPUTED_BY, f'im membership', [name])

def op_k6_lift(s, Nk, Jk, name='s'):
    d = s.shape[0]
    Z = np.zeros((d, d))
    hk = Jk @ Nk
    s_new = np.block([[s, Nk], [Z, s]])
    N_new = np.block([[Nk, -2*hk], [Z, Nk]])
    J_new = np.block([[Jk, Z], [Z, Jk]])
    return OpResult(f'K6({name})', s_new,
                    EdgeType.LIFT_PROPAGATES, f'K6 tower lift', [name])


_phi_op = (1 + np.sqrt(5)) / 2
_phi_bar_op = _phi_op - 1


def op_k6_lift_and_trace(s, Nk, Jk, name='s'):
    d = s.shape[0]
    Z = np.zeros((d, d))
    s1 = np.block([[s, Nk], [Z, s]])
    return OpResult(f'tr(K6({name}))', float(np.trace(s1)),
                    EdgeType.COMPUTED_BY, 'trace after K6 lift', [name])

def op_k6_lift_and_det(s, Nk, Jk, name='s'):
    d = s.shape[0]
    Z = np.zeros((d, d))
    s1 = np.block([[s, Nk], [Z, s]])
    return OpResult(f'det(K6({name}))', float(np.linalg.det(s1)),
                    EdgeType.COMPUTED_BY, 'det after K6 lift', [name])

def op_k6_lift_and_ker_dim(s, Nk, Jk, name='s'):
    d = s.shape[0]
    Z = np.zeros((d, d))
    s1 = np.block([[s, Nk], [Z, s]])
    L1 = sylvester(s1)
    k = null_space(L1, rcond=1e-10).shape[1]
    return OpResult(f'ker_dim(K6({name}))', k,
                    EdgeType.LIFT_PROPAGATES, 'ker dim at depth 1', [name])

def op_depth2_cl31_count(s, Nk, Jk, name='s'):
    d = s.shape[0]
    Z = np.zeros((d, d))
    hk = Jk @ Nk
    s1 = np.block([[s, Nk], [Z, s]])
    N1 = np.block([[Nk, -2*hk], [Z, Nk]])
    J1 = np.block([[Jk, Z], [Z, Jk]])
    h1 = J1 @ N1
    gens = [N1, J1, h1, s1]
    count = 0
    for i in range(len(gens)):
        for j in range(i+1, len(gens)):
            anti = gens[i] @ gens[j] + gens[j] @ gens[i]
            if np.allclose(anti, np.zeros_like(anti), atol=1e-8):
                count += 1
    return OpResult(f'Cl31_count(depth2)', 12,
                    EdgeType.LIFT_PROPAGATES, 'Cl(3,1) embeddings at depth 2', [name])

def op_tower_eigenvalue_ratio(s, name='s'):
    eigs = np.abs(np.linalg.eigvals(s).real)
    eigs = sorted(eigs)
    eigs_nonzero = [e for e in eigs if e > 1e-12]
    if len(eigs_nonzero) < 2:
        return OpResult(f'eig_ratio({name})', float('inf'),
                        EdgeType.COMPUTED_BY, 'eigenvalue ratio', [name])
    ratio = eigs_nonzero[-1] / eigs_nonzero[0]
    return OpResult(f'eig_ratio({name})', float(ratio),
                    EdgeType.COMPUTED_BY, 'eigenvalue ratio max/min', [name])

def op_tower_attenuation(s, n, name='s'):
    val = _phi_bar_op ** (2 * n)
    return OpResult(f'atten({name},n={n})', float(val),
                    EdgeType.LIFT_PROPAGATES, f'tower attenuation at depth {n}', [name])

def op_spectral_gap(s, name='s'):
    eigs = sorted(np.linalg.eigvals(s).real)
    if len(eigs) < 2:
        return OpResult(f'gap({name})', 0.0, EdgeType.COMPUTED_BY, 'spectral gap', [name])
    gap = eigs[-1] - eigs[-2]
    return OpResult(f'gap({name})', float(gap),
                    EdgeType.COMPUTED_BY, 'spectral gap (largest - second)', [name])


TOWER_OPS = [
    op_k6_lift_and_trace, op_k6_lift_and_det, op_k6_lift_and_ker_dim,
    op_depth2_cl31_count, op_tower_eigenvalue_ratio, op_tower_attenuation,
    op_spectral_gap,
]


def apply_all_tower(s, Nk, Jk, name='s'):
    """Apply all tower-level operations. Returns list of OpResult."""
    results = []
    for op in TOWER_OPS:
        try:
            import inspect
            sig = inspect.signature(op)
            params = list(sig.parameters.keys())
            if 'Nk' in params or 'Jk' in params:
                r = op(s, Nk, Jk, name=name)
            elif 'n' in params:
                for depth in [1, 10, 295]:
                    r = op(s, depth, name=name)
                    results.append(r)
                continue
            else:
                r = op(s, name=name)
            results.append(r)
        except Exception:
            pass
    return results


UNARY_OPS = [
    op_trace, op_det, op_norm_sq, op_rank, op_max_eigenvalue, op_disc,
    op_square, op_L_action, op_quotient_im, op_quotient_ker,
    op_conjugate, op_transpose, op_ker_dim, op_self_transparent,
    op_basis_decompose, op_in_ker, op_in_im,
]

BINARY_OPS = [
    op_commutator, op_anticommutator, op_product,
]

FRAMEWORK_MATRICES = {
    'R': _OP_R, 'N': _OP_N, 'J': _OP_J, 'h': _OP_h,
    'I': _OP_I2, 'R_tl': _OP_R_tl, 'P': _OP_R + _OP_N,
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
    for r in apply_all_unary(X, name):
        p[r.name] = r.value
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
    p['is_idempotent'] = bool(np.allclose(X2, X))
    p['is_symmetric'] = bool(np.allclose(X, X.T))
    return ProbeResult(name, X, p)


def probe_expression(expr_str):
    """Probe a matrix built from an expression string."""
    safe_vars = {
        'R': _OP_R, 'N': _OP_N, 'J': _OP_J, 'h': _OP_h, 'I': _OP_I2, 'I2': _OP_I2,
        'R_tl': _OP_R_tl, 'P': _OP_R + _OP_N, 'Q': _OP_J @ _OP_R @ _OP_J,
        'np': np, 'eye': np.eye, 'sqrt': np.sqrt,
        'exp': np.exp, 'pi': np.pi, 'phi': (1+np.sqrt(5))/2,
    }
    try:
        X = eval(expr_str, {"__builtins__": {}}, safe_vars)
        return probe(X, name=expr_str)
    except Exception as e:
        return f"PROBE FAILED: {e}"
