---
type: entity
role: CORE-ALGEBRA
theorem: "Thm 2.4b"
tags: [core-algebra, forced]
---

# $N^2 = -I$ is necessary

> **Theorem 2.4b.**

The 2-dimensional kernel necessarily contains N with N^2 = -I.

## Dependencies

- [[N]]
- [[Ker-im-decomposition]]

## Proof

*Proof.* At a=1, general b >= 1: the kernel of \{R,X\}=X is spanned by K_1 = [1&1 \ 0&-1], K_2 = [0&-b \ 1&0] (derived by solving RX+XR=X entry-by-entry). Direct computation: K_1^2=I, K_2^2=-bI, K_1K_2+K_2K_1=I (all proportional to I — this follows from [R,X^2]=0 for X  ker, forcing X^2 into the commutant of R). The quadratic form (alpha K_1+beta K_2)^2 = (alpha^2+alphabeta-bbeta^2)I has matrix $Q = 

## Source

`paper/paper_v2.md` line 95
