"""
tower.py — All depths simultaneously. The spine visible.

The engine computes one depth at a time. The Tower holds all depths
at once and lets you query across them: invariants, transitions,
generation decay, the physics spine, and the recursive law.

The Tower IS the framework's self-product tower S_{n+1} = S_n × S_n
made into an object you can ask questions of.
"""
import numpy as np
from algebra import sylvester, ker_im_decomposition, quotient
from scipy.linalg import null_space


class Tower:
    """All depths simultaneously."""

    def __init__(self, max_depth=4):
        from production import Production, _companion, _swap
        from observer import Observer
        from image import Image
        from kernel import Kernel

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
        """What is constant across all depths."""
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
        if depth == 0: return "distinction"
        if depth == 1: return "quantum + gauge (su(3)+su(2)+u(1))"
        if depth == 2: return "spacetime (Cl(3,1)→so(3,1))"
        if depth == 3: return "suppressed (K1' cutoff)"
        return f"depth {depth}"

    # === THE SPINE ===

    def spine(self):
        """The physics spine: what's new at each depth."""
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
        """ker²→im rank at each depth. The void's reach."""
        results = []
        for d in self.depths:
            obs = d["observer"]
            if obs.frame is None:
                obs.observe()
            ker_basis = obs.frame["ker_basis"]
            _, _, _, Q_ker = ker_im_decomposition(obs.state)

            n_ker = min(len(ker_basis), 8)
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

        lines.extend(["", "=" * 60])
        return "\n".join(lines)

    def __repr__(self):
        return f"Tower(depths=0-{self.max_depth})"


if __name__ == "__main__":
    import time
    t0 = time.time()
    tower = Tower(max_depth=4)
    print(tower.report())
    print(f"\nComputed in {time.time()-t0:.2f}s")
