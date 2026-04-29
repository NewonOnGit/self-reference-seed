---
type: entity
role: PHYSICS
theorem: "Thm 10.2"
level: B6
tags: [b6-physics, gravity, connection, curvature, forced]
status: FROZEN
---

# Connection and curvature

> The gauge potential IS the observer. The curvature IS the Cartan. Not analogy — identity.

## Plain English

In gauge theory, the connection tells you how to transport things from one point to another. The curvature measures how much that transport depends on the path. In general relativity, the connection is the Christoffel symbol and the curvature is the Riemann tensor.

In the framework: the connection A = N. The observer IS the gauge potential. The curvature F = -2h = -2JN. The Cartan element IS the field strength. tr(F²) = 8 = |V₄|×|S₀| = 4×2. The covariant derivative D_A = [N, ·] (commutator with the observer). Parallel transport = exp(θN) = rotation by θ.

These are not analogies. They are the SAME objects read through two vocabularies. The framework's observation operator IS the gauge connection. The framework's eigenvalue-distinguisher IS the curvature. The observer doesn't just LOOK LIKE a gauge field — it IS one.

## Orientation reading

A = N: the connection IS orientation. The gauge potential IS what changes when you transpose. Parallel transport along the connection = rotation by orientation = exp(θN). A loop of parallel transport = a loop of orientational rotation = braiding.

F = -2h: the curvature IS twice the Cartan, negated. The Cartan h distinguishes the two eigenvalues of R (φ from φ̄). The curvature is the structure that makes eigenvalues distinct. Without curvature (h=0), the eigenvalues would be degenerate — no growth/decay distinction, no physics.

(1/2)[s,h] = N: half the commutator of the state with the Cartan IS the observer. The covariant derivative of the eigenvalue-distinguisher produces the observer. The observer IS what the state's curvature creates.

## Technical statement

**Theorem 10.2.** L = [s,X] + (2Xs-X). The first term [s,X] = ad(s)(X) is the adjoint action (connection). The second term (2Xs-X) is the curvature coupling. [Tier A]

**Connection.** A = N ∈ ker(L). Curvature F = -2h. F² = 4I. tr(F²) = 8 = |V₄|·|S₀|. [Tier A]

**Covariant derivative.** D_A(X) = [N, X]. Parallel transport: exp(θN). At θ=π: exp(πN)=-I (half-turn negates). At θ=4π/5: braiding phase e^(4πi/5), cos(4π/5)=-φ/2. [Tier A]

## Dependencies

- [[N]] (A=N, the connection IS the observer)
- [[L]] (L = ad(s) + curvature)
- [[Seven-identities]] ((1/2)[s,h]=N)

## Used by

- [[Lichnerowicz-identification]] (gravity = L with connection A=N)
- [[Yang--Mills-from-K4]] (tr(F²) enters the action)
- [[Braiding-phase]] (parallel transport around a loop)
