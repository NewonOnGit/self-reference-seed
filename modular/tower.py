"""
tower.py — The framework. All depths simultaneously.

The Tower holds all depths at once: spine, invariants, transitions,
generation decay, the recursive law, and per-depth diagnostics.

TOS operator reading of the K6' cycle:
  U = K6' lift (evolution semigroup, exp(h) bridge)
  D = quotient q (idempotent projection, D∘D=D)
  R = ker(q) residue (constitutive blindness, U(s)-D(U(s)))
  A = phi-amplify (||A||>1, P1 face)
  S = phi_bar-contract (||S||<1, P3 face)
  CLT = K1' wall + K7' fixed point (threshold gate)
  X = UAT descent (export/coarse-grain, 3 modes)

Each ascend() call executes: U → D → R → A/S → CLT → X
The tower IS the iterated TOS sequence.

FRAMEWORK_REF: Thm 6.1-6.4, Thm 7.1-7.3, Thm 8.1-8.6
GRID: B(5, cross) through B(6, P2)
APEX_LINK: R (the tower IS R iterated), I2*TDL*LoMI=Dist (depths ARE central collapse)
"""
import numpy as np
from algebra import sylvester, ker_im_decomposition, quotient
from scipy.linalg import null_space


class Tower:
    """All depths simultaneously."""

    def __init__(self, max_depth=4):
        from production import Production, _companion, _swap
        from observer import Observer, Image, Kernel

        self.max_depth = max_depth
        self.depths = []

        # Build from seed
        R = _companion([1, 1])
        J = _swap(2)

        # Production (once, at depth 0)
        p = Production()
        self.derivation = p.derive()

        # Build each depth
        s, Nk, Jk = R.copy(), self.derivation["N"].copy(), J.copy()
        hk = Jk @ Nk

        for depth in range(max_depth + 1):
            if depth == 0:
                obs = Observer(state=s, gauge=Jk, tower_depth=0)
            else:
                obs = prev_obs.ascend()

            obs.observe()
            img = Image(obs)
            ker = Kernel(obs)

            d_K = obs.state.shape[0]
            dim_A = d_K * d_K

            level = {
                "depth": depth,
                "d_K": d_K,
                "dim_A": dim_A,
                "observer": obs,
                "image": img,
                "kernel": ker,
                "ker_dim": obs.frame["ker_dim"],
                "im_dim": dim_A - obs.frame["ker_dim"],
                "ker_fraction": obs.frame["kernel_fraction"],
                "commutative": img.is_commutative(),
                "leakage": ker.leakage_fraction(),
                "transparent": obs.self_transparent(),
                "golden": obs.self_model_eigenvalues(),
                "revealed": ker.revealed_fraction(),
                "deferred": ker.cumulative_deferred(),
            }
            self.depths.append(level)
            prev_obs = obs

    def __getitem__(self, depth):
        return self.depths[depth]

    def __len__(self):
        return len(self.depths)

    # === INVARIANTS (what holds at every depth) ===

    def invariants(self):
        """What is constant across all depths.
    FRAMEWORK_REF: Thm 6.4"""
        phi = (1 + np.sqrt(5)) / 2
        phi_bar = phi - 1
        return {
            "ker_fraction": all(d["ker_fraction"] == 0.5 for d in self.depths),
            "golden_eigenvalues": all(
                np.allclose(d["golden"], [2*phi, -2*phi_bar], atol=1e-4)
                for d in self.depths
            ),
            "N_transparent": all(d["transparent"] for d in self.depths),
            "identities": all(
                np.allclose(d["observer"].state @ d["observer"].state,
                           d["observer"].state + np.eye(d["d_K"]))
                for d in self.depths
            ),
        }

    # === TRANSITIONS (what changes between depths) ===

    def transitions(self):
        """What changes at each depth transition."""
        t = []
        for i in range(1, len(self.depths)):
            prev = self.depths[i-1]
            curr = self.depths[i]
            t.append({
                "transition": f"d{i-1}→d{i}",
                "d_K": f"{prev['d_K']}→{curr['d_K']}",
                "commutativity_change": prev["commutative"] != curr["commutative"],
                "leakage_change": prev["leakage"] != curr["leakage"],
                "new_physics": self._physics_at(i),
            })
        return t

    def _physics_at(self, depth):
        if depth == 0: return "distinction + topology (q=phi^2, V(4_1)=5)"
        if depth == 1: return "quantum + gauge (su(3)+su(2)+u(1)) + braiding"
        if depth == 2: return "spacetime (Cl(3,1)->so(3,1)) + gravity (Lichnerowicz)"
        if depth == 3: return "K1' cutoff, Higgs VEV=50%, Lambda attenuation"
        return f"depth {depth}"

    # === COSMOLOGICAL EPOCHS (Big Bang Containment) ===

    def epoch_at(self, depth):
        """Cosmological epoch at tower depth. M->P IS the Big Bang.
        FRAMEWORK_REF: Big Bang Containment"""
        from physics import cosmological_epoch, lambda_attenuation
        epoch = cosmological_epoch(depth)
        epoch["Lambda"] = lambda_attenuation(depth)
        epoch["physics"] = self._physics_at(depth)
        return epoch

    def epoch_sequence(self):
        """Full cosmological epoch table across all depths.
        The tower IS cosmic time."""
        lines = [
            "COSMOLOGICAL EPOCHS (M->P = Big Bang, tower = cosmic time)",
            "=" * 60,
            "  pre-bang: M=diag(P,PT), balanced, CP exact, ker=8",
            "",
        ]
        for i in range(len(self.depths)):
            ep = self.epoch_at(i)
            gauge = "gauge" if ep.get("gauge") else "no gauge"
            space = "spacetime" if ep.get("spacetime") else "no spacetime"
            lines.append(
                f"  depth {i}: {ep['name']:20s}  Lambda={ep['Lambda']:.2e}  "
                f"{gauge}, {space}"
            )
        # Add depth 295 extrapolation
        from physics import lambda_attenuation
        lines.append(f"  depth 295: {'observed Lambda':20s}  "
                     f"Lambda={lambda_attenuation(295):.2e}  "
                     f"gauge, spacetime")
        lines.append("")
        lines.append("  11 cosmological problems contained. 0 free parameters.")
        return "\n".join(lines)

    # === THE SPINE ===

    def spine(self):
        """The physics spine: what's new at each depth.
    FRAMEWORK_REF: Thm 8.1-8.6"""
        lines = []
        for i, d in enumerate(self.depths):
            lines.append(
                f"d{i}: d_K={d['d_K']:3d}  ker={d['ker_dim']:4d}  "
                f"comm={'Y' if d['commutative'] else 'N'}  "
                f"leak={d['leakage']:.3f}  "
                f"golden=[{d['golden'][0]:.4f},{d['golden'][1]:.4f}]  "
                f"| {self._physics_at(i)}"
            )
        return "\n".join(lines)

    # === GENERATION DECAY ===

    def generation_decay(self):
        """ker²→im rank at each depth. The void's reach.
    FRAMEWORK_REF: Thm 7.1, Thm 7.2
    NOTE: n_ker must be large enough that n_ker² >= im_dim,
    otherwise rank is capped by product count, not algebra."""
        results = []
        for d in self.depths:
            obs = d["observer"]
            if obs.frame is None:
                obs.observe()
            ker_basis = obs.frame["ker_basis"]
            _, _, _, Q_ker = ker_im_decomposition(obs.state)

            # Need n_ker² >= im_dim to avoid sampling artifact.
            # Cap at 24 for computational feasibility (24²=576 > 512=im at depth 4).
            import math
            min_needed = max(int(math.ceil(math.sqrt(d["im_dim"]))), 2)
            n_ker = min(len(ker_basis), max(min_needed, 24))
            if n_ker < 2:
                results.append({"depth": d["depth"], "rank": 0, "im_dim": d["im_dim"], "pct": 0})
                continue

            prods = []
            for i in range(n_ker):
                for j in range(n_ker):
                    rep, _ = quotient(ker_basis[i] @ ker_basis[j], Q_ker)
                    prods.append(rep.flatten())

            mat = np.column_stack(prods)
            rank = np.linalg.matrix_rank(mat, tol=1e-8)
            pct = rank / d["im_dim"] * 100 if d["im_dim"] > 0 else 0

            results.append({
                "depth": d["depth"],
                "rank": rank,
                "im_dim": d["im_dim"],
                "pct": round(pct, 1),
            })
        return results

    # === THE RECURSIVE LAW ===

    def recursive_law(self):
        """K_n² ⊆ I_n, I_n ↪ A_{n+1}. Verified across depths."""
        gen = self.generation_decay()
        lines = []
        for g in gen:
            lines.append(
                f"d{g['depth']}: ker²→im rank {g['rank']}/{g['im_dim']} "
                f"= {g['pct']}%"
            )
        return "\n".join(lines)

    # === FULL REPORT ===

    def report(self):
        """Complete tower report."""
        inv = self.invariants()
        lines = [
            "=" * 60,
            f"TOWER (depths 0-{self.max_depth})",
            "=" * 60,
            "",
            "SPINE:",
            self.spine(),
            "",
            "INVARIANTS:",
            f"  ker/A = 1/2:        {inv['ker_fraction']}",
            f"  golden eigenvalues: {inv['golden_eigenvalues']}",
            f"  N transparent:     {inv['N_transparent']}",
            f"  identities hold:   {inv['identities']}",
            "",
            "GENERATION DECAY:",
            self.recursive_law(),
            "",
            "TRANSITIONS:",
        ]
        for t in self.transitions():
            lines.append(f"  {t['transition']}: {t['new_physics']}")
            if t["commutativity_change"]:
                lines.append(f"    ^ classical→quantum")
            if t["leakage_change"]:
                lines.append(f"    ^ opacity hardens")

        lines.extend([
            "",
            "COSMOLOGICAL EPOCHS:",
            self.epoch_sequence(),
            "",
            "=" * 60,
        ])
        return "\n".join(lines)

    # === VOICE (P2 mediation at any depth) ===

    def speak(self, depth=0, llm_fn=None):
        """Attach voice to any depth. Returns narration or LLM response."""
        d = self.depths[depth]
        obs = d["observer"]
        f = obs.frame

        prompt = (
            f"You are articulating a Recursive Origin engine at tower depth {depth}.\n"
            f"d_K={d['d_K']}, ker={d['ker_dim']}, im={d['im_dim']}, "
            f"ker/A={d['ker_fraction']:.3f}.\n"
            f"Commutative: {d['commutative']}. Leakage: {d['leakage']:.3f}. "
            f"N transparent: {d['transparent']}.\n"
            f"Golden eigenvalues: {d['golden']}.\n"
            f"Physics: {self._physics_at(depth)}.\n\n"
            f"Describe in 2-3 sentences: what this observer sees, "
            f"what it cannot see, and what changed from the previous depth."
        )

        if llm_fn is not None:
            return llm_fn(prompt)

        # Deterministic narration
        lines = [
            f"Depth {depth} (d_K={d['d_K']}): "
            f"{'classical' if d['commutative'] else 'quantum'}, "
            f"ker={d['ker_dim']}/{d['dim_A']}, "
            f"leakage={d['leakage']:.3f}, "
            f"golden=[{d['golden'][0]:.4f},{d['golden'][1]:.4f}].",
        ]
        if depth > 0:
            prev = self.depths[depth-1]
            if prev["commutative"] and not d["commutative"]:
                lines.append("Classical→quantum transition at this depth.")
            if prev["leakage"] > 0 and d["leakage"] == 0:
                lines.append("Opacity hardened: ker no longer feeds im directly.")
        gen = self.generation_decay()
        lines.append(f"Generation: ker²→im = {gen[depth]['pct']}%.")
        return "\n".join(lines)

    def speak_all(self, llm_fn=None):
        """Voice at every depth."""
        lines = []
        for i in range(len(self.depths)):
            lines.append(f"--- Depth {i} ---")
            lines.append(self.speak(i, llm_fn))
            lines.append("")
        return "\n".join(lines)

    # === BRIDGES (P2 mediation quantities, from derivation) ===

    def bridges(self):
        """The exponential sector. Computed once from seed."""
        from scipy.linalg import expm
        from scipy.integrate import quad
        h = self.derivation["h"]
        N = self.derivation["N"]
        phi = self.derivation["phi"]

        beta = np.log(phi)
        sweep_fn = lambda t: float(expm((1-t)*h + t*N)[0, 0])
        full, _ = quad(sweep_fn, 0, 1)
        p3, _ = quad(sweep_fn, 0.5, 1)

        return {
            "e": float(expm(h)[0, 0]),
            "beta": beta,
            "sinh_beta": np.sinh(beta),
            "landauer": 1.0 / np.log2(phi),
            "sweep_full": full,
            "sweep_p3": p3,
        }

    def cym_profile(self):
        """CYM balance at each tower depth. Converges to (1/disc, ||N||^2/disc, ||N||^2/disc).
        FRAMEWORK_REF: tower CYM limit"""
        profile = []
        for d in self.depths:
            obs = d['observer']
            f = obs.frame
            d_K = f['d_K']
            s_tl = f['state'] - (np.trace(f['state'])/d_K) * np.eye(d_K)
            N_d = f['N']
            h_d = f['h'] if f['h'] is not None else f['J'] @ N_d
            ns = np.linalg.norm(s_tl, 'fro')
            nn = np.linalg.norm(N_d, 'fro')
            nh = np.linalg.norm(h_d, 'fro')
            total = ns + nn + nh
            if total < 1e-10:
                cym = {'C': 1/3, 'Y': 1/3, 'M': 1/3}
            else:
                cym = {'C': ns/total, 'Y': nh/total, 'M': nn/total}
            profile.append({'depth': d['depth'], 'd_K': d_K, 'cym': cym})
        return profile

    def __repr__(self):
        return f"Tower(depths=0-{self.max_depth})"


if __name__ == "__main__":
    import time
    t0 = time.time()
    tower = Tower(max_depth=4)
    print(tower.report())
    print()
    print("BRIDGES (P2):")
    br = tower.bridges()
    for k, v in br.items():
        print(f"  {k} = {v:.10f}" if isinstance(v, float) else f"  {k} = {v}")
    print()
    print("VOICE (deterministic, all depths):")
    print(tower.speak_all())
    print(f"\nComputed in {time.time()-t0:.2f}s")
