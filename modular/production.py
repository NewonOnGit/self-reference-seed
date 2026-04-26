"""
production.py — One operation, five readings.

Apply L_{s,s} and read the result. That's the entire derivation.
    A. SEED:     [1,1] and 2 -> R, J
    B. ALGEBRA:  L_ss -> N, P, h, Q, identities, constants
    C. TOWER:    K6' x2 -> Cl(3,1), so(3,1)
    D. PHYSICS:  arithmetic on B+C
    E. DYNAMICS: L on L's output -> transparency, conservation
"""
import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq
from itertools import combinations
from algebra import sylvester, ker_im_decomposition, quotient as alg_quotient


def _companion(coeffs):
    d = len(coeffs)
    C = np.zeros((d, d), dtype=float)
    C[:d-1, 1:] = np.eye(d - 1)
    C[d-1, :] = coeffs
    return C


def _swap(dim):
    J = np.zeros((dim, dim), dtype=float)
    for i in range(dim):
        J[i, dim - 1 - i] = 1.0
    return J


class Production:
    """One operation, five readings."""

    def derive(self):
        rec = {}

        # ============================================================
        # A. SEED — build s from the two primitives
        # ============================================================
        R = _companion([1, 1])          # f^2 = f + id
        J = _swap(2)                     # |S_0| = 2
        I2 = np.eye(2)
        d = 2

        assert np.allclose(R @ R, R + I2)
        assert np.allclose(J @ J, I2)

        # Cayley-Hamilton consequences (forced)
        tr_R = np.trace(R)
        det_R = np.linalg.det(R)
        disc = int(round(tr_R**2 - 4 * det_R))
        R_tl = R - (tr_R / d) * I2
        phi = float(max(np.abs(np.linalg.eigvals(R).real)))
        phi_bar = phi - 1

        rec.update({
            "R": R, "J": J, "disc": disc, "R_tl": R_tl,
            "phi": phi, "phi_bar": phi_bar,
            "scalar_channel": float((R @ R_tl + R_tl @ R - R_tl)[0, 0]),
        })

        # ============================================================
        # B. ALGEBRA — apply L_ss, read ker/im, extract everything
        # ============================================================
        L, ker_basis, ker_dim, Q_k = ker_im_decomposition(R)

        # N: min-norm rotation in ker with N^2=-I, gauge bit
        K1, K2 = ker_basis[0], ker_basis[1]
        c1 = (K1 @ K1)[0, 0]; c2 = (K2 @ K2)[0, 0]
        c12 = (K1 @ K2 + K2 @ K1)[0, 0]
        Qf = np.array([[c1, c12/2], [c12/2, c2]])
        ev, evec = np.linalg.eigh(Qf)
        sc = 1.0 / np.sqrt(-ev[0])
        alpha, beta = sc * evec[:, 0]
        N = alpha * K1 + beta * K2
        if (J @ N)[0, 0] < 0:
            N = -N
        assert np.allclose(N @ N, -I2)

        # P: single generator
        P = R + N
        assert np.allclose(P @ P, P)
        assert np.linalg.matrix_rank(P) == 1
        assert not np.allclose(P, P.T)
        assert np.allclose((P + P.T) / 2, R)
        assert np.allclose((P - P.T) / 2, N)

        # Remaining generators
        h = J @ N
        Q = J @ R @ J

        # Seven identities
        identities = {
            "R²=R+I": np.allclose(R @ R, R + I2),
            "N²=-I": np.allclose(N @ N, -I2),
            "{R,N}=N": np.allclose(R @ N + N @ R, N),
            "RNR=-N": np.allclose(R @ N @ R, -N),
            "NRN=R-I": np.allclose(N @ R @ N, R - I2),
            "(RN)²=I": np.allclose((R @ N) @ (R @ N), I2),
            "[R,N]²=5I": np.allclose(
                (R @ N - N @ R) @ (R @ N - N @ R), disc * I2
            ),
        }

        # Five constants
        e_val = float(expm(h)[0, 0])
        def _sin_zero(theta):
            return expm(theta * N)[1, 0]
        pi_val = brentq(_sin_zero, 3.0, 3.2, xtol=1e-15)
        assert np.allclose(expm(pi_val * N), -I2, atol=1e-12)

        rec.update({
            "N": N, "P": P, "h": h, "Q": Q,
            "P_idempotent": True,
            "identities": identities,
            "e": e_val, "pi": pi_val,
            "ker_dim": ker_dim, "ker_basis": ker_basis,
            "frobenius_sum": np.linalg.norm(R, 'fro')**2 + np.linalg.norm(N, 'fro')**2,
        })

        # ============================================================
        # C. TOWER — iterate B (K6' to depth 2)
        # ============================================================
        Z = np.zeros((d, d))
        basis = [("I", I2), ("J", J), ("N", N), ("h", h)]
        tensor_basis = [
            (f"{a}x{b}", np.kron(ma, mb))
            for a, ma in basis for b, mb in basis
            if not (a == "I" and b == "I")
        ]

        n31 = n22 = 0
        cl31_gens = None
        for combo in combinations(range(len(tensor_basis)), 4):
            elements = [tensor_basis[i][1] for i in combo]
            if all(
                np.allclose(elements[i] @ elements[j] + elements[j] @ elements[i], 0)
                for i in range(4) for j in range(i + 1, 4)
            ):
                pos = sum(1 for e in elements if np.trace(e @ e) > 0)
                neg = 4 - pos
                if (pos, neg) == (3, 1):
                    n31 += 1
                    if cl31_gens is None:
                        cl31_gens = elements
                elif (pos, neg) == (2, 2):
                    n22 += 1

        # so(3,1) closure
        so31_close = False
        so31_dim = 0
        if cl31_gens is not None:
            lie_gens = []
            for i in range(4):
                for j in range(i + 1, 4):
                    lie_gens.append(
                        (cl31_gens[i] @ cl31_gens[j] - cl31_gens[j] @ cl31_gens[i]) / 2
                    )
            lie_mat = np.column_stack([g.flatten() for g in lie_gens])
            so31_dim = np.linalg.matrix_rank(lie_mat, tol=1e-8)
            so31_close = True
            for i in range(6):
                for j in range(i + 1, 6):
                    bracket = lie_gens[i] @ lie_gens[j] - lie_gens[j] @ lie_gens[i]
                    coeffs, _, _, _ = np.linalg.lstsq(lie_mat, bracket.flatten(), rcond=None)
                    if not np.allclose(lie_mat @ coeffs, bracket.flatten(), atol=1e-8):
                        so31_close = False
                        break
                if not so31_close:
                    break

        # K6' continuous verification
        I4 = np.eye(4)
        k6_cont = all(
            np.allclose(
                np.block([[R, t*N], [Z, R]]) @ np.block([[R, t*N], [Z, R]]),
                np.block([[R, t*N], [Z, R]]) + I4
            ) for t in [0, 0.25, 0.5, 0.75, 1.0]
        )

        rec.update({
            "cl31_count": n31, "cl22_count": n22, "cl_total": n31 + n22,
            "cl_ratio_check": (n31 * 3 == n22 * 2),
            "so31_brackets_close": so31_close, "so31_dim": so31_dim,
            "k6_continuous": k6_cont,
        })

        # ============================================================
        # D. PHYSICS — evaluate arithmetic on B+C outputs
        # ============================================================

        # alpha_S via K4 deficit
        Z_part = 1.0 / (1.0 - phi_bar ** 2)
        rho_eq = 1.0 - 1.0 / Z_part
        alpha_S = 0.5 - rho_eq

        # sin^2(theta_W) from matter content
        # Q_L:(3,2)_1/3  u_R:(3,1)_4/3  d_R:(3,1)_-2/3  L_L:(1,2)_-1  e_R:(1,1)_-2
        su3d = [3,3,3,1,1]; su2d = [2,1,1,2,1]
        Yc = [1/3, 4/3, -2/3, -1, -2]; chi = [1,-1,-1,1,-1]
        sum_T3_sq = 3*(0.25+0.25) + 0 + 0 + (0.25+0.25) + 0
        sum_Q_sq = (3*((2/3)**2+(1/3)**2) + 3*(2/3)**2 + 3*(1/3)**2 + (0+1) + 1)
        sin2_tW = sum_T3_sq / sum_Q_sq

        # Anomalies
        anomalies = {
            "SU3³": sum(chi[i]*0.5*su2d[i] for i in range(5) if su3d[i]==3),
            "SU2²U1": sum(chi[i]*0.5*su3d[i]*Yc[i] for i in range(5) if su2d[i]==2),
            "SU3²U1": sum(chi[i]*0.5*su2d[i]*Yc[i] for i in range(5) if su3d[i]==3),
            "U1³": sum(chi[i]*su3d[i]*su2d[i]*Yc[i]**3 for i in range(5)),
            "U1grav": sum(chi[i]*su3d[i]*su2d[i]*Yc[i] for i in range(5)),
            "Witten": sum(su3d[i] for i in range(5) if su2d[i]==2 and chi[i]==1),
        }
        for name, val in anomalies.items():
            if name == "Witten":
                assert val % 2 == 0
            else:
                assert abs(val) < 1e-10

        # Exponents
        dim_gauge = (3**2-1) + (2**2-1) + 1  # 12
        delta_nu = dim_gauge + disc            # 17
        exp_nu = 2 * delta_nu                  # 34
        exp_B = exp_nu + 2 * disc              # 44

        # Proton mass
        koide_Q = np.linalg.norm(N, 'fro')**2 / np.linalg.norm(R, 'fro')**2
        proton = 3 / koide_Q  # N_c / Q

        rec.update({
            "alpha_S": alpha_S,
            "alpha_S_chain": {"Z": Z_part, "rho_eq": rho_eq},
            "sin2_theta_W": sin2_tW,
            "anomalies": anomalies, "anomalies_all_zero": True,
            "dim_gauge": dim_gauge,
            "nu_exponent": exp_nu, "nu_mass_ratio": phi_bar ** exp_nu,
            "eta_B_exponent": exp_B, "eta_B": phi_bar ** exp_B,
            "koide_NR": koide_Q, "proton_ratio": proton,
            "L_bits": np.log2(phi),
            "landauer_cost": 1.0 / np.log2(phi),
            "bekenstein_ratio": 2.0,
        })

        # ============================================================
        # E. DYNAMICS — L applied to L's own output
        # ============================================================
        L_eigs = sorted(np.linalg.eigvals(L).real)

        # N self-transparency
        L_NN = sylvester(N)
        from scipy.linalg import null_space
        ker_NN = null_space(L_NN, rcond=1e-10).shape[1]
        assert ker_NN == 0

        # ker generates im (Q_k from ker_im_decomposition)
        NR = N @ R
        ker_gen_im = all(
            np.linalg.norm(Q_k @ (Q_k.T @ (K1 @ K2).flatten())) < 1e-10
            for K1 in [N, NR] for K2 in [N, NR]
        )

        # Conservation
        ker_LT = null_space(L.T, rcond=1e-10)

        rec.update({
            "L_eigenvalues": L_eigs,
            "N_self_transparent": True, "N_ker_dim": ker_NN,
            "ker_generates_im": ker_gen_im,
            "conserved_charges": ker_LT.shape[1],
        })

        return rec

    def __repr__(self):
        return "Production(one operation, five readings)"


# ---- self-test ----
if __name__ == "__main__":
    p = Production()
    d = p.derive()

    checks = [
        ("R²=R+I", all(d["identities"].values())),
        ("P²=P", d["P_idempotent"]),
        ("so(3,1)", d["so31_brackets_close"]),
        ("anomalies", d["anomalies_all_zero"]),
        ("K6' continuous", d["k6_continuous"]),
        ("N transparent", d["N_self_transparent"]),
        ("ker→im", d["ker_generates_im"]),
        ("α_S", abs(d["alpha_S"] - 0.1180339887) < 1e-8),
        ("sin²θ_W", abs(d["sin2_theta_W"] - 0.375) < 1e-10),
        ("proton", abs(d["proton_ratio"] - 4.5) < 1e-10),
    ]

    all_pass = True
    for name, ok in checks:
        status = "✓" if ok else "✗"
        print(f"  {status} {name}")
        if not ok:
            all_pass = False

    print(f"\n  {'ALL PASS' if all_pass else 'FAILURES DETECTED'}")
    print(f"  One operation. Five readings. {len(d)} outputs.")
