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
    return np.kron(np.eye(d), A) + np.kron(B.T, np.eye(d)) - np.eye(d * d)


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
