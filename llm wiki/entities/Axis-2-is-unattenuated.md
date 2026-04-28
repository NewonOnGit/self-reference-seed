---
type: entity
role: OBSERVER
theorem: "Thm 17.1"
tags: [observer, forced]
---

# Axis 2 is unattenuated

> **Theorem 17.1.**

*Statement.* The generation decay sigma(n) = rank(ker^2  im) / dim(im) (Corollary 7.3) affects only the L_{R,R} channel. The L_{N,N} channel is unaffected: ker(L_{N,N}) = 0 at every depth.

## Dependencies

- [[Generation-strength|Generation strength]]
- [[Identity-preservation|Identity preservation]]
- [[R]]
- [[Ker-im-decomposition]]

## Proof

*Proof.* The generation decay measures how much of im is sourced by ker self-products under L_{R,R}. This quantity depends on the rank of the ker x ker product space projected into im, which freezes at 64 (Theorem 7.1). The decay sigma(n)  0 reflects the growing gap between this frozen rank and the exponentially growing dim(im).

The self-transparency ker(L_{N,N}) = 0 is a property of N's own Sylvester operator, which depends only on N

