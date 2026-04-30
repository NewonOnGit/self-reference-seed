---
type: other
grid: B(6, cross)
status: computed
tags: [b6-physics, verified, gravity, other]
links: [L, N, h, Λ, n_cosmo, Einstein equations]
---

# Gravity (Lichnerowicz closure)

**Definition.** L_{s,s} restricted to sl(2,R) with Killing metric IS the Lichnerowicz Laplacian.

**Source.** THEORY.md:237-241, paper_v2.md:§10, modular/physics.py:lichnerowicz()

**Equations.**
- L(h)=-I, L(e)=+I, L(f)=+I. Eigenvalues {-1,+1,+1}.
- L = [s,X] + (2Xs-X) = Connection + Curvature
- (1/2)[s,h] = N: the covariant derivative of the Cartan IS the observer

**Depends on.** [L](L.md), [N](N.md), [h](h.md), Killing form B(X,Y)=4tr(XY)

**Required by.** [Λ](lambda.md), [n_cosmo](n_cosmo.md), [Einstein equations](einstein.md)

**Status.** COMPUTED (spectral match). OPEN (intertwining map to Sym²(T*M)).

**Verified.** physics.py checks "L eigenvalues {-1,+1,+1}", "nabla_s(h)=N", "L(R_tl)=(disc/2)*I", "L=ad+Ric"

**Notes.** Closes the gravity gap. Previous chain L→Landauer→Bekenstein→Jacobson→Einstein had Jacobson as external input. Now internal. The scalar channel L(R_tl)=(disc/2)I IS Λ.
