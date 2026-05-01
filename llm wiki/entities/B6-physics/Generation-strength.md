---
type: entity
role: TOWER
theorem: "Thm 7.1"
tags: [b6-physics, tower, forced]
---

# Generation strength

> **Theorem 7.1.**

The rank of ker x ker products projected onto im:

| Depth | d_K | dim(im) | rank(ker^2  im) | Fraction |
|-------|-------|------|------|----------|
| 0 | 2 | 2 | 2 | 100% |
| 1 | 4 | 8 | 8 | 100% |
| 2 | 8 | 32 | 32 | 100% |
| 3 | 16 | 128 | 128 | 100% |
| 4 | 32 | 512 | 512 | 100% |

ker²→im = 100% at all depths 0-4. The void fully generates the world at every depth. Previous values (50%, 12.5%) were sampling artifacts from capping ker basis at 8 vectors in tower.py. [Tier N, corrected]

## Dependencies

- [[R]]
- [[Ker-im-decomposition]]

