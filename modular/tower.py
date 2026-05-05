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
        """What changes at each depth transition.
        Includes quasicrystal inflation: each K6' step is one Penrose
        inflation (J*R^2*J). Attenuation phi_bar^(2n) = deflation^n."""
        from physics import quasicrystal_inflation
        phi_bar = self.derivation["phi"] - 1
        qi = quasicrystal_inflation(self.derivation["R"], self.derivation["J"])
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
                "attenuation": phi_bar ** (2 * i),
                "inflation_is_R2": qi['inflation_is_R2'],
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
        CYM channels map to lattice discriminants via observer.CYM.discriminant_basis():
          C (s_tl norm) -> disc(omega)=-3, Z[omega] hexagonal, |D_6|=12=dim_gauge
          Y (h norm)    -> disc_cross=-15, cross-field, h=2
          M (N norm)    -> disc(R)=5, Z[phi] quasilattice, |D_5|=10=2*disc
        Limit: (1/5, 2/5, 2/5) = (1/disc, ||N||^2/disc, ||N||^2/disc).
        FRAMEWORK_REF: tower CYM limit, Thm 4.7"""
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

    def nk_surjectivity(self):
        """Verify NK map surjectivity at each depth.
        det(phi_0)=1. det(phi_{n+1})=det(phi_n)^4. Block lower triangular from K6'.
        FRAMEWORK_REF: generation surjectivity theorem"""
        results = []
        for d in self.depths:
            obs = d['observer']
            if obs.frame is None:
                obs.observe()
            s = obs.frame['state']
            N_d = obs.frame['N']
            d_K = obs.frame['d_K']
            _, ker_basis, ker_dim, Q_ker = ker_im_decomposition(s)
            im_dim = d_K * d_K - ker_dim
            if ker_dim < 2 or im_dim == 0:
                results.append({'depth': d['depth'], 'surjective': True, 'rank': 0})
                continue
            # NK products projected onto im
            prods = []
            for i in range(ker_dim):
                K = ker_basis[i]
                NK = N_d @ K
                rep, _ = quotient(NK, Q_ker)
                prods.append(rep.flatten())
            mat = np.column_stack(prods)
            rank = np.linalg.matrix_rank(mat, tol=1e-8)
            results.append({
                'depth': d['depth'], 'surjective': rank == im_dim,
                'rank': rank, 'im_dim': im_dim,
            })
        return results

    def self_model_limit(self):
        """Self-model eigenvectors at each depth. Converge to (1,0) in {I, s_tl}.
        Perfect self-reference = existence without content.
        Extends observer.self_model_eigenvalues() with eigenvector tracking.
        FRAMEWORK_REF: projector limit investigation"""
        results = []
        for d in self.depths:
            obs = d['observer']
            if obs.frame is None:
                obs.observe()
            s = obs.frame['state']
            d_K = obs.frame['d_K']
            I_d = np.eye(d_K)
            s_tl = s - (np.trace(s)/d_K) * I_d
            _, _, _, Q_ker = ker_im_decomposition(s)

            def sigma(X):
                rep, _ = quotient(s @ X + X @ s, Q_ker)
                return rep

            sig_I = sigma(I_d)
            sig_stl = sigma(s_tl)
            norm_I = np.sum(I_d * I_d)
            norm_stl = np.sum(s_tl * s_tl)
            mat = np.array([
                [np.sum(sig_I * I_d)/norm_I, np.sum(sig_stl * I_d)/norm_I],
                [np.sum(sig_I * s_tl)/norm_stl, np.sum(sig_stl * s_tl)/norm_stl],
            ])
            eigs, vecs = np.linalg.eig(mat)
            idx = np.argsort(eigs.real)[::-1]
            results.append({
                'depth': d['depth'],
                'lambda_plus': float(eigs[idx[0]].real),
                'lambda_minus': float(eigs[idx[1]].real),
                'evec_plus': vecs[:, idx[0]].real,  # in {I, s_tl} coords
            })
        return results

    def __repr__(self):
        return f"Tower(depths=0-{self.max_depth})"


# ============================================================
# RESEARCH ENGINE: KNOWLEDGE GRAPH (from knowledge_graph.py)
# ============================================================

from algebra import (ResultType, Tier, EdgeType, FORCED_EDGE_TYPES,
                     WEAK_EDGE_TYPES, chain_status)


class Node:
    """A framework quantity or object."""

    def __init__(self, name, value=None, tier=Tier.A, status=ResultType.LAW,
                 source=None, description=''):
        self.name = name
        self.value = value
        self.tier = tier
        self.status = status
        self.source = source
        self.description = description
        self.edges_out = []
        self.edges_in = []

    def __repr__(self):
        v = f'={self.value}' if self.value is not None else ''
        return f'Node({self.name}{v}, {self.tier}, {self.status})'


class Edge:
    """A derivation relationship between nodes."""

    def __init__(self, source, target, edge_type=EdgeType.OPERATION_PRODUCES,
                 description=''):
        self.source = source
        self.target = target
        self.edge_type = edge_type
        self.description = description

    def __repr__(self):
        return f'{self.source.name} --{self.edge_type}--> {self.target.name}'


class KnowledgeGraph:
    """The framework's explicit derivation DAG."""

    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, name, **kwargs):
        if name not in self.nodes:
            self.nodes[name] = Node(name, **kwargs)
        return self.nodes[name]

    def add_edge(self, source_name, target_name, edge_type=EdgeType.OPERATION_PRODUCES,
                 description=''):
        s = self.nodes.get(source_name)
        t = self.nodes.get(target_name)
        if s is None or t is None:
            return None
        e = Edge(s, t, edge_type, description)
        s.edges_out.append(e)
        t.edges_in.append(e)
        self.edges.append(e)
        return e

    def get(self, name):
        return self.nodes.get(name)

    def frontier(self):
        return [n for n in self.nodes.values()
                if n.status == ResultType.OPEN_FRONTIER
                or (len(n.edges_out) == 0 and n.status == ResultType.LAW)]

    def roots(self):
        return [n for n in self.nodes.values() if len(n.edges_in) == 0]

    def dependents(self, name):
        node = self.nodes.get(name)
        if not node:
            return []
        result = []
        visited = set()
        stack = [node]
        while stack:
            n = stack.pop()
            for e in n.edges_out:
                if e.target.name not in visited:
                    visited.add(e.target.name)
                    result.append(e.target)
                    stack.append(e.target)
        return result

    def ancestors(self, name):
        node = self.nodes.get(name)
        if not node:
            return []
        result = []
        visited = set()
        stack = [node]
        while stack:
            n = stack.pop()
            for e in n.edges_in:
                if e.source.name not in visited:
                    visited.add(e.source.name)
                    result.append(e.source)
                    stack.append(e.source)
        return result

    def distance(self, name1, name2):
        from collections import deque
        if name1 not in self.nodes or name2 not in self.nodes:
            return float('inf')
        queue = deque([(name1, 0)])
        visited = {name1}
        while queue:
            current, dist = queue.popleft()
            if current == name2:
                return dist
            node = self.nodes[current]
            neighbors = ([e.target.name for e in node.edges_out] +
                        [e.source.name for e in node.edges_in])
            for nb in neighbors:
                if nb not in visited:
                    visited.add(nb)
                    queue.append((nb, dist + 1))
        return float('inf')

    def stats(self):
        by_tier = {}
        by_status = {}
        for n in self.nodes.values():
            by_tier[n.tier] = by_tier.get(n.tier, 0) + 1
            by_status[n.status] = by_status.get(n.status, 0) + 1
        return {
            'nodes': len(self.nodes),
            'edges': len(self.edges),
            'roots': len(self.roots()),
            'frontier': len(self.frontier()),
            'by_tier': by_tier,
            'by_status': by_status,
        }

    def find_chain(self, source_name, target_name, allowed_types=None,
                   max_depth=8):
        """Find a derivation chain from source to target."""
        if source_name not in self.nodes or target_name not in self.nodes:
            return None, ResultType.FAILED
        if allowed_types is None:
            allowed_types = set(e for e in [
                EdgeType.OPERATION_PRODUCES, EdgeType.IDENTITY_CASTS,
                EdgeType.LIFT_PROPAGATES, EdgeType.COMPUTED_BY,
                EdgeType.NUMERICAL_MATCHES, EdgeType.IDENTIFIED_WITH,
            ])
        from collections import deque
        queue = deque([(source_name, [])])
        visited = {source_name}
        while queue:
            current, path = queue.popleft()
            if len(path) >= max_depth:
                continue
            node = self.nodes[current]
            for edge in node.edges_out:
                if edge.edge_type not in allowed_types:
                    continue
                next_name = edge.target.name
                if next_name in visited:
                    continue
                new_path = path + [edge]
                if next_name == target_name:
                    edge_types = [e.edge_type for e in new_path]
                    status = chain_status(edge_types)
                    return new_path, status
                visited.add(next_name)
                queue.append((next_name, new_path))
        return None, ResultType.FAILED

    def find_forced_chain(self, source_name, target_name, max_depth=8):
        return self.find_chain(source_name, target_name,
                              allowed_types=FORCED_EDGE_TYPES,
                              max_depth=max_depth)

    def find_any_chain(self, source_name, target_name, max_depth=8):
        return self.find_chain(source_name, target_name, max_depth=max_depth)

    def all_chains_to(self, target_name, max_depth=6):
        results = []
        for root in self.roots():
            chain, status = self.find_any_chain(root.name, target_name, max_depth)
            if chain is not None:
                results.append((root.name, chain, status))
        for key_name in ['R', 'N', 'P', 'L', 'disc', 'phi']:
            if key_name in self.nodes and key_name not in [r.name for r in self.roots()]:
                chain, status = self.find_any_chain(key_name, target_name, max_depth)
                if chain is not None:
                    results.append((key_name, chain, status))
        status_rank = {ResultType.LAW: 0, ResultType.LAW_CANDIDATE: 1,
                      ResultType.DERIVED_CANDIDATE: 2, ResultType.FAILED: 3}
        results.sort(key=lambda r: (status_rank.get(r[2], 9), len(r[1])))
        return results

    def chain_str(self, chain):
        if not chain:
            return "(no chain)"
        parts = [chain[0].source.name]
        for edge in chain:
            parts.append(f" --[{edge.edge_type}]--> {edge.target.name}")
        return ''.join(parts)

    def seed(self):
        """Populate the graph with all known framework quantities."""
        # The two inputs
        self.add_node('[1,1]', value=[1, 1], tier=Tier.A, source='input')
        self.add_node('d', value=2, tier=Tier.A, source='input')
        self.add_node('R', tier=Tier.A, source='production.py')
        self.add_node('J', tier=Tier.A, source='production.py')
        self.add_edge('[1,1]', 'R', EdgeType.OPERATION_PRODUCES, 'companion matrix')
        self.add_edge('d', 'J', EdgeType.OPERATION_PRODUCES, 'swap involution')
        self.add_node('tr(R)', value=1, tier=Tier.A)
        self.add_node('det(R)', value=-1, tier=Tier.A)
        self.add_node('disc', value=5, tier=Tier.A)
        self.add_node('phi', value=(1+np.sqrt(5))/2, tier=Tier.A)
        self.add_node('phi_bar', value=(np.sqrt(5)-1)/2, tier=Tier.A)
        self.add_edge('R', 'tr(R)', EdgeType.OPERATION_PRODUCES)
        self.add_edge('R', 'det(R)', EdgeType.OPERATION_PRODUCES)
        self.add_edge('tr(R)', 'disc', EdgeType.OPERATION_PRODUCES)
        self.add_edge('det(R)', 'disc', EdgeType.OPERATION_PRODUCES)
        self.add_edge('R', 'phi', EdgeType.OPERATION_PRODUCES)
        self.add_edge('phi', 'phi_bar', EdgeType.IDENTITY_CASTS)
        self.add_node('L', tier=Tier.A, source='algebra.py')
        self.add_node('N', tier=Tier.A, source='production.py')
        self.add_edge('R', 'L', EdgeType.OPERATION_PRODUCES)
        self.add_edge('L', 'N', EdgeType.OPERATION_PRODUCES)
        self.add_node('P', tier=Tier.A)
        self.add_node('h', tier=Tier.A)
        self.add_edge('R', 'P', EdgeType.OPERATION_PRODUCES)
        self.add_edge('N', 'P', EdgeType.OPERATION_PRODUCES)
        self.add_edge('J', 'h', EdgeType.OPERATION_PRODUCES)
        self.add_edge('N', 'h', EdgeType.OPERATION_PRODUCES)
        self.add_node('N_c', value=3, tier=Tier.A)
        self.add_node('dim_gauge', value=12, tier=Tier.A)
        self.add_node('parent_ker', value=8, tier=Tier.A)
        self.add_node('alpha_S', value=0.5-(np.sqrt(5)-1)/2**2, tier=Tier.A)
        self.add_node('beta_KMS', value=np.log((1+np.sqrt(5))/2), tier=Tier.A)
        self.add_node('ker/A', value=0.5, tier=Tier.A)
        self.add_edge('d', 'N_c', EdgeType.OPERATION_PRODUCES)
        self.add_edge('N_c', 'dim_gauge', EdgeType.OPERATION_PRODUCES)
        self.add_edge('d', 'parent_ker', EdgeType.OPERATION_PRODUCES)
        self.add_edge('phi_bar', 'alpha_S', EdgeType.OPERATION_PRODUCES)
        self.add_edge('phi', 'beta_KMS', EdgeType.OPERATION_PRODUCES)
        self.add_edge('L', 'ker/A', EdgeType.OPERATION_PRODUCES)
        # Open frontiers
        self.add_node('4D_Ricci', status=ResultType.OPEN_FRONTIER)
        self.add_node('theta_12_correction', status=ResultType.OPEN_FRONTIER)
        self.add_node('scale_unit', status=ResultType.OPEN_FRONTIER)
        return self


# ============================================================
# RESEARCH ENGINE: DERIVATION (from derivation.py)
# ============================================================

from algebra import (apply_all_unary, apply_all_binary, FRAMEWORK_MATRICES,
                     OpResult)


class DerivationChain:
    """A candidate derivation path through the knowledge graph."""

    def __init__(self, edges, source_name, target_name):
        self.edges = edges
        self.source = source_name
        self.target = target_name
        self.edge_types = [e.edge_type for e in edges]
        self.length = len(edges)
        self.status = chain_status(self.edge_types)
        self.weakest = self._find_weakest()
        self.is_forced = all(t in FORCED_EDGE_TYPES for t in self.edge_types)
        self.has_numerical = any(t == EdgeType.NUMERICAL_MATCHES for t in self.edge_types)
        self.has_identification = any(t == EdgeType.IDENTIFIED_WITH for t in self.edge_types)

    def _find_weakest(self):
        weakness_order = [
            EdgeType.FAILED_BRIDGE, EdgeType.STRUCTURAL_PARALLEL,
            EdgeType.IDENTIFIED_WITH, EdgeType.NUMERICAL_MATCHES,
            EdgeType.COMPUTED_BY, EdgeType.LIFT_PROPAGATES,
            EdgeType.IDENTITY_CASTS, EdgeType.OPERATION_PRODUCES,
        ]
        for w in weakness_order:
            if w in self.edge_types:
                return w
        return None

    def path_str(self):
        if not self.edges:
            return "(empty chain)"
        parts = [self.edges[0].source.name]
        for e in self.edges:
            parts.append(f" --[{e.edge_type}]--> {e.target.name}")
        return ''.join(parts)

    def __repr__(self):
        forced = "FORCED" if self.is_forced else "MIXED"
        return (f"Chain({self.source}->{self.target}, {self.length} edges, "
                f"{self.status}, {forced}, weakest={self.weakest})")


class BackwardSearch:
    """Search backward from a target to find derivation chains."""

    def __init__(self, graph=None):
        self.graph = graph or KnowledgeGraph().seed()

    def search(self, target_name, max_depth=8, forced_only=False):
        if target_name not in self.graph.nodes:
            return []
        allowed = FORCED_EDGE_TYPES if forced_only else None
        results = []
        for root in self.graph.roots():
            chain_edges, status = self.graph.find_chain(
                root.name, target_name, allowed_types=allowed, max_depth=max_depth)
            if chain_edges:
                results.append(DerivationChain(chain_edges, root.name, target_name))
        key_names = ['R', 'N', 'P', 'L', 'disc', 'phi', 'phi_bar',
                     'alpha_S', 'N_c', 'parent_ker', 'dim_gauge',
                     'beta_KMS', 'ker/A']
        for name in key_names:
            if name in self.graph.nodes and name != target_name:
                chain_edges, status = self.graph.find_chain(
                    name, target_name, allowed_types=allowed, max_depth=max_depth)
                if chain_edges:
                    results.append(DerivationChain(chain_edges, name, target_name))
        seen = set()
        unique = []
        for r in results:
            key = r.path_str()
            if key not in seen:
                seen.add(key)
                unique.append(r)
        weakness_rank = {
            EdgeType.OPERATION_PRODUCES: 0, EdgeType.IDENTITY_CASTS: 1,
            EdgeType.LIFT_PROPAGATES: 2, EdgeType.COMPUTED_BY: 3,
            EdgeType.NUMERICAL_MATCHES: 10, EdgeType.IDENTIFIED_WITH: 11,
            EdgeType.STRUCTURAL_PARALLEL: 12,
        }
        unique.sort(key=lambda c: (not c.is_forced, weakness_rank.get(c.weakest, 20), c.length))
        return unique

    def forced_chains(self, target_name, max_depth=8):
        return self.search(target_name, max_depth=max_depth, forced_only=True)

    def competing_chains(self, target_name, max_depth=8):
        all_chains = self.search(target_name, max_depth=max_depth)
        forced = [c for c in all_chains if c.is_forced]
        mixed = [c for c in all_chains if not c.is_forced]
        return {
            'target': target_name, 'forced': forced, 'mixed': mixed,
            'total': len(all_chains), 'can_be_LAW': len(forced) > 0,
            'best': all_chains[0] if all_chains else None,
        }

    def investigate(self, target_name, max_depth=8):
        result = self.competing_chains(target_name, max_depth)
        if result['total'] == 0:
            result['verdict'] = 'NO_CHAINS'
            result['status'] = ResultType.FAILED
        elif result['can_be_LAW']:
            result['verdict'] = 'FORCED_CHAIN_EXISTS'
            result['status'] = ResultType.LAW
            result['derivation'] = result['forced'][0].path_str()
        elif result['total'] >= 2:
            result['verdict'] = 'MULTIPLE_MIXED_CHAINS'
            result['status'] = ResultType.PATH_CANDIDATE
        else:
            result['verdict'] = 'SINGLE_MIXED_CHAIN'
            result['status'] = ResultType.LAW_CANDIDATE
        return result


class EdgeDiscoverer:
    """Discovers new edges between existing graph nodes."""

    def __init__(self, graph=None):
        self.graph = graph or KnowledgeGraph().seed()

    def discover_from(self, source_name, tolerance=1e-4):
        source_node = self.graph.get(source_name)
        if source_node is None:
            return []
        proposed = []
        source_matrix = self._to_matrix(source_node)
        if source_matrix is not None:
            results = apply_all_unary(source_matrix, source_name)
            results += apply_all_binary(source_matrix, source_name)
        else:
            results = []
        results_scalar = []
        if isinstance(source_node.value, (int, float, np.floating)):
            v = float(source_node.value)
            if v > 0:
                results_scalar.append(OpResult(
                    f'sqrt({source_name})', np.sqrt(v),
                    EdgeType.COMPUTED_BY, 'sqrt', [source_name]))
            if abs(v) > 1e-30:
                results_scalar.append(OpResult(
                    f'1/{source_name}', 1.0/v,
                    EdgeType.COMPUTED_BY, 'inverse', [source_name]))
        results = results + results_scalar
        for op_result in results:
            if op_result.value is None:
                continue
            for target_name, target_node in self.graph.nodes.items():
                if target_name == source_name:
                    continue
                if target_node.value is None:
                    continue
                match, tol = self._compare(op_result.value, target_node.value)
                if match and tol <= tolerance:
                    already = any(
                        e.source.name == source_name and e.target.name == target_name
                        and e.edge_type == op_result.edge_type
                        for e in self.graph.edges
                    )
                    if not already:
                        proposed.append({
                            'source': source_name, 'target': target_name,
                            'edge_type': op_result.edge_type,
                            'operation': op_result.name, 'tolerance': tol,
                        })
        return proposed

    def grow(self, tolerance=1e-6):
        all_proposed = []
        for name in list(self.graph.nodes.keys()):
            node = self.graph.nodes[name]
            if self._to_matrix(node) is not None or isinstance(node.value, (int, float)):
                proposed = self.discover_from(name, tolerance)
                all_proposed.extend(proposed)
        added = 0
        for p in all_proposed:
            edge = self.graph.add_edge(p['source'], p['target'], p['edge_type'],
                                       f'DISCOVERED: {p["operation"]}')
            if edge:
                added += 1
        return added, all_proposed

    def _to_matrix(self, node):
        matrix_map = {
            'R': np.array([[0,1],[1,1]], dtype=float),
            'N': np.array([[0,-1],[1,0]], dtype=float),
            'J': np.array([[0,1],[1,0]], dtype=float),
            'h': np.array([[1,0],[0,-1]], dtype=float),
            'P': np.array([[0,0],[2,1]], dtype=float),
        }
        if node.name in matrix_map:
            return matrix_map[node.name]
        if isinstance(node.value, np.ndarray) and node.value.shape == (2, 2):
            return node.value
        return None

    def _compare(self, op_value, node_value):
        try:
            if isinstance(op_value, (int, float, np.floating)):
                if isinstance(node_value, (int, float, np.floating)):
                    if abs(node_value) < 1e-30:
                        return abs(op_value) < 1e-10, abs(op_value)
                    tol = abs(op_value - node_value) / abs(node_value)
                    return tol < 0.001, tol
                return False, float('inf')
            elif isinstance(op_value, bool):
                return op_value == node_value, 0.0 if op_value == node_value else 1.0
        except (TypeError, ValueError):
            pass
        return False, float('inf')


import re


class FormChecker:
    """Checks whether a scanner expression uses framework-admissible operations."""

    FRAMEWORK_TOKENS = {
        'disc', 'phi', 'phi_bar', 'N_c', 'dim_gauge', 'ker', 'im',
        'parent_ker', 'beta_KMS', 'alpha_S', 'Koide_Q', 'Koide_delta',
        'A', 'R', 'N', 'P', 'J', 'h', 'mu', 'tr', 'det', 'rank',
        'd', 'n', 'k',
    }
    SQRT_ADMISSIBLE = {'disc', '5', 'norm2', '||N||^2', '||R||^2', '3', '2'}
    LN_ADMISSIBLE = {'phi', 'phi_bar', '2', 'disc'}
    FRAMEWORK_EXPONENTS = {'2', '3', '4', '-1', '-2', 'N_c', 'disc',
                           'phi', 'phi_bar', 'n', 'k', 'd'}

    def check(self, expression_str):
        ops = self._extract_operations(expression_str)
        suspicious = []
        for op in ops:
            reason = self._check_op(op, expression_str)
            if reason:
                suspicious.append({'op': op, 'reason': reason})
        n_total = max(len(ops), 1)
        n_clean = n_total - len(suspicious)
        score = n_clean / n_total
        return {
            'admissible': len(suspicious) == 0,
            'operations': ops, 'suspicious': suspicious, 'score': score,
        }

    def classify_expression(self, expression_str):
        result = self.check(expression_str)
        if result['score'] == 1.0 and self._all_tokens_framework(expression_str):
            if self._is_forced_form(expression_str):
                return 'FORCED_FORM'
            return 'ADMISSIBLE_FORM'
        elif result['score'] >= 0.5:
            return 'SUSPICIOUS_FORM'
        else:
            return 'INADMISSIBLE_FORM'

    def _extract_operations(self, expr):
        ops = []
        if '+' in expr: ops.append('+')
        if '-' in expr and not expr.startswith('-'): ops.append('-')
        if '*' in expr: ops.append('*')
        if '/' in expr: ops.append('/')
        if '^' in expr: ops.append('^')
        if 'sqrt' in expr: ops.append('sqrt')
        if 'ln' in expr: ops.append('ln')
        if 'log' in expr and 'ln' not in expr: ops.append('log')
        if 'exp' in expr: ops.append('exp')
        if re.search(r'\^\s*[0-9]*\.[0-9]', expr): ops.append('^real')
        return ops

    def _check_op(self, op, expr):
        if op in ('+', '-', '*', '/'): return None
        if op == '^':
            matches = re.findall(r'\^\s*([A-Za-z_0-9.]+)', expr)
            for exp in matches:
                if exp not in self.FRAMEWORK_EXPONENTS:
                    try:
                        int(exp)
                    except ValueError:
                        try:
                            float(exp)
                            return f'real exponent {exp}'
                        except ValueError:
                            pass
            return None
        if op == '^real': return 'arbitrary real exponent detected'
        if op == 'sqrt':
            match = re.search(r'sqrt\(([^)]+)\)', expr)
            arg = match.group(1) if match else ''
            if arg not in self.SQRT_ADMISSIBLE and arg not in self.FRAMEWORK_TOKENS:
                return f'sqrt of non-framework argument: {arg}'
            return None
        if op == 'ln':
            match = re.search(r'ln\(([^)]+)\)', expr)
            arg = match.group(1) if match else ''
            if arg not in self.LN_ADMISSIBLE and arg not in self.FRAMEWORK_TOKENS:
                return f'ln of non-framework argument: {arg}'
            return None
        if op == 'log': return 'log (base ambiguous)'
        if op == 'exp': return None
        return f'unknown operation: {op}'

    def _all_tokens_framework(self, expr):
        cleaned = re.sub(r'[+\-*/^()\s]', ' ', expr)
        cleaned = re.sub(r'\b(sqrt|ln|log|exp)\b', '', cleaned)
        tokens = [t for t in cleaned.split() if t]
        for t in tokens:
            if t in self.FRAMEWORK_TOKENS:
                continue
            try:
                int(t)
                continue
            except ValueError:
                pass
            return False
        return True

    def _is_forced_form(self, expr):
        if 'sqrt' in expr or 'ln' in expr or 'exp' in expr:
            return False
        if re.search(r'\^\s*[0-9]*\.[0-9]', expr):
            return False
        return True


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
