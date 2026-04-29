---
type: entity
role: OPERATION
level: B3
tags: [b3-algebra, operation, center-map, core]
status: FROZEN
---

# L — the operation

> One operation. Five readings. Everything built from it.

## Plain English

L_{s,s}(X) = sX + Xs - X. That's the entire framework in one formula. Take a state s, act on any element X from both sides, subtract X. What survives is the center — what both orientations agree on. What gets killed is the orientation — what depends on which way you're looking.

L lives in 42 lines of Python (algebra.py). Every module imports it. Applied once, it produces the algebra. Applied iteratively (through the K6' tower), it builds the physics spine. Its eigenvalues give the dynamics. Its kernel gives the observer. Its kernel's self-action gives self-transparency. One operation. Five readings.

## Orientation reading

L IS the center map.

sX = left action (one orientation). Xs = right action (reflected orientation, Pᵀ). Their sum sX + Xs is orientation-INVARIANT: it combines both orientations equally. Subtracting X removes the trivial part. What's left is the center: what both orientations agree on, minus what was already there.

L kills orientation:
- L(N) = {R,N} - N = N - N = 0. Pure orientation → killed.
- L(NR) = 0. Pure orientation → killed.

L preserves center:
- L(I) = 2R_tl. Identity → center content (nontrivial).
- L(R_tl) = (5/2)I. Traceless center → scalar = Λ (cosmological constant).

On sl(2,ℝ): L(X) = tr(RX)·I. "How much of the center is in X?" That's the center question.

## Five readings

| Reading | What L does | Face |
|---------|-------------|------|
| **Algebra** | Splits the algebra into ker (hidden) and im (visible) | P3 |
| **Category** | Quotient q: A → A/ker(L). The observation. | P3 |
| **Tower** | Iterated via K6', builds the depth spine | P1 |
| **Physics** | Gravity (gauge=ker, physics=im, Λ=scalar channel) | P1 |
| **Dynamics** | Eigenvalues ±√5 give oscillation frequency | P2 |

## Technical

- L_{s,s}(X) = sX + Xs - X as a linear operator on M_n(ℝ)
- Eigenvalues at depth 0: {-√5, 0, 0, +√5} = {-√disc, 0, 0, +√disc}
- ker = span{N, NR}, dim 2. im = span{I, R_tl}, dim 2. ker/A = 1/2.
- Scalar channel: L(R_tl) = (disc/2)·I = Λ
- L is self-adjoint at depth 0 (s=R is symmetric)
- L_{N,N} has no kernel (self-transparent)
- Code: `algebra.py` line 13, function `sylvester(A, B=None)`

## Dependencies

- [[R]] (the state s = R)

## Used by

Everything. L is the one operation. All five readings. All physics. All observation. All dynamics.
