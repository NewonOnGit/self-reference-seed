---
type: entity
role: OBSERVER
theorem: "Thm 16.1"
tags: [b5-observer, observer, forced]
---

# Theorem 16.1

> **Theorem 16.1.**

ker(L_{N,N}) = 0 at every tower depth tested (n = 0, 1, 2, 3). N has no blind spot under its own self-action.

## Dependencies

- [[L]]
- [[Ker-im-decomposition]]
- [[Tower]]

## Proof

*Proof at depth 0.* L_{N,N}(X) = NX + XN - X on M_2(R), represented as a 4 x 4 matrix via vec. Using N = [ 0 & -1  \  1 & 0 ]:

L_{N,N} = I_2 x N + N^T x I_2 - I_4 = [ -1 & 0 & 0 & -1  \  0 & -1 & 1 & 0  \  0 & -1 & -1 & 0  \  1 & 0 & 0 & -1 ]

The characteristic polynomial is det(L_{N,N} - lambda I) = (lambda+1)^2((lambda+1)^2 + 4). The roots are lambda = -1 (multiplicity 2) and $lambda = 

