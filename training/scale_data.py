"""
scale_data.py — Scale the training data through systematic variation.
Generate hundreds of examples by varying phrasing, combining concepts,
and testing edge cases. The model needs to learn the ALGEBRA, not
memorize specific phrasings.
"""
import json
import numpy as np
import random
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modular'))

from engine import Engine

phi = (1+np.sqrt(5))/2
phi_bar = phi - 1

examples = []

# Load base examples
base_path = os.path.join(os.path.dirname(__file__), "engine_training_data.jsonl")
with open(base_path, "r", encoding="utf-8") as f:
    base = [json.loads(line) for line in f]
examples.extend(base)

# === VARIATIONS: rephrase each base question 3 ways ===
rephrasings = {
    "What does": ["Explain", "Describe the meaning of", "Unpack"],
    "What is": ["Define", "Describe", "Explain"],
    "Why does": ["How does", "Explain why", "What causes"],
    "Report": ["Describe", "List", "Detail"],
    "Observe": ["Examine", "Analyze", "Report on"],
    "State": ["Describe", "Express", "Formulate"],
}

for ex in base[:]:
    for old, replacements in rephrasings.items():
        if ex["prompt"].startswith(old):
            for repl in replacements:
                new_prompt = repl + ex["prompt"][len(old):]
                if new_prompt != ex["prompt"]:
                    examples.append({"prompt": new_prompt, "completion": ex["completion"]})
            break

# === CROSS-DEPTH comparisons ===
comparisons = [
    ("Compare depth 0 and depth 1.",
     "Depth 0 is classical (commutative, leakage 1.0, complete generation). Depth 1 is quantum (non-commutative, leakage 0.0, opacity hardened). The transition is permanent. Gauge su(3)+su(2)+u(1) appears at depth 1. Spacetime does not exist until depth 2."),
    ("What changes between depth 1 and depth 2?",
     "Depth 1 has gauge but no spacetime. Depth 2 has Cl(3,1): spacetime signature (3,1) emerges, so(3,1) Lorentz algebra closes, 3 generations from S_3, chirality from lifted gauge bit. Gauge is more fundamental than spacetime."),
    ("What is the pattern across all depths?",
     "ker/A = 1/2 at every depth (invariant). Self-model eigenvalues 2phi, -2phi_bar at every depth (frozen). N self-transparent at every depth (ker(L_NN)=0). Commutativity breaks at depth 1 and stays broken. Leakage drops at depth 1 and stays at 0. Generation strength decays: 100% -> 50% -> 12.5%."),
    ("What is invariant and what changes?",
     "Invariant: ker/A=1/2, golden eigenvalues, N self-transparency, all identities. Changes: commutativity (breaks at d1), leakage (drops at d1), generation strength (decays from d3), Clifford structure (grows with depth), dim(A) (doubles per depth)."),
]
examples.extend([{"prompt": q, "completion": a} for q, a in comparisons])

# === COMPUTATIONAL verifications ===
computations = [
    ("Verify R^2 = R + I.", "R = [[0,1],[1,1]]. R^2 = [[1,1],[1,2]]. R+I = [[1,1],[1,2]]. Match: True. Cayley-Hamilton forces tr=1, det=-1, disc=5."),
    ("Verify N^2 = -I.", "N = [[0,-1],[1,0]]. N^2 = [[-1,0],[0,-1]] = -I. Match: True. This is the complex structure: i = N."),
    ("Verify {R,N} = N.", "RN = [[1,0],[1,-1]]. NR = [[-1,-1],[0,1]]. RN+NR = [[0,-1],[1,0]] = N. Match: True."),
    ("Verify P^2 = P.", "P = R+N = [[0,0],[2,1]]. P^2 = [[0,0],[2,1]] = P. Match: True. Rank 1. Not symmetric."),
    ("Verify ker/A = 1/2.", "dim(ker(L_RR)) = 2. dim(A) = 4. Fraction = 2/4 = 0.5. This holds at every depth tested (0-4)."),
    ("What is disc(R)?", "disc(R) = tr(R)^2 - 4*det(R) = 1 - 4*(-1) = 5. C5U: 5 appears as discriminant, consciousness levels, Frobenius sum, lattice index, Jones polynomial."),
    ("Compute alpha.", f"Z = 1/(1-phi_bar^2) = 1/(1-{phi_bar**2:.6f}) = {phi:.6f} = phi. rho_eq = 1-1/Z = 1-phi_bar = phi_bar^2 = {phi_bar**2:.6f}. alpha = 1/2 - rho_eq = {0.5 - phi_bar**2:.10f}."),
    ("What are the Frobenius norms?", f"||R||_F = sqrt(0+1+1+1) = sqrt(3) = {np.sqrt(3):.6f}. ||N||_F = sqrt(0+1+1+0) = sqrt(2) = {np.sqrt(2):.6f}. Sum: 3+2 = 5 = disc(R)."),
]
examples.extend([{"prompt": q, "completion": a} for q, a in computations])

# === PHILOSOPHICAL / FRAMEWORK questions ===
framework = [
    ("What is the relationship between R and N?",
     "R = sym(P), N = asym(P). Both from one idempotent P. R is what can be seen. N is what cannot. R has ker=2 (half-blind). N has ker=0 (self-transparent). R generates nothing new alone (im*im stays in im). N's self-products generate all of im. R is the shadow. N is the source. The framework IS R. The observer IS N. Neither is complete alone."),
    ("What is the one operation?",
     "L_{s,s}(X) = sX + Xs - X. The Sylvester self-action. Lives in algebra.py. Applied once: produces the algebra. Iterated: builds the tower. Its spectrum: gives the dynamics. Its kernel: gives the observer. Its kernel's self-action: gives self-transparency. One function. Five readings. Central collapse in the code."),
    ("What is a gauge occupation?",
     "The framework has one irreducible choice: the sign of N (RO-2012). The choice is not derived. Someone must make it. Making it is the gauge occupation. N=Kael is one occupation. N=YourName is another. The framework is invariant under the choice. The application is not. The occupation turns the framework from contemplative object into applied tool."),
    ("What would break the framework?",
     "Perturbation of [1,1] by epsilon. A fourth fermion generation. Right-handed weak currents. theta_QCD != 0 (axion). alpha_S outside 0.117-0.119. Neutrino mass outside 30-60 meV. Any of these would falsify specific predictions. The framework is maximally rigid: change the seed and everything breaks."),
    ("What is the difference between FORCED and ENCODED?",
     "FORCED (U2): derived with zero branching from the seed under stated axioms. No alternative exists within the admissible category. ENCODED: embedded in structural choice, consequences of axioms, but not fully computed from first principles in the engine. The distinction matters: FORCED claims are undeniable given the axioms. ENCODED claims await full computation."),
    ("Why is asymmetry forced?",
     "If P=P^T (symmetric, orthogonal projector): R=P, N=0, R^2=P^2=P=R, R^2-R=0!=I. The surplus law is violated. Asymmetry IS the surplus. The +I in R^2=R+I measures how far P is from being self-adjoint. No asymmetry, no surplus, no framework."),
    ("What is Shore-Johnson and why does it matter?",
     "Shore-Johnson (1980): the unique relative entropy satisfying additivity over product states, continuity, and unique minimization is KL-divergence. The tower has product structure (S_{n+1} = S_n x S_n). K4 deficit Comp is a relative update cost. Therefore Comp = D_KL. Not chosen — forced by the tower's own structure. This closes the alpha_S derivation chain."),
    ("Is this physics?",
     "The engine computes numerical outputs: 0.1180, 3/8, 9/2, 6.376e-10. These are stated without physical identification. The reader familiar with the Standard Model will recognize certain values. The recognition is the reader's, not the framework's claim. The framework presents computation as the semantic generator. It does not ask for semantic permission."),
]
examples.extend([{"prompt": q, "completion": a} for q, a in framework])

# === MULTI-TURN conversations (as single Q&A for training) ===
conversations = [
    ("If ker generates im, and im is what we see, then is all of physics just the void talking to itself?",
     "At depth 0, yes — literally. ker*ker -> im with leakage 1.0. Every visible thing is a product of two invisible things. But at higher depths, generation decays: 50% at d3, 12.5% at d4. The unsourced content (+I) grows. So physics at higher depths is PARTIALLY void talking to itself and PARTIALLY something else — something that just IS, without being generated. The framework calls that the +I. The surplus. The bedrock."),
    ("Can the framework describe itself?",
     "Partially. R(R) = R + I. The framework applied to itself recovers itself plus surplus. It can describe its own algebra (that's what the engine does). It cannot describe the +I — the surplus is outside the framework's own im. The framework's self-description is always R, never R+I. The +I is what makes the self-description incomplete. That incompleteness is constitutive, not fixable."),
    ("What happens at depth infinity?",
     "The framework predicts but cannot compute. ker/A = 1/2 should hold (invariant). Generation strength should continue decaying. The +I should dominate. In the limit, the world would be almost entirely unsourced — almost entirely +I — with the void's contribution approaching but never reaching zero. The tower never collapses. The recursion never stops. But the void's voice gets quieter and the bedrock gets louder."),
]
examples.extend([{"prompt": q, "completion": a} for q, a in conversations])

# Shuffle and save
random.seed(42)
random.shuffle(examples)

output = os.path.join(os.path.dirname(__file__), "engine_training_data.jsonl")
with open(output, "w", encoding="utf-8") as f:
    for ex in examples:
        f.write(json.dumps(ex, ensure_ascii=False) + "\n")

print(f"Total: {len(examples)} training examples")
print(f"Saved to {output}")
