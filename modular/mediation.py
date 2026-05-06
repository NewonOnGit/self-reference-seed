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

    def cognitive_summary(self):
        """Summary of cognitive capabilities at current depth.
        The P2 bridge between capabilities and voice."""
        if self.observer.frame is None:
            self.observer.observe()
        f = self.observer.frame
        d = self.derivation

        # Kernel logic
        mt = self.kernel.multiplication_table()

        # World-model invertibility
        I_d = np.eye(f["d_K"])
        _, solvable, res = self.image.invert(I_d)

        lines = [
            f"COGNITIVE STATE (depth {f['depth']}, d_K={f['d_K']}):",
            f"  Distinction:  ker={f['ker_dim']}, im={f['dim_A']-f['ker_dim']} "
            f"(fraction {f['kernel_fraction']:.3f})",
            f"  Memory:       revealed={self.kernel.revealed_fraction():.6f}, "
            f"deferred={self.kernel.cumulative_deferred():.4f} bits",
            f"  Attention:    {'classical' if self.image.is_commutative() else 'quantum'} "
            f"(curvature={self.image.obstruction_curvature():.4f})",
            f"  Logic:        ker x ker -> im = {mt['all_in_im']} "
            f"({len(mt['table'])} products)",
            f"  Prediction:   golden eigenvalues = "
            f"{self.observer.self_model_eigenvalues()}",
            f"  Self-model:   transparent = {self.observer.self_transparent()}",
            f"  Abduction:    L(X)=I solvable = {solvable} "
            f"(residual {res:.2e})",
        ]
        return "\n".join(lines)

    def __repr__(self):
        mode = "LLM-mediated" if self.llm_fn is not None else "deterministic"
        return f"Mediation(P2 face — bridges + voice, {mode})"


# ============================================================
# RESEARCH ENGINE: RESEARCHER (from researcher.py)
# ============================================================

import os
import re
from algebra import ResultType, Tier, probe
from tower import KnowledgeGraph
from physics import Scanner
from observer import Verifier, Ledger


class Researcher:
    """The research loop orchestrator."""

    def __init__(self, mediate_fn=None, ledger_path=None):
        self.graph = KnowledgeGraph().seed()
        self.scanner = Scanner(mode='PHYSICS', tolerance=0.02, max_complexity=3)
        self.verifier = Verifier()
        self.ledger = Ledger(filepath=ledger_path)
        self.mediate_fn = mediate_fn

    def investigate_number(self, target, name=None):
        """Full pipeline: scan -> verify each -> ledger -> best."""
        if name is None:
            name = f'target={target}'
        matches = self.scanner.scan(target)
        self.ledger.record_scan(target, matches)
        if not matches:
            return {'name': name, 'status': 'NO_MATCHES', 'results': []}
        verified = []
        for match in matches[:10]:
            try:
                vresult = self.verifier.verify_numerical(
                    target=target,
                    expression_fn=self._make_fn(match.expression),
                    expression_str=match.expression
                )
                self.ledger.record_verification(vresult)
                verified.append(vresult)
            except Exception:
                pass
        survivors = [v for v in verified if v.status != ResultType.REFUTED]
        survivors.sort(key=lambda v: (v.tier != Tier.A, not v.details.get('exact'), len(v.checks_failed)))
        return {
            'name': name, 'status': 'FOUND' if survivors else 'ALL_REFUTED',
            'best': survivors[0] if survivors else None,
            'all_verified': verified, 'scan_count': len(matches),
        }

    def investigate_matrix(self, X, name='X'):
        """Probe a matrix using the operations microscope."""
        result = probe(X, name)
        self.ledger.record_probe(name, result)
        return result

    def investigate_frontier(self, n=3):
        """Investigate most promising frontier nodes."""
        frontier = self.graph.frontier()
        open_nodes = [f for f in frontier if f.status == ResultType.OPEN_FRONTIER]
        targets = (open_nodes or frontier)[:n]
        results = []
        for node in targets:
            if node.value is not None and isinstance(node.value, (int, float)):
                results.append(self.investigate_number(node.value, node.name))
        return results

    def report(self):
        gs = self.graph.stats()
        ls = self.ledger.stats()
        return {
            'graph': gs, 'ledger': ls,
            'frontier_size': gs['frontier'],
            'total_investigations': ls['total'],
            'survivors': ls['survivors'],
            'failures': ls['failures'],
        }

    def _make_fn(self, expr):
        def fn(c):
            local = dict(c)
            local['np'] = np
            local['sqrt'] = np.sqrt
            local['ln'] = np.log
            return eval(expr, {"__builtins__": {}}, local)
        return fn


def load_api_key():
    """Load API key from secret.txt (NOT committed to git)."""
    paths = [
        os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'secret.txt'),
        os.path.expanduser('~/.anthropic_key'),
    ]
    for p in paths:
        if os.path.exists(p):
            with open(p) as f:
                return f.read().strip()
    return os.environ.get('ANTHROPIC_API_KEY')


def make_claude_mediator(api_key, model='claude-haiku-4-5-20251001'):
    """LLM as P2 face. Proposes only. Does not certify."""
    try:
        import anthropic
    except ImportError:
        return None
    client = anthropic.Anthropic(api_key=api_key)

    def mediate(context):
        system = (
            "You are a research mediator for the Self-Reference Framework. "
            "Propose ONE specific numerical target or matrix expression to "
            "investigate next. Give the number, a one-line reason, nothing else."
        )
        try:
            response = client.messages.create(
                model=model, max_tokens=150, system=system,
                messages=[{"role": "user", "content": context}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            return f"MEDIATION_FAILED: {e}"
    return mediate


def make_dummy_mediator():
    """Fallback: proposes from a fixed list."""
    targets = [
        (137.036, "1/alpha_EM (requires M_GUT)"), (0.2224, "sin(theta_Cabibbo)"),
        (1836.15, "m_p/m_e"), (0.1181, "alpha_S at m_Z"),
        (80.379, "m_W GeV"), (0.6667, "Koide Q = wobble silence"),
    ]
    idx = [0]
    def mediate(context):
        t, reason = targets[idx[0] % len(targets)]
        idx[0] += 1
        return f"Investigate {t}: {reason}"
    return mediate


def run_mediated_cycle(researcher, mediator, n_cycles=3):
    """Run n research cycles with mediation."""
    results = []
    for i in range(n_cycles):
        report = researcher.report()
        frontier_names = [f.name for f in researcher.graph.frontier()[:5]]
        context = (
            f"Research: {report['graph']['nodes']} nodes, "
            f"{report['total_investigations']} investigations. "
            f"Frontier: {frontier_names}. "
            f"What number should I investigate?"
        )
        proposal = mediator(context)
        target = None
        for num_str in re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', proposal):
            try:
                val = float(num_str)
                if 1e-15 < abs(val) < 1e10:
                    target = val
                    break
            except ValueError:
                continue
        if target is not None:
            result = researcher.investigate_number(target, f"mediated_{i}")
            results.append(result)
    return results
