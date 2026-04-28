---
type: entity
role: CORE-ALGEBRA
theorem: "Thm 1.3"
tags: [core-algebra, forced]
---

# Three generating equations

> **Theorem 1.3.**

From P^2 = P with P != P^T:

| Equation | Content |
|----------|---------|
| R^2 = R + I | Persistence with memory |
| \{R, N\} = N | Observation stabilizes the blind spot |
| N^2 = -I | The blind spot has closed internal motion |

## Dependencies

- [[P]]
- [[R]]
- [[N]]

## Proof

*Proof.* Write P = R + N. Since R = (P+P^T)/2 is symmetric and N = (P-P^T)/2 is antisymmetric, every product separates cleanly under transposition: (R^2)^T = R^2 (symmetric), (N^2)^T = N^2 (symmetric since (-N)(-N) = N^2), and \{R,N\}^T = -\{R,N\} (antisymmetric since (RN)^T = -NR).

Expanding P^2 = P:

(R+N)^2 = R^2 + \{R,N\} + N^2 = R + N

Symmetric part: R^2 + N^2 = R. Antisymmetric part: \{R,N\} = N.

In M_2(R), every antisymmetric matrix has the form $N 

