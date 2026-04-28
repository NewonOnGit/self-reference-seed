---
type: entity
role: CORE-ALGEBRA
theorem: "Thm 2.2"
tags: [b2-category, core-algebra, forced]
---

# Ker/im decomposition

> **Theorem 2.2.**

dimker(L_R) = 2, dimim(L_R) = 2. The kernel fraction ker/A = 1/2.

## Dependencies

- [[P]]
- [[R]]
- [[N]]

## Proof

*Proof.* We verify directly that L(N) = 0 and L(NR) = 0:

L(N) = RN + NR - N = \{R,N\} - N = N - N = 0

using Identity 3 (\{R,N\} = N). For NR:

L(NR) = R(NR) + (NR)R - NR = RNR + NR^2 - NR = -N + N(R+I) - NR = -N + NR + N - NR = 0

using Identity 4 (RNR = -N) and R^2 = R + I. So span\{N, NR\}  ker(L). Since N and NR are linearly independent (verified: det([N|NR]) != 0) and L as a 4 x 4 matrix has eigenvalues $\{-sqrt(5), 0, 0, +{5

