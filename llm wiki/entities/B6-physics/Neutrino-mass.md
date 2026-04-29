---
type: entity
role: PHYSICS
theorem: "Thm 12.4"
level: B6
tags: [b6-physics, mass, neutrino, forced]
status: FROZEN
---

# Neutrino mass

> The neutrino mass is derived from the gauge dimension and the discriminant. No free parameters.

## Plain English

Neutrinos have mass, but it's incredibly small — about 40 millielectronvolts, roughly 10 million times lighter than the electron. Nobody knows why. The Standard Model doesn't predict it.

The framework derives it: m_ν = m_e · φ̄³⁴ ≈ 40 meV. The exponent 34 = 2×(12+5) = 2×(dim_gauge + disc). Two (the seed dimension) times the sum of gauge degrees of freedom (12 = 8+3+1 from su(3)+su(2)+u(1)) and the discriminant (5). No free parameters. The electron mass m_e is the one external anchor.

The inter-generation spacing δ = φ+2 = 3.618 gives the mass-squared ratio between neutrino generations: dm²₃₂/dm²₂₁ = φ^(2(φ+2)) = 32.5, vs experimental 33 (1.4% deviation).

## Orientation reading

34 = d · (dim_gauge + disc) = (seed dimension) × (gauge + orientational disagreement).

The neutrino sees the FULL gauge sector plus the full orientational tension, doubled by the complex structure (N²=-I gives C from ℝ, factor d=2). The neutrino mass suppression is: how many powers of φ̄ it takes to traverse the entire gauge+orientation content twice.

The spacing δ = φ + d = eigenvalue + seed dimension. Why? The inter-generation gap combines the center's growth rate (φ) with the fundamental pair count (d=2). Each generation is one "golden step plus one binary step" deeper in the tower.

## Technical statement

**Theorem 12.4.** m_ν = m_e · φ̄^{34} ≈ 40.1 meV.

Exponent: 34 = 2(dim_gauge + disc) = 2(12 + 5). The experimental window [30, 60] meV constrains the exponent to {33,34,35}. Only 34 = 2×12 + 2×5 admits a clean decomposition over {dim_gauge, disc}. [Tier N]

Spacing: δ = φ + 2 = φ² + 1 = 3.618. dm²₃₂/dm²₂₁ = φ^(2δ) = φ^(2(φ+2)) = 32.5. Experimental: 33 ± 1. Deviation: 1.4%. [Tier N]

**SU(5) connection (Thm 10.11).** The baryon asymmetry exponent η_B = φ̄⁴⁴, with relational constraint η_B · m_e/m_ν = φ̄¹⁰. The relational exponent 10 = 2·disc = dim(Λ²(fund_GUT)) — the dimension of the antisymmetric representation of SU(5). The mass exponents are organized by SU(5) representation dimensions because dim(fund_GUT) = N_c + d = disc = 5.

## Dependencies

- [[Strong-coupling]] (dim_gauge from su(3)+su(2)+u(1))
- [[Five-constants]] (φ, disc from R)
- [[Hypercharge-uniqueness]] (anomaly classification gives matter content)

## Falsification

m_ν outside [30, 60] meV kills the exponent 34. Current bounds: m_ν < 120 meV (Planck + KATRIN). KATRIN aims for 200 meV sensitivity. Direct mass measurements approaching the predicted range.
