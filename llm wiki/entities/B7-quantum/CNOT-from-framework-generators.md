---
type: entity
role: QUANTUM
theorem: "Thm 15.4"
level: B7
tags: [b7-quantum, gates, CNOT, forced]
status: FROZEN
---

# CNOT from framework generators

> Every quantum gate built from {h, J}. No quantum mechanics assumed. The Cartan decides; the swap acts.

## Plain English

The CNOT gate is the fundamental two-qubit operation in quantum computing. It flips the second qubit if the first is |1⟩. In standard quantum computing, CNOT is a given. Here it's DERIVED:

CNOT = (I+h)/2 ⊗ I + (I-h)/2 ⊗ J

The Cartan h has eigenvalues +1 and -1. (I+h)/2 projects onto |0⟩. (I-h)/2 projects onto |1⟩. If control is |0⟩: do nothing (⊗I). If |1⟩: swap (⊗J). That's CNOT.

Hadamard: H = (J+h)/√2. Ground plus Cartan, normalized. All from {h, J}. No quantum postulates. The Hilbert space comes from N²=-I. The gates come from the algebra's own generators.

## Orientation reading

h distinguishes eigenvalues. J swaps them. CNOT = "if the Cartan says -1, swap." The quantum gate is the algebra's own decision structure. The Bell state |Φ⁺⟩ = (|00⟩+|11⟩)/√2 comes from CNOT(H⊗I)|00⟩ — entanglement from non-commutativity, which comes from N²=-I, which comes from P≠Pᵀ.

## Technical statement

**Theorem 15.4.** CNOT = (I+h)/2 ⊗ I + (I-h)/2 ⊗ J. Matches standard CNOT matrix. [Tier A]

**Theorem 15.5.** H = (J+h)/√2. H²=I. [Tier A]

**Eight quantum algorithms** from {h,J,N}: Deutsch-Jozsa, Teleportation, Grover, Phase Estimation, Shor(N=15), Quantum Walk, HHL, VQE(H₂). 8/8 pass.

## Dependencies

- [[N]] (N²=-I gives Hilbert space)
- [[Hilbert-space-from-asymmetry]] (inner product)

## Used by

- [[Bell-violation-—-Tsirelson-saturation]] (CNOT creates Bell state)
- [[Fibonacci-TQC-universality]] (extends to topological QC)
