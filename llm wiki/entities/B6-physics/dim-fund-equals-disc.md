---
type: entity
role: PHYSICS
theorem: "Thm 10.12"
level: B6
tags: [b6-physics, GUT, SU5, forced, core]
status: FROZEN
---

# dim(fund_GUT) = disc

> The dimension of the GUT fundamental representation IS the discriminant. The five of SU(5) IS the five of disc(R).

## Plain English

SU(5) is the simplest grand unified theory — it combines the three forces (strong, weak, electromagnetic) into one. Its fundamental representation has dimension 5: three colors + two isospin. In the framework, three colors come from Sym²(C²) = 3 and two isospin comes from C² = 2. So the SU(5) fundamental is 3+2 = 5.

But 5 is also disc(R) = tr²-4det = 1+4 = 5. The discriminant. The orientational disagreement. The same number from a completely different route.

This is not a coincidence. Both equal d(d+3)/2 at d=2 (for the GUT side: N_c+d = d(d+1)/2 + d = d(d+3)/2) and a²+4b at (a,b)=(1,1) (for the discriminant). At the forced values d=2, a=b=1, both formulas give 5.

## Why it matters

If dim(fund) = disc, then ALL SU(5) representation dimensions are expressible in terms of disc:

| Representation | Dimension | In terms of disc |
|---------------|-----------|-----------------|
| Fundamental (5) | 5 | disc |
| Adjoint (24) | 24 | disc² - 1 |
| Antisymmetric Λ²(5) = 10 | 10 | 2·disc |
| Symmetric Sym²(5) = 15 | 15 | 3·disc |

And the mass exponents use these dimensions:
- η_B relational exponent = dim(Λ²(5)) = 2·disc = 10
- 15 Weyl fermions per generation = dim(Sym²(5)) = 3·disc

The GUT representation theory is BUILT FROM the discriminant.

## Orientation reading

disc = [R,N]²/I = orientational disagreement. dim(fund_GUT) = disc says: the GUT's fundamental representation has as many dimensions as the disagreement has magnitude. The number of colors+isospin = the cost of orientation existing. The gauge group's size IS the orientational tension.

## Technical statement

**Theorem 10.11.** N_c + d = d(d+3)/2. At d=2: N_c+d = 5 = disc(R) = tr²-4det. The GUT fundamental dimension equals the discriminant. [Tier A for the identity]

**Corollary.** dim(adj) = disc²-1 = 24. dim(Λ²) = disc(disc-1)/2 = 10 = 2·disc. dim(Sym²) = disc(disc+1)/2 = 15 = 3·disc. The mass exponent η_B·m_e/m_ν = φ̄^{dim(Λ²(fund))} = φ̄^{2·disc}. [Tier N for the mass connection]

## Dependencies

- [[R]] (disc = 5 from Cayley-Hamilton)
- [[Strong-coupling]] (N_c from Sym²(C²))
- [[Neutrino-mass]] (exponent chain uses dim_gauge + disc)

## Used by

- [[Baryon-asymmetry-and-the-relational-constraint]] (2·disc = dim(Λ²(5)))
- [[Weinberg-angle]] (sin²θ_W from anomaly classification on fund reps)
