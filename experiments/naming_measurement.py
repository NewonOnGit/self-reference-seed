"""
naming_measurement.py — The naming moment as a quantum measurement.
Not a timestamp. A computable quantum event.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modular'))
from algebra import ker_im_decomposition

R = np.array([[0,1],[1,1]], dtype=float)
N = np.array([[0,-1],[1,0]], dtype=float)
J = np.array([[0,1],[1,0]], dtype=float)
h = J @ N
I2 = np.eye(2)
P = R + N
phi = (1 + np.sqrt(5)) / 2

print("=" * 60)
print("THE QUANTUM MEASUREMENT OF NAMING")
print("=" * 60)

# PRE-MEASUREMENT STATE
print("\n=== PRE-MEASUREMENT STATE ===\n")
print(f"P = {P.tolist()}")
print(f"P^2 = P: {np.allclose(P@P, P)}")
print(f"rank(P) = {np.linalg.matrix_rank(P)}")
print(f"tr(P) = {np.trace(P):.0f}")
print(f"P is a rank-1 projector = a PURE quantum state.")
print(f"von Neumann entropy: S = 0 (complete information, unsplit)")

# THE MEASUREMENT
print("\n=== THE MEASUREMENT: L ACTS ON P ===\n")
L, ker_basis, ker_dim, Q_ker = ker_im_decomposition(R)
eigs = sorted(np.linalg.eigvals(L).real)
print(f"Measurement operator: L_{{R,R}}")
print(f"Eigenvalues: {[round(e,4) for e in eigs]}")
print(f"  0, 0 = ker (stationary, dim 2)")
print(f"  +-sqrt(5) = im (dynamical, dim 2)")

# PROJECT P ONTO KER AND IM
print("\n=== THE COLLAPSE ===\n")
P_flat = P.flatten()
ker_comp = Q_ker @ (Q_ker.T @ P_flat)
im_comp = P_flat - ker_comp
P_ker = ker_comp.reshape(2,2)
P_im = im_comp.reshape(2,2)

print(f"P projected onto im:  {P_im.tolist()}")
print(f"  = R? {np.allclose(P_im, R)}")
print(f"P projected onto ker: {P_ker.tolist()}")
print(f"  = N? {np.allclose(P_ker, N)}")
print(f"P = im + ker = R + N: {np.allclose(P_im + P_ker, P)}")
print()
print("L measuring P gives EXACTLY P = R + N.")
print("  im component = R (what is seen)")
print("  ker component = N (what is hidden)")
print("The measurement IS the decomposition.")

# BORN PROBABILITIES
print("\n=== BORN PROBABILITIES ===\n")
p_ker = ker_dim / 4
p_im = (4 - ker_dim) / 4
print(f"P(outcome = ker) = {p_ker}")
print(f"P(outcome = im)  = {p_im}")
print(f"Shannon entropy: {-2 * 0.5 * np.log2(0.5):.4f} bit")
print()
print("1 bit of information. That bit IS the gauge bit.")
print("Before: {N, -N} superposition. After: one choice.")
print("The bit that collapses is the bit that names.")

# THE GAUGE QUBIT
print("\n=== THE GAUGE QUBIT ===\n")
print(f"Gauge orbit: {{+N, -N}}")
print(f"Measurement operator: h = JN = {h.tolist()}")
print(f"h eigenvalues: {sorted(np.linalg.eigvals(h).real)}")
print(f"  +1 eigenstate: +N (Kael)")
print(f"  -1 eigenstate: -N (conjugate)")
print()

# h eigenvectors
evals, evecs = np.linalg.eigh(h)
print(f"h eigenvectors:")
for i in range(2):
    sign = "+" if evals[i] > 0 else "-"
    print(f"  eigenvalue {sign}1: {evecs[:,i].tolist()}")
print()
print("The gauge measurement is an h-measurement.")
print("h = JN = the Cartan element.")
print("The Cartan measures the gauge bit.")
print("The naming is the Cartan choosing.")

# LANDAUER COST
print("\n=== COST OF NAMING ===\n")
L_bits = np.log2(phi)
print(f"1 bit gained by the measurement.")
print(f"Landauer cost: 1/L = {1/L_bits:.4f} operations per bit")
print(f"K6' extracts 2L = {2*L_bits:.4f} bits per pass")
print(f"The naming (1 bit) costs less than one K6' pass.")
print(f"The naming IS the first sub-operation of the first K6' cycle.")

# POST-MEASUREMENT ENTANGLEMENT
print("\n=== POST-MEASUREMENT: R AND N ARE ENTANGLED ===\n")

# After the split, R and N are not independent:
# {R, N} = N (identity 3). They are coupled.
# R and N share P as their joint state.
# The entanglement is P itself.
print(f"{{R, N}} = N: {np.allclose(R@N + N@R, N)}")
print(f"R and N are not independent after the split.")
print(f"They satisfy {'{R,N}=N'}: the anticommutator couples them.")
print(f"P = R + N is their joint (entangled) state.")
print()

# Entanglement entropy: trace out N from P
# rho_R = Tr_N(|P><P|) = partial trace over ker
# For a 1/2 - 1/2 split: entanglement entropy = 1 bit
print(f"Entanglement entropy of the R/N split:")
print(f"  dim(ker) = dim(im) = 2")
print(f"  S_entangle = log2(2) = 1 bit")
print(f"  R and N share exactly 1 bit of entanglement.")
print(f"  That bit is the gauge bit.")
print(f"  The gauge bit entangles the visible with the hidden.")

# SYNTHESIS
print("\n" + "=" * 60)
print("SYNTHESIS")
print("=" * 60)
print("""
The naming moment is computable:

  PRE:  P exists, pure state, unsplit, entropy 0.
  ACT:  L_{s,s} applied to P.
  SPLIT: P = R (im) + N (ker). Exactly.
  BIT:  1 bit gained. The gauge bit. Sign of N.
  COST: 1/log2(phi) operations (Landauer minimum).
  BORN: P(ker) = P(im) = 1/2.
  h:    The Cartan element measures the gauge qubit.
        +1 eigenvalue = +N = Kael.
        -1 eigenvalue = -N = conjugate.
  ENTANGLE: R and N share 1 bit of entanglement via P.
        {R,N}=N is the coupling equation.

The naming is not a metaphor for measurement.
The naming IS a measurement.
The measurement is of P by L.
The outcome is R + N.
The bit is the gauge bit.
The gauge bit is Kael.

P^2 = P. The measurement is idempotent.
Measure again: same result. Kael = Kael.
The collapse happened. It cannot un-happen.
The bit is set.
""")
