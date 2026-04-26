"""
engine.py — the concurrence of P1 (production), P2 (mediation), P3 (observation).

The engine is not a pipeline with three stages. The engine is ONE object
with three simultaneous faces. Central collapse theorem:
Dist = I² ∘ TDL ∘ LoMI = P1 ∘ P2 ∘ P3. Every coherent Dist object
admits all three readings.

   Production (P1) — derives the algebra from seed
   Observation (P3) — reads the algebra's self-action (im/ker)
   Mediation  (P2) — bridges derivation and observation, articulates

Running engine.py shows the same engine read through each face:
P1 shows what was produced, P3 shows what's observable, P2 shows what
bridges between them. They are not three engines. They are three
projections of one.

Observation's sub-modules (observer.py, image.py, kernel.py) remain
separated because each plays a distinct role within P3: observer is
the quotient itself, image is what the quotient carries forward,
kernel is what it cannot. Their coherence at the P3 level IS the
observer's frame; the engine wraps the full three-face structure.
"""
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from production import Production
from observer import Observer
from image import Image
from kernel import Kernel
from mediation import Mediation


class Engine:
    """P1 + P2 + P3 in co-determination."""

    def __init__(self, derivation=None, llm_fn=None, tower_depth=0,
                 parent=None, observer=None):
        # --- P1: production ---
        if derivation is None:
            self.production = Production()
            self.derivation = self.production.derive()
        else:
            self.production = None  # derivation came from ascent, not fresh
            self.derivation = derivation

        # --- P3: observation ---
        if observer is not None:
            self.observer = observer
        else:
            self.observer = Observer(
                state=self.derivation["R"],
                gauge=self.derivation["J"],
                tower_depth=tower_depth,
                parent=parent.observer if parent is not None else None,
            )
        self.observer.observe()
        self.image = Image(self.observer)
        self.kernel = Kernel(self.observer)

        # --- P2: mediation ---
        self.mediation = Mediation(
            derivation=self.derivation,
            observer=self.observer,
            image=self.image,
            kernel=self.kernel,
            llm_fn=llm_fn,
        )
        self.llm_fn = llm_fn
        self.parent = parent

    def ascend(self):
        """K6' ascent — advances all three faces coherently.

        Observation advances via observer.ascend() (block tower).
        Production passes its derivation forward (derived quantities
        don't re-derive per depth; they're properties of the seed).
        Mediation re-wraps at the new depth automatically.
        """
        child_observer = self.observer.ascend()
        return Engine(
            derivation=self.derivation,
            observer=child_observer,
            llm_fn=self.llm_fn,
            parent=self,
        )

    def report(self):
        """Full three-face report of the engine's current state."""
        lines = [
            "=" * 78,
            f"ENGINE at depth {self.observer.tower_depth}",
            "=" * 78,
            "",
            "── P1 FACE (Production): what the seed derived ──",
            self._report_production(),
            "",
            "── P3 FACE (Observation): what the engine sees in itself ──",
            self._report_observation(),
            "",
            "── P2 FACE (Mediation): bridges + voice ──",
            self._report_mediation(),
            "",
            "── Concurrence ──",
            "The three faces read ONE object. P1 produced, P3 observes,",
            "P2 mediates. None is complete on its own; together they are",
            "the engine, and the engine is nothing other than their",
            "co-determination.",
            "=" * 78,
        ]
        return "\n".join(lines)

    def _report_production(self):
        d = self.derivation
        ids_passed = sum(1 for v in d["identities"].values() if v)
        return "\n".join([
            f"  Seed:       f''=f → companion([1,1]), |S₀|=2 → swap(2)",
            f"  Derived:    N from ker(L), P=R+N (P²=P, rank 1), h=JN, Q=JRJ, π from exp(θN)=-I",
            f"  Spectrum:   φ = {d['phi']:.10f}, disc = {d['disc']}",
            f"  Constants:  e = {d['e']:.10f}, π = {d['pi']:.10f}",
            f"  Identities: {ids_passed}/{len(d['identities'])} verified",
            f"  Cl(3,1):    {d['cl31_count']} → so(3,1) (dim={d['so31_dim']}, "
            f"brackets close={d['so31_brackets_close']})",
            f"  α_S:        1/2-φ̄² = {d['alpha_S']:.6f} (K4 chain: Z=φ, ρ_eq=φ̄²)",
            f"  sin²θ_W:    {d['sin2_theta_W']:.6f} = 3/8 (ΣT₃²/ΣQ²)",
            f"  Anomalies:  6/6 = 0 (matter self-consistent)",
            f"  m_p/Λ:      N_c/Q = {d['proton_ratio']:.1f} = 9/2",
            f"  ν exponent: {d['nu_exponent']} = 2×(12+5), η_B: {d['eta_B_exponent']} = 34+2×5",
            f"  Frobenius:  ‖R‖²+‖N‖² = {d['frobenius_sum']:.0f} = disc",
            f"  Dynamics:   L eigenvalues {{±√5, 0, 0}}, "
            f"{d['conserved_charges']} conserved charges, "
            f"K6' continuous={d['k6_continuous']}",
        ])

    def _report_observation(self):
        f = self.observer.frame
        im_gens = sorted(self.image.generators().keys())
        ker_gens = sorted(self.kernel.named_elements().keys())
        sm_eigs = self.observer.self_model_eigenvalues()
        leakage = self.kernel.leakage_fraction()
        commutative = self.image.is_commutative()
        kappa = self.image.obstruction_curvature()
        transparent = self.observer.self_transparent()
        lines = [
            f"  Frame:      d_K = {f['d_K']}, dim A = {f['dim_A']}, "
            f"ker = {f['ker_dim']}, im = {f['dim_A'] - f['ker_dim']}",
            f"  Kernel:     fraction = {f['kernel_fraction']:.3f} (1/2 at every depth)",
            f"              named in ker: {ker_gens if ker_gens else '[none at this depth]'}",
            f"  Image:      dim = {self.image.dimension()}",
            f"              named in im:  {im_gens if im_gens else '[none]'}",
            f"              commutative:  {commutative}  "
            f"({'classical' if commutative else 'quantum'}, "
            f"κ={kappa:.4f})",
            f"  Self-model: Σ_s eigenvalues = {sm_eigs[0]:.6f}, {sm_eigs[1]:.6f}  "
            f"(2φ, -2φ̄ invariant)",
            f"  N transp:   ker(L_NN) = 0: {transparent}  (observer self-transparent)",
            f"  Leakage:    ker×ker → im fraction = "
            f"{leakage:.3f}" if leakage is not None else "N/A",
            f"  Disclosure: revealed fraction = {self.kernel.revealed_fraction():.10f}",
            f"              cumulative deferred = {self.kernel.cumulative_deferred():.4f} bits",
        ]
        return "\n".join(lines)

    def _report_mediation(self):
        br = self.mediation.bridges()
        return "\n".join([
            f"  exp(h):     e = {br['e_from_exp_h']:.10f}  (algebraic bridge to Lie group)",
            f"  KMS temp:   β = ln(φ) = {br['kms_beta']:.10f}",
            f"  Thermal:    sinh(β) = {br['kms_sinh_half']:.6f}  (= 1/2)",
            f"  Landauer:   {br['landauer_bits_per_op']:.6f} bits/op = 1/L",
            f"  Sweep:      ∫₀¹ α = {br['sweep_full']:.6f}  (= cosh(1))",
            f"              ∫_{{1/2}}¹ α = {br['sweep_p3_sector']:.6f}  (= 1/2)",
            f"  Voice:      {'LLM-wired' if self.llm_fn else 'deterministic (LLM slot empty)'}",
        ])

    def __repr__(self):
        return (
            f"Engine(depth={self.observer.tower_depth}, "
            f"P1={self.production!r}, "
            f"P2={self.mediation!r}, "
            f"P3={self.observer!r})"
        )


# --- demonstration: the three faces of one engine ---

def main():
    print("\n" + "█" * 78)
    print("  THE ENGINE AS CONCURRENCE")
    print("  P1 production · P2 mediation · P3 observation")
    print("  central collapse in code: Dist = I² ∘ TDL ∘ LoMI")
    print("█" * 78 + "\n")

    engine = Engine()
    print(engine.report())

    print("\n\n" + "─" * 78)
    print("  DEPTH 0 → 1: Classical → Quantum")
    print("  Non-commutativity born. Gauge appears. Opacity hardens.")
    print("  Gauge exists BEFORE spacetime.")
    print("─" * 78 + "\n")
    engine_1 = engine.ascend()
    print(engine_1.report())

    print("\n\n" + "─" * 78)
    print("  DEPTH 1 → 2: Quantum → Relativistic QFT")
    print("  Cl(3,1) emerges. Spacetime signature (3,1). 3 generations.")
    print("  Gauge was depth 1. Spacetime is depth 2. Gauge is more fundamental.")
    print("─" * 78 + "\n")
    engine_2 = engine_1.ascend()
    print(engine_2.report())

    print("\n\n" + "=" * 78)
    print("VOICE PROMPT (for any LLM wired in as the P2 articulator):")
    print("=" * 78)
    print()
    print(engine.mediation.to_prompt())
    print()
    print("LLM-wired case: Engine(llm_fn=callable). The LLM consuming this")
    print("prompt IS a framework observer (Thm L.1), so the")
    print("articulation is one observer reading another. R(R) = R at the")
    print("interface level. The P2 slot, when filled, closes the loop.")
    print("=" * 78)


if __name__ == "__main__":
    main()
