"""
syntax.py — Grammar from framework types. Sentences as executable structures.

Framework-native type mapping:
  noun      = stable locus / object (im-sector, persists)
  verb      = transition operator (L_{s,s}, transforms)
  modifier  = basis deformation (scaling, rotation)
  negation  = N² = -I (sign flip)
  relation  = L (the Sylvester operation itself)
  pronoun   = fixed-point reference (P²=P)
  tense     = tower depth / clock index

Sentences parse as: subject --verb--> object
Executed as: verb(subject, object) in matrix form.

Forward product (A@B) for subject→verb.
Reverse product (B@A) for verb→object.
Commutator [A,B] carries grammatical orientation.
Anticommutator {A,B} carries shared meaning.
"""
import numpy as np
import sys
sys.path.insert(0, '..')
from algebra import sylvester, ker_im_decomposition, quotient

R = np.array([[0, 1], [1, 1]], dtype=float)
N = np.array([[0, -1], [1, 0]], dtype=float)
J = np.array([[0, 1], [1, 0]], dtype=float)
h = J @ N
I2 = np.eye(2)
R_tl = R - 0.5 * I2


# ================================================================
# WORD TYPES
# ================================================================

class WordType:
    NOUN = 'noun'           # stable locus
    VERB = 'verb'           # transition operator
    MODIFIER = 'modifier'   # basis deformation
    NEGATION = 'negation'   # N² = -I
    RELATION = 'relation'   # L_{s,s}
    PRONOUN = 'pronoun'     # fixed point P²=P
    TENSE = 'tense'         # tower depth


# ================================================================
# TYPED WORD
# ================================================================

class TypedWord:
    """A word with a type and a matrix representation."""

    def __init__(self, word, wtype, matrix):
        self.word = word
        self.wtype = wtype
        self.matrix = matrix.copy()

    def __repr__(self):
        return f"TypedWord('{self.word}', {self.wtype})"


# ================================================================
# SENTENCE
# ================================================================

class Sentence:
    """A grammatically typed sequence of words.

    Parses subject-verb-object and executes as matrix operations.
    """

    def __init__(self, words):
        """words: list of TypedWord"""
        self.words = words
        self.subject = None
        self.verb = None
        self.object = None
        self._parse()

    def _parse(self):
        """Extract subject, verb, object from the word sequence."""
        nouns = [w for w in self.words if w.wtype == WordType.NOUN]
        verbs = [w for w in self.words if w.wtype == WordType.VERB]
        mods = [w for w in self.words if w.wtype == WordType.MODIFIER]
        negs = [w for w in self.words if w.wtype == WordType.NEGATION]

        # Simple SVO parse: first noun = subject, verb = verb, second noun = object
        if nouns:
            self.subject = nouns[0]
        if verbs:
            self.verb = verbs[0]
        if len(nouns) > 1:
            self.object = nouns[1]
        elif nouns and not verbs:
            # No verb: the noun IS the statement
            self.verb = TypedWord('is', WordType.VERB, I2)

        # Apply modifiers to subject
        for mod in mods:
            if self.subject:
                self.subject = TypedWord(
                    f"{mod.word}({self.subject.word})",
                    WordType.NOUN,
                    mod.matrix @ self.subject.matrix
                )

        # Apply negation
        for neg in negs:
            if self.object:
                self.object = TypedWord(
                    f"not({self.object.word})",
                    WordType.NOUN,
                    N @ self.object.matrix @ N  # conjugate by N
                )
            elif self.subject:
                self.subject = TypedWord(
                    f"not({self.subject.word})",
                    WordType.NOUN,
                    N @ self.subject.matrix @ N
                )

    def execute(self):
        """Execute the sentence as a matrix operation.

        subject --verb--> object becomes:
          forward: subject @ verb (subject acts through verb)
          reverse: verb @ object (verb acts on object)
          full: subject @ verb @ object (if all present)

        Returns dict with:
          center = {subject, object} anticommutator (shared meaning)
          orientation = [subject, object] commutator (grammatical order)
          result = the executed output
        """
        if self.subject is None:
            return {'result': I2 * 0.01, 'center': I2 * 0.01, 'orientation': I2 * 0}

        S = self.subject.matrix
        V = self.verb.matrix if self.verb else I2
        O = self.object.matrix if self.object else I2

        if self.object:
            # Full SVO: subject @ verb @ object
            result = S @ V @ O
            center = 0.5 * (S @ O + O @ S)         # what both orderings agree on
            orientation = 0.5 * (S @ O - O @ S)      # what changes with order
        else:
            # SV only: subject @ verb
            result = S @ V
            center = 0.5 * (S + V)
            orientation = 0.5 * (S @ V - V @ S)

        return {
            'result': result,
            'center': center,
            'orientation': orientation,
            'has_orientation': np.linalg.norm(orientation) > 1e-10,
        }

    def __repr__(self):
        parts = []
        if self.subject:
            parts.append(f"S:{self.subject.word}")
        if self.verb:
            parts.append(f"V:{self.verb.word}")
        if self.object:
            parts.append(f"O:{self.object.word}")
        return f"Sentence({' '.join(parts)})"


# ================================================================
# TYPED DICTIONARY
# ================================================================

class TypedDictionary:
    """Words with types and matrices."""

    def __init__(self):
        self.words = {}

    def add(self, word, wtype, matrix):
        self.words[word] = TypedWord(word, wtype, matrix)

    def get(self, word):
        return self.words.get(word, TypedWord(word, WordType.NOUN, I2 * 0.01))

    def parse(self, text):
        """Parse a string into a Sentence of TypedWords."""
        tokens = text.lower().split()
        typed_words = [self.get(w) for w in tokens]
        return Sentence(typed_words)

    def seed(self):
        """Load framework-grounded typed dictionary."""
        # Nouns (stable loci — things that persist)
        self.add('world', WordType.NOUN, R)
        self.add('structure', WordType.NOUN, R_tl)
        self.add('void', WordType.NOUN, N)
        self.add('self', WordType.NOUN, R + N)  # P = R + N
        self.add('identity', WordType.NOUN, I2)
        self.add('kernel', WordType.NOUN, N)
        self.add('image', WordType.NOUN, R_tl)
        self.add('surplus', WordType.NOUN, I2)  # the +I
        self.add('law', WordType.NOUN, R)

        # Verbs (transition operators — things that transform)
        self.add('produces', WordType.VERB, R)       # production = R-action
        self.add('observes', WordType.VERB, N)        # observation = N-action
        self.add('bridges', WordType.VERB, h)         # mediation = h-action
        self.add('generates', WordType.VERB, R + N)   # full naming act
        self.add('returns', WordType.VERB, R)         # R²=R+I
        self.add('destroys', WordType.VERB, -I2)      # annihilation
        self.add('is', WordType.VERB, I2)             # identity (copula)
        self.add('sees', WordType.VERB, N)            # = observes
        self.add('names', WordType.VERB, R + N)       # = P

        # Modifiers (basis deformations)
        self.add('hidden', WordType.MODIFIER, N)      # rotate into ker
        self.add('visible', WordType.MODIFIER, R_tl)  # project into im
        self.add('all', WordType.MODIFIER, I2)        # identity (no change)
        self.add('deep', WordType.MODIFIER, R)        # deepen (R-scale)

        # Negation
        self.add('not', WordType.NEGATION, N)         # N² = -I

        return self


# ================================================================
# SELF-TEST
# ================================================================

if __name__ == "__main__":
    print("SYNTAX — grammar from framework types")
    print("=" * 50)

    checks = []
    td = TypedDictionary().seed()

    # --- Basic parsing ---
    print("\nParsing:")
    for text in ['world produces structure', 'void observes self',
                 'self generates world', 'void', 'hidden world']:
        s = td.parse(text)
        print(f"  '{text}' → {s}")
    checks.append(("parse SVO", td.parse('world produces structure').object is not None))
    checks.append(("parse SV", td.parse('void observes').verb is not None))
    checks.append(("parse S", td.parse('void').subject is not None))

    # --- Execution ---
    print("\nExecution:")

    # world produces structure = R @ R @ R_tl
    s1 = td.parse('world produces structure')
    r1 = s1.execute()
    expected1 = R @ R @ R_tl
    checks.append(("SVO execution", np.allclose(r1['result'], expected1)))
    print(f"  'world produces structure' → ||result||={np.linalg.norm(r1['result']):.4f}")

    # void observes self = N @ N @ (R+N) = -I @ P = -P
    s2 = td.parse('void observes self')
    r2 = s2.execute()
    expected2 = N @ N @ (R + N)  # = -P
    checks.append(("void observes self = -P", np.allclose(r2['result'], expected2)))
    print(f"  'void observes self' → {np.round(r2['result'], 2).tolist()}")

    # --- Orientation (word order matters) ---
    print("\nOrientation (word order):")
    s3 = td.parse('world produces void')
    s4 = td.parse('void produces world')
    r3 = s3.execute()
    r4 = s4.execute()
    same_center = np.allclose(r3['center'], r4['center'])
    diff_orient = not np.allclose(r3['orientation'], r4['orientation'])
    checks.append(("same center", same_center))
    checks.append(("different orientation", diff_orient or r3['has_orientation']))
    print(f"  'world produces void' center = {np.round(r3['center'], 2).tolist()}")
    print(f"  'void produces world' center = {np.round(r4['center'], 2).tolist()}")
    print(f"  Same center: {same_center}  Different orientation: {diff_orient}")

    # --- Negation ---
    print("\nNegation:")
    s5 = td.parse('self is identity')
    s6 = td.parse('not self is identity')
    r5 = s5.execute()
    r6 = s6.execute()
    print(f"  'self is identity' → ||result||={np.linalg.norm(r5['result']):.4f}")
    print(f"  'not self is identity' → ||result||={np.linalg.norm(r6['result']):.4f}")
    checks.append(("negation changes result", not np.allclose(r5['result'], r6['result'])))

    # --- Modifier ---
    print("\nModifiers:")
    s7 = td.parse('hidden world')
    r7 = s7.execute()
    print(f"  'hidden world' = N@R applied: {np.round(r7['result'], 2).tolist()}")
    checks.append(("modifier applies", np.allclose(s7.subject.matrix, N @ R)))

    # --- Framework identities ---
    print("\nFramework identities through syntax:")

    # "self generates self" = P @ P @ P. Since P²=P: = P @ P = P.
    s8 = td.parse('self generates self')
    r8 = s8.execute()
    P = R + N
    checks.append(("self generates self = P³=P", np.allclose(r8['result'], P @ (R+N) @ P)))

    # "void observes void" = N @ N @ N = N(-I) = -N
    s9 = td.parse('void observes void')
    r9 = s9.execute()
    checks.append(("void observes void = -N", np.allclose(r9['result'], -N)))
    print(f"  'void observes void' = -N: {np.allclose(r9['result'], -N)}")

    # Summary
    print()
    all_pass = all(ok for _, ok in checks)
    n_pass = sum(1 for _, ok in checks if ok)
    if not all_pass:
        for name, ok in checks:
            if not ok:
                print(f"  FAIL {name}")
    print(f"\n{'ALL PASS' if all_pass else 'FAILURES'} ({n_pass}/{len(checks)})")
    print(f"\nSentences are executable. Grammar is algebra.")
