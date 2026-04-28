---
type: entity
role: PHYSICS
theorem: "Thm 12.7"
tags: [physics, forced]
---

# Yang--Mills from K4

> **Theorem 12.7.**  The complexity functional $\mathrm{Comp}(\rho) = D_\mathrm{KL}(\rho \| \rho_\mathrm{eq})$ (Theorem 12.1) applied to gauge-field configurations $A_\mu$ with field strength $F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu + [A_\mu, A_\nu]$: at quadratic order in the field strength, $\mathrm{Comp}(A) \propto \int \mathrm{tr}(F \wedge *F)$. This follows from the KL-divergence expanding as a quadratic form in the deviation from equilibrium, with the gauge-invariant quadratic being $\mathrm{tr}(F^2)$. K4 minimization $\partial\delta/\partial A_\mu = 0$ gives $D_\mu F^{\mu\nu} = 0$ (source-free Yang--Mills). The same functional produces two outputs: the coupling constant $\alpha_S$ (Theorem 12.2, from the partition function) and the field equations (from the variational principle). [Tier A f

## Dependencies

- [[KL-uniqueness|KL uniqueness]]
- [[Strong-coupling|Strong coupling]]

## Proof sketch

(See paper_v2.md for full proof.)

## Source

`paper/paper_v2.md` line 428
