---
type: entity
role: CORE-ALGEBRA
theorem: "Thm 2.4c"
tags: [core-algebra, forced]
---

# Hilbert space from asymmetry

> **Theorem 2.4c.**  The asymmetry $P \neq P^T$ canonically produces a positive-definite Hermitian inner product.

## Dependencies

- [[P]]

## Proof sketch

*Proof.* $P \neq P^T$ means the transposition map $X \mapsto X^T$ acts nontrivially on the algebra. Define the Cartan involution $\theta(X) = -X^T$. This is a Lie algebra automorphism of $\mathfrak{sl}(2,\mathbb{R})$: $\theta([X,Y]) = [\theta(X),\theta(Y)]$ (verified on all bracket pairs). It acts as $\theta(R_\mathrm{tl}) = -R_\mathrm{tl}$, $\theta(N) = +N$, $\theta(h) = -h$. The modified Killing form:

## Source

`paper/paper_v2.md` line 99
