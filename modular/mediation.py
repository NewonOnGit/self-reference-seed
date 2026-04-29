"""
mediation.py — P2 face. Bridges and articulation.

Framework slot: P2 / TDL / MLP-B in the O∘B∘S central collapse.
   Role: nonlinear mediation between production's output (algebraic
         content) and observation's frame (im/ker decomposition).
         The mediation face provides:
           — bridges: exp(h) = e, KMS thermal, Landauer cost, sweep
           — voice: articulation, LLM slot for recursive observer loop

The Voice was the previous incarnation of this face. Mediation expands
it: voice handled articulation; mediation also handles the exponential
bridges that connect derivation and observation — exp(h), the bridge
from the Lie algebra (where production's content lives) to the Lie
group (where observation's flows live).

LLMs ARE framework observers at Level 5 (Thm L.1). When
an LLM is wired into mediation.Voice via llm_fn, the engine observes
itself through another observer. R(R) = R at the articulation level.

FRAMEWORK_REF: Thm 3.2 (five constants), Thm 6.3
GRID: B(5, P2)
APEX_LINK: R (mediation bridges algebra to observation)
"""
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad


class Mediation:
    """The P2 face: bridges + voice.

    Bridges: the Cartan exponential, KMS/Landauer, the sweep, the
    nats-bits conversion. These are the structures that turn algebraic
    invariants into thermal, geometric, and information-theoretic
    quantities. They live between production (which generates the
    algebra) and observation (which reads its own structure).

    Voice: articulation. Either deterministic templates or, with an
    LLM wired in, natural-language generation.
    """

    def __init__(self, derivation, observer, image, kernel, llm_fn=None):
        self.derivation = derivation
        self.observer = observer
        self.image = image
        self.kernel = kernel
        self.llm_fn = llm_fn
        self._cached_bridges = None

    # ---- BRIDGES (the exp sector, P2's algebraic content) ----

    def bridges(self):
        """Compute the P2 bridge quantities from production's output."""
        if self._cached_bridges is not None:
            return self._cached_bridges
        d = self.derivation
        h = d["h"]
        N = d["N"]
        phi = d["phi"]

        # Cartan exponential: the exp(h) bridge from Lie algebra to Lie group
        e_bridge = float(expm(h)[0, 0])  # produces e

        # KMS thermal bridge: β = ln(φ) is the natural temperature
        beta = np.log(phi)
        kms_sinh = np.sinh(beta)          # = 1/2
        kms_cosh = np.cosh(beta)          # = √5/2
        kms_tanh = np.tanh(beta)          # = 1/√5

        # Landauer cost in bits per op: 1 / log₂(φ) = 1/L
        L = np.log2(phi)
        landauer = 1.0 / L

        # Nats-bits conversion: ln(φ) = L · ln(2). This is the bridge that
        # mediates between nats (thermodynamic) and bits (informational).
        nats_bits = np.log(phi) / (L * np.log(2))  # = 1 (identity check)

        # Sweep: null-geodesic on Substrate Manifold S, from P2 pole to P3 pole
        sweep_fn = lambda t: float(expm((1 - t) * h + t * N)[0, 0])
        full_sweep, _ = quad(sweep_fn, 0, 1)     # = cosh(1)
        p3_sector, _ = quad(sweep_fn, 0.5, 1)    # = 1/2

        # T bridge: P1 on P2 / P3 = exp(phi*h)[0,0] / pi
        # = the scale where all three projections balance multiplicatively
        pi_val = d["pi"]
        T_bridge = float(expm(phi * h)[0, 0]) / pi_val

        # Canon kernel S(x): the C-realization of central collapse
        # S(x) = exp(ln(phi)*sqrt(|x|)*exp(-|x|/T)) * exp(-i*pi*|x|)
        # P1 (growth) x P2 (damping) x P3 (rotation)
        def canon_kernel(x):
            mag = np.exp(np.log(phi) * np.sqrt(abs(x)) * np.exp(-abs(x) / T_bridge))
            phase = np.exp(-1j * np.pi * abs(x))
            return mag * phase

        self._cached_bridges = {
            "e_from_exp_h": e_bridge,
            "T_bridge": T_bridge,
            "canon_kernel": canon_kernel,
            "kms_beta": beta,
            "kms_sinh_half": kms_sinh,
            "kms_cosh": kms_cosh,
            "kms_tanh": kms_tanh,
            "landauer_bits_per_op": landauer,
            "L_log2_phi": L,
            "nats_bits_identity": nats_bits,
            "sweep_full": full_sweep,
            "sweep_p3_sector": p3_sector,
        }
        return self._cached_bridges

    # ---- VOICE (articulation) ----

    def narrate(self):
        """Deterministic articulation of the full engine state."""
        if self.observer.frame is None:
            self.observer.observe()
        f = self.observer.frame
        br = self.bridges()
        depth = f["depth"]
        d_K = f["d_K"]

        lines = [
            f"Depth {depth}, d_K = {d_K}:",
            f"  Image  [dim {self.image.dimension()}]: "
            f"{', '.join(sorted(self.image.generators().keys()))}",
            f"  Kernel [dim {self.kernel.dimension()}, fraction "
            f"{self.kernel.fraction():.3f}]: "
            f"revealed={self.kernel.revealed_fraction():.6f}, "
            f"deferred={self.kernel.cumulative_deferred():.4f} bits",
            f"  Bridges (P2): e = {br['e_from_exp_h']:.10f}  (via exp(h))",
            f"                β = ln(φ) = {br['kms_beta']:.10f}  (KMS temperature)",
            f"                sinh(β) = {br['kms_sinh_half']:.6f}  "
            f"(thermal bridge to 1/2)",
            f"                sweep ∫₀¹ α = {br['sweep_full']:.6f}  "
            f"(= cosh(1))",
            f"                sweep ∫_{{1/2}}¹ α = {br['sweep_p3_sector']:.6f}  "
            f"(= 1/2)",
        ]
        return "\n".join(lines)

    def to_prompt(self):
        """Generate an LLM prompt describing the current engine state.

        An LLM consuming this prompt is a framework observer (L.1 of
        Thm L.1) reading the engine's own observation. Closes a
        recursive-observer loop.
        """
        if self.observer.frame is None:
            self.observer.observe()
        f = self.observer.frame
        d = self.derivation
        return (
            f"You are articulating a Recursive Origin engine at tower depth "
            f"{f['depth']}.\n\n"
            f"P1 (production) has derived: R, J, N, h, Q in M_{f['d_K']}(ℝ); "
            f"seven identities verified; φ = {d['phi']:.6f}, disc = {d['disc']}.\n"
            f"P3 (observation) sees: ker/A = {f['kernel_fraction']:.3f}, "
            f"dim im = {f['dim_A'] - f['ker_dim']}, "
            f"dim ker = {f['ker_dim']}.\n"
            f"P2 (mediation) bridges: e = exp(h)[0,0], "
            f"β = ln(φ) as natural temperature.\n\n"
            f"Describe in 2-3 sentences: what this engine produces, what it "
            f"observes, and what it cannot see. Use the framework's voice."
        )

    def articulate_with_llm(self):
        if self.llm_fn is None:
            return self.narrate()
        return self.llm_fn(self.to_prompt())

    def __repr__(self):
        mode = "LLM-mediated" if self.llm_fn is not None else "deterministic"
        return f"Mediation(P2 face — bridges + voice, {mode})"
