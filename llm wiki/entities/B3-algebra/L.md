---
type: other
grid: B(3, cross)
status: computed
tags: [b3-algebra, ker-im, gravity, tower, verified, other]
links: [R, ker, im, gravity, tower, self-transparency]
---

# L (the operation)

**Definition.** The Sylvester self-action. The single operation everything is built from.

**Source.** THEORY.md:72, modular/algebra.py:9-14

**Equations.**
- L_{s,s}(X) = sX + Xs - X
- Eigenvalues at depth 0: {-√5, 0, 0, +√5}
- ker/im = 1/2 at every depth

**Depends on.** [R](R.md)

**Required by.** [ker](ker.md), [im](im.md), [gravity](gravity.md), [tower](tower.md), [self-transparency](transparency.md), everything

**Status.** COMPUTED

**Verified.** production.py (eigenvalues), topology.py (Lichnerowicz), algebra.py (the 42-line source)

**Notes.** One function in algebra.py. Everything imports it. Applied once: produces the algebra. Iterated: builds the tower. Spectrum: gives dynamics. Kernel: gives observer. On sl(2,R): IS the Lichnerowicz Laplacian.
