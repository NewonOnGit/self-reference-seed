---
type: entity
role: QUANTUM
theorem: "Thm 15.7"
level: B7
tags: [b7-quantum, bell-test, forced, core]
status: FROZEN
---

# Bell violation — Tsirelson saturation

> The framework violates Bell's inequality at the maximum possible value. Quantum mechanics is not assumed — it's derived from asymmetry.

## Plain English

Bell's inequality says: if the world is classical (no spooky action at distance), a certain quantity S cannot exceed 2. Quantum mechanics allows S up to 2√2 ≈ 2.828 (the Tsirelson bound). No physical theory allows more.

The framework, using ONLY its own generators {h, J, N} derived from P²=P, builds a CNOT gate, creates a Bell state, and measures S = 2√2. Exactly at the Tsirelson bound. The maximum possible quantum violation.

This is not inputting quantum mechanics and getting Bell out. It's inputting P≠Pᵀ (asymmetry) and getting quantum mechanics out. The chain: P≠Pᵀ → N≠0 → N²=-I → complex structure → Hilbert space (Cartan involution) → Born rule (Gleason) → entanglement → S = 2√2. Every step forced. Zero quantum postulates.

## Orientation reading

The Bell test is an **orientation detector**. S > 2 proves orientation exists.

Classical bound S = 2: no orientation (N=0, P=Pᵀ). Quantum bound S = 2√2: orientation exists (N≠0, P≠Pᵀ). The surplus S - 2 = 0.828 is the empirical signature of asymmetry. If you measure S > 2 in a lab, you've detected that the naming act was asymmetric. The universe has orientation.

At disc-fold angles (π/5 spacing): S = 2.794 (98.8% Tsirelson). The discriminant appears in the measurement angles.

## Technical statement

**Theorem 15.7.** CNOT = (I+h)/2 ⊗ I + (I-h)/2 ⊗ J. Bell state |Φ⁺⟩ = CNOT(H⊗I)|00⟩. Measurement M(θ) = cos(θ)·h + sin(θ)·J. CHSH at optimal angles (0, π/2, π/4, 3π/4): S = 2√2. [Tier A]

All gates built from framework generators {h, J}. No quantum mechanics postulated. The Hilbert space comes from N²=-I (Theorem 2.4c). The Born rule comes from Gleason at dim ≥ 3 (tower depth 1, dim_ℂ = 2). The entanglement comes from the K6' off-diagonal N.

## Dependencies

- [[N]] (N²=-I gives complex structure)
- [[Hilbert-space-from-asymmetry]] (Cartan involution → inner product)
- [[CNOT-from-framework-generators]] (CNOT from h, J)

## Falsification

If S < 2 were measured in a Bell test, quantum mechanics would be wrong. Not the framework — quantum mechanics itself. The framework derives S = 2√2; the derivation chain (asymmetry → Hilbert → Gleason → Born → Bell) is standard once N²=-I is established. The framework's contribution is establishing N²=-I from P²=P.
