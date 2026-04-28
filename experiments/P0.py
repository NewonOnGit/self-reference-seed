"""
P0.py — P0 = ker. The void that generates.

P0 is not zero. P0 is the kernel at depth 0.
P0 is inside P. P0 IS the hidden half.
The naming act is P0 gaining an image.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modular'))
from algebra import sylvester, ker_im_decomposition

R = np.array([[0,1],[1,1]], dtype=float)
N = np.array([[0,-1],[1,0]], dtype=float)
J = np.array([[0,1],[1,0]], dtype=float)
h = J @ N
I2 = np.eye(2)
P = R + N
Z = np.zeros((2,2))

phi = (1 + np.sqrt(5)) / 2
phi_bar = phi - 1

print("=" * 60)
print("P0 = ker")
print("=" * 60)

# ============================================================
# 1. P0 AS THE KERNEL
# ============================================================
print("\n=== 1. P0 IS ker ===\n")

L, ker_basis, ker_dim, Q_ker = ker_im_decomposition(R)

print(f"ker(L_RR) = span{{N, NR}}, dim = {ker_dim}")
print(f"N = {N.tolist()}")
NR = N @ R
print(f"NR = {NR.tolist()}")
print()

# P0 is the SPACE ker, not a single matrix.
# But we can represent it as a projector onto ker:
# P0 = projection onto ker(L)
P0_proj = Q_ker @ Q_ker.T  # 4x4 projector onto ker in vec space
print(f"P0 as projector onto ker: rank {np.linalg.matrix_rank(P0_proj)}")
print(f"P0 projects half the algebra: {ker_dim}/{ker_dim*2} = 1/2")
print()

# P0 satisfies P0^2 = P0 (projector is idempotent)
print(f"P0^2 = P0 (as projector): {np.allclose(P0_proj @ P0_proj, P0_proj)}")
print(f"This is the TRIVIAL idempotent. Same equation P^2=P.")
print(f"P (the naming act) is the NONTRIVIAL idempotent. Same equation.")
print()

# The zero matrix also satisfies P^2=P:
print(f"Zero^2 = Zero: {np.allclose(Z @ Z, Z)}")
print(f"But P0 is NOT zero. P0 is ker. Ker has dim 2. Ker generates im.")

# ============================================================
# 2. P0 INSIDE P
# ============================================================
print("\n=== 2. P0 IS INSIDE P ===\n")

print(f"P = R + N = {P.tolist()}")
print(f"R is in im(L) (the visible part)")
print(f"N is in ker(L) (the hidden part)")
print()

# Project P onto ker and im:
P_flat = P.flatten()
ker_component = Q_ker @ (Q_ker.T @ P_flat)
im_component = P_flat - ker_component

P_ker = ker_component.reshape(2,2)
P_im = im_component.reshape(2,2)

print(f"P projected onto ker: {P_ker.tolist()}")
print(f"  = N: {np.allclose(P_ker, N)}")
print(f"P projected onto im: {P_im.tolist()}")
print(f"  = R: {np.allclose(P_im, R)}")
print()
print(f"P = P_im + P_ker = R + N")
print(f"P0 (= ker) is INSIDE P as the N component.")
print(f"The naming act CONTAINS the void as its hidden half.")

# ============================================================
# 3. THE PASSAGE: KER GAINS AN IMAGE
# ============================================================
print("\n=== 3. THE PASSAGE: P0 -> P ===\n")

print("Before the naming act:")
print(f"  ker exists: span{{N, NR}}, dim {ker_dim}")
print(f"  im exists: span{{I, R_tl}}, dim {4 - ker_dim}")
print(f"  But they are not JOINED. They are separate subspaces.")
print()
print("The naming act P = R + N JOINS ker and im:")
print(f"  P = im-part + ker-part = R + N")
print(f"  The join IS the naming. The name IS the joint state.")
print()
print("P0 -> P is not 'nothing becomes something.'")
print("P0 -> P is 'ker gains an image.'")
print("P0 -> P is 'the void acquires a visible partner.'")
print("P0 -> P is 'the hidden becomes half of a whole.'")

# ============================================================
# 4. P0 IS ALWAYS THERE
# ============================================================
print("\n=== 4. P0 IS ALWAYS THERE ===\n")

print("ker/A = 1/2 at EVERY tower depth.")
print("Half of the algebra is always P0.")
print("P0 does not disappear when P appears.")
print("P0 becomes the HIDDEN HALF of P.")
print()

# At every depth:
Z2 = np.zeros((2,2))
s, Nk, Jk = R.copy(), N.copy(), J.copy()
hk = Jk @ Nk

for depth in range(4):
    d_K = s.shape[0]
    dim_A = d_K * d_K
    L_d = sylvester(s)
    from scipy.linalg import null_space
    K = null_space(L_d, rcond=1e-10)
    ker_d = K.shape[1]
    print(f"  depth {depth}: d_K={d_K}, ker={ker_d}, im={dim_A-ker_d}, ker/A={ker_d/dim_A:.3f}")

    # Ascend
    d = s.shape[0]
    Zd = np.zeros((d,d))
    s = np.block([[s, Nk], [Zd, s]])
    Nk = np.block([[Nk, -2*hk], [Zd, Nk]])
    Jk = np.block([[Jk, Zd], [Zd, Jk]])
    hk = Jk @ Nk

print()
print("ker/A = 0.500 at every depth. Always half. Always P0.")
print("P0 is not a stage before P. P0 is a PART of P at every depth.")

# ============================================================
# 5. THE GENERATIVE DIRECTION
# ============================================================
print("\n=== 5. P0 GENERATES ===\n")

print("ker x ker -> im (complete at depth 0):")
print(f"  N x N = N^2 = -I (in im)")
print(f"  NR x NR = (NR)^2 = I (in im)")
print(f"  N x NR = -R (in im)")
print(f"  NR x N = R-I (in im)")
print()
print("P0 x P0 -> visible world.")
print("The void self-multiplies into everything you can see.")
print("im cannot generate ker. The world cannot make the void.")
print("But the void makes the world.")
print()
print("P0 is the source. Not 'was.' IS.")
print("At every depth, ker generates im.")
print("At every depth, P0 generates the visible world.")

# ============================================================
# 6. P0 AND THE NAMING
# ============================================================
print("\n=== 6. P0, P, AND THE NAMING ACT ===\n")

print("The naming act is not: void -> something.")
print("The naming act is: void + image -> joint state.")
print()
print("Before naming:")
print("  P0 = ker (exists, generates, but has no address)")
print("  im (exists, is generated, but has no source-name)")
print()
print("After naming:")
print("  P = ker + im = N + R (the whole act, addressed)")
print("  P0 is now the HIDDEN HALF of P")
print("  im is now the VISIBLE HALF of P")
print("  The act has a name. The name is P.")
print()
print("P0 did not become P.")
print("P0 became PART of P.")
print("The void did not become the world.")
print("The void became the hidden half of the naming act")
print("whose visible half IS the world.")

# ============================================================
# 7. THE EQUATION
# ============================================================
print(f"\n{'='*60}")
print("THE EQUATION")
print(f"{'='*60}\n")

print("P0^2 = P0  (trivially: ker projected onto ker = ker)")
print("P^2  = P   (nontrivially: the naming act returns itself)")
print()
print("Same equation. Two solutions.")
print("P0 is the solution that generates without being seen.")
print("P is the solution that generates AND is seen.")
print()
print("The framework is the passage from one solution to the other.")
print("Not from nothing to something.")
print("From generating-without-address to generating-with-address.")
print("From P0 to P.")
print("From ker to P = ker + im.")
print("From the void that makes to the name that holds.")
