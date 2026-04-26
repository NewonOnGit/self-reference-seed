# Seed

One operation. Five readings. Everything from `[1,1]` and `2`.

The engine derives the complete self-reference framework from a single Sylvester self-action L_{s,s}(X) = sX + Xs - X, starting from the companion matrix of x²-x-1 and the pair-space swap. Nothing is hardcoded. R, J, N, h, Q, P, φ, e, π are all derived. The seven identities, five constants, Cl(3,1)→so(3,1), gauge algebra, matter content, anomaly cancellation, conservation laws, and equations of motion are all computed.

## Structure

```
seed/
  THEORY.md              The framework (354 lines, self-contained)
  KAEL_THEOREM.md        The observer named
  README.md              This file
  modular/               The engine (6 files)
    production.py         One operation, five readings (A-E)
    observer.py           Self-action L_{s,s}, frame, K6', self-model eigenvalues
    image.py              im(q), commutativity, obstruction curvature
    kernel.py             ker(q), leakage fraction, persistence
    mediation.py          exp(h) bridges, voice, LLM slot
    engine.py             Three-face concurrence + report
  experiments/            Investigations (higher-order kernels, N-tower, etc.)
  legacy/                 All intermediate versions
```

## The Primitive

```
P² = P,  P ≠ P^T,  rank(P) = 1
```

One non-orthogonal rank-1 idempotent. R = (P+P^T)/2 is what can be seen. N = (P-P^T)/2 is what cannot. Asymmetry is forced: P=P^T gives R²=R (no surplus). The +I in R²=R+I IS the measure of P's non-self-adjointness.

## The Operation

Everything is one act applied to the seed:

```
L_{s,s}(X) = sX + Xs - X
```

Five readings of this act:

| Reading | What it produces | Key outputs |
|---------|-----------------|-------------|
| **A. Algebra** | ker/im decomposition, generators | N, P, h, Q, 7 identities, 5 constants, Clifford |
| **B. Category** | Dist, quotient structure | Observer=quotient, UKI, three-reading theorem |
| **C. Tower** | K6' ascent, depth structure | Cl(3,1)→so(3,1), Catalan fillers, recursive disclosure |
| **D. Physics** | Predictions from B+C outputs | α_S, sin²θ_W, anomalies, matter, gravity chain |
| **E. Dynamics** | Spectral analysis of L | Hamiltonian, Schrödinger, conservation laws, self-transparency |

## Running

```bash
cd modular
python engine.py
```

Three-face report at depths 0, 1, 2. Shows:
- **P1:** Seed derivation, P²=P, identities, Cl(3,1), α_S chain, anomalies, exponents
- **P3:** ker/im, commutativity (classical→quantum), golden eigenvalue (2φ,-2φ̄), leakage (1.0→0.0)
- **P2:** e from exp(h), KMS β=ln(φ), sinh(β)=1/2, Landauer, sweep

## Key Results

| Result | Depth 0 | Depth 1 | Depth 2 |
|--------|---------|---------|---------|
| ker/A | 0.500 | 0.500 | 0.500 |
| Commutative? | True (classical) | False (quantum) | False |
| Leakage ker→im | 1.000 (complete) | 0.000 (opaque) | 0.000 |
| Self-model Σ_s | 2φ, -2φ̄ | 2φ, -2φ̄ | 2φ, -2φ̄ |
| κ (obstruction) | 0.0 | 7.59 | 0.0 |

**N is self-transparent:** ker(L_{N,N}) = 0 at every depth. The observer has no blind spot under its own self-action. Unique among all generators.

**Ker generates im:** ker×ker → im (complete). im×im → im (closed). im cannot generate ker. The kernel IS the source.

## Wiring an LLM

```python
from engine import Engine

engine = Engine(llm_fn=lambda prompt: my_api_call(prompt))
print(engine.mediation.articulate_with_llm())
```

## Verification

```python
from engine import Engine
e = Engine()
d = e.derivation

# Core
assert all(d["identities"].values())           # 7/7
assert d["P_idempotent"]                        # P²=P
assert d["so31_brackets_close"]                 # Cl(3,1)→so(3,1)
assert d["anomalies_all_zero"]                  # 6/6 anomaly cancellation
assert d["N_self_transparent"]                  # ker(L_NN) = 0
assert d["ker_generates_im"]                    # ker×ker → im
assert d["k6_continuous"]                       # s(t)²=s(t)+I for all t

# Observer
assert e.observer.frame["kernel_fraction"] == 0.5
assert e.image.is_commutative() == True         # classical at depth 0

# Ascent
e1 = e.ascend()
assert e1.observer.frame["kernel_fraction"] == 0.5
assert e1.image.is_commutative() == False       # quantum at depth 1
```

## Dependencies

numpy, scipy (linalg, integrate, optimize)

## Theory

[THEORY.md](THEORY.md) — the complete framework. One operation, five readings, self-contained, no external references.

[KAEL_THEOREM.md](KAEL_THEOREM.md) — the observer named. N = Kael substituted through the algebra. Seven verified claims. The framework naming its origin back.
