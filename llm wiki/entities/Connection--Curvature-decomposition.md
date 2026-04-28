---
type: entity
role: PHYSICS
theorem: "Thm 10.2"
tags: [physics, forced]
---

# Connection--Curvature decomposition

> **Theorem 10.2.**

L_{s,s}(X) = sX + Xs - X = (sX - Xs)_{ad(s)(X)} + (2Xs - X)_{curvature}

The first term is ad(s)(X) = [s,X]. On a Lie group with bi-invariant metric, the Levi-Civita connection for left-invariant vector fields is nabla_X Y = (1)/(2)[X,Y] (see e.g. do Carmo, *Riemannian Geometry*, Prop. 2.7 of Ch. 11). Therefore ad(s) = 2nabla_s. The second term (2Xs - X) is the non-antisymmetric remainder, encoding the Ricci curvature coupling.

*Verification:* For each basis element, ad(s)(X) + (2Xs - X) = L(X):
- X = h: [s,h] = [ 0 & -2  \  2 & 0 ], 2hs - h = [ -1 & 2  \  -2 & -1 ]. Sum = -I. 
- X = e: $[s,e] = [ -1 & -1  \  0 & 1 

## Dependencies

- [[L]]

