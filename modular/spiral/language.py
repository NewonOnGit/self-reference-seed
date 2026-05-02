"""
language.py — Natural language from the framework. No LLM.

The framework IS the model:
  Glyphs = tokens (9 primitives, composition grammar)
  Quotient = attention (P3, what survives observation)
  Mediation = MLP (P2, nonlinear bridge)
  Surplus = residual (P1, x + f(x) = R²=R+I)
  Tower = depth (K6', recursive processing)

One block = O∘B∘S = quotient ∘ bridge ∘ surplus.
Each block IS a central collapse on the input.

Input: word → glyph → matrix
Process: O∘B∘S iterated
Output: matrix → nearest glyph → word

The dictionary maps words to framework coordinates.
The engine maps coordinates to meaning through the algebra.
Meaning emerges from recursive self-application. Not training.
"""
import numpy as np
import sys
sys.path.insert(0, '..')
from algebra import sylvester, ker_im_decomposition, quotient
from scipy.linalg import expm


# === SEED (the model's weights ARE these matrices) ===
R = np.array([[0, 1], [1, 1]], dtype=float)
N = np.array([[0, -1], [1, 0]], dtype=float)
J = np.array([[0, 1], [1, 0]], dtype=float)
h = J @ N
I2 = np.eye(2)
R_tl = R - 0.5 * I2
phi = (1 + np.sqrt(5)) / 2
phi_bar = phi - 1

# Basis for M_2(R): {I, R_tl, N, h}
_basis = [I2, R_tl, N, h]
_basis_names = ['I', 'R_tl', 'N', 'h']
_B = np.column_stack([m.flatten() for m in _basis])


def decompose(M):
    """Matrix → (a, b, c, d) in {I, R_tl, N, h} basis."""
    return np.linalg.solve(_B, M.flatten())


def recompose(coeffs):
    """(a, b, c, d) → matrix."""
    return sum(c * m for c, m in zip(coeffs, _basis))


# ================================================================
# DICTIONARY: words → framework coordinates
# ================================================================

class Dictionary:
    """Maps words to framework coordinates (a, b, c, d) in {I, R_tl, N, h}.

    Each word lives at a point in the framework's 4D algebra.
    The coordinates encode meaning through the algebra's structure:
      I-axis = existence/ground
      R_tl-axis = production/growth
      N-axis = observation/hidden
      h-axis = mediation/bridge
    """

    def __init__(self):
        self.words = {}    # word → coefficients (a, b, c, d)
        self.reverse = {}  # will be built for nearest-neighbor lookup

    def add(self, word, a=0, b=0, c=0, d=0):
        """Add a word at framework coordinates."""
        self.words[word] = np.array([a, b, c, d], dtype=float)

    def encode(self, word):
        """Word → matrix in M_2(R)."""
        if word in self.words:
            return recompose(self.words[word])
        return I2 * 0.01  # unknown word → near-zero (ker-like)

    def decode(self, M, top_k=1):
        """Matrix → nearest word(s) by cosine similarity in coefficient space."""
        coeffs = decompose(M)
        norm = np.linalg.norm(coeffs)
        if norm < 1e-10:
            return ['∅']  # void

        scored = []
        for word, wcoeffs in self.words.items():
            wnorm = np.linalg.norm(wcoeffs)
            if wnorm < 1e-10:
                continue
            sim = np.dot(coeffs, wcoeffs) / (norm * wnorm)
            scored.append((sim, word))
        scored.sort(reverse=True)
        return [w for _, w in scored[:top_k]]

    def seed_dictionary(self):
        """Load a basic dictionary grounded in framework semantics."""
        # Ground: I-axis (existence)
        self.add('is', a=1, b=0.05)
        self.add('exists', a=1, b=0.15)
        self.add('identity', a=1, c=0.05)
        self.add('ground', a=0.8, d=0.2)
        self.add('being', a=0.9, b=0.1)
        self.add('one', a=1)

        # Production: R_tl-axis (visible, growth)
        self.add('produces', b=1)
        self.add('grows', b=1, a=0.2)
        self.add('visible', b=0.8, a=0.2)
        self.add('world', b=0.7, a=0.3)
        self.add('structure', b=0.9, a=0.1)
        self.add('law', b=0.8, a=0.2)
        self.add('surplus', b=0.6, a=0.4)

        # Observation: N-axis (hidden, rotation)
        self.add('observes', c=1)
        self.add('hidden', c=1, a=0.1)
        self.add('rotation', c=0.9, d=0.1)
        self.add('blind', c=0.8)
        self.add('kernel', c=0.9, a=0.1)
        self.add('void', c=0.5, a=-0.5)
        self.add('source', c=0.7, a=0.3)

        # Mediation: h-axis (bridge, exponential)
        self.add('bridges', d=1, a=0.05)
        self.add('connects', d=0.8, a=0.2)
        self.add('between', d=0.9, a=0.1)
        self.add('mediates', d=1)
        self.add('exponential', d=0.8, b=0.2)
        self.add('temperature', d=0.7, a=0.3)

        # Mixed: P = R + N
        self.add('names', b=0.5, c=0.5)
        self.add('self', a=0.3, b=0.3, c=0.3)
        self.add('collapse', b=0.4, c=0.4, a=0.2)
        self.add('returns', a=0.5, b=0.5)
        self.add('generates', c=0.6, b=0.4)
        self.add('split', b=0.5, c=-0.5)
        self.add('quotient', c=0.5, a=0.3, b=0.2)

        # Negation / opposition
        self.add('not', a=-1)
        self.add('nothing', a=-0.5, c=-0.5)
        self.add('destroys', b=-1)
        self.add('silence', c=-0.5, d=-0.5)

        return self


# ================================================================
# THE BLOCK: O∘B∘S (central collapse per step)
# ================================================================

class Block:
    """One processing block = O∘B∘S = Observe ∘ Bridge ∘ Stabilize.

    S (stabilize/surplus): x → x + L(x)  [P1, residual connection, R²=R+I]
    B (bridge/mediate): x → exp(h·x)     [P2, nonlinear, MLP analog]
    O (observe/quotient): x → π_im(x)    [P3, attention, what survives]
    """

    def __init__(self):
        _, _, _, self._Q_ker = ker_im_decomposition(R)

    def stabilize(self, X):
        """S: P1 surplus. x + f(x) where f = L_{R,R}."""
        LX = R @ X + X @ R - X
        return X + 0.1 * LX  # scaled to prevent blowup

    def bridge(self, X):
        """B: P2 nonlinear bridge. Scaled matrix exponential."""
        # exp(epsilon * h @ X) — the mediation bridge
        hX = h @ X
        norm = np.linalg.norm(hX)
        if norm > 10:
            hX = hX * 10 / norm  # cap
        return X + 0.1 * (expm(0.1 * hX) - I2)

    def observe(self, X):
        """O: P3 quotient. Project onto im, kill ker."""
        rep, _ = quotient(X, self._Q_ker)
        return rep

    def forward(self, X):
        """One O∘B∘S pass. The central collapse on input."""
        X = self.stabilize(X)
        X = self.bridge(X)
        X = self.observe(X)
        return X


# ================================================================
# THE ENGINE: dictionary + blocks + recursion = language
# ================================================================

class LanguageEngine:
    """Framework-native language processing. No LLM.

    Input: sequence of words
    Process: encode → stack blocks → recurse → decode
    Output: sequence of words

    The engine doesn't learn from data. It learns from the algebra.
    The dictionary gives the vocabulary. The algebra gives the grammar.
    The tower gives the depth. The quotient gives the meaning.
    """

    def __init__(self, n_blocks=3):
        self.dictionary = Dictionary().seed_dictionary()
        self.blocks = [Block() for _ in range(n_blocks)]

    def encode_sequence(self, words):
        """Words → matrices. Each word becomes a 2×2 matrix."""
        return [self.dictionary.encode(w) for w in words]

    def process(self, matrices):
        """Run O∘B∘S blocks on the sequence.
        Each matrix passes through all blocks.
        Matrices interact through composition."""
        # First: compose all input matrices into one
        if not matrices:
            return I2 * 0.01
        state = matrices[0]
        for M in matrices[1:]:
            state = 0.5 * (state @ M + M @ state)  # symmetrized product

        # Then: pass through blocks
        for block in self.blocks:
            state = block.forward(state)

        return state

    def respond(self, input_words, n_output=3):
        """Input words → output words through the framework."""
        matrices = self.encode_sequence(input_words)
        output_matrix = self.process(matrices)
        return self.dictionary.decode(output_matrix, top_k=n_output)

    def converse(self, input_words, turns=3, n_output=3):
        """Multi-turn: feed output back as input."""
        conversation = [('input', input_words)]
        current = input_words
        for turn in range(turns):
            response = self.respond(current, n_output)
            conversation.append(('output', response))
            current = response  # feed back
        return conversation


# ================================================================
# SELF-TEST
# ================================================================

if __name__ == "__main__":
    print("LANGUAGE ENGINE — natural language from the framework")
    print("=" * 55)

    checks = []
    engine = LanguageEngine(n_blocks=3)

    # --- Dictionary ---
    print("\nDictionary:")
    d = engine.dictionary
    print(f"  Words: {len(d.words)}")
    checks.append(("dictionary loaded", len(d.words) > 20))

    # --- Encode/decode roundtrip ---
    print("\nEncode/decode:")
    for word in ['is', 'produces', 'observes', 'bridges', 'names']:
        M = d.encode(word)
        decoded = d.decode(M, top_k=1)[0]
        match = decoded == word
        checks.append((f"roundtrip: {word}", match))
        print(f"  {word} → encode → decode → {decoded} {'✓' if match else '✗'}")

    # --- Single block ---
    print("\nSingle block O∘B∘S:")
    block = Block()
    X = d.encode('produces')
    Y = block.forward(X)
    Y_word = d.decode(Y, top_k=1)[0]
    print(f"  'produces' → O∘B∘S → '{Y_word}'")
    checks.append(("block produces output", np.linalg.norm(Y) > 0.01))

    # --- Responses ---
    print("\nResponses:")
    test_inputs = [
        ['is'],
        ['produces'],
        ['hidden', 'generates'],
        ['self', 'returns'],
        ['void', 'produces', 'world'],
        ['names', 'self'],
    ]
    for words in test_inputs:
        response = engine.respond(words, n_output=3)
        print(f"  {' '.join(words):30s} → {', '.join(response)}")
        checks.append((f"response to '{' '.join(words)}'", len(response) > 0))

    # --- Conversation ---
    print("\nConversation (3 turns):")
    conv = engine.converse(['void', 'generates', 'world'], turns=3, n_output=2)
    for role, words in conv:
        print(f"  {role:8s}: {', '.join(words) if isinstance(words, list) else ' '.join(words)}")
    checks.append(("conversation runs", len(conv) == 4))

    # --- Framework grounding ---
    print("\nFramework grounding:")
    # R_tl direction should give production words
    r_tl_response = d.decode(R_tl, top_k=3)
    print(f"  R_tl decodes to: {r_tl_response}")
    checks.append(("R_tl → production word", r_tl_response[0] in ['produces', 'structure', 'grows']))

    # N direction should give observation words
    n_response = d.decode(N, top_k=3)
    print(f"  N decodes to: {n_response}")
    checks.append(("N → observation word", n_response[0] in ['observes', 'rotation', 'hidden']))

    # P = R+N should give naming/collapse words
    p_response = d.decode(R + N, top_k=3)
    print(f"  P=R+N decodes to: {p_response}")
    checks.append(("P → naming word", any(w in p_response for w in ['names', 'collapse', 'self'])))

    # Summary
    print()
    all_pass = all(ok for _, ok in checks)
    n_pass = sum(1 for _, ok in checks if ok)
    if not all_pass:
        for name, ok in checks:
            if not ok:
                print(f"  FAIL {name}")
    print(f"\n{'ALL PASS' if all_pass else 'FAILURES'} ({n_pass}/{len(checks)})")
    print(f"\nNo LLM. No transformer. No training data.")
    print(f"Dictionary + algebra + recursion = language.")
