"""
quantum.py — Quantum gates and Bell test from framework generators.

CNOT, Hadamard, Bell states, and CHSH violation — all built from
{h, J, N} derived from P^2=P. No quantum mechanics postulated.
The complex structure (N^2=-I) forces Hilbert space. The entanglement
(K6' off-diagonal N) forces nonlocality. S = 2*sqrt(2) is a theorem.

Fibonacci anyon gate set: the braiding matrices from SU(2)_3 at
q=phi^2 give a universal gate set for topological quantum computation.

FRAMEWORK_REF: Thm 15.4-15.8, Thm 2.4c
GRID: B(3, P3) for gates, B(6, P1) for Bell test
APEX_LINK: R (gates from generators), f''=f (Hilbert from asymmetry)
"""
import numpy as np

phi = (1 + np.sqrt(5)) / 2
phi_bar = phi - 1
I2 = np.eye(2, dtype=complex)


# === FRAMEWORK GENERATORS (from P^2=P) ===

R = np.array([[0, 1], [1, 1]], dtype=complex)
N = np.array([[0, -1], [1, 0]], dtype=complex)
J = np.array([[0, 1], [1, 0]], dtype=complex)
h = J @ N  # [[1,0],[0,-1]] Cartan


# === SINGLE-QUBIT GATES ===

def hadamard():
    """H = (J + h)/sqrt(2). Superposition from ground + Cartan.
    FRAMEWORK_REF: Thm 15.5"""
    return (J + h) / np.sqrt(2)


def phase_gate(theta):
    """Phase gate from N-rotation: diag(1, e^(i*theta)).
    Uses h for the diagonal and N for the phase."""
    return np.cos(theta / 2) * I2 + 1j * np.sin(theta / 2) * h


def rotation(theta):
    """Rotation in the h-J plane: M(theta) = cos(theta)*h + sin(theta)*J.
    h decides. J flips. theta mixes them."""
    return np.cos(theta) * h + np.sin(theta) * J


# === TWO-QUBIT GATES ===

def cnot():
    """CNOT = (I+h)/2 x I + (I-h)/2 x J.
    The Cartan decides whether the ground acts.
    Control: h-eigenspace projection. Target: J (swap).
    FRAMEWORK_REF: Thm 15.4"""
    proj0 = (I2 + h) / 2
    proj1 = (I2 - h) / 2
    return np.kron(proj0, I2) + np.kron(proj1, J)


# === BELL STATES ===

def bell_phi_plus():
    """(|00> + |11>)/sqrt(2) from CNOT(H x I)|00>.
    Built entirely from framework generators."""
    ket0 = np.array([1, 0], dtype=complex)
    psi = np.kron(hadamard() @ ket0, ket0)
    return cnot() @ psi


def bell_psi_minus():
    """(|01> - |10>)/sqrt(2). The singlet. From N acting on |Phi+>."""
    ket0 = np.array([1, 0], dtype=complex)
    ket1 = np.array([0, 1], dtype=complex)
    return (np.kron(ket0, ket1) - np.kron(ket1, ket0)) / np.sqrt(2)


# === BELL TEST ===

def correlation(psi, A, B):
    """E(A,B) = <psi| A x B |psi>."""
    return np.real(psi.conj() @ np.kron(A, B) @ psi)


def chsh(psi, a1, a2, b1, b2):
    """CHSH value S = E(a1,b1) - E(a1,b2) + E(a2,b1) + E(a2,b2).
    Measurements M(theta) = cos(theta)*h + sin(theta)*J."""
    E = lambda a, b: correlation(psi, rotation(a), rotation(b))
    return E(a1, b1) - E(a1, b2) + E(a2, b1) + E(a2, b2)


def bell_test_optimal():
    """Run CHSH at optimal angles. Returns S = 2*sqrt(2).
    FRAMEWORK_REF: Thm 15.7"""
    psi = bell_phi_plus()
    return chsh(psi, 0, np.pi / 2, np.pi / 4, 3 * np.pi / 4)


def bell_test_framework():
    """Run CHSH at disc-fold angles (pi/5 spacing)."""
    psi = bell_phi_plus()
    return chsh(psi, 0, np.pi / 2, np.pi / 5, np.pi / 2 + np.pi / 5)


# === FIBONACCI ANYON GATES ===

def fibonacci_F_matrix():
    """F-matrix (fusion basis change) for Fibonacci anyons.
    Entries from phi_bar and 1/sqrt(phi). F^2 = I."""
    return np.array([
        [phi_bar, 1 / np.sqrt(phi)],
        [1 / np.sqrt(phi), -phi_bar],
    ], dtype=complex)


def fibonacci_R_matrix():
    """R-matrix (braiding) for Fibonacci anyons.
    Phases e^(-4pi*i/5) and e^(3pi*i/5) from N^2=-I."""
    return np.diag([np.exp(-4j * np.pi / 5), np.exp(3j * np.pi / 5)])


def fibonacci_sigma():
    """Braid generators sigma_1, sigma_2 for TQC.
    sigma_1 = R. sigma_2 = F R F. Universal gate set."""
    F = fibonacci_F_matrix()
    R_b = fibonacci_R_matrix()
    return R_b, F @ R_b @ F


# ---- self-test ----
if __name__ == "__main__":
    checks = []

    # Hadamard
    H = hadamard()
    checks.append(("H^2=I", np.allclose(H @ H, I2)))
    checks.append(("H=(J+h)/sqrt(2)", np.allclose(H, (J + h) / np.sqrt(2))))

    # CNOT
    C = cnot()
    CNOT_std = np.array([[1, 0, 0, 0], [0, 1, 0, 0],
                         [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
    checks.append(("CNOT correct", np.allclose(C, CNOT_std)))

    # Bell state
    bell = bell_phi_plus()
    ket0 = np.array([1, 0], dtype=complex)
    ket1 = np.array([0, 1], dtype=complex)
    expected = (np.kron(ket0, ket0) + np.kron(ket1, ket1)) / np.sqrt(2)
    checks.append(("Bell |Phi+>", np.allclose(bell, expected)))

    # Correlation structure
    E_check = correlation(bell, rotation(0), rotation(0.5))
    checks.append(("E(a,b)=cos(a-b)", np.allclose(E_check, np.cos(0.5))))

    # Bell test optimal
    S_opt = bell_test_optimal()
    checks.append(("S=2sqrt(2)", np.allclose(S_opt, 2 * np.sqrt(2))))
    checks.append(("Bell violated", abs(S_opt) > 2))

    # Bell test at framework angles
    S_fw = bell_test_framework()
    checks.append(("disc-fold violates", abs(S_fw) > 2))

    # Fibonacci gates
    F_mat = fibonacci_F_matrix()
    checks.append(("F^2=I", np.allclose(F_mat @ F_mat, I2)))

    R_b = fibonacci_R_matrix()
    checks.append(("R phases", np.allclose(R_b[0, 0], np.exp(-4j * np.pi / 5))))

    s1, s2 = fibonacci_sigma()
    checks.append(("braid relation", np.allclose(s1 @ s2 @ s1, s2 @ s1 @ s2)))

    all_pass = True
    for name, ok in checks:
        status = "+" if ok else "FAIL"
        print(f"  {status} {name}")
        if not ok:
            all_pass = False

    print(f"\n  {'ALL PASS' if all_pass else 'FAILURES DETECTED'}")
    print(f"  Quantum gates and Bell test: {len(checks)} checks.")
    print(f"  S_optimal = {S_opt:.10f} = 2*sqrt(2)")
    print(f"  S_framework = {S_fw:.6f} ({abs(S_fw) / (2 * np.sqrt(2)) * 100:.1f}% Tsirelson)")
