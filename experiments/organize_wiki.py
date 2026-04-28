"""
organize_wiki.py — Move entity pages into tower-level folders.
Also enriches tags for Obsidian graph coloring.
"""
import os
import re
import shutil

ENTITIES = os.path.join(os.path.dirname(__file__), '..', 'llm wiki', 'entities')

# Page -> tower level mapping (from the index structure)
LEVEL_MAP = {
    # B0 - SUBSTRATE
    'P.md': 'B0-substrate', 'Asymmetry-is-forced.md': 'B0-substrate',
    'Three-generating-equations.md': 'B0-substrate',
    'Cayley--Hamilton-consequences.md': 'B0-substrate',
    'Complex-structure-from-asymmetry.md': 'B0-substrate',
    'The-naming-triangle.md': 'B0-substrate',
    'Hilbert-space-from-asymmetry.md': 'B0-substrate',
    'Thm-1.2.md': 'B0-substrate',

    # B2 - CATEGORY
    'Thm-2.1.md': 'B2-category', 'Ker-im-decomposition.md': 'B2-category',
    'Scalar-channel.md': 'B2-category', 'Spectrum.md': 'B2-category',
    'N2---I-is-necessary.md': 'B2-category', 'Clifford-grading.md': 'B2-category',
    'Generation-direction.md': 'B2-category',

    # B3 - ALGEBRA
    'R.md': 'B3-algebra', 'N.md': 'B3-algebra', 'L.md': 'B3-algebra',
    'Seven-identities.md': 'B3-algebra', 'Five-constants.md': 'B3-algebra',
    'Fibonacci--Lucas-towers.md': 'B3-algebra', 'Thm-3.3.md': 'B3-algebra',
    'Perturbation-fragility.md': 'B3-algebra',
    'Alternative-seed-failure.md': 'B3-algebra',

    # B4 - CROSS-PROJECTION
    'Quantum-deformation-at-the-golden-point.md': 'B4-cross-projection',
    'Jones--discriminant.md': 'B4-cross-projection',
    'Fusion--persistence.md': 'B4-cross-projection',
    'Clifford--Fibonacci.md': 'B4-cross-projection',
    'Knot-spectrum.md': 'B4-cross-projection',
    'R-matrix-eigenvalues.md': 'B4-cross-projection',

    # B5 - OBSERVER
    'Tower.md': 'B5-observer', 'Observer.md': 'B5-observer',
    'Identity-preservation.md': 'B5-observer', 'Filler-uniqueness.md': 'B5-observer',
    'Continuity.md': 'B5-observer', 'Tower-invariants.md': 'B5-observer',
    'Thm-16.1.md': 'B5-observer', 'Thm-6.1.md': 'B5-observer',
    'Uniqueness-of-self-transparency.md': 'B5-observer',
    'The-explanatory-gap.md': 'B5-observer',
    'Total-capacity.md': 'B5-observer', 'Thm-17.0.md': 'B5-observer',
    'Axis-2-is-unattenuated.md': 'B5-observer',
    'Three-mechanisms-of-broken-recursion.md': 'B5-observer',
    'Healing-requires-Axis-2.md': 'B5-observer',
    'External-bridge.md': 'B5-observer',
    'Kernel-concentration.md': 'B5-observer',
    'Cosmological-persistence.md': 'B5-observer',

    # B6 - PHYSICS
    'gravity.md': 'B6-physics', 'Lichnerowicz-identification.md': 'B6-physics',
    'The-connection-produces-the-observer.md': 'B6-physics',
    'Gauge-invariance.md': 'B6-physics', 'Vacuum-Einstein.md': 'B6-physics',
    'Gravitational-wave-spectrum.md': 'B6-physics',
    'Einstein--Hilbert-action.md': 'B6-physics',
    'Cosmological-constant-from-scalar-channel.md': 'B6-physics',
    'Lambda-is-depth-invariant.md': 'B6-physics',
    'Cosmological-attenuation.md': 'B6-physics',
    'The-cosmological-braid.md': 'B6-physics',
    'Two-routes-to-n_mathrmcosmo.md': 'B6-physics',
    'Depth-2-Clifford-structure.md': 'B6-physics',
    'Depth-2-metric.md': 'B6-physics',
    'K1-suppression.md': 'B6-physics',
    'Classical-to-quantum-transition.md': 'B6-physics',
    'Opacity-hardening.md': 'B6-physics',
    'Generation-strength.md': 'B6-physics',
    'The-rank-64-identification.md': 'B6-physics',
    'Holographic-bound.md': 'B6-physics',
    'Matter-content.md': 'B6-physics',
    'Anomaly-cancellation.md': 'B6-physics',
    'Hypercharge-uniqueness.md': 'B6-physics',
    'Weinberg-angle.md': 'B6-physics',
    'EW-breaking.md': 'B6-physics',
    'K1-as-topological-phase-boundary.md': 'B6-physics',
    'Strong-coupling.md': 'B6-physics',
    'KL-uniqueness.md': 'B6-physics',
    'Neutrino-mass.md': 'B6-physics',
    'Proton-mass-ratio.md': 'B6-physics',
    'Baryon-asymmetry-and-the-relational-constraint.md': 'B6-physics',
    'Yang--Mills-from-K4.md': 'B6-physics',

    # B7 - QUANTUM
    'bell.md': 'B7-quantum',
    'CNOT-from-framework-generators.md': 'B7-quantum',
    'Hadamard.md': 'B7-quantum',
    'Bell-violation--Tsirelson-saturation.md': 'B7-quantum',
    'Bell-state.md': 'B7-quantum',
    'Spin-statistics.md': 'B7-quantum',
    'Fibonacci-TQC-universality.md': 'B7-quantum',
    'Braiding-phase.md': 'B7-quantum',
    'Verlinde-formula.md': 'B7-quantum',

    # B8 - CLOSURE
    'Self-description.md': 'B8-closure',
    'wiki.md': 'B8-closure',
    'Production.md': 'B8-closure',
    'Image.md': 'B8-closure',
    'Mediation.md': 'B8-closure',
    'Glyphs.md': 'B8-closure',
    'Kernel.md': 'B8-closure',
}

moved = 0
unmapped = []
for fname in sorted(os.listdir(ENTITIES)):
    if not fname.endswith('.md'):
        continue
    src = os.path.join(ENTITIES, fname)
    if os.path.isdir(src):
        continue

    level = LEVEL_MAP.get(fname)
    if level:
        dst_dir = os.path.join(ENTITIES, level)
        dst = os.path.join(dst_dir, fname)
        if not os.path.exists(dst):
            shutil.move(src, dst)
            moved += 1
    else:
        unmapped.append(fname)

# Also update tags in moved files to include tower level
for level_dir in os.listdir(ENTITIES):
    level_path = os.path.join(ENTITIES, level_dir)
    if not os.path.isdir(level_path) or not level_dir.startswith('B'):
        continue
    level_tag = level_dir.lower()
    for fname in os.listdir(level_path):
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(level_path, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if level_tag not in content:
            content = content.replace('tags: [', f'tags: [{level_tag}, ', 1)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)

print(f"Moved {moved} files into tower-level folders")
if unmapped:
    print(f"Unmapped ({len(unmapped)}): {unmapped[:10]}")

# Count per folder
for d in sorted(os.listdir(ENTITIES)):
    dp = os.path.join(ENTITIES, d)
    if os.path.isdir(dp):
        count = len([f for f in os.listdir(dp) if f.endswith('.md')])
        print(f"  {d}: {count} pages")
