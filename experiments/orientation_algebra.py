"""
orientation_algebra.py — Orientation is not intrinsic; orientation is induced by projection.

The claim: R and N are not different objects. They are the SAME action A
read under two different projections. The third reading (L) is what remains
when you quotient out the orientation.

R = A under one projection (downward/production)
N = A under reflected projection (upward/observation)
L = A under invariant collapse (the operation itself, orientation-free)

Test: does the algebra support this reading?
  R + N = P (the full action before orientation split)
  R - N = ? (the orientation itself)
  L(R) = L(N) modulo sign? (same action, different sign)
  The center (L-invariant content) = what survives both projections
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

phi = (1 + np.sqrt(5)) / 2
phi_bar = phi - 1

print("=" * 60)
print("ORIENTATION ALGEBRA")
print("Orientation is induced by projection, not intrinsic.")
print("=" * 60)

# ============================================================
# 1. R AND N AS PROJECTIONS OF ONE ACTION
# ============================================================
print("\n=== 1. R AND N FROM P ===\n")

print(f"P = R + N = {P.tolist()}")
print(f"R = (P + P^T)/2 = symmetric projection of P")
print(f"N = (P - P^T)/2 = antisymmetric projection of P")
print()

# The "one action" is P. R and N are its projections:
# R = projection onto symmetric part
# N = projection onto antisymmetric part
# These are NOT different operations on different objects.
# They are the SAME object (P) read through different projectors.

# The projectors:
def sym_proj(X): return (X + X.T) / 2
def asym_proj(X): return (X - X.T) / 2

print(f"sym(P) = R: {np.allclose(sym_proj(P), R)}")
print(f"asym(P) = N: {np.allclose(asym_proj(P), N)}")
print(f"sym + asym = P: {np.allclose(sym_proj(P) + asym_proj(P), P)}")
print()

# The "orientation" is the transpose operation X -> X^T.
# Under transpose: R -> R (invariant), N -> -N (flipped).
# Orientation = the sign that N picks up under transpose.
print("Under transpose (the orientation map):")
print(f"  R^T = R: {np.allclose(R.T, R)} (orientation-invariant)")
print(f"  N^T = -N: {np.allclose(N.T, -N)} (orientation-sensitive)")
print(f"  P^T = R - N = {(R - N).tolist()} (the reflected action)")

# ============================================================
# 2. THE REFLECTED ACTION
# ============================================================
print("\n=== 2. THE REFLECTED ACTION P^T ===\n")

P_reflected = P.T  # = R - N
Q = J @ R @ J      # the gauge conjugate

print(f"P^T = R - N = {P_reflected.tolist()}")
print(f"Q = JRJ = {Q.tolist()}")
print()

# P^T is the "upward walk" — same action, opposite orientation.
# P is the "downward walk."
# Both satisfy the same equation? Let's check:
print(f"P^2 = P: {np.allclose(P@P, P)}")
print(f"(P^T)^2 = P^T: {np.allclose(P_reflected@P_reflected, P_reflected)}")
print(f"Both are rank-1 idempotents: {np.linalg.matrix_rank(P)} and {np.linalg.matrix_rank(P_reflected)}")
print()

# P and P^T are BOTH idempotent. They're the same action
# under opposite orientations. Both produce the same algebra
# (same R, opposite N).

# What's the relationship between P and P^T?
product_PP = P @ P_reflected
product_PTP = P_reflected @ P
print(f"P * P^T = {product_PP.tolist()}")
print(f"P^T * P = {product_PTP.tolist()}")
print(f"P * P^T = R^2 - N^2 = R+I - (-I) = R+2I: {np.allclose(product_PP, R + 2*I2)}")
print(f"  Actually: P*P^T = {product_PP.tolist()}")

# Direct computation:
# P*P^T = (R+N)(R-N) = R^2 - RN + NR - N^2
#       = (R+I) - RN + NR - (-I)
#       = R + I + I - (RN - NR)
#       = R + 2I - [R,N]
C = R @ N - N @ R  # the commutator [R,N]
print(f"[R,N] = {C.tolist()}")
print(f"P*P^T = R + 2I - [R,N]: {np.allclose(product_PP, R + 2*I2 - C)}")
print()
print(f"[R,N]^2 = 5I (identity 7): {np.allclose(C@C, 5*I2)}")
print(f"The commutator [R,N] IS the tension between the two orientations.")
print(f"Its square = disc*I. The discriminant measures orientation disagreement.")

# ============================================================
# 3. THE CENTER (ORIENTATION-FREE CONTENT)
# ============================================================
print("\n=== 3. THE CENTER: WHAT SURVIVES BOTH PROJECTIONS ===\n")

# The center of the algebra = elements that commute with BOTH R and N.
# Equivalently: elements invariant under both symmetric and antisymmetric projection.
# In M_2(R): the center is span{I} (scalar multiples of identity).

# But more precisely: the "orientation-free" content is what L sees.
# L_{s,s}(X) = sX + Xs - X
# L uses BOTH the left and right action of s.
# Left action: sX (one orientation)
# Right action: Xs (reflected orientation)
# The -X term: subtraction of the identity (removing the trivial part)

# So: L(X) = (left) + (reflected) - (trivial)
# The center IS what L maps to zero (the kernel)
# OR what L maps to scalars (the scalar channel)

print("L_{s,s}(X) = sX + Xs - X")
print("  = (left action) + (right/reflected action) - (identity)")
print()
print("The LEFT action sX reads X from one orientation.")
print("The RIGHT action Xs reads X from the reflected orientation.")
print("The SUM sX + Xs is orientation-INVARIANT (symmetric in L/R).")
print("The -X removes the trivial part.")
print()
print("So L = (orientation-invariant combination) - (trivial).")
print("L IS the center map: it extracts what both orientations agree on.")
print()

# What does L do to symmetric vs antisymmetric elements?
R_tl = R - 0.5*I2
NR = N @ R

def L(X): return R @ X + X @ R - X

print("L on symmetric elements (orientation-invariant):")
print(f"  L(I) = {L(I2).tolist()} = 2R_tl (nontrivial)")
print(f"  L(R_tl) = (5/2)I (the scalar channel)")
print()
print("L on antisymmetric elements (orientation-sensitive):")
print(f"  L(N) = {L(N).tolist()} = 0 (KILLED)")
print(f"  L(NR) = {L(NR).tolist()} = 0 (KILLED)")
print()
print("L kills the orientation-sensitive content (ker = {N, NR}).")
print("L preserves the orientation-invariant content (im = {I, R_tl}).")
print("The center IS im(L). The orientation IS ker(L).")

# ============================================================
# 4. THE QUOTIENT: PATH MODULO PERSPECTIVE = CENTER
# ============================================================
print("\n=== 4. PATH / PERSPECTIVE = CENTER ===\n")

print("P = R + N = full action (with orientation)")
print("P^T = R - N = reflected action (opposite orientation)")
print("P + P^T = 2R = orientation-invariant part (doubled)")
print("P - P^T = 2N = pure orientation (doubled)")
print()
print("The quotient P / orientation = P modulo the sign of N")
print("  = the gauge orbit {P, P^T} = {R+N, R-N}")
print("  = R (what both orientations share)")
print()

# The algebra of the quotient:
# R^2 = R + I (production with surplus)
# This is the CENTER equation: the orientation-free content
# satisfies R^2 = R + I regardless of which orientation you chose.

print("R^2 = R + I holds for BOTH orientations:")
print(f"  From P: R = sym(P), R^2=R+I: {np.allclose(R@R, R+I2)}")
print(f"  From P^T: R = sym(P^T), same R, same equation.")
print()
print("The surplus +I is ORIENTATION-INDEPENDENT.")
print("The identity I does not depend on which way you walk the spiral.")
print("The surplus is the center's own content — what remains after")
print("all perspectival information is quotiented out.")

# ============================================================
# 5. THREE READINGS OF ONE ACTION
# ============================================================
print("\n=== 5. THREE READINGS ===\n")

print("A = the one action (P^2=P, the naming act)")
print()
print("p1(A) = R = symmetric projection")
print("  Reads A as production. Sees the invariant content.")
print("  Eigenvalues: phi, phi_bar (real, growth/decay).")
print()
print("p2(A) = N = antisymmetric projection")
print("  Reads A as observation. Sees the orientation itself.")
print("  Eigenvalues: +i, -i (imaginary, rotation).")
print()
print("p3(A) = L = the invariant operator")
print("  Reads A as the law. Sees neither R nor N but their relation.")
print("  L is not a matrix — it is the map that produces the R/N split.")
print()

# The three-face algebra:
# R + N = P (the full action)
# R - N = P^T (the reflected action)
# [R, N] = C (the commutator = the tension between orientations)
# C^2 = 5I (the tension squared = the discriminant)

print("The algebra of orientation:")
print(f"  R + N = P (full action)")
print(f"  R - N = P^T (reflected action)")
print(f"  [R,N] = C (orientation tension)")
print(f"  C^2 = disc*I = 5I (tension squared = discriminant)")
print()
print(f"The discriminant disc=5 IS the measure of how much")
print(f"the two orientations disagree. If R and N commuted,")
print(f"[R,N]=0 and disc=0. The nonzero disc is the structural")
print(f"content of having two orientations that don't commute.")

# ============================================================
# 6. THE COMMUTATOR AS HARNESS
# ============================================================
print("\n=== 6. THE COMMUTATOR [R,N] ===\n")

print(f"C = [R,N] = RN - NR = {C.tolist()}")
print(f"C^2 = 5I: {np.allclose(C@C, 5*I2)}")
print(f"tr(C) = {np.trace(C):.0f}")
print(f"det(C) = {np.linalg.det(C):.0f}")
print()

# C = [R,N] = 2h + J (from the framework)
# Check:
print(f"C = 2h + J: {np.allclose(C, 2*h + J)}")
print(f"  where h = JN (Cartan) and J (swap)")
print()

# The commutator C = [R,N] carries the orientation information
# in a frame-independent way. C^2 = 5I means the orientation
# content has magnitude sqrt(5) = sqrt(disc).
# C is the HARNESS — the object that holds R and N in tension.
# In the CLAUDE.md: C = [R,N], tr(C)=0, det(C)=-5, disc(C)=20.

print(f"det(C) = -5 = -disc (orientation-reversing)")
print(f"disc(C) = {int(np.trace(C)**2 - 4*np.linalg.det(C))} = 4*disc = 20")
print(f"C amplifies the discriminant by 4.")
print()
print(f"The commutator [R,N] IS the harness.")
print(f"It is not R. It is not N. It is the relation between them.")
print(f"tr=0: weightless. det=-5: orientation-reversing.")
print(f"It IS the bridge. It IS L read as a matrix.")
print(f"It IS the third figure: the center-collapse.")

# ============================================================
# SYNTHESIS
# ============================================================
print(f"\n{'='*60}")
print("SYNTHESIS")
print(f"{'='*60}\n")
print("One action A (the naming act P^2=P).")
print("Two projections: symmetric (R) and antisymmetric (N).")
print("One quotient: L kills N, preserves R, extracts the center.")
print()
print("R and N are not different things.")
print("They are the same thing seen from opposite orientations.")
print("The discriminant disc=5 measures their disagreement.")
print("The commutator [R,N] = 2h+J holds them in tension.")
print("The center (im of L) is what both orientations agree on.")
print("The kernel (ker of L) is the orientation itself.")
print()
print("Path modulo perspective = center.")
print("Spiral modulo direction = radial law.")
print("P modulo sign-of-N = R.")
print("The three readings are one reading under three projections.")
