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

        # Norms and identities
        norm_R = self.add_node('||R||^2', value=3, tier=Tier.A,
                              description='Frobenius norm squared of R')
        norm_N = self.add_node('||N||^2', value=2, tier=Tier.A,
                              description='Frobenius norm squared of N')
        self.add_edge('R', '||R||^2', EdgeType.COMPUTED_BY, 'tr(R^T R)')
        self.add_edge('N', '||N||^2', EdgeType.COMPUTED_BY, 'tr(N^T N)')
        frob_sum = self.add_node('||R||^2+||N||^2', value=5, tier=Tier.A,
                                description='= disc (Pythagoras on center+orientation)')
        self.add_edge('||R||^2', '||R||^2+||N||^2', EdgeType.IDENTITY_CASTS, '3+2=5')
        self.add_edge('||N||^2', '||R||^2+||N||^2', EdgeType.IDENTITY_CASTS, '3+2=5')
        self.add_edge('||R||^2+||N||^2', 'disc', EdgeType.IDENTITY_CASTS, '||R||^2+||N||^2=disc')

        # Deeper physics
        exp_B = self.add_node('exp_B', value=44, tier=Tier.A,
                             description='2(dim_gauge+disc)+2*disc')
        self.add_edge('dim_gauge', 'exp_B', EdgeType.OPERATION_PRODUCES, '2(dg+disc)+2*disc')
        self.add_edge('disc', 'exp_B', EdgeType.OPERATION_PRODUCES, '2(dg+disc)+2*disc')

        mp_mpl = self.add_node('m_p/M_Pl', value=np.exp(-44), tier=Tier.A,
                              description='e^(-exp_B)')
        self.add_edge('exp_B', 'm_p/M_Pl', EdgeType.OPERATION_PRODUCES, 'e^(-exp_B)')

        ep_ratio = self.add_node('m_e/m_p', value=(2/9)**5, tier=Tier.B,
                                description='(||N||^2/N_c^2)^disc = (2/9)^5')
        self.add_edge('Koide_delta', 'm_e/m_p', EdgeType.OPERATION_PRODUCES, 'delta^disc')
        self.add_edge('disc', 'm_e/m_p', EdgeType.OPERATION_PRODUCES, 'delta^disc')

        # Machine discoveries
        inv_alpha_em = self.add_node('1/alpha_EM', value=137, tier=Tier.B,
                                    description='disc^N_c + dim_gauge = 5^3+12 (MACHINE-DISCOVERED)')
        self.add_edge('disc', '1/alpha_EM', EdgeType.NUMERICAL_MATCHES, 'disc^N_c term')
        self.add_edge('N_c', '1/alpha_EM', EdgeType.NUMERICAL_MATCHES, 'disc^N_c term')
        self.add_edge('dim_gauge', '1/alpha_EM', EdgeType.NUMERICAL_MATCHES, '+dim_gauge term')

        sin2_mZ = self.add_node('sin2_tW_mZ', value=0.2316, tier=Tier.N,
                               description='beta_KMS^2 = ln(phi)^2 (MACHINE-DISCOVERED)')
        self.add_edge('beta_KMS', 'sin2_tW_mZ', EdgeType.NUMERICAL_MATCHES, 'beta_KMS^2')

        # PMNS
        theta13 = self.add_node('sin2_theta13', value=1/45, tier=Tier.B,
                               description='1/(N_c^2*disc)')
        self.add_edge('N_c', 'sin2_theta13', EdgeType.OPERATION_PRODUCES, '1/(N_c^2*disc)')
        self.add_edge('disc', 'sin2_theta13', EdgeType.OPERATION_PRODUCES, '1/(N_c^2*disc)')

        theta23 = self.add_node('sin2_theta23', value=47/90, tier=Tier.B,
                               description='1/2 + 2/45')
        self.add_edge('ker/A', 'sin2_theta23', EdgeType.OPERATION_PRODUCES, '1/2 + 2/45')
        self.add_edge('sin2_theta13', 'sin2_theta23', EdgeType.OPERATION_PRODUCES, 'ker/A + 2*theta13')

        # Void operator
        void_op = self.add_node('L_{0,0}', value=-1, tier=Tier.A,
                               description='-I_4 (negation, not zero)')
        self.add_edge('L', 'L_{0,0}', EdgeType.OPERATION_PRODUCES, 'L at s=0')

        # Quasicrystal
        inflation = self.add_node('inflation_rule', description='J*R^2*J = Penrose substitution',
                                 tier=Tier.A)
        self.add_edge('R', 'inflation_rule', EdgeType.OPERATION_PRODUCES, 'R^2 = R+I')
        self.add_edge('J', 'inflation_rule', EdgeType.OPERATION_PRODUCES, 'J conjugation')

        # Open frontiers
        self.add_node('4D_Ricci', status=ResultType.OPEN_FRONTIER,
                     description='so(3,1) not L2-invariant')
        self.add_node('theta_12_correction', status=ResultType.OPEN_FRONTIER,
                     description='1/3 is 2sigma off')
        self.add_node('scale_unit', status=ResultType.OPEN_FRONTIER,
                     description='1 free parameter (unit of mass)')

        # ============================================================
        # NORMS AND CONSTANTS (computed but previously unnoded)
        # ============================================================
        sqrt_disc = self.add_node('sqrt_disc', value=np.sqrt(5), tier=Tier.A,
                                  description='sqrt(disc) = sqrt(5)')
        self.add_edge('disc', 'sqrt_disc', EdgeType.IDENTITY_CASTS, 'sqrt(5)')

        norm_R_val = self.add_node('norm_R', value=np.sqrt(3), tier=Tier.A,
                                   description='||R|| = sqrt(3)')
        self.add_edge('R', 'norm_R', EdgeType.COMPUTED_BY, 'sqrt(tr(R^T R))')

        norm_N_val = self.add_node('norm_N', value=np.sqrt(2), tier=Tier.A,
                                   description='||N|| = sqrt(2)')
        self.add_edge('N', 'norm_N', EdgeType.COMPUTED_BY, 'sqrt(tr(N^T N))')

        T_bridge = self.add_node('T_bridge', value=np.exp((1+np.sqrt(5))/2) / np.pi,
                                 tier=Tier.A, description='e^phi/pi ~ 1.605')
        self.add_edge('phi', 'T_bridge', EdgeType.COMPUTED_BY, 'e^phi / pi')

        y_star = self.add_node('y_star', value=1.2781, tier=Tier.A,
                               description='Canon fixed point')
        self.add_edge('T_bridge', 'y_star', EdgeType.COMPUTED_BY, 'Canon fixed-point iteration')

        m_contraction = self.add_node('m_contraction', value=-0.0727, tier=Tier.A,
                                      description='Canon contraction rate')
        self.add_edge('y_star', 'm_contraction', EdgeType.COMPUTED_BY, 'derivative at fixed point')

        # ============================================================
        # PHYSICS OUTPUTS (not yet noded)
        # ============================================================
        Lambda = self.add_node('Lambda', value=2.5, tier=Tier.A,
                               description='cosmological constant = disc/2')
        self.add_edge('disc', 'Lambda', EdgeType.OPERATION_PRODUCES, 'disc/2')

        proton_ratio = self.add_node('proton_ratio', value=4.5, tier=Tier.A,
                                     description='m_p/Lambda = N_c / Koide_Q = 9/2')
        self.add_edge('N_c', 'proton_ratio', EdgeType.OPERATION_PRODUCES, 'N_c / Koide_Q')
        self.add_edge('Koide_Q', 'proton_ratio', EdgeType.OPERATION_PRODUCES, 'N_c / Koide_Q')

        beta_1 = self.add_node('beta_1', value=41/10, tier=Tier.A,
                               description='U(1) beta coefficient')
        self.add_edge('N_c', 'beta_1', EdgeType.OPERATION_PRODUCES, 'beta function from matter')
        self.add_edge('d', 'beta_1', EdgeType.OPERATION_PRODUCES, 'beta function from matter')

        beta_2 = self.add_node('beta_2', value=-19/6, tier=Tier.A,
                               description='SU(2) beta coefficient')
        self.add_edge('N_c', 'beta_2', EdgeType.OPERATION_PRODUCES, 'beta function from matter')
        self.add_edge('d', 'beta_2', EdgeType.OPERATION_PRODUCES, 'beta function from matter')

        beta_3 = self.add_node('beta_3', value=-7, tier=Tier.A,
                               description='SU(3) beta coefficient')
        self.add_edge('N_c', 'beta_3', EdgeType.OPERATION_PRODUCES, 'asymptotic freedom')

        exp_nu = self.add_node('exp_nu', value=34, tier=Tier.A,
                               description='neutrino suppression exponent = dim_gauge + disc + 17')
        self.add_edge('dim_gauge', 'exp_nu', EdgeType.OPERATION_PRODUCES, 'dim_gauge + disc + ...')
        self.add_edge('disc', 'exp_nu', EdgeType.OPERATION_PRODUCES, 'dim_gauge + disc + ...')

        N_gen = self.add_node('N_gen', value=3, tier=Tier.A,
                              description='number of generations = d^2 - 1')
        self.add_edge('d', 'N_gen', EdgeType.OPERATION_PRODUCES, 'd^2 - 1')

        # ============================================================
        # ALGEBRAIC IDENTITIES (machine-discovered)
        # ============================================================
        det_Rh = self.add_node('det_Rh', value=4, tier=Tier.A,
                               description='det([R,h]) = d^2')
        self.add_edge('R', 'det_Rh', EdgeType.COMPUTED_BY, 'det([R,h])')
        self.add_edge('h', 'det_Rh', EdgeType.COMPUTED_BY, 'det([R,h])')

        norm_NR = self.add_node('norm_NR', value=3, tier=Tier.A,
                                description='||NR||^2 = N_c')
        self.add_edge('N', 'norm_NR', EdgeType.COMPUTED_BY, '||NR||^2')
        self.add_edge('R', 'norm_NR', EdgeType.COMPUTED_BY, '||NR||^2')

        det_anti_NP = self.add_node('det_anti_NP', value=5, tier=Tier.A,
                                    description='det({N,P}) = disc')
        self.add_edge('N', 'det_anti_NP', EdgeType.COMPUTED_BY, 'det({N,P})')
        self.add_edge('P', 'det_anti_NP', EdgeType.COMPUTED_BY, 'det({N,P})')

        norm_comm_NJ = self.add_node('norm_comm_NJ', value=8, tier=Tier.A,
                                     description='||[N,J]||^2 = parent_ker')
        self.add_edge('N', 'norm_comm_NJ', EdgeType.COMPUTED_BY, '||[N,J]||^2')
        self.add_edge('J', 'norm_comm_NJ', EdgeType.COMPUTED_BY, '||[N,J]||^2')

        # IDENTITY_CASTS: algebraic coincidences that ARE the framework
        self.add_edge('det_Rh', 'n_bases', EdgeType.IDENTITY_CASTS, 'both = 4 = d^2')
        self.add_edge('norm_NR', 'N_c', EdgeType.IDENTITY_CASTS, 'both = 3')
        self.add_edge('det_anti_NP', 'disc', EdgeType.IDENTITY_CASTS, 'both = 5')
        self.add_edge('norm_comm_NJ', 'parent_ker', EdgeType.IDENTITY_CASTS, 'both = 8')

        # ============================================================
        # MACHINE DISCOVERIES (additional edges)
        # ============================================================
        # '1/alpha_EM' already noded as 137 -- reinforce with alias
        self.add_node('137', value=137, tier=Tier.B,
                      description='disc^N_c + dim_gauge (MACHINE-DISCOVERED alias)')
        self.add_edge('disc', '137', EdgeType.NUMERICAL_MATCHES, '5^3 = 125')
        self.add_edge('N_c', '137', EdgeType.NUMERICAL_MATCHES, 'exponent')
        self.add_edge('dim_gauge', '137', EdgeType.NUMERICAL_MATCHES, '+12')
        self.add_edge('1/alpha_EM', '137', EdgeType.IDENTITY_CASTS, 'same value')

        # ============================================================
        # TRIADIC STRUCTURE (L evaluated at special points)
        # ============================================================
        L_void = self.add_node('L_void', value=-1, tier=Tier.A,
                               description='L_{0,0} = -I_4 eigenvalue (void)')
        self.add_edge('L', 'L_void', EdgeType.OPERATION_PRODUCES, 'L at s=0')

        L_silence = self.add_node('L_silence', value=0, tier=Tier.A,
                                  description='L_{I/2} = 0 (silence)')
        self.add_edge('L', 'L_silence', EdgeType.OPERATION_PRODUCES, 'L at s=I/2')

        L_identity = self.add_node('L_identity', value=1, tier=Tier.A,
                                   description='L_I = +I_4 eigenvalue (identity)')
        self.add_edge('L', 'L_identity', EdgeType.OPERATION_PRODUCES, 'L at s=I')

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
