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
    disc(R)=5, disc(N)=-4, disc(omega)=-3. Sum=−2=−||N||^2. Product=60=2*30."""
    return {
        'disc_R': 5, 'disc_N': -4, 'disc_omega': -3,
        'sum_R_omega': 2, 'triple_sum': -2, 'triple_product': 60,
        'cross_field_disc': -15, 'compositum_index': 30,
    }
