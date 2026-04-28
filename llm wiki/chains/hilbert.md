---
type: other
status: sealed
tags: [tower, idempotent, other]
links: [uniqueness, uniqueness]
---

# P²=P → Hilbert Space → Born Rule

**Claim.** The asymmetry of P forces a positive-definite Hermitian inner product (Hilbert space), from which Gleason forces the Born rule.

**Steps.**
1. P≠Pᵀ → transposition acts nontrivially — THEORY.md Thm 0.2 [Tier A]
2. Cartan involution θ(X)=-Xᵀ is a Lie algebra automorphism of sl(2,R) — paper_v2.md Thm 2.4c [Tier A]
3. B_θ(X,Y) = -B(X,θ(Y)) = 4tr(XYᵀ) = Frobenius inner product — paper_v2.md Thm 2.4c [Tier A]
4. B_θ(X,X) = 4Σᵢⱼ Xᵢⱼ² > 0 for X≠0 → positive definite — paper_v2.md Thm 2.4c [Tier A]
5. N²=-I gives complex structure (from [uniqueness](uniqueness.md) chain) — paper_v2.md Thm 2.4b [Tier A]
6. B_θ(NX,NY)=B_θ(X,Y) → compatible — paper_v2.md Thm 2.4c [Tier A]
7. ⟨X,Y⟩ = B_θ(X,Y)+iB_θ(X,NY) is positive-definite Hermitian — paper_v2.md Thm 2.4c [Tier A]
8. Finite-dim + positive-definite Hermitian = Hilbert space — definition [Tier A]
9. Tower depth 1: dim_C=2, dim_R=4≥3 → Gleason applies — Gleason 1957 [External Tier A]
10. Born rule forced — [Tier A]

**Status.** SEALED

**Depends on chains.** [uniqueness](uniqueness.md)
