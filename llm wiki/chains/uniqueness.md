---
type: other
status: sealed
tags: [ker-im, idempotent, other]
links: []
---

# Uniqueness of (a,b)=(1,1)

**Claim.** Among R²=aR+bI with a,b∈Z₊, only (1,1) produces ker≠0, N²=-I, and P²=P.

**Steps.**
1. Eigenvalues of L are α_i+α_j-1 (Kronecker sum, commuting factors) — algebra.py [Tier A]
2. ker≠0 iff some eigenvalue=0. Only α+β-1=a-1=0 has solutions → a=1 — paper_v2.md Thm 2.5b [Tier A]
3. λ₁=a+√(a²+4b)-1>0 always. λ₃=a-√(a²+4b)-1<0 always. Neither zero. — paper_v2.md Thm 2.5b [Tier A]
4. At a=1: ker dim=2 (double zero eigenvalue) — paper_v2.md Thm 2.5b [Tier A]
5. Quadratic form on ker: K₁²=I, K₂²=-bI, det(Q)=-b-1/4<0 → N²=-I exists — paper_v2.md Thm 2.4b [Tier A]
6. P²=P entry-by-entry forces a²=1, so a=1 — paper_v2.md Thm 1.3 [Tier A]
7. det(P)=0 + a=1 forces b=1 — paper_v2.md Thm 1.3 [Tier A]

**Status.** SEALED

**Depends on chains.** (none — this is foundational)
