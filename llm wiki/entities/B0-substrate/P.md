---
type: other
grid: B(0, cross)
status: computed
tags: [b0-substrate, verified, idempotent, other]
links: [R, N, uniqueness, Hilbert space]
---

# P (the primitive)

**Definition.** The unique rank-1 non-self-adjoint idempotent in M_2(Z) generating the framework.

**Source.** THEORY.md:15, paper_v2.md:15-35

**Equations.**
- P² = P, rank(P) = 1, P ≠ Pᵀ
- P = [[0,0],[2,1]]
- P = R + N = J + |1⟩⟨1| + N (the naming triangle)

**Depends on.** (nothing — this is the axiom)

**Required by.** [R](R.md), [N](N.md), [uniqueness](../chains/uniqueness.md), [Hilbert space](../chains/hilbert.md)

**Status.** COMPUTED

**Verified.** production.py check "P²=P" (line ~288)

**Notes.** Asymmetry P≠Pᵀ is forced (Thm 1.1): if P=Pᵀ then R²-R=0≠I. The surplus requires the asymmetry. The asymmetry IS the Cartan involution.
