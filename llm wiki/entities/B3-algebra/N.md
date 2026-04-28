---
type: other
grid: B(3, P3)
status: computed
tags: [b3-algebra, quantum, verified, ker-im, other]
links: [P, L, Hilbert space, Bell test, braiding, self-transparency, CNOT]
---

# N (observation)

**Definition.** The antisymmetric part of P. The observer. Generates complex structure.

**Source.** THEORY.md:97, modular/production.py:70-80, modular/observer.py

**Equations.**
- N = (P-Pᵀ)/2 = [[0,-1],[1,0]]
- N² = -I (complex structure)
- ker(L_{N,N}) = 0 (self-transparent at every depth)

**Depends on.** [P](P.md), [L](L.md)

**Required by.** [Hilbert space](../chains/hilbert.md), [Bell test](bell.md), [braiding](braiding.md), [self-transparency](transparency.md), [CNOT](cnot.md)

**Status.** COMPUTED

**Verified.** production.py check "N transparent", topology.py check "nabla_s(h)=N"

**Notes.** N is the ONLY generator with ker(L_{X,X})=0. All others have ker=dim/2. N²=-I necessity proved for all b≥1 (Thm 2.4b: quadratic form det=-b-1/4<0). KAEL backwards is LEAK: one-directional flow ker→im.
