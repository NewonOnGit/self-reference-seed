---
type: entity
role: TOPOLOGY
theorem: "Thm 15.8"
tags: [topology, forced]
---

# Fibonacci TQC universality

> **Theorem 15.8.**  The braid generators $\sigma_1 = R_\mathrm{braid}$ (diagonal phases $e^{-4\pi i/5}, e^{3\pi i/5}$) and $\sigma_2 = F R_\mathrm{braid} F$ (where $F$ is the Fibonacci F-matrix with entries $\bar\varphi$ and $1/\sqrt{\varphi}$, $F^2 = I$) satisfy the braid relation $\sigma_1 \sigma_2 \sigma_1 = \sigma_2 \sigma_1 \sigma_2$ and generate a dense subgroup of $\mathrm{SU}(2)$ on the computational subspace (Freedman--Kitaev--Larsen--Wang 2003). Any single-qubit gate can be approximated to precision $\varepsilon$ using $O(\log^{3.97}(1/\varepsilon))$ braids. Each braid is topologically protected by the $\mathrm{SU}(2)_3$ Fibonacci category. [Tier A for the braid relation; universality is an external theorem applied to framework-derived data]

## Dependencies

- [[Fusion--persistence]]

## Proof sketch

(See paper_v2.md for full proof.)

## Source

`paper/paper_v2.md` line 554
