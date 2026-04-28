---
type: entity
role: CORE-ALGEBRA
theorem: "Thm 2.4c"
tags: [b0-substrate, core-algebra, forced]
---

# Hilbert space from asymmetry

> **Theorem 2.4c.**

The asymmetry P != P^T canonically produces a positive-definite Hermitian inner product.

## Dependencies

- [[P]]

## Proof

*Proof.* P != P^T means the transposition map X  X^T acts nontrivially on the algebra. Define the Cartan involution theta(X) = -X^T. This is a Lie algebra automorphism of sl(2,R): theta([X,Y]) = [theta(X),theta(Y)] (verified on all bracket pairs). It acts as theta(R_tl) = -R_tl, theta(N) = +N, theta(h) = -h. The modified Killing form:

B_theta(X,Y) = -B(X,theta(Y)) = 4tr(XY^T)

is the Frobenius inner product (sc

