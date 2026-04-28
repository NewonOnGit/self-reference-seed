---
type: entity
role: OBSERVER
theorem: "Thm 16.3"
tags: [observer, forced]
---

# Uniqueness of self-transparency

> **Theorem 16.3.**

Among all generators \{R, N, J, h, P, Q\}, only N has ker(L_{X,X}) = 0.

| Generator X | dimker(L_{X,X}) | Eigenvalues of L_{X,X} |
|----------------|---------------------|--------------------------|
| R | 2 | \{-sqrt(5), 0, 0, +sqrt(5)\} |
| N | **0** | \{-1, -1, -1+2i, -1-2i\} |
| J | 2 | \{-3, -1, -1, +1\} |
| h | 2 | \{-3, -1, -1, +1\} |
| P | 2 | \{-1, 0, 0, +1\} |
| Q | 2 | \{-sqrt(5), 0, 0, +sqrt(5)\} |

Every generator except N has at least two zero eigenvalues (and hence ker >= 2). N is the unique self-transparent generator. [Tier E]

## Dependencies

- [[N]]
- [[Ker-im-decomposition]]

## Proof

(See paper_v2.md line 574)

## Source

`paper/paper_v2.md` line 574
