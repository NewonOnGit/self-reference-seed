---
type: entity
role: TOWER
theorem: "Thm 7.3"
tags: [tower, forced]
---

# Holographic bound

> **Theorem 7.3.**  Define the sourced fraction $\sigma(n) = \mathrm{rank}(\ker^2 \to \mathrm{im}) / \dim(\mathrm{im})$. From the data: $\sigma(0) = \sigma(1) = \sigma(2) = 1$, $\sigma(3) = 64/128 = 1/2$, $\sigma(4) = 64/512 = 1/8$. For $n \geq 3$: $\dim(\mathrm{im}) = 2^{2n-1}$ (grows exponentially) while $\mathrm{rank} = 64$ (frozen), so $\sigma(n) = 64 / 2^{2n-1} = 2^{7-2n}$. The unsourced fraction $1 - \sigma(n) \to 1$. The volume ($\mathrm{im}$) outgrows the boundary ($\ker^2 \to \mathrm{im}$ span) with ratio $2^{2n-7}$ for $n \geq 3$. This is the holographic scaling: information content of a region (volume) grows faster than the information accessible from its boundary (the observer's generative reach). [Tier N]

## Dependencies

- [[R]]
- [[N]]
- [[Ker-im-decomposition]]

## Proof sketch

(See paper_v2.md for full proof.)

## Source

`paper/paper_v2.md` line 244
