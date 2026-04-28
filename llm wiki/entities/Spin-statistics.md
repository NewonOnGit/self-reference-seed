---
type: entity
role: TOPOLOGY
theorem: "Thm 15.2"
tags: [topology, forced]
---

# Spin-statistics

> **Theorem 15.2.**

*Statement.* At tower depth 2, L_{s_2,s_2}(Psi) = 0 on a two-particle spinor state Psi requires antisymmetric exchange (eta = -1).

## Dependencies

- [[Identity-preservation|Identity preservation]]
- [[L]]
- [[Tower]]

## Proof

*Proof.* At depth 2, N_2  M_8(R) satisfies N_2^2 = -I_8 (Theorem 6.2). The rotation generator N_2 has eigenvalues +- i (each with multiplicity 4). A rotation by angle theta in the spinor representation is exp(theta N_2 / 2). At theta = 2pi:

exp(pi N_2) = cos(pi) I + sin(pi) N_2 = -I

(using N_2^2 = -I to exponentiate via exp(theta N_2) = costheta  I + sintheta  N_2). A full 2pi rotation gives -I in the spinor representation — the defini

## Source

`paper/paper_v2.md` line 496
