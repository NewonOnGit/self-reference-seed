"""
algebra.py — Shared algebraic operations. The single Sylvester function
used by both production and observer. No duplication.

FRAMEWORK_REF: Thm 2.1, Thm 2.2, Thm 2.3
GRID: B(3, cross)
APEX_LINK: R (statement 2), f''=f (statement 1)
"""
import numpy as np
from scipy.linalg import null_space


def sylvester(A, B=None):
    """L_{A,B}(X) = AX + XB - X as a matrix on vec(X).
    FRAMEWORK_REF: Thm 2.1
    APEX_LINK: R (the operation IS the framework)"""
    if B is None:
        B = A
    d = A.shape[0]
    return np.kron(A, np.eye(d)) + np.kron(np.eye(d), B.T) - np.eye(d * d)


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


def discriminant_arithmetic():
    """The three discriminants and their relations.
    disc(R)=5, disc(N)=-4, disc(omega)=-3. Sum=-2=-||N||^2. Product=60=2*30.
    Compositum Q(zeta_30): degree phi(30)=8=parent_ker."""
    return {
        'disc_R': 5, 'disc_N': -4, 'disc_omega': -3,
        'sum_R_omega': 2, 'triple_sum': -2, 'triple_product': 60,
        'cross_field_disc': -15, 'compositum_index': 30,
        'compositum_degree': 8,  # phi(30) = 8 = parent_ker
        'abs_disc_sum': 12,      # |5|+|-4|+|-3| = 12 = dim_gauge
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


def lattice_symmetry_orders():
    """Dihedral group orders of the three framework lattices.
    |D_4(Z[i])| = 8 = parent_ker. |D_6(Z[omega])| = 12 = dim_gauge.
    |D_5(Z[phi])| = 10 = 2*disc. Product = 960.
    The lattice symmetry groups ARE the framework structure constants.
    FRAMEWORK_REF: Geometry investigation"""
    return {
        'D4_order': 8,    # Z[i] square lattice, 4-fold -> |D_4|=8=parent_ker
        'D6_order': 12,   # Z[omega] hex lattice, 6-fold -> |D_6|=12=dim_gauge
        'D5_order': 10,   # Z[phi] quasilattice, 5-fold -> |D_5|=10=2*disc
        'product': 960,   # 8*12*10
        'lcm_rotations': 60,  # lcm(4,6,5)=60=|A_5|=icosahedral
    }


def penrose_substitution(R, J):
    """The Penrose inflation matrix is R^2 conjugated by J.
    M_sub = [[2,1],[1,1]]. R^2 = [[1,1],[1,2]]. J*R^2*J = M_sub.
    Same eigenvalues: phi^2, phi_bar^2. Same char poly: x^2-3x+1.
    R^2 = R + I IS the quasicrystal inflation rule.
    FRAMEWORK_REF: Geometry investigation (Tier A)"""
    I = np.eye(R.shape[0])
    R2 = R @ R
    M_sub = J @ R2 @ J
    phi = (1 + np.sqrt(5)) / 2
    phi_bar = phi - 1
    return {
        'R_squared': R2,
        'substitution_matrix': M_sub,
        'conjugate_by_J': np.allclose(M_sub, np.array([[2, 1], [1, 1]])),
        'same_eigenvalues': np.allclose(sorted(np.linalg.eigvals(M_sub).real),
                                         sorted([phi_bar**2, phi**2])),
        'inflation_eigenvalue': phi**2,
        'deflation_eigenvalue': phi_bar**2,
        'R2_is_R_plus_I': np.allclose(R2, R + I),
    }
