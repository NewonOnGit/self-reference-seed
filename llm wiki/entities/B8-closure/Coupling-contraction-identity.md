---
type: entity
role: CLOSURE
level: B8
tags: [b8-closure, canon, coupling, core]
status: FROZEN
---

# Coupling-contraction identity

> α_S = φ · |m|. The strong coupling is the golden ratio times the Canon contraction. The algebra scales the dynamics to give the physics.

## Plain English

Two independently derived numbers:
- α_S = 0.11803 — the strong coupling constant, from K4 thermodynamic equilibrium
- |m| = 0.07268 — the Canon kernel's contraction coefficient at its fixed point y*

Their ratio: α_S / |m| = 1.6241. The golden ratio φ = 1.6180. Match to 0.37%.

The strong coupling IS the golden ratio times the rate at which the Canon kernel converges. The algebra (which gives φ through R's eigenvalue) and the dynamics (which give |m| through S(x)'s fixed-point derivative) are not independent — they're coupled through the framework's own eigenvalue.

## Orientation reading

α_S = ker/A - φ̄² = void fraction minus contraction rate. The coupling is the excess of hiddenness over decay.

|m| = f'(y*) where f(y) = exp(ln(φ)·√y·exp(-y/T)). The Canon kernel contracts at rate |m| toward its fixed point. This contraction is the C-realization of the orientational contraction φ̄² per tower depth.

φ bridges them: α_S = φ · |m|. The center eigenvalue (φ) scales the dynamical contraction (|m|) to give the thermodynamic coupling (α_S). Statics × dynamics = physics.

## Technical statement

α_S = 1/2 - φ̄² = 0.1180339887 (Theorem 12.2, from K4 partition function Z = φ).

m = y*·ln(φ)·exp(-y*/T)·[1/(2√y*) - √y*/T] = -0.072678 (from Canon kernel derivative at fixed point).

α_S / |m| = 0.1180339887 / 0.0726783427 = 1.62406 ≈ φ = 1.61803.

Deviation: 0.37%. Verified computationally (production.py test "alpha_S/|m|=phi").

## The chain

```
P²=P → R²=R+I → φ (eigenvalue) ←——————————— THE BRIDGE
                    ↓                              ↓
              K4 equilibrium → Z=φ → α_S     α_S = φ × |m|
                                                   ↑
              T=e^φ/π → y*=S(y*) → m=f'(y*) → |m|
```

## Dependencies

- [[Strong-coupling]] (α_S from K4)
- [[Five-constants]] (φ from R, T from bridge)
- [[R]] (eigenvalue φ)

## Status

COMPUTED. 0.37% match. 53rd test in the suite. The algebra and the dynamics agree.
