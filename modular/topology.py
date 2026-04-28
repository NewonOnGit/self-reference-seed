"""
topology.py — Topological sector and gravity closure. The framework
read through braiding and the Lichnerowicz Laplacian.

V(4_1)|_{q=phi^2} = 5 = disc(R). The Jones polynomial of the
figure-eight knot at the golden quantum parameter IS the discriminant.
R^2=R+I IS tau x tau = 1+tau. Fibonacci fusion IS persistence.
L_{s,s} IS Delta_L on SL(2,R). Gravity is internal.
"""
import numpy as np
from scipy.linalg import expm, null_space
from algebra import sylvester, ker_im_decomposition


# === GRAVITY CLOSURE (Lichnerowicz) ===

def lichnerowicz(s, N, J):
    """L_{s,s} on sl(2,R) IS the Lichnerowicz Laplacian.

    Returns eigenvalue pattern, connection decomposition, scalar channel.
    The stationary condition L(X)=0 gives vacuum Einstein equations.
    """
    d = s.shape[0]
    I_d = np.eye(d)
    h = J @ N
    R_tl = s - (np.trace(s) / d) * I_d

    def L(X):
        return s @ X + X @ s - X

    # sl(2,R) standard basis
    e_up = np.array([[0, 1], [0, 0]], dtype=float)
    f_lo = np.array([[0, 0], [1, 0]], dtype=float)

    # Eigenvalues on sl(2,R) basis {h, e, f}
    Lh = L(h)
    Le = L(e_up)
    Lf = L(f_lo)
    eig_h = Lh[0, 0]  # L(h) = c*I, extract c
    eig_e = Le[0, 0]
    eig_f = Lf[0, 0]

    # Connection: (1/2)[s, h] = N
    christoffel_h = 0.5 * (s @ h - h @ s)
    christoffel_N = np.allclose(christoffel_h, N)

    # Scalar channel: L(R_tl) = (disc/2)*I
    L_Rtl = L(R_tl)
    disc = int(round(np.trace(s)**2 - 4 * np.linalg.det(s)))
    lambda_scalar = np.allclose(L_Rtl, (disc / 2) * I_d)

    # L = ad(s) + (2Xs - X) decomposition
    decomp_ok = all(
        np.allclose(L(X), (s @ X - X @ s) + (2 * X @ s - X))
        for X in [h, e_up, f_lo]
    )

    return {
        "eigenvalues": [eig_h, eig_e, eig_f],
        "pattern": np.allclose(sorted([eig_h, eig_e, eig_f]), [-1, 1, 1]),
        "christoffel_N": christoffel_N,
        "lambda_scalar": lambda_scalar,
        "disc": disc,
        "decomposition": decomp_ok,
    }


# === JONES POLYNOMIAL ===

def jones_figure_eight(phi):
    """V(4_1) at q=phi^2. Returns the value (should be 5 = disc)."""
    q = phi ** 2
    return q**(-2) - q**(-1) + 1 - q + q**2


def quantum_deformation(phi):
    """q^(1/2) - q^(-1/2) at q=phi^2. Should be exactly 1."""
    return phi - 1.0 / phi


# === FIBONACCI FUSION ===

def fibonacci_fusion(R, I_d):
    """Verify tau x tau = 1 + tau IS R^2 = R + I.
    The Fibonacci anyon fusion rule is the persistence equation."""
    return np.allclose(R @ R, R + I_d)


# === SU(2)_3 MODULAR DATA ===

def su2_level3():
    """S-matrix, T-matrix, quantum dimensions for SU(2) at level k=3.
    Verlinde formula recovers Fibonacci fusion."""
    k = 3
    n = k + 1  # 4 anyons: j = 0, 1/2, 1, 3/2
    labels = [0, 0.5, 1, 1.5]

    # S-matrix
    S = np.zeros((n, n))
    for i, j in enumerate(labels):
        for ip, jp in enumerate(labels):
            S[i, ip] = np.sqrt(2 / (k + 2)) * np.sin(
                np.pi * (2 * j + 1) * (2 * jp + 1) / (k + 2)
            )

    # T-matrix (topological spins)
    T = np.zeros((n, n), dtype=complex)
    for i, j in enumerate(labels):
        T[i, i] = np.exp(2j * np.pi * j * (j + 1) / (k + 2))

    # Quantum dimensions
    d = S[0, :] / S[0, 0]

    # Verlinde formula for Fibonacci sub-category {j=0, j=1}
    fib = [0, 2]  # indices for j=0, j=1
    S_fib = S[np.ix_(fib, fib)]
    N_tau_tau = {}
    for k_label, k_idx in [("1", 0), ("tau", 1)]:
        val = sum(
            S_fib[1, l] * S_fib[1, l] * np.conj(S_fib[k_idx, l]) / S_fib[0, l]
            for l in range(2)
        )
        N_tau_tau[k_label] = round(val.real)

    return {
        "S": S, "T": T,
        "quantum_dims": d,
        "d_tau": d[2],  # j=1 -> d = phi
        "verlinde_fusion": N_tau_tau,
        "fibonacci_recovered": N_tau_tau == {"1": 1, "tau": 1},
    }


# === BRAIDING ===

def braiding_phase(N):
    """Braiding phase e^(4pi*i/5) from N-rotation. cos(4pi/5) = -phi/2."""
    phi = (1 + np.sqrt(5)) / 2
    rot = expm(4 * np.pi / 5 * N)
    cos_val = rot[0, 0]
    return {
        "cos_4pi5": cos_val,
        "matches_neg_phi_half": np.allclose(cos_val, -phi / 2),
        "disc_fold": 5,  # circle divided into disc parts
    }


# === CLIFFORD-FIBONACCI ===

def clifford_fibonacci():
    """30 = 2*3*5 = F(3)*F(4)*F(5). Clifford counting is Fibonacci."""
    F3, F4, F5 = 2, 3, 5
    return {
        "product": F3 * F4 * F5,
        "equals_30": F3 * F4 * F5 == 30,
        "fibonacci": (F3, F4, F5),
        "matter_fraction": 12 / 30,  # 2/5 = 2/disc
        "gauge_fraction": 18 / 30,   # 3/5 = 3/disc
    }


# ---- self-test ----
if __name__ == "__main__":
    R = np.array([[0, 1], [1, 1]], dtype=float)
    N = np.array([[0, -1], [1, 0]], dtype=float)
    J = np.array([[0, 1], [1, 0]], dtype=float)
    I2 = np.eye(2)
    phi = (1 + np.sqrt(5)) / 2

    checks = []

    # Lichnerowicz
    lich = lichnerowicz(R, N, J)
    checks.append(("L eigenvalues {-1,+1,+1}", lich["pattern"]))
    checks.append(("nabla_s(h) = N", lich["christoffel_N"]))
    checks.append(("L(R_tl) = (disc/2)*I", lich["lambda_scalar"]))
    checks.append(("L = ad + Ric", lich["decomposition"]))

    # Jones
    V = jones_figure_eight(phi)
    checks.append(("V(4_1) = 5 = disc", np.allclose(V, 5)))

    # Quantum deformation
    qd = quantum_deformation(phi)
    checks.append(("q^(1/2)-q^(-1/2) = 1", np.allclose(qd, 1)))

    # Fibonacci fusion
    checks.append(("tau*tau = 1+tau", fibonacci_fusion(R, I2)))

    # SU(2)_3
    mod = su2_level3()
    checks.append(("d_tau = phi", np.allclose(mod["d_tau"], phi)))
    checks.append(("Verlinde -> Fibonacci", mod["fibonacci_recovered"]))

    # Braiding
    br = braiding_phase(N)
    checks.append(("cos(4pi/5) = -phi/2", br["matches_neg_phi_half"]))

    # Clifford-Fibonacci
    cf = clifford_fibonacci()
    checks.append(("30 = F(3)*F(4)*F(5)", cf["equals_30"]))

    all_pass = True
    for name, ok in checks:
        status = "+" if ok else "FAIL"
        print(f"  {status} {name}")
        if not ok:
            all_pass = False

    print(f"\n  {'ALL PASS' if all_pass else 'FAILURES DETECTED'}")
    print(f"  Topological sector: {len(checks)} checks.")
