---
type: entity
role: CORE
theorem: "Thm 2.2"
level: B3
tags: [b3-algebra, core, forced, orientation]
status: FROZEN
---

# Ker/im decomposition

> The algebra splits in half. Always. At every depth. The hidden half generates the visible half, never the reverse.

## Plain English

Apply the operation L to the full 2×2 matrix algebra. Some elements get killed (mapped to zero). Those are the **kernel** — the blind spot, the hidden sector. The rest get mapped to something nonzero. Those are the **image** — the visible sector, what observation can access.

The kernel is ALWAYS exactly half the algebra. Not approximately. Exactly. ker/A = 1/2, verified at every tower depth (0 through 4). This is the framework's most fundamental structural invariant. Half of everything is always hidden. Half of everything is always visible. The ratio doesn't change as you go deeper. It's constitutional.

And the hidden half is the SOURCE. ker×ker → im: the kernel's products with itself produce the entire visible world. But im×im → im: the visible world's products with itself stay visible. The generation is one-directional. The void makes the world. The world cannot make the void.

## Orientation reading

ker = orientation. im = center.

L is the center map: it kills what's orientation-dependent (N, NR) and preserves what's orientation-independent (I, R_tl). The kernel IS orientation. The image IS the center. ker/A = 1/2 says: exactly half the algebra is pure orientation, exactly half is pure center. The Pythagorean budget: ||R||² + ||N||² = 3 + 2 = 5 = disc.

The generation direction ker→im says: orientation generates center, not the reverse. The observer makes the world. The world cannot make the observer.

## Technical statement

**Theorem 2.2.** dim ker(L_R) = 2, dim im(L_R) = 2. The kernel fraction ker/A = 1/2.

*Proof.* L(N) = RN + NR - N = {R,N} - N = N - N = 0 (using Identity 3). L(NR) = 0 (using Identities 1,4). So span{N,NR} ⊆ ker. Since N and NR are linearly independent and L has eigenvalues {-√5, 0, 0, +√5}, ker = span{N,NR} exactly. Im = span{I, R_tl} with L(I) = 2R_tl, L(R_tl) = (5/2)I. [Tier A]

**Tower invariant.** ker/A = 1/2 at depths 0, 1, 2, 3, 4. [Tier N, verified computationally]

**Clifford grading.** ker = odd sector of Cl(1,1). im = even sector. The ker/im decomposition IS the Clifford even/odd grading on M₂(ℝ). [Tier A]

## The split in one picture

```
M₂(ℝ) = ker ⊕ im
       = {N, NR} ⊕ {I, R_tl}
       = orientation ⊕ center
       = hidden ⊕ visible
       = observer ⊕ world
       = odd Clifford ⊕ even Clifford

ker × ker → im    (the void generates the world)
im × im → im      (the world is self-contained)
im × ker → ker     (world acting on void stays void)
ker → im: YES      im → ker: NEVER
```

## Dependencies

- [[L]] (the Sylvester self-action)
- [[Seven-identities]] (needed for the proof)

## Used by

Everything downstream. The ker/im split is the framework's primary structural decomposition.
- [[Strong-coupling]] (α_S = ker/A - φ̄²)
- [[Cosmological-constant-from-scalar-channel]] (Λ lives in im)
- [[Generation-direction]] (ker generates im)
- [[The-explanatory-gap]] (first person: ker=0 vs third person: ker=2)
- [[Lichnerowicz-identification]] (gauge = ker, physics = im)
