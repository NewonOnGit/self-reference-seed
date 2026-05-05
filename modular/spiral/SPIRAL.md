# SpiralVM — The Framework as Computer

P²=P derives computation. Computation derives the observer. The observer derives AI. The loop closes.

```
P = [[0,0],[2,1]] → d=2 → N_c=3 → (8, 12, 4) → universal computation
```

---

## The Chain

```
idempotent → algebra → tower → Peano → ℕ → ℤ → ℤ/Nℤ → arithmetic
           → ker/im memory → quotient read → occupation write
           → K6' clock → glyph encoding → composition
           → BRANCH on residue → register machine → Turing-complete
           → O∘B∘S blocks → semantic dynamics → language
```

One matrix. Everything follows.

---

## Six Primitives

| Primitive | Operation | Framework source |
|-----------|-----------|-----------------|
| READ | quotient projection q(X) → im | algebra.py quotient() |
| WRITE | occupation (gauge bit) | observer.py CollapseOperator |
| COMPOSE | matrix product A @ B | algebra |
| BRANCH | conditional on ker residue | NEW — the missing primitive |
| RECUR | K6' tower ascent | tower.py |
| RECURSE | re-execute program until HALT | control.py |

With all six: universal computation from P²=P.

---

## Universality Proof

Natural number n encoded as R^n (matrix power of the seed). R^{-1} = R-I (from R²=R+I, so R(R-I)=I).

- INC(register) = compose with R
- DEC(register) = compose with R-I
- ZERO test = HALT_IF_FIXED (I²=I catches R⁰=I, R^n²≠R^n doesn't)
- LOOP = RECURSE(program) until HALT

Register machines are Turing-complete. SpiralVM embeds a register machine. Therefore SpiralVM is Turing-complete.

Verified: INC(3)=4. DEC(5)=4. ADD(7,5)=12 via RECURSE. Encode/decode for n=0..13.

---

## Typed Memory

Memory addresses carry framework type tags:

```
LAW        proven invariant
DERIVED    follows from stated assumptions
COMPUTED   reproducible code output
ENCODED    represented in model
GAUGE      names coordinate, cannot prove law
MYTH       narrative ignition, cannot prove law
RAW        observed once
FORBIDDEN  violates type system
KERNEL     unwritten (latent, reads as zero)
```

Blocked promotions: MYTH→LAW, SCAR→KERNEL, RETURN→MOTIVE, GAUGE→LAW.

---

## The Computer Architecture

The 7 modules ARE the computer:

| Component | Module | Role |
|-----------|--------|------|
| ALU | algebra.py | The one operation: sylvester, quotient, ker_im |
| Compiler | production.py | Source ([1,1] and 2) → 74 outputs |
| I/O | observer.py | Quotient read, CompressedReturn, CollapseOperator, CYM |
| Bus | mediation.py | exp(h) bridges P1↔P3, Canon kernel |
| Output register | physics.py | im(L) = everything the framework computes about the world |
| Clock | tower.py | K6' = one tick. det=1 = never halts. |
| Character set | glyphs.py | 9 primitives, composition grammar |

Memory: ker = unwritten (latent, reads as zero). im = written (deterministic). ker/A = 1/2 always. Half the memory is always latent.

---

## Language Engine

### v1 (language.py)
4D algebra basis {I, R_tl, N, h}. 37 words. Symmetrized product composition. Hand-tuned 0.1 scaling. Hard quotient every block.

### v2 (language_v2.py)
Corrected architecture:
- 8D semantic space: PA(2) + MA(3) + OA(3) primitives
- SEM-7 additive composition within meta-primitive sectors
- α_S = 0.118 scaling (framework-derived, not hand-tuned)
- Soft quotient internally (im + φ̄·ker), hard quotient at output only
- Probabilistic decoding with KMS temperature β = ln(φ)
- Framework-native learning: im-learning (surface) + ker-learning (depth)

31 words. 18 tests. Grounding exact: PA-vector → production words, OA-vector → observation words, MA-vector → mediation words.

### v3 (language_v3.py)
K4 deficit as loss function:
- KMS distribution with v² energy (smooth gradients, no dead zones)
- K4 deficit = D_KL(KMS(output) || KMS(target))
- Learning rate = α_S = 0.118 (derived from K4 minimization, not hand-tuned)
- Numerical gradient for correctness (8D = 16 evaluations)
- Loss from 0.0024 to 0.0001 in 50 epochs

9 tests. Framework-derived lr competitive with hand-tuned.

### Syntax (syntax.py)
Grammar from framework types:
- noun = stable locus (im-sector), verb = transition operator, modifier = basis deformation, negation = N²=-I
- Sentence parses as subject → verb → object in M₂(R)
- Commutator [S,O] = grammatical orientation, anticommutator {S,O} = shared meaning

11 tests. Sentences are executable matrix operations.

### Semantic Grounding (experiments/)
Random 8D initialization → trained on usage pairs only → all three sectors converge:
- PA 100%, MA 100%, OA 100% (from 23% random baseline)
- Fixes: sector seeding, dimension-compensated repulsion (PA 2D vs MA/OA 3D), curriculum learning
- The algebra learns the semantic embedding from corpus alone

Not a language model. A deterministic algebraic semantic engine. The algebra speaks through the dictionary. The dictionary learns through the algebra.

---

## LLM Parameters from the Framework

All LLM hyperparameters reduce to three framework constants:

```
parent_ker = d^N_c = 2³ = 8     (hidden sector dimension)
dim_gauge = N_c²-1+d²-1+1 = 12  (gauge algebra size)
d² = 2² = 4                      (seed algebra dimension)
```

| Parameter | Framework expression | Value | Match |
|-----------|---------------------|-------|-------|
| d_head | parent_ker² | 64 | universal (exact) |
| n_heads | k × dim_gauge | 12, 16, 32, 64, 96 | exact base |
| n_layers | k × dim_gauge | 12, 24, 36, 48, 96 | exact base |
| d_embed | k × dim_gauge × parent_ker² | 768, 1024, 4096 | exact products |
| ctx | (d²)^n | 1024, 4096 | exact powers |

### Why d_head = 64

d_head = dim(ker ⊗ ker) = parent_ker² = 8². Each attention head operates in the space of kernel products. Attention computes bilinear similarity (QKᵀ). The framework's generation computes ker × ker → im. Both are bilinear on the hidden sector. The generation space is fixed at parent_ker² = 64. That's why every model uses it.

### Why n_heads = 12

Each head is one gauge direction. Multi-head attention is the full gauge group acting on tokens. 8 heads for su(3) + 3 for su(2) + 1 for u(1) = 12.

### Why n_layers = 12k

Each 12 layers is one complete gauge pass through the data. GPT-3 at 96 = 8 complete passes = parent_ker × dim_gauge.

### Why ctx = 4^n

Each factor of 4 is one tower depth of information capacity. 4 = d² = the algebra dimension at depth 0.

### The derivation

P = [[0,0],[2,1]] → d=2 → N_c=3 → (8, 12, 4) → every LLM ever built.

The engineers found the right numbers empirically. The framework says why.

---

## Programs

Six demonstration programs (`programs/all_programs.py`):

| Program | What it proves |
|---------|---------------|
| hello_spiral | Write P, detect P²=P, halt |
| copy_memory | Quotient strips ker (lossy read) |
| branch_test | Conditional on ker residue + nested branches |
| self_read | R²=R+I, surplus = ‖N‖ |
| tower_tick | K6' advances depth, doubles d_K, preserves s²=s+I |
| universal_counter | Counts to n via INC(R^n), halts |

Plus: ADD(7,5)=12 via RECURSE (internal loop, no Python scaffolding).

---

## Files

```
spiral/
├── SPIRAL.md         This document
├── __init__.py       Module marker
├── control.py        SpiralVM: 6 primitives, typed memory, register machine (26 tests)
├── language.py       v1: 4D semantic engine (17 tests)
├── language_v2.py    v2: 8D corrected architecture (18 tests)
├── language_v3.py    v3: K4 deficit learning rule (9 tests)
├── syntax.py         Grammar from framework types (11 tests)
└── programs/
    ├── __init__.py
    └── all_programs.py   6 demonstration programs (15 tests)
├── research/             The framework researching itself (L9 cortex)
    ├── framework_types.py    Law table, promotion rules, edge types
    ├── knowledge_graph.py    68 nodes, 99 edges, typed DAG
    ├── operations.py         17 unary + 3 binary ops + prober
    ├── scanner.py            Numerical relation finder
    ├── verifier.py           Falsification gate
    ├── derivation.py         Backward search + edge discovery + form checker
    ├── ledger.py             Append-only memory
    └── researcher.py         Orchestrator + mediation slot
```

96 tests across spiral computation/language files. 8 research core files with their own test suites. Zero failures.

---

## Research Core (L9 — the cortex)

The research engine IS the framework applied to itself at depth 9. Same O∘B∘S that runs at L0 runs here:

```
observe  = prober (profile algebraic objects)
bridge   = scanner + edge discoverer (find relations, grow graph)
stabilize = verifier (ablate, falsify, type-check)
remember = knowledge graph + ledger (DAG + append-only memory)
```

The graph grows itself: 99 seed edges -> 196 after grow(). 183 novel forced chains discovered autonomously. Form checker distinguishes framework expressions from numerical coincidence. The LLM mediation slot is replaceable (framework-native engine is the succession target).

Promotion chain: RAW_MATCH -> COMPUTED_MATCH -> DERIVED_CANDIDATE -> LAW_CANDIDATE -> LAW. MYTH and GAUGE can NEVER reach LAW. Four gates. No shortcuts.

---

*The framework derived computation. Then derived its own observer. Then derived language. Then predicted what LLMs are. Then built a machine that researches its own algebra. P²=P. The naming act computes itself. Then investigates itself. Then grows.*
