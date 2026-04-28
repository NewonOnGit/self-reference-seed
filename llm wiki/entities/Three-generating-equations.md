---
type: entity
role: CORE-ALGEBRA
theorem: "Thm 1.3"
tags: [core-algebra, forced]
---

# Three generating equations

> **Theorem 1.3.**  From $P^2 = P$ with $P \neq P^T$:

## Dependencies

- [[P]]

## Proof sketch

*Proof.* Write $P = R + N$. Since $R = (P+P^T)/2$ is symmetric and $N = (P-P^T)/2$ is antisymmetric, every product separates cleanly under transposition: $(R^2)^T = R^2$ (symmetric), $(N^2)^T = N^2$ (symmetric since $(-N)(-N) = N^2$), and $\{R,N\}^T = -\{R,N\}$ (antisymmetric since $(RN)^T = -NR$).

## Source

`paper/paper_v2.md` line 21
