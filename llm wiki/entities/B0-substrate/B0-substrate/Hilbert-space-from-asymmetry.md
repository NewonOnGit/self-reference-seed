---
type: entity
role: CORE
theorem: "Thm 2.4c"
level: B0
tags: [b0-substrate, core, forced, quantum]
status: FROZEN
---

# Hilbert space from asymmetry

> Quantum mechanics is not postulated. It is derived from the fact that the naming act is not its own mirror.

## Plain English

Quantum mechanics lives in Hilbert space — a vector space with an inner product that lets you compute probabilities. Where does Hilbert space come from? In standard physics, it's assumed. In this framework, it's derived.

The chain: P ≠ Pᵀ (the naming act is asymmetric) → the transposition map X → Xᵀ acts nontrivially → this defines a Cartan involution θ(X) = -Xᵀ → the modified Killing form B_θ(X,Y) = 4·tr(XYᵀ) is positive definite (it's the Frobenius inner product) → combined with N²=-I (complex structure), you get a Hermitian inner product → that IS a Hilbert space.

At tower depth 1: dim_ℂ = 2, dim_ℝ = 4 ≥ 3. Gleason's theorem applies: the Born rule is forced. Probabilities = |⟨ψ|φ⟩|². Not assumed. Forced.

The entire chain: asymmetry → transposition → Cartan → positive-definite → complex structure → Hilbert → Born → quantum mechanics. Eight steps, zero postulates, one input (P≠Pᵀ).

## Orientation reading

The asymmetry P≠Pᵀ IS orientation existing. Orientation forces a nontrivial transposition map. That map defines the Cartan involution, which produces a positive-definite form. The positive form + the complex structure (from N²=-I) = Hilbert space. Quantum mechanics IS orientation's inner product structure.

Without orientation (P=Pᵀ): no Cartan involution, no positive-definite form, no Hilbert space, no Born rule, no quantum mechanics, no Bell violation. Classical world only.

## Technical statement

**Theorem 2.4c.** P≠Pᵀ forces N≠0. N²=-I gives complex structure: (a+bi)v = av+bNv. The Cartan involution θ(X)=-Xᵀ is forced by P≠Pᵀ. B_θ(X,Y) = 4tr(XYᵀ) is positive definite (Frobenius). Compatibility: B_θ(NX,NY) = B_θ(X,Y). The Hermitian form ⟨X,Y⟩ = B_θ(X,Y) + i·B_θ(X,NY) is positive definite. This IS a Hilbert space. Tower depth 1 gives dim_ℂ=2, dim_ℝ=4≥3: Gleason forces Born rule. [Tier A]

## Dependencies

- [[P]] (P≠Pᵀ)
- [[Asymmetry-is-forced]] (N≠0)
- [[N]] (N²=-I, complex structure)

## Used by

- [[Bell-violation-—-Tsirelson-saturation]] (Hilbert → entanglement → S=2√2)
- [[CNOT-from-framework-generators]] (quantum gates live in Hilbert space)
- [[The-explanatory-gap]] (ker/im decomposition in Hilbert space)
