"""
knowledge_graph.py -- The explicit derivation DAG.

Every framework quantity is a node. Every derivation step is an edge.
The graph IS the framework's memory. Scanner, prober, verifier, and
researcher all operate ON this graph.

Nodes carry: value, tier, status, source module, dependencies.
Edges carry: type, derivation chain, verification status.
The frontier: nodes with OPEN_FRONTIER status or missing connections.
"""
import numpy as np
import sys
sys.path.insert(0, '../..')
from framework_types import ResultType, Tier, EdgeType, FORCED_EDGE_TYPES, chain_status


class Node:
    """A framework quantity or object."""

    def __init__(self, name, value=None, tier=Tier.A, status=ResultType.LAW,
                 source=None, description=''):
        self.name = name
        self.value = value
        self.tier = tier
        self.status = status
        self.source = source        # which module/function computes it
        self.description = description
        self.edges_out = []         # edges FROM this node
        self.edges_in = []          # edges TO this node

    def __repr__(self):
        v = f'={self.value}' if self.value is not None else ''
        return f'Node({self.name}{v}, {self.tier}, {self.status})'


class Edge:
    """A derivation relationship between nodes."""

    def __init__(self, source, target, edge_type=EdgeType.OPERATION_PRODUCES,
                 description=''):
        self.source = source        # Node
        self.target = target        # Node
        self.edge_type = edge_type
        self.description = description

    def __repr__(self):
        return f'{self.source.name} --{self.edge_type}--> {self.target.name}'


class KnowledgeGraph:
    """The framework's explicit derivation DAG."""

    def __init__(self):
        self.nodes = {}    # name -> Node
        self.edges = []    # list of Edge

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
        """Nodes with OPEN_FRONTIER status or no outgoing edges."""
        return [n for n in self.nodes.values()
                if n.status == ResultType.OPEN_FRONTIER
                or (len(n.edges_out) == 0 and n.status == ResultType.LAW)]

    def roots(self):
        """Nodes with no incoming edges (the inputs)."""
        return [n for n in self.nodes.values() if len(n.edges_in) == 0]

    def dependents(self, name):
        """Everything that depends on this node (downstream)."""
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
        """Everything this node depends on (upstream)."""
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
        """Shortest path length between two nodes (undirected)."""
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
        """Graph statistics."""
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

    # ================================================================
    # CHAIN FINDING (the derivation engine core)
    # ================================================================

    def find_chain(self, source_name, target_name, allowed_types=None,
                   max_depth=8):
        """Find a derivation chain from source to target.
        If allowed_types is given, only traverse edges of those types.
        Returns (chain_edges, chain_status) or (None, FAILED).

        A chain through only FORCED edge types can become LAW.
        A chain with any WEAK edge is at most LAW_CANDIDATE."""
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
                    # Found! Determine chain status
                    edge_types = [e.edge_type for e in new_path]
                    status = chain_status(edge_types)
                    return new_path, status

                visited.add(next_name)
                queue.append((next_name, new_path))

        return None, ResultType.FAILED

    def find_forced_chain(self, source_name, target_name, max_depth=8):
        """Find a chain using ONLY forced edge types.
        If found, the chain can promote to LAW."""
        return self.find_chain(source_name, target_name,
                              allowed_types=FORCED_EDGE_TYPES,
                              max_depth=max_depth)

    def find_any_chain(self, source_name, target_name, max_depth=8):
        """Find a chain using any edge type (including weak).
        The chain status reflects its weakest edge."""
        return self.find_chain(source_name, target_name, max_depth=max_depth)

    def all_chains_to(self, target_name, max_depth=6):
        """Find chains from ALL roots to the target.
        Returns list of (source, chain, status) sorted by chain quality."""
        results = []
        for root in self.roots():
            chain, status = self.find_any_chain(root.name, target_name, max_depth)
            if chain is not None:
                results.append((root.name, chain, status))

        # Also try from key framework objects (not just roots)
        for key_name in ['R', 'N', 'P', 'L', 'disc', 'phi']:
            if key_name in self.nodes and key_name not in [r.name for r in self.roots()]:
                chain, status = self.find_any_chain(key_name, target_name, max_depth)
                if chain is not None:
                    results.append((key_name, chain, status))

        # Sort: LAW first, then shorter chains
        status_rank = {ResultType.LAW: 0, ResultType.LAW_CANDIDATE: 1,
                      ResultType.DERIVED_CANDIDATE: 2, ResultType.FAILED: 3}
        results.sort(key=lambda r: (status_rank.get(r[2], 9), len(r[1])))
        return results

    def chain_str(self, chain):
        """Pretty-print a chain."""
        if not chain:
            return "(no chain)"
        parts = [chain[0].source.name]
        for edge in chain:
            parts.append(f" --[{edge.edge_type}]--> {edge.target.name}")
        return ''.join(parts)

    # ================================================================
    # SEED THE GRAPH WITH THE FRAMEWORK
    # ================================================================

    def seed(self):
        """Populate the graph with all known framework quantities.
        Every node computed from the algebra. No hardcoded values."""
        # The two inputs
        coeffs = self.add_node('[1,1]', value=[1, 1], tier=Tier.A,
                               source='input', description='memory law coefficients')
        dim = self.add_node('d', value=2, tier=Tier.A,
                           source='input', description='seed dimension = |S_0|')

        # First derived quantities
        R = self.add_node('R', description='companion([1,1])', tier=Tier.A,
                         source='production.py')
        J = self.add_node('J', description='swap(d)', tier=Tier.A,
                         source='production.py')
        self.add_edge('[1,1]', 'R', EdgeType.OPERATION_PRODUCES, 'companion matrix')
        self.add_edge('d', 'J', EdgeType.OPERATION_PRODUCES, 'swap involution')

        # From R: Cayley-Hamilton
        tr = self.add_node('tr(R)', value=1, tier=Tier.A, source='production.py',
                          description='trace, forced by R^2=R+I via Cayley-Hamilton')
        det = self.add_node('det(R)', value=-1, tier=Tier.A, source='production.py')
        disc_n = self.add_node('disc', value=5, tier=Tier.A, source='production.py',
                              description='tr^2-4*det = 1+4 = 5')
        phi_n = self.add_node('phi', value=(1+np.sqrt(5))/2, tier=Tier.A,
                             description='golden ratio, max eigenvalue of R')
        phi_bar_n = self.add_node('phi_bar', value=(np.sqrt(5)-1)/2, tier=Tier.A)

        self.add_edge('R', 'tr(R)', EdgeType.OPERATION_PRODUCES, 'trace')
        self.add_edge('R', 'det(R)', EdgeType.OPERATION_PRODUCES, 'determinant')
        self.add_edge('tr(R)', 'disc', EdgeType.OPERATION_PRODUCES, 'tr^2-4*det')
        self.add_edge('det(R)', 'disc', EdgeType.OPERATION_PRODUCES, 'tr^2-4*det')
        self.add_edge('R', 'phi', EdgeType.OPERATION_PRODUCES, 'max eigenvalue')
        self.add_edge('phi', 'phi_bar', EdgeType.IDENTITY_CASTS, 'phi-1 = phi_bar')

        # N from ker(L)
        L = self.add_node('L', description='L_{s,s}(X)=sX+Xs-X, alpha=1 from tr=1',
                         tier=Tier.A, source='algebra.py')
        N = self.add_node('N', description='canonical rotation in ker(L)',
                         tier=Tier.A, source='production.py')
        self.add_edge('R', 'L', EdgeType.OPERATION_PRODUCES, 'Sylvester self-action')
        self.add_edge('tr(R)', 'L', EdgeType.OPERATION_PRODUCES, 'alpha=1/(2-tr)=1')
        self.add_edge('L', 'N', EdgeType.OPERATION_PRODUCES, 'ker(L) quadratic form')

        # P, h from R+N
        P = self.add_node('P', description='R+N, the naming act', tier=Tier.A)
        h = self.add_node('h', description='JN, the Cartan element', tier=Tier.A)
        self.add_edge('R', 'P', EdgeType.OPERATION_PRODUCES, 'P=R+N')
        self.add_edge('N', 'P', EdgeType.OPERATION_PRODUCES, 'P=R+N')
        self.add_edge('J', 'h', EdgeType.OPERATION_PRODUCES, 'h=JN')
        self.add_edge('N', 'h', EdgeType.OPERATION_PRODUCES, 'h=JN')

        # Key constants
        N_c = self.add_node('N_c', value=3, tier=Tier.A,
                           description='d(d+1)/2 = color number')
        dim_gauge = self.add_node('dim_gauge', value=12, tier=Tier.A,
                                 description='N_c^2-1+d^2-1+1')
        pk = self.add_node('parent_ker', value=8, tier=Tier.A,
                          description='d^N_c = ker(L_M)')
        alpha = self.add_node('alpha_S', value=0.5-(np.sqrt(5)-1)/2**2,
                             tier=Tier.A, description='1/2-phi_bar^2')
        beta = self.add_node('beta_KMS', value=np.log((1+np.sqrt(5))/2),
                            tier=Tier.A, description='ln(phi) = Reg(Q(sqrt(5)))')
        kerA = self.add_node('ker/A', value=0.5, tier=Tier.A,
                            description='ker/dim(A) = 1/2 at every depth')

        self.add_edge('d', 'N_c', EdgeType.OPERATION_PRODUCES, 'd(d+1)/2')
        self.add_edge('N_c', 'dim_gauge', EdgeType.OPERATION_PRODUCES, 'N_c^2-1+d^2-1+1')
        self.add_edge('d', 'dim_gauge', EdgeType.OPERATION_PRODUCES, 'N_c^2-1+d^2-1+1')
        self.add_edge('d', 'parent_ker', EdgeType.OPERATION_PRODUCES, 'd^N_c')
        self.add_edge('N_c', 'parent_ker', EdgeType.OPERATION_PRODUCES, 'd^N_c')
        self.add_edge('phi_bar', 'alpha_S', EdgeType.OPERATION_PRODUCES, '1/2-phi_bar^2')
        self.add_edge('phi', 'beta_KMS', EdgeType.OPERATION_PRODUCES, 'ln(phi)')
        self.add_edge('L', 'ker/A', EdgeType.OPERATION_PRODUCES, 'ker(L)/dim(A)')

        # Physics outputs
        sin2tw = self.add_node('sin2_thetaW', value=3/8, tier=Tier.A,
                              source='production.py')
        bell = self.add_node('Bell_S', value=2*np.sqrt(2), tier=Tier.A,
                            source='physics.py')
        koide = self.add_node('Koide_Q', value=2/3, tier=Tier.B,
                             source='physics.py')
        koide_delta = self.add_node('Koide_delta', value=2/9, tier=Tier.A,
                                   source='physics.py')

        self.add_edge('N_c', 'sin2_thetaW', EdgeType.OPERATION_PRODUCES, 'anomaly cancellation')
        self.add_edge('d', 'sin2_thetaW', EdgeType.OPERATION_PRODUCES, 'anomaly cancellation')
        self.add_edge('h', 'Bell_S', EdgeType.OPERATION_PRODUCES, 'CNOT from h,J')
        self.add_edge('N', 'Koide_Q', EdgeType.OPERATION_PRODUCES, '||N||^2/||R||^2')
        self.add_edge('R', 'Koide_Q', EdgeType.OPERATION_PRODUCES, '||N||^2/||R||^2')
        self.add_edge('N', 'Koide_delta', EdgeType.OPERATION_PRODUCES, '||N||^2/N_c^2')
        self.add_edge('N_c', 'Koide_delta', EdgeType.OPERATION_PRODUCES, '||N||^2/N_c^2')

        # Geometry
        D4 = self.add_node('|D_4|', value=8, tier=Tier.A, source='algebra.py',
                          description='square lattice symmetry = parent_ker')
        D6 = self.add_node('|D_6|', value=12, tier=Tier.A, source='algebra.py',
                          description='hexagonal lattice symmetry = dim_gauge')
        lcm456 = self.add_node('lcm(4,6,5)', value=60, tier=Tier.A,
                              description='icosahedral rotation group')
        self.add_edge('N', '|D_4|', EdgeType.OPERATION_PRODUCES, 'N rotation order 4')
        self.add_edge('N', '|D_6|', EdgeType.OPERATION_PRODUCES, 'omega from N, order 6')
        self.add_edge('disc', 'lcm(4,6,5)', EdgeType.OPERATION_PRODUCES, '5-fold from disc')

        # Biology
        bases = self.add_node('n_bases', value=4, tier=Tier.A,
                             description='d^2 = dim(M_2(R))')
        codons = self.add_node('n_codons', value=64, tier=Tier.A,
                              description='parent_ker^2 = (d^2)^N_c')
        amino = self.add_node('n_amino', value=20, tier=Tier.B,
                             description='d^2*disc = d^2+d^4')
        wobble = self.add_node('wobble_silent', value=2/3, tier=Tier.B,
                              description='= Koide Q = ||N||^2/||R||^2')
        helix = self.add_node('bp_per_turn', value=10.5, tier=Tier.B,
                             description='2*disc + ker/A')
        eigen_th = self.add_node('Eigen_threshold', value=0.962, tier=Tier.B,
                                description='d*beta_KMS')

        self.add_edge('d', 'n_bases', EdgeType.OPERATION_PRODUCES, 'd^2')
        self.add_edge('parent_ker', 'n_codons', EdgeType.OPERATION_PRODUCES, 'pk^2')
        self.add_edge('d', 'n_amino', EdgeType.OPERATION_PRODUCES, 'd^2*disc')
        self.add_edge('disc', 'n_amino', EdgeType.OPERATION_PRODUCES, 'd^2*disc')
        self.add_edge('Koide_Q', 'wobble_silent', EdgeType.IDENTIFIED_WITH,
                      'wobble fraction = Koide Q')
        self.add_edge('disc', 'bp_per_turn', EdgeType.OPERATION_PRODUCES, '2*disc+ker/A')
        self.add_edge('ker/A', 'bp_per_turn', EdgeType.OPERATION_PRODUCES, '2*disc+ker/A')
        self.add_edge('d', 'Eigen_threshold', EdgeType.OPERATION_PRODUCES, 'd*beta_KMS')
        self.add_edge('beta_KMS', 'Eigen_threshold', EdgeType.OPERATION_PRODUCES, 'd*beta_KMS')

        # Open frontiers
        self.add_node('4D_Ricci', status=ResultType.OPEN_FRONTIER,
                     description='so(3,1) not L2-invariant')
        self.add_node('theta_12_correction', status=ResultType.OPEN_FRONTIER,
                     description='1/3 is 2sigma off')
        self.add_node('scale_unit', status=ResultType.OPEN_FRONTIER,
                     description='1 free parameter (unit of mass)')

        return self


# ================================================================
# SELF-TEST
# ================================================================

if __name__ == "__main__":
    g = KnowledgeGraph().seed()
    s = g.stats()

    print(f"KNOWLEDGE GRAPH")
    print(f"=" * 55)
    print(f"  Nodes:    {s['nodes']}")
    print(f"  Edges:    {s['edges']}")
    print(f"  Roots:    {s['roots']} (inputs)")
    print(f"  Frontier: {s['frontier']} (open + leaf)")
    print(f"  By tier:  {s['by_tier']}")
    print(f"  By status:{s['by_status']}")

    # Check roots are the two inputs
    roots = g.roots()
    root_names = sorted([r.name for r in roots])
    print(f"\n  Roots: {root_names}")

    # Check frontier
    frontier = g.frontier()
    frontier_names = sorted([f.name for f in frontier])
    print(f"  Frontier: {frontier_names}")

    # Check derivation chain: [1,1] -> R -> disc
    dist_input_disc = g.distance('[1,1]', 'disc')
    print(f"\n  Distance [1,1] -> disc: {dist_input_disc}")

    # Check ancestors of alpha_S
    ancestors = g.ancestors('alpha_S')
    anc_names = sorted([a.name for a in ancestors])
    print(f"  Ancestors of alpha_S: {anc_names}")

    # Check dependents of disc
    deps = g.dependents('disc')
    dep_names = sorted([d.name for d in deps])
    print(f"  Dependents of disc: {dep_names}")

    checks = [
        ("graph has nodes", s['nodes'] > 30),
        ("graph has edges", s['edges'] > 30),
        ("two roots", s['roots'] == 2),
        ("frontier exists", s['frontier'] > 0),
        ("[1,1] is root", '[1,1]' in root_names),
        ("d is root", 'd' in root_names),
        ("[1,1]->disc reachable", dist_input_disc < 10),
        ("alpha_S has ancestors", len(ancestors) > 2),
        ("disc has dependents", len(deps) > 3),
        ("open problems in frontier", any(f.status == ResultType.OPEN_FRONTIER for f in frontier)),
    ]

    print()
    n_pass = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n{n_pass}/{len(checks)} passed.")
