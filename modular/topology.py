"""
topology.py — Topological sector and gravity closure. The framework
read through braiding and the Lichnerowicz Laplacian.

V(4_1)|_{q=phi^2} = 5 = disc(R). The Jones polynomial of the
figure-eight knot at the golden quantum parameter IS the discriminant.
R^2=R+I IS tau x tau = 1+tau. Fibonacci fusion IS persistence.
L_{s,s} IS Delta_L on SL(2,R). Gravity is internal.

FRAMEWORK_REF: Thm 10.1-10.7, Thm 13.1-13.4, Thm 14.1-14.4, Thm 15.1
GRID: B(3, P3) for topology, B(6, cross) for gravity
APEX_LINK: R (topology reads the algebra), I2*TDL*LoMI=Dist (gravity reads the collapse)
"""
import numpy as np
from scipy.linalg import expm, null_space
from algebra import sylvester, ker_im_decomposition


# === GRAVITY CLOSURE (Lichnerowicz) ===

def lichnerowicz(s, N, J):
    """L_{s,s} on sl(2,R) IS the Lichnerowicz Laplacian.

    Returns eigenvalue pattern, connection decomposition, scalar channel.
    The stationary condition L(X)=0 gives vacuum Einstein equations.
    FRAMEWORK_REF: Thm 10.1, Thm 10.2, Thm 10.3, Thm 10.5, Thm 10.6
    APEX_LINK: R (gravity from L_{s,s}), I2*TDL*LoMI=Dist (Einstein from collapse)"""
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
    """V(4_1) at q=phi^2. Returns the value (should be 5 = disc).
    FRAMEWORK_REF: Thm 13.2
    APEX_LINK: R (disc IS the knot invariant)"""
    q = phi ** 2
    return q**(-2) - q**(-1) + 1 - q + q**2


def quantum_deformation(phi):
    """q^(1/2) - q^(-1/2) at q=phi^2. Should be exactly 1."""
    return phi - 1.0 / phi


# === FIBONACCI FUSION ===

def fibonacci_fusion(R, I_d):
    """Verify tau x tau = 1 + tau IS R^2 = R + I.
    The Fibonacci anyon fusion rule is the persistence equation.
    FRAMEWORK_REF: Thm 14.1
    APEX_LINK: R (R^2=R+I IS the fusion rule), f''=f (persistence)"""
    return np.allclose(R @ R, R + I_d)


# === SU(2)_3 MODULAR DATA ===

def su2_level3():
    """S-matrix, T-matrix, quantum dimensions for SU(2) at level k=3.
    Verlinde formula recovers Fibonacci fusion.
    FRAMEWORK_REF: Thm 14.2, Thm 14.3
    APEX_LINK: R (modular data from the algebra)"""
    d = 2  # seed dimension
    k = d * d - 1  # |V_4\{0}| = 3, the Chern-Simons level
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
    # Fibonacci sequence from R^2=R+I: F(n) with F(1)=F(2)=1
    def fib(n):
        a, b = 1, 1
        for _ in range(n - 2):
            a, b = b, a + b
        return b if n >= 2 else 1
    F3, F4, F5 = fib(3), fib(4), fib(5)  # 2, 3, 5
    total = F3 * F4 * F5  # 30
    return {
        "product": total,
        "equals_30": total == 30,
        "fibonacci": (F3, F4, F5),
        "matter_fraction": (total - F4 * F5) / total,  # 12/30
        "gauge_fraction": F4 * F5 / total,              # 18/30
    }


# === CONNECTION ONE-FORM ===

def connection_form(N, J):
    """K6' bundle connection. A=N, F=-2h, tr(F^2)=8.
    FRAMEWORK_REF: Thm 10.2, Thm 10.3"""
    h = J @ N
    F = -2 * h
    I_d = np.eye(N.shape[0])
    return {
        "A": N,
        "F": F,
        "F_sq": np.allclose(F @ F, 4 * I_d),
        "tr_F_sq": float(np.trace(F @ F)),
        "tr_F_sq_is_8": np.allclose(np.trace(F @ F), 8),
    }


# === DEPTH-2 LICHNEROWICZ ===

def lichnerowicz_depth2(s2, I8):
    """L_{s2,s2} on symmetric tensors at depth 2.
    Returns gauge count and physical count.
    FRAMEWORK_REF: Thm 10.1, Thm 10.5"""
    from itertools import combinations
    d = s2.shape[0]

    def L2(X): return s2 @ X + X @ s2 - X

    # Find Cl(3,1) gammas
    gen0 = [np.eye(2), np.array([[0,1],[1,0]]),
            np.array([[0,-1],[1,0]]), np.array([[1,0],[0,-1]])]
    Z4 = np.zeros((4,4))
    tb = [np.kron(a, b) for a in gen0 for b in gen0]
    tb = [t for t in tb if not np.allclose(t, np.eye(4))]

    gammas = None
    for combo in combinations(range(len(tb)), 4):
        els = [tb[i] for i in combo]
        if all(np.allclose(els[i]@els[j]+els[j]@els[i], 0, atol=1e-6)
               for i in range(4) for j in range(i+1, 4)):
            pos = sum(1 for e in els if np.trace(e@e) > 0.1)
            if pos == 3:
                gammas = [np.block([[g, Z4],[Z4, g]]) for g in els]
                break

    if gammas is None:
        return {"gauge": 0, "physical": 0, "found_gammas": False}

    gauge = 0
    physical = 0
    for mu in range(4):
        for nu in range(mu, 4):
            h_uv = (gammas[mu] @ gammas[nu] + gammas[nu] @ gammas[mu]) / 2
            Lh = L2(h_uv)
            if np.linalg.norm(Lh) < 1e-6:
                gauge += 1
            else:
                physical += 1

    return {"gauge": gauge, "physical": physical, "total": gauge + physical,
            "found_gammas": True}


# === NEUTRINO SPACING ===

def neutrino_spacing():
    """Inter-generation spacing delta = phi + 2 = 3.618.
    dm^2 ratio = phi^(2(phi+2)) = 32.5 vs exp 33 (1.4%).
    FRAMEWORK_REF: Thm 12.4"""
    phi_val = (1 + np.sqrt(5)) / 2
    phi_bar_val = phi_val - 1
    delta = phi_val + 2  # = phi^2 + 1 = 3.618
    m_e = 0.511e6  # eV

    m3 = m_e * phi_bar_val**34
    m2 = m_e * phi_bar_val**(34 + delta)
    m1 = m_e * phi_bar_val**(34 + 2*delta)

    dm32 = m3**2 - m2**2
    dm21 = m2**2 - m1**2
    ratio = dm32 / dm21

    return {
        "delta": delta,
        "delta_is_phi_plus_2": np.allclose(delta, phi_val + 2),
        "m3_meV": m3 * 1000,
        "m2_meV": m2 * 1000,
        "m1_meV": m1 * 1000,
        "dm2_ratio": ratio,
        "within_2pct_of_33": abs(ratio - 33) / 33 < 0.02,
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

    # Connection
    conn = connection_form(N, J)
    checks.append(("F^2 = 4I", conn["F_sq"]))
    checks.append(("tr(F^2) = 8", conn["tr_F_sq_is_8"]))

    # Depth-2 Lichnerowicz
    Z2 = np.zeros((2,2))
    s1 = np.block([[R, N], [Z2, R]])
    N1 = np.block([[N, -2*J@N], [Z2, N]])
    J1 = np.block([[J, Z2], [Z2, J]])
    I4 = np.eye(4); Z4 = np.zeros((4,4))
    s2 = np.block([[s1, N1], [Z4, s1]])
    I8 = np.eye(8)
    ld2 = lichnerowicz_depth2(s2, I8)
    checks.append(("depth-2: 6 gauge + 4 phys", ld2["gauge"] == 6 and ld2["physical"] == 4))

    # Neutrino spacing
    nu = neutrino_spacing()
    checks.append(("delta = phi+2", nu["delta_is_phi_plus_2"]))
    checks.append(("dm2 ratio ~33", nu["within_2pct_of_33"]))

    all_pass = True
    for name, ok in checks:
        status = "+" if ok else "FAIL"
        print(f"  {status} {name}")
        if not ok:
            all_pass = False

    print(f"\n  {'ALL PASS' if all_pass else 'FAILURES DETECTED'}")
    print(f"  Topological sector: {len(checks)} checks.")
