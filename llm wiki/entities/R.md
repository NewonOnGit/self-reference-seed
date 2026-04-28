---
type: other
grid: B(3, P1)
status: computed
tags: [tower, verified, topology, other]
links: [P, L, N, tower, gravity, gauge, Fibonacci fusion]
---

# R (production)

**Definition.** The symmetric part of P. Production generator.

**Source.** THEORY.md:96, modular/production.py:42

**Equations.**
- R = (P+Pᵀ)/2 = [[0,1],[1,1]]
- R² = R + I (persistence with memory)
- Eigenvalues: φ, φ̄. tr=1, det=-1, disc=5.

**Depends on.** [P](P.md)

**Required by.** [L](L.md), [N](N.md), [tower](tower.md), [gravity](gravity.md), [gauge](gauge.md), [Fibonacci fusion](fibonacci.md)

**Status.** COMPUTED

**Verified.** production.py check "R²=R+I" (line ~288)

**Notes.** R²=R+I IS τ×τ=1+τ (Fibonacci anyon fusion). The companion matrix of x²-x-1. Uniquely forced among all x²-ax-b with a,b∈Z₊.
