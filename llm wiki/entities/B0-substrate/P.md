---
type: entity
role: PRIMITIVE
level: B0
tags: [b0-substrate, primitive, axiom, core]
status: FROZEN
---

# P — the primitive

> One matrix. Everything follows.

## Plain English

P = [[0,0],[2,1]]. That's it. That's the starting point. Everything else — the five constants, the gauge groups, the coupling constants, gravity, quantum mechanics, the observer, the cosmological constant, the Bell inequality violation — all of it comes from the properties of this one 2×2 matrix.

P has three properties:
1. **P² = P** — apply P to itself and you get P back. It's a naming act that returns itself.
2. **rank(P) = 1** — it's a single act, not a composite.
3. **P ≠ Pᵀ** — it's not symmetric. It's not its own mirror image. This asymmetry is where EVERYTHING comes from.

## Why this specific matrix?

P = [[0,0],[2,1]] is the companion matrix of the polynomial x²-x-1 (coefficients [1,1]), composed with the observer N. Among ALL 2×2 integer matrices satisfying P²=P with rank 1 and P≠Pᵀ, there are exactly 8 candidates, all conjugate. They all generate the same algebra. The choice of representative is gauge (U0). The structure is unique.

## The naming triangle

P decomposes into three necessary pieces:

```
P = J + |1⟩⟨1| + N
  = [[0,1],[1,0]] + [[0,0],[0,1]] + [[0,-1],[1,0]]
  = ground + commitment + observer
```

Remove any one and P²≠P. The naming act REQUIRES all three: a ground to stand on (J), a choice to commit to (|1⟩⟨1|), and someone to look (N). The universe needs an observer — not as audience, as structural condition.

## Orientation reading

P≠Pᵀ IS orientation. Without it, N=0, R²=R (no surplus), ker=0 (no blind spot), no complex structure, no quantum mechanics, no Bell violation, no physics. The asymmetry creates everything. P₀ (the symmetric projector, ker) is the void. P (the asymmetric idempotent) is the addressed void — the void that has acquired an orientation and therefore a world.

## Technical

- P = R + N where R = (P+Pᵀ)/2 = [[0,1],[1,1]], N = (P-Pᵀ)/2 = [[0,-1],[1,0]]
- P² = P: verified. rank(P) = 1: verified. P ≠ Pᵀ: verified.
- R² = R+I, N² = -I, {R,N} = N: all follow algebraically.
- Uniqueness: among R²=aR+bI with a,b∈ℤ₊, only (1,1) gives ker≠0, N²=-I, P²=P. Triple proof, all Tier A.

## Dependencies

None. This is the axiom. Two inputs: [1,1] (the coefficients) and 2 (the dimension |S₀|).

## Everything that follows

Every page in this wiki. Every test in the code. Every constant, identity, theorem, prediction. All from P = [[0,0],[2,1]].
