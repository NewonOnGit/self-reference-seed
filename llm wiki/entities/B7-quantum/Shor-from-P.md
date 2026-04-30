---
type: entity
role: QUANTUM
theorem: "Thm 15c.3"
level: B7
tags: [b7-quantum, shor, arithmetic, forced, core]
status: FROZEN
---

# Shor's algorithm from P²=P

> Every computational step of Shor's quantum factoring algorithm is forced from one asymmetric idempotent. The only external input: "factor this N."

## Plain English

Shor's algorithm factors large numbers exponentially faster than any known classical algorithm. It's the reason quantum computers could break encryption. In standard quantum computing, the algorithm is presented as a recipe using quantum gates, quantum Fourier transforms, and number theory.

In the framework: every piece is forced from P²=P.

The complex structure (N²=-I) gives all phases. The tower depths give natural numbers (Peano axioms). The quotient grammar gives integers, modular arithmetic, and the multiplicative group. The Euclidean algorithm IS iterated quotient compression. Every QFT entry is exp(θN). Every measurement is P²=P (rank-1 projection). Every post-processing step (continued fractions) is the Euclidean algorithm on rationals.

15 = 3 × 5. From P = [[0,0],[2,1]]. 29 checks pass.

## The chain

```
P²=P, P≠Pᵀ
  → N²=-I (complex structure: all phases)
  → Tower depths → N (Peano arithmetic)
  → N → Z (Grothendieck completion)
  → Z → Z/NZ (period-N quotient)
  → Euclidean algorithm (iterated quotient → Bezout → (Z/NZ)*)
  → Modular exponentiation (iterated group operation)
  → QFT (pure N-rotations: F_{jk} = exp(2πjk/Q · N)/√Q)
  → Measurement (P²=P idempotent projection, Born rule)
  → Continued fractions (Euclidean on rationals)
  → gcd(a^(r/2)±1, N) → nontrivial factors
```

## Key identifications

- **Every phase gate = exp(θN).** Hadamard, controlled-phase, QFT — all pure N-rotations.
- **Tower depths = natural numbers.** K6' successor = Peano successor.
- **Euclidean algorithm = iterated quotient compression.** The framework's quotient grammar computes gcd.
- **Measurement = P²=P.** The projection |k⟩⟨k| IS a rank-1 idempotent.
- **Modular exponentiation = iterated group operation in (Z/NZ)*,** which is forced by Bezout, which is forced by Euclidean, which IS L applied to the integer lattice.

## Dependencies

- [[N]] (N²=-I gives all phases)
- [[Tower-and-K6]] (depths = Peano arithmetic)
- [[CNOT-from-framework-generators]] (quantum gates from {h,J,N})
- [[P]] (P²=P = measurement postulate)

## Verified

29 computational checks. 15 = 3 × 5 via order-finding (r=4 for a=7 mod 15), b=a^(r/2)=4, gcd(3,15)=3, gcd(5,15)=5. All from [[0,0],[2,1]].
