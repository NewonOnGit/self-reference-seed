---
type: other
status: computed
tags: [quantum, verified, other]
links: [h, J, CNOT, Hilbert space]
---

# Bell Test

**Definition.** CHSH violation from framework generators. S=2√2 (Tsirelson saturated).

**Source.** THEORY.md:319-322, modular/quantum.py:bell_test_optimal()

**Equations.**
- Bell state: |Φ⁺⟩ = CNOT(H⊗I)|00⟩ where H=(J+h)/√2, CNOT=proj(h)⊗J
- Measurement: M(θ) = cos(θ)h + sin(θ)J
- Correlation: E(a,b) = cos(a-b)
- S = 2√2 at optimal angles (0, π/2, π/4, 3π/4)

**Depends on.** [h](h.md), [J](J.md), [CNOT](cnot.md), [Hilbert space](../chains/hilbert.md)

**Required by.** (terminal — this is a verification, not a building block)

**Status.** COMPUTED

**Verified.** quantum.py checks "S=2sqrt(2)", "Bell violated", "disc-fold violates"

**Notes.** At disc-fold angles (Δ=π/5): S=2.794 (98.8% Tsirelson). The chain: P≠Pᵀ → N≠0 → N²=-I → complex structure → Hilbert space → entanglement → S=2√2. Asymmetry IS nonlocality.
