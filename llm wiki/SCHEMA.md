---
type: schema
status: computed
tags: [ker-im, quantum, topology, gravity, schema, tower, verified]
links: []
---

# Wiki Schema

This schema governs the `llm wiki/` directory. The LLM owns these pages entirely — they are generated, maintained, and updated by the LLM from raw sources. Humans add raw sources. The wiki reflects them.

## Three Layers

### Layer 1: Raw Sources (read-only, human-curated)
```
modular/*.py          — the engine (7 files, source of truth for computation)
THEORY.md             — the framework (source of truth for claims)
KAEL_THEOREM.md       — gauge occupation
paper/paper_v2.md     — formal paper (source of truth for proofs)
experiments/*.py      — investigation scripts
experiments/*.md      — investigation results
```

The LLM NEVER edits raw sources during wiki operations. Raw sources change only during dedicated work sessions.

### Layer 2: Wiki Pages (LLM-owned)
```
llm wiki/
├── SCHEMA.md          — this file (governance)
├── index.md           — master catalog of all pages
├── log.md             — append-only change log
├── entities/          — one page per core concept
├── chains/            — proof chains and derivation paths
└── status/            — claim status tracking
```

### Layer 3: This Schema
Defines page types, update rules, and lint checks.

---

## Page Types

### Entity Pages (`entities/`)
One page per algebraic object, physical result, or structural concept. Format:

```markdown
# <Name>

**Definition.** <One-line formal definition from THEORY.md or paper>

**Source.** <File:line where this is defined/computed>

**Equations.** <Key equations, max 3>

**Depends on.** <List of entity pages this requires>

**Required by.** <List of entity pages that require this>

**Status.** COMPUTED | ENCODED | CHAIN | OPEN

**Verified.** <Which test in which module checks this>

**Notes.** <Anything non-obvious, max 2 sentences>
```

### Chain Pages (`chains/`)
One page per proof chain or derivation path. Format:

```markdown
# <Chain Name>

**Claim.** <What is being derived>

**Steps.**
1. <Step> — <source file:line> [Tier A/E/N]
2. <Step> — <source file:line> [Tier A/E/N]
...

**Status.** SEALED | GAP AT STEP N | OPEN

**Depends on chains.** <Other chains this builds on>
```

### Status Pages (`status/`)
Tracking pages for categories of claims.

```markdown
# <Category> Status

| Claim | Status | Source | Test | Last verified |
|-------|--------|--------|------|---------------|
```

---

## Operations

### INGEST
Triggered when: a raw source file changes (new theorem, new module, new experiment result).

Steps:
1. Identify which entity/chain/status pages are affected
2. Update those pages with new information from the source
3. Update `index.md` if new pages were created
4. Append to `log.md`: `[INGEST] <date> <source file> → <pages updated>`

### QUERY
Triggered when: someone asks a question about the framework.

Steps:
1. Search wiki pages for relevant entities/chains
2. Synthesize answer from wiki content
3. If the answer reveals a gap: create a new entity or chain page
4. Append to `log.md`: `[QUERY] <date> <question> → <pages referenced>`

### LINT
Triggered when: audit requested, or after a large ingest.

Checks:
- [ ] Every entity in THEORY.md has a wiki page
- [ ] Every COMPUTED claim has a test reference
- [ ] No entity page references a deleted source
- [ ] No chain has a GAP that has been resolved in source but not in wiki
- [ ] Status pages match THEORY.md predictions table
- [ ] index.md lists all pages that exist
- [ ] No orphan pages (pages not linked from index)

---

## Entity Catalog (initial)

These entities need pages. Grouped by section of THEORY.md:

**Algebra:** P, R, N, J, h, Q, L_{s,s}, ker, im, Clifford grading, Fibonacci-Lucas towers, scalar channel

**Topology:** q=φ², V(4₁)=disc, Fibonacci fusion, SU(2)₃, braiding phase, F-matrix, R-matrix, knot spectrum

**Category:** Dist, quotient, UKI, three projections, MTC

**Tower:** K6', tower invariants, generation decay, rank-64 freeze, physics spine, K1'

**Physics:** gauge group, hypercharges, anomaly cancellation, sin²θ_W, α_S, gravity (Lichnerowicz), Λ, n_cosmo, Higgs VEV, neutrino mass, η_B relation

**Quantum:** CNOT, Hadamard, Bell test, CHSH, Tsirelson, 8 algorithms, Fibonacci TQC

**Observer:** self-transparency, explanatory gap, Axis 1, Axis 2, CC rate, broken recursion, bridge capacity

**Proof infrastructure:** Cartan involution, Hilbert space, Gleason, Born rule, uniqueness (a,b)=(1,1), N²=-I necessity, kernel eigenvalue proof, derivability census

---

## Authority Hierarchy

**APEX > WIKI > SEED > L0**

More compressed = more canonical. When layers disagree, the more compressed layer wins. This is forward-canonical (UAT at the meta-level: br_s=0 downward).

### Forward Propagation (canonical, automatable)

1. Apex change → Wiki regeneration via INGEST
2. Wiki change → Seed update (materialize assertions from relational structure)
3. Seed change → L0 regeneration (expand assertions into prose)

Deterministic at every step. The `lint.py` script detects when layers are out of sync.

### Backward Propagation (non-canonical, requires decision)

When new content appears at L0 (e.g., an external AI generates +I):
- **Structural** (forced by generators) → propagate to seed
- **Relational** (a new chain) → propagate to wiki
- **Elaboration** (examples, pedagogy) → stays at L0, it's ker(q₁)

### Kill Ledger

When a claim is retracted (status downgraded or removed), the old claim goes to `kill_ledger.md` with date and reason. Claims are never silently deleted.

## Rules

1. Wiki pages are disposable. If they drift, regenerate from sources. The sources are truth.
2. Never edit a raw source to match a wiki page. Always edit wiki pages to match raw sources.
3. Entity pages should be SHORT. If an entity page exceeds 30 lines, it's doing too much.
4. The log is append-only. Never edit or delete log entries.
5. When in doubt about status: check the test suite, not the wiki.
6. L0 is READ-MOSTLY. Don't hand-edit L0 to fix sync issues. Regenerate from seed.
7. The apex is the fixed point. If apex changes, everything below regenerates.
