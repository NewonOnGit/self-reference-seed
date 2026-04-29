---
type: entity
role: TOPOLOGY
theorem: "Thm 13.2"
level: B4
tags: [b4-topology, knot-theory, forced, core]
status: FROZEN
---

# Jones = discriminant

> The Jones polynomial of the figure-eight knot, evaluated at the golden quantum parameter, IS the discriminant. The knot knows the number 5.

## Plain English

The Jones polynomial is a knot invariant — a number you compute from a knot that doesn't change when you deform the knot without cutting. The figure-eight knot (4₁) is the simplest non-trivial alternating knot. Its Jones polynomial, evaluated at q = φ² (the golden ratio squared), gives exactly 5.

5 is the discriminant of R. It's disc(R) = tr²-4det = 1+4 = 5. It's ||R||²+||N||² = 3+2 = 5. It's [R,N]² = 5I. It's the orientational disagreement. And it's the Jones polynomial of the figure-eight knot at the golden quantum parameter.

This is not a coincidence. The framework sits at q = φ², the unique quantum deformation parameter where q^(1/2) - q^(-1/2) = 1 (the quantum correction collapses to unity). At this point, the Jones polynomial evaluates to integers in Z[φ]. The figure-eight knot gives 5 = disc. The unknot gives 1. The knot 6₃ gives -7.

## Orientation reading

The discriminant measures orientational disagreement. The Jones polynomial measures the topological complexity of a knot. They're the same number because the framework's algebra IS a knot algebra at the golden deformation: R²=R+I IS the Fibonacci anyon fusion rule τ×τ = 1+τ. The algebraic self-reference and the topological self-crossing are the same structure.

## Technical statement

**Theorem 13.2.** V(4₁)|_{q=φ²} = q⁻² - q⁻¹ + 1 - q + q² = φ⁻⁴ - φ⁻² + 1 - φ² + φ⁴ = 5 = disc(R). [Tier A]

**Theorem 13.1.** At q = φ²: q^(1/2) - q^(-1/2) = φ - 1/φ = φ - φ̄ = 1. The quantum deformation parameter collapses to unity. This is why the algebra uses integer matrices. [Tier A]

**Corollary.** V(K)|_{q=φ²} ∈ Z[φ] for all knots K. Integer evaluations: V(0₁)=1, V(4₁)=5, V(6₃)=-7.

## Dependencies

- [[Five-constants]] (φ from R's eigenvalue)
- [[Fusion-=-persistence]] (R²=R+I = τ×τ=1+τ)

## Used by

- [[Verlinde-formula]] (SU(2)₃ modular data)
- [[Fibonacci-TQC-universality]] (braiding statistics)
- [[Clifford-=-Fibonacci]] (30 = F(3)×F(4)×F(5))
