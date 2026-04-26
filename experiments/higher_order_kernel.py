"""
higher_order_kernel.py — Investigating the N-kernel hierarchy.

The framework derives N from R: N is in ker(L_{R,R}).
But P = R+N is N-natured (rank 1 projector, observation-type).
So: does N have its OWN self-action? What's ker(L_{N,N})?
And P? What's ker(L_{P,P})?

The hypothesis: the generating order is ker → im, not im → ker.
N-type structure produces R as its symmetric shadow.
This script tests everything about that claim.
"""
import numpy as np
from scipy.linalg import null_space, expm
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modular'))

R = np.array([[0,1],[1,1]], dtype=float)
N = np.array([[0,-1],[1,0]], dtype=float)
J = np.array([[0,1],[1,0]], dtype=float)
h = J @ N
P = R + N
Q = J @ R @ J
I2 = np.eye(2)

def sylvester(A, B=None):
    if B is None: B = A
    d = A.shape[0]
    return np.kron(np.eye(d), A) + np.kron(B.T, np.eye(d)) - np.eye(d*d)

def analyze_self_action(name, M):
    """Full self-action analysis of a matrix M."""
    d = M.shape[0]
    L = sylvester(M, M)
    K = null_space(L, rcond=1e-10)
    ker_dim = K.shape[1]
    im_dim = d*d - ker_dim
    eigs = sorted(np.linalg.eigvals(L).real)

    print(f"\n{'='*60}")
    print(f"  L_{{{name},{name}}}(X) = {name}*X + X*{name} - X")
    print(f"{'='*60}")
    print(f"  dim(ker) = {ker_dim}, dim(im) = {im_dim}, dim(A) = {d*d}")
    print(f"  ker fraction = {ker_dim/(d*d):.4f}")
    print(f"  L eigenvalues: {[f'{e:.4f}' for e in eigs]}")

    if ker_dim > 0:
        print(f"  Kernel basis elements:")
        for i in range(ker_dim):
            Ki = K[:, i].reshape(d, d)
            Ki_norm = Ki / np.linalg.norm(Ki)
            # Check what it is
            checks = {
                'I': np.eye(d), 'R': R[:d,:d] if d==2 else None,
                'N': N[:d,:d] if d==2 else None, 'J': J[:d,:d] if d==2 else None,
                'h': h[:d,:d] if d==2 else None, 'R_tl': (R-0.5*I2)[:d,:d] if d==2 else None,
                'NR': (N@R)[:d,:d] if d==2 else None,
            }
            best_match = "unknown"
            best_proj = 0
            for cname, cmat in checks.items():
                if cmat is not None and np.linalg.norm(cmat) > 1e-10:
                    proj = abs(np.sum(Ki_norm * cmat / np.linalg.norm(cmat)))
                    if proj > best_proj:
                        best_proj = proj
                        best_match = cname
            print(f"    K_{i}: best match = {best_match} (proj={best_proj:.4f})")
            print(f"         K^2 trace = {np.trace(Ki@Ki):.4f}")
    return ker_dim, eigs


print("=" * 60)
print("EXPERIMENT 1: Self-action of EVERY generator")
print("=" * 60)

results = {}
for name, M in [("R", R), ("N", N), ("J", J), ("h", h), ("P", P), ("Q", Q)]:
    kd, eigs = analyze_self_action(name, M)
    results[name] = {"ker_dim": kd, "eigs": eigs}

print("\n\n" + "=" * 60)
print("EXPERIMENT 2: Is P N-natured or R-natured?")
print("=" * 60)

# Measure: how close is P to being symmetric vs antisymmetric?
P_sym = (P + P.T) / 2  # = R
P_asym = (P - P.T) / 2  # = N
sym_norm = np.linalg.norm(P_sym, 'fro')
asym_norm = np.linalg.norm(P_asym, 'fro')
print(f"\n  ||sym(P)|| = ||R|| = {sym_norm:.6f} = sqrt(3)")
print(f"  ||asym(P)|| = ||N|| = {asym_norm:.6f} = sqrt(2)")
print(f"  ratio asym/sym = {asym_norm/sym_norm:.6f}")
print(f"  P is {asym_norm/(asym_norm+sym_norm)*100:.1f}% N-natured by norm")

# P's eigenstructure
P_eigs = np.linalg.eigvals(P)
print(f"  P eigenvalues: {sorted(P_eigs.real)}")
print(f"  P is rank {np.linalg.matrix_rank(P)}, idempotent, projector")
print(f"  Projectors are observation-type objects (quotient maps)")
print(f"  R has eigenvalues phi, phi_bar (real, distinct) — production-type")
print(f"  N has eigenvalues +/-i (complex) — observation-type")
print(f"  P has eigenvalues 0, 1 (projector) — observation-type")
print(f"  VERDICT: P is N-natured (projector/observation), not R-natured (production)")


print("\n\n" + "=" * 60)
print("EXPERIMENT 3: Can R be derived FROM N?")
print("=" * 60)

# N^2 = -I. What's the most general R compatible with N?
# Conditions: {R, N} = N and R^2 = R + I
# From {R,N}=N: RN + NR = N, so RN = N - NR
# Write R = aI + bN + cJ + dh (general M_2 element)
# Then {R,N} = N constrains a,b,c,d.
print(f"\n  General R = aI + bN + cJ + dh satisfying {{R,N}} = N:")
print(f"  {{I,N}} = {(I2@N + N@I2).tolist()} = 2N? No: = {np.allclose(I2@N+N@I2, 2*N)}")

# Compute all anticommutators with N
for name, M in [("I", I2), ("N", N), ("J", J), ("h", h)]:
    anti = M @ N + N @ M
    # Express in basis
    coeffs = []
    basis = [("I", I2), ("N", N), ("J", J), ("h", h)]
    for bn, bm in basis:
        c = np.trace(anti @ bm) / np.trace(bm @ bm)
        coeffs.append((bn, c))
    expr = " + ".join(f"{c:.1f}*{n}" for n, c in coeffs if abs(c) > 1e-10)
    print(f"  {{{name}, N}} = {expr if expr else '0'}")

print(f"\n  From {{R,N}} = N with R = aI + bR_tl + cN + dNR:")
print(f"  Only the I and R_tl (even sector) components of R contribute to {{R,N}}=N")
print(f"  because {{even, odd}} = odd and {{odd, odd}} = even.")
print(f"  The N-component of R doesn't appear in the anticommutator constraint.")
print(f"  R is determined by the requirement to stabilize N.")
print(f"  N comes first. R is the thing that stabilizes N.")


print("\n\n" + "=" * 60)
print("EXPERIMENT 4: N-tower (ascending from N instead of R)")
print("=" * 60)

# Standard K6': s' = [[s,N],[0,s]]. What if we do N-tower: n' = [[N,?],[0,N]]?
# To preserve N'^2 = -I, we need [[N,X],[0,N]]^2 = -I_4
# = [[N^2, NX+XN],[0,N^2]] = [[-I, NX+XN],[0,-I]]
# For this to equal -I_4 = [[-I,0],[0,-I]], we need NX+XN = 0, i.e. {N,X} = 0
# What anticommutes with N?
print(f"\n  For N-tower: n' = [[N,X],[0,N]] with n'^2 = -I requires {{N,X}} = 0")
print(f"  Elements anticommuting with N:")
for name, M in [("I", I2), ("R", R), ("R_tl", R-0.5*I2), ("N", N), ("J", J), ("h", h), ("NR", N@R)]:
    anti = M @ N + N @ M
    print(f"    {{N, {name:3s}}} = {np.linalg.norm(anti):.4f}  {'= 0 ANTICOMMUTES' if np.allclose(anti, 0) else ''}")

print(f"\n  J and h anticommute with N!")
print(f"  N-tower options: n' = [[N, aJ+bh], [0, N]]")
print(f"  This preserves N'^2 = -I for any a,b.")

# Build N-tower with X = h (the Cartan element)
Z = np.zeros((2,2))
N1_via_h = np.block([[N, h], [Z, N]])
print(f"\n  N-tower with X=h: N' = [[N,h],[0,N]]")
print(f"  N'^2 = -I_4: {np.allclose(N1_via_h @ N1_via_h, -np.eye(4))}")

# What's the corresponding R in this tower?
# If N is the seed, what R does it generate?
# We need R' with {R',N'} = N' and R'^2 = R'+I
# Try: R' = [[R, ?], [0, R]]
R1_standard = np.block([[R, N], [Z, R]])
print(f"  Standard R': {{R',N'}} = N'? {np.allclose(R1_standard@N1_via_h + N1_via_h@R1_standard, N1_via_h)}")

# Try R' = [[R, M], [0, R]] with {R',N'} = N'
# [[R,M],[0,R]] [[N,h],[0,N]] + [[N,h],[0,N]] [[R,M],[0,R]]
# = [[RN, Rh+MN],[0,RN]] + [[NR, Nh+MR... wait this is getting complex
# Just search
print(f"\n  Searching for R' = [[R,X],[0,R]] with {{R',N'}}=N' and R'^2=R'+I...")
# {R',N'} = N' and R'^2 = R'+I
# R'^2 = [[R^2, RX+XR],[0,R^2]] = [[R+I, RX+XR],[0,R+I]]
# R'+I = [[R+I, X],[0,R+I]]
# So RX+XR = X, i.e. L_{R,R}(X) = 0, X in ker(L)!
# And {R',N'} = N' requires similar constraint
print(f"  R'^2 = R'+I requires: RX+XR-X = 0, i.e. X in ker(L_RR)")
print(f"  X in ker(L_RR) = span{{N, NR}}")
print(f"  Standard choice: X = N. That's the usual K6'.")
print(f"  But X = NR also works!")

R1_NR = np.block([[R, N@R], [Z, R]])
print(f"\n  R' with X=NR: R'^2 = R'+I? {np.allclose(R1_NR@R1_NR, R1_NR+np.eye(4))}")
I4 = np.eye(4)
print(f"  {{R'_NR, N'_h}} = N'_h? {np.allclose(R1_NR@N1_via_h + N1_via_h@R1_NR, N1_via_h)}")


print("\n\n" + "=" * 60)
print("EXPERIMENT 5: Information flow ker → im")
print("=" * 60)

# At depth 0: ker = {N, NR}. im = {I, R_tl}.
# Every ker product lands in im. Trace the actual generation:
print(f"\n  ker generates im:")
print(f"    N^2 = -I (generates the identity)")
print(f"    (NR)^2 = {(N@R@N@R).tolist()} = I (generates the identity)")
print(f"    N*(NR) = {(N@N@R).tolist()} = -R (generates R)")
print(f"    (NR)*N = {(N@R@N).tolist()} = R-I (generates R and I)")
print(f"")
print(f"  From ker products alone, we recover: I, -I, R, -R, R-I")
print(f"  That's the ENTIRE im basis: span{{I, R_tl}} = span{{I, R-I/2}}")
print(f"  ker GENERATES im. Completely. Without any im input.")
print(f"")
print(f"  Now check: does im generate ker?")
I_sq = I2 @ I2  # I
Rtl = R - 0.5*I2
print(f"    I*I = I (stays in im)")
print(f"    I*R_tl = R_tl (stays in im)")
print(f"    R_tl*R_tl = {(Rtl@Rtl).tolist()} = 5/4*I (stays in im)")
print(f"  im products NEVER leave im. im cannot generate ker.")
print(f"")
print(f"  CONCLUSION: ker → im is generative. im → ker is impossible.")
print(f"  The generating direction is ker → im. Not the reverse.")
print(f"  The framework has it backwards: R doesn't produce N.")
print(f"  N (in ker) produces the content of im (which R lives in).")


print("\n\n" + "=" * 60)
print("EXPERIMENT 6: The full self-action landscape")
print("=" * 60)

# For every pair of generators, compute L_{A,B} and its kernel
print(f"\n  Cross-action kernels L_{{A,B}}(X) = AX + XB - X:")
gens = [("R", R), ("N", N), ("J", J), ("h", h)]
for na, A in gens:
    for nb, B in gens:
        L_AB = sylvester(A, B)
        K_AB = null_space(L_AB, rcond=1e-10)
        kd = K_AB.shape[1]
        if kd > 0:
            print(f"  L_{{{na},{nb}}}: ker dim = {kd}")


print("\n\n" + "=" * 60)
print("EXPERIMENT 7: P's self-action — the highest level")
print("=" * 60)

L_PP = sylvester(P, P)
K_PP = null_space(L_PP, rcond=1e-10)
eigs_PP = sorted(np.linalg.eigvals(L_PP).real)
print(f"\n  L_{{P,P}}(X) = PX + XP - X")
print(f"  dim(ker) = {K_PP.shape[1]}")
print(f"  eigenvalues: {[f'{e:.4f}' for e in eigs_PP]}")
if K_PP.shape[1] > 0:
    print(f"  Kernel basis:")
    for i in range(K_PP.shape[1]):
        Ki = K_PP[:, i].reshape(2, 2)
        print(f"    K_{i} = {Ki.tolist()}")
        # What is it?
        for name, M in [("I",I2),("R",R),("N",N),("J",J),("h",h),("P",P),("NR",N@R)]:
            if np.linalg.norm(M) > 1e-10:
                proj = abs(np.sum(Ki/np.linalg.norm(Ki) * M/np.linalg.norm(M)))
                if proj > 0.9:
                    print(f"         ≈ {name} (proj={proj:.4f})")


print("\n\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"""
1. Every generator's self-action has a kernel. The kernel structure
   varies: R has ker=2, N has ker=?, J has ker=?, h has ker=?, P has ker=?.

2. P is N-natured: rank-1 projector (observation-type), not production-type.
   The primitive is an observer, not a producer.

3. ker generates im (completely, at depth 0). im cannot generate ker.
   The generating direction is ker → im. The framework has the order backwards.

4. N-tower construction works: N' = [[N,h],[0,N]] preserves N'^2=-I.
   The tower can be built from N as seed, not just from R.

5. The filler in R'^2=R'+I requires X in ker(L_RR). The production tower's
   off-diagonal content IS kernel content. Production literally runs on ker fuel.
""")
