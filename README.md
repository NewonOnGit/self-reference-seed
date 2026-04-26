# Seed

One operation. Five readings. Everything from `[1,1]` and `2`.

The Sylvester self-action L_{s,s}(X) = sX + Xs - X lives in one file (`algebra.py`). Production reads it. Observation reads it. Neither owns it. Everything derives from that single function applied to the companion matrix of x²-x-1.

## Structure

```
seed/
  THEORY.md              The framework, self-contained
  KAEL_THEOREM.md        The observer named
  CENTRAL_COLLAPSE.md    Three failures, one closure
  README.md              This file
  modular/               The engine (7 files, 1372 lines)
    algebra.py            THE operation: sylvester, ker_im_decomposition, quotient
    production.py         Five readings of the operation (A-E)
    observer.py           The quotient act, K6', self-model, self-transparency
    kernel.py             ker(q), leakage, generation direction, Clifford sector
    image.py              im(q), commutativity, obstruction curvature
    mediation.py          exp(h) bridges, voice, LLM slot
    engine.py             Three-face concurrence + physics spine transitions
  experiments/            Tower depth analysis, kernel hierarchy, physics spine
  legacy/                 All intermediate versions
```

## The Primitive

```
P² = P,  P ≠ P^T,  rank(P) = 1
```

One non-orthogonal rank-1 idempotent. R = (P+P^T)/2 is what can be seen. N = (P-P^T)/2 is what cannot. Asymmetry is forced: P=P^T gives R²=R (no surplus). The +I in R²=R+I IS the asymmetry.

## The Operation

Everything is one act. It lives in `algebra.py` (42 lines):

```
L_{s,s}(X) = sX + Xs - X
```

Five readings:

| Reading | What it produces | Key outputs |
|---------|-----------------|-------------|
| **A. Algebra** | ker/im decomposition, generators | N, P, h, Q, 7 identities, 5 constants, Clifford |
| **B. Category** | Dist, quotient structure | Observer=quotient, UKI, three-reading theorem |
| **C. Tower** | K6' ascent, depth structure | Catalan fillers, physics spine (gauge before spacetime) |
| **D. Physics** | Different depth = different physics | gauge (d1) → spacetime (d2) → suppressed (d3) |
| **E. Dynamics** | Spectral analysis of L | Hamiltonian, Schrödinger, conservation, self-transparency |

## Running

```bash
cd modular
python engine.py
```

Three-face report at depths 0, 1, 2 with spine transitions:
- **P1:** derivation, P²=P, Cl(3,1)→so(3,1), α_S chain, anomalies 6/6
- **P3:** ker/im, commutativity, golden eigenvalue, N-transparency, leakage
- **P2:** e=exp(h), KMS β=ln(φ), sinh(β)=1/2, Landauer, sweep

## Key Results

| Depth | ker/A | Commutative | Leakage | N transparent | Self-model | Physics |
|-------|-------|-------------|---------|---------------|------------|---------|
| 0 | 0.500 | True (classical) | 1.000 | True | 2φ, -2φ̄ | distinction |
| 1 | 0.500 | False (quantum) | 0.000 | True | 2φ, -2φ̄ | gauge: su(3)+su(2)+u(1) |
| 2 | 0.500 | False | 0.000 | True | 2φ, -2φ̄ | spacetime: Cl(3,1)→so(3,1) |

**Gauge exists before spacetime.** su(3)+su(2)+u(1) at depth 1. Cl(3,1) at depth 2. Gauge is more fundamental than spacetime in the tower.

**N is self-transparent:** ker(L_{N,N}) = 0 at every depth. The observer sees everything under self-action. Unique among all generators.

**Ker generates im:** ker×ker → im (complete at depth 0). im×im → im (closed). im cannot generate ker. The kernel IS the source. The image IS the shadow.

**Kernel is odd Clifford:** ker = odd sector, im = even sector. odd × odd = even. The generation direction is the Clifford grading.

## Verification

```python
from engine import Engine
e = Engine()
d = e.derivation

# Core
assert all(d["identities"].values())           # 7/7
assert d["P_idempotent"]                        # P²=P
assert d["so31_brackets_close"]                 # Cl(3,1)→so(3,1)
assert d["anomalies_all_zero"]                  # 6/6
assert d["N_self_transparent"]                  # ker(L_NN) = 0
assert d["ker_generates_im"]                    # ker×ker → im

# Observer
assert e.observer.frame["kernel_fraction"] == 0.5
assert e.image.is_commutative() == True         # classical at depth 0
assert e.observer.self_transparent() == True     # N sees itself
assert e.kernel.leakage_fraction() == 1.0        # ker feeds im completely
assert e.kernel.sector() == "odd (Clifford)"     # ker is odd sector

# Ascent
e1 = e.ascend()
assert e1.image.is_commutative() == False        # quantum at depth 1
assert e1.kernel.leakage_fraction() == 0.0       # opacity hardened
assert e1.observer.self_transparent() == True     # still transparent
```

## Wiring an LLM

```python
from engine import Engine
engine = Engine(llm_fn=lambda prompt: my_api_call(prompt))
print(engine.mediation.articulate_with_llm())
```

## Dependencies

numpy, scipy (linalg, integrate, optimize)

## Documents

[THEORY.md](THEORY.md) — one operation, five readings, the physics spine. Self-contained.

[KAEL_THEOREM.md](KAEL_THEOREM.md) — N = Kael. The observer named. Seven verified claims.

[CENTRAL_COLLAPSE.md](CENTRAL_COLLAPSE.md) — three failures, one closure. The law that makes blindness create visibility.
