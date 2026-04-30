# From One Idempotent: Parent Layer, Algebra, Physics, and Observer

**Abstract.** Before the collapse: a balanced parent $M = \mathrm{diag}(P, P^T)$ carrying both gauge branches. After the collapse: an occupied child $P$, rank 1, asymmetric, with $R = (P+P^T)/2$ and $N = (P-P^T)/2$ satisfying $R^2=R+I$, $N^2=-I$, $\{R,N\}=N$. The Sylvester self-action $L_{s,s}(X)=sX+Xs-X$ splits the algebra into ker (orientation) and im (center) with invariant fraction $1/2$ at every tower depth. $P$ is not the primitive: it is the child-collapse of the parent through cross-sector quenching ($8 \to 4$) and branch selection ($4 \to 2$). The intertwiner $K=2J-h$ and the harness $C=2h+J$ are dual objects, both squaring to $\mathrm{disc} \cdot I$. The asymmetric idempotent family $R^2=R+\mu I$ has discriminants $1+k^2$ that reproduce all framework quantities: $2, 5, 10, 17, 26, 37, 50$. The tower forces Peano arithmetic; every step of Shor's algorithm follows from $P^2=P$. The disclosure rank formula $2^{2n+1}-\binom{2n}{n}$ gives $1, 6, 26, 108$ with redundancy equal to the central binomial coefficient. All from two inputs: $[1,1]$ and $2$. Zero free parameters. 60 automated tests pass.

---

## Part 0: The Parent Layer

### 0. The Balanced Carrier

**Definition 0.1.** The parent carrier on $W = V_+ \oplus V_-$:

$$M = \mathrm{diag}(P, P^T), \quad M^2=M, \quad \mathrm{rank}(M)=2, \quad \mathrm{tr}(M)=2$$

$M$ holds both gauge branches without collapsing either.

**Theorem 0.2 (Parent spine).** With $\hat{R}=\mathrm{diag}(R,R)$ and $\hat{N}=\mathrm{diag}(N,-N)$:

$$\hat{R}^2 = \hat{R}+I_4, \quad \{\hat{R},\hat{N}\}=\hat{N}, \quad \hat{N}^2=-I_4, \quad M=\hat{R}+\hat{N}$$

The parent satisfies the same unit spine as the child. The parent is not a container — it is itself a lawful seed. [Tier A]

**Theorem 0.3 (Exchange invariance).** The intertwiner $K = 2J - h$ satisfies $K^2 = \mathrm{disc}\cdot I$, $\det(K) = -\mathrm{disc}$, $KPK^{-1}=P^T$. The harness $C = [R,N] = 2h+J$ satisfies $C^2=\mathrm{disc}\cdot I$, $\det(C)=-\mathrm{disc}$. $K$ and $C$ are dual: swap the coefficients of $J$ and $h$, both square to $\mathrm{disc}\cdot I$. The branch exchange $T = \begin{pmatrix}0&K^{-1}\\K&0\end{pmatrix}$ gives $T^2=I$, $TMT^{-1}=M$. [Tier A]

### 1. The Collapse

**Theorem 1.1 (Parent Sylvester decomposition).** $L_{M,M}$ on $\mathrm{End}(W)$ decomposes into four sectors: child-preserving ($A$), mirror-preserving ($D$), cross-sectors ($B$,$C$). $\dim\ker(L_M)=8 = 2+2+4$ (child + mirror + cross-mixing). [Tier N]

**Theorem 1.2 (Collapse by quotient).** Cross-sector quenching kills branch-mixing: $8 \to 4$ diagonal-only directions. Branch selection via $\Sigma=\mathrm{diag}(I_2,-I_2)$: $4 \to 2$ child + $2$ mirror. The $A$-sector contains exactly $\ker(L_P)$. Child recovered. Mirror persists hidden. The 4 cross modes = entanglement between branches that occupation destroys. [Tier N, verified]

**Theorem 1.3 (Child recovery).** After branch selection, the child algebra recovers completely: $P=R+N$, $R^2=R+I$, $\{R,N\}=N$, $N^2=-I$, seven identities, ker/im, tower, physics. [Tier A]

---

## Part I: The Algebra

### 2. The Primitive

**Theorem 2.1 (Single generator).** $P = R+N = [[0,0],[2,1]]$. $P^2=P$, rank 1, $P \neq P^T$. The asymmetry is forced: if $P=P^T$ then $R^2-R=0 \neq I$ (Theorem 2.2). $P = J+|1\rangle\langle 1|+N$: ground + commitment + observer. Remove any one: $P^2 \neq P$.

**Corollary 2.3 (Hilbert space from asymmetry).** $P \neq P^T \to N \neq 0 \to N^2=-I \to$ complex structure $\to$ Cartan involution $\theta(X)=-X^T \to B_\theta = 4\mathrm{tr}(XY^T)$ positive definite $\to$ Hilbert space $\to$ Gleason $\to$ Born rule $\to$ quantum mechanics. [Tier A]

**Theorem 2.4 ($P = I$ on $\mathrm{im}(P)$).** On the 1-dimensional image of $P$: $P$ acts as the identity. On $\ker(P)$: $P=0$. The naming act IS the identity on what it names. [Tier A]

### 3. The Operation

**Definition 3.1.** $L_{s,s}(X) = sX + Xs - X$. Lives in `algebra.py` (51 lines).

**Theorem 3.2 (Ker/im decomposition).** $\ker(L_R) = \mathrm{span}\{N, NR\}$, $\mathrm{im}(L_R)=\mathrm{span}\{I,R_\mathrm{tl}\}$. $\ker/A=1/2$. [Tier A]

**Theorem 3.3 (Orientation decomposition).** $R$ = center (transpose-invariant). $N$ = orientation (sign-flips). $L$ kills orientation, preserves center. $L|_{\mathfrak{sl}(2,\mathbb{R})}(X) = \mathrm{tr}(RX)\cdot I$: the Killing-form contraction. [Tier A]

**Theorem 3.4 (Spectrum).** Eigenvalues of $L_R$: $\{-\sqrt{5}, 0, 0, +\sqrt{5}\}$. [Tier A]

### 4. Identities, Constants, Clifford

**Theorem 4.1 (Seven identities).** $R^2=R+I$, $N^2=-I$, $\{R,N\}=N$, $RNR=-N$, $NRN=R-I$, $(RN)^2=I$, $[R,N]^2=5I$. [Tier A]

**Theorem 4.2 (Five constants + bridge).** $\varphi$ (eigenvalue of $R$), $\sqrt{3}$ ($\|R\|$), $\sqrt{2}$ ($\|N\|$), $e$ ($\exp(h)_{00}$), $\pi$ (half-period of $N$-rotation). $T = e^\varphi/\pi$ (bridge: P1 on P2 / P3). $\|R\|^2+\|N\|^2=3+2=5=\mathrm{disc}$. [Tier A]

**Theorem 4.3 (Clifford grading).** $M_2(\mathbb{R})=\mathrm{Cl}(1,1)$. $\mathrm{im}=\mathrm{even}$, $\ker=\mathrm{odd}$. $\mathrm{odd}\times\mathrm{odd}=\mathrm{even}$: ker generates im. [Tier A]

### 5. The Asymmetric Idempotent Family

**Theorem 5.1 (Universal laws).** ALL rank-1 asymmetric idempotents: $R^2+N^2=R$, $\{R,N\}=N$, $N^2=-\mu I$, $R^2=R+\mu I$, $\mathrm{disc}=1+4\mu$. [Tier A]

**Theorem 5.2 (Family tower).** Integer family $P=[[0,0],[k,1]]$: $\mathrm{disc}=1+k^2$. Every framework quantity IS a family discriminant:

| $k$ | $\mathrm{disc}$ | Framework quantity |
|-----|---------|-------------------|
| 1 | 2 | $d = |S_0|$ |
| 2 | 5 | $\mathrm{disc}(R)$ (golden discriminant) |
| 3 | 10 | $2\cdot\mathrm{disc} = \dim(\Lambda^2(\mathrm{fund}))$ |
| 4 | 17 | $\dim_\mathrm{gauge}+\mathrm{disc} = 2^{d^2}+1$ (Fermat prime $F_d$) |
| 5 | 26 | $\mathrm{disclosure\_rank}(2) = d_\mathrm{crit}(\text{bosonic string})$ |
| 6 | 37 | $\mathrm{adj}(\mathrm{SU}(5))+\mathrm{fund}+\dim(\mathfrak{su}(3))$ |
| 7 | 50 | $\mathrm{fund}\times\Lambda^2 = \mathrm{adj}+d_\mathrm{crit}$ |

[Tier A for universal law; Tier N for disc identifications]

### 6. Uniqueness and the Selector Stack

**Theorem 6.1 (Seed selection).** Among $R^2=aR+bI$ with $a,b\in\mathbb{Z}_+$: nontrivial Sylvester kernel requires $a=1$; scalar channel requires $a=1$; idempotent closure requires $(a,b)=(1,1)$. Triple forcing. [Tier A / Tier E]

**Theorem 6.2 (Kernel canonicalization).** Given selected $R$, the kernel quadratic form canonically yields $N$ up to sign by negative-unit normalization: $N^2=-I$. $P=R+N$ closes to rank-1 idempotence. [Tier A, implemented in `production.py` and `observer.py`]

**Theorem 6.3 ($N^2=-I$ necessity).** Quadratic form $\det Q = -b-1/4 < 0$ for all $b \geq 1$. Indefinite signature guarantees negative rotation. [Tier A]

---

## Part II: The Tower

### 7. K6' Ascent and Invariants

**Theorem 7.1 (K6' lift).** $s'=[[s,N],[0,s]]$, $N'=[[N,-2h],[0,N]]$, $J'=[[J,0],[0,J]]$. Preserves all identities. Filler $N$ is unique (up to sign) among ker elements. [Tier A]

**Theorem 7.2 (Tower invariants).** $\ker/A=1/2$, golden eigenvalues $\{2\varphi,-2\bar\varphi\}$, $N$ self-transparent ($\ker(L_{N,N})=0$), all identities — at every depth. [Tier N, depths 0–4]

### 8. P₀, Generation Decay, Recursive Disclosure

**Theorem 8.1 ($P_0 = \ker$).** Two solutions to $X^2=X$: $P_0$ (trivial, symmetric, void) and $P$ (nontrivial, asymmetric, named). $P_0 \to P$: ker gains an image. $\ker/A=1/2$ always. [Tier A]

**Theorem 8.2 (Generation decay).** $\mathrm{rank}(\ker^2\to\mathrm{im})$: $\{2,8,32,64,64\}$ at depths 0–4. Freezes at 64. [Tier N]

**Theorem 8.3 (Recursive disclosure).** $L_{n+1}([[K,0],[0,K]]) = [[0,\{K,N\}],[0,0]]$. Since $\{K,N\}\neq 0$ for all $K\in\ker(L_n)$: total disclosure. $0/32$ survive depth $2\to 3$. The graviton IS the disclosure event. [Tier N]

**Theorem 8.4 (Disclosure rank formula).** $\mathrm{disclosure\_rank}(n) = 2^{2n+1}-\binom{2n}{n}$. Redundancy = central binomial. Values: $1$ (scalar), $6$ (Lorentz), $26$ ($d_\mathrm{crit}$), $108$. [Tier N]

**Cross-connection.** $64 = 2^{\mathrm{disclosure\_rank}(1)} = 2^{\dim(\mathfrak{so}(3,1))}$. The freeze IS $2^{\text{Lorentz}}$. [Tier N]

### 9. The Physics Spine

Depth 0→1: classical→quantum (permanent). Depth 1→2: quantum→relativistic QFT ($\mathrm{Cl}(3,1)$, $\mathfrak{so}(3,1)$, 3 generations). Depth 2→3: K1' suppression. 12 Cl(3,1) + 18 Cl(2,2) = 30 = $d\cdot N_c\cdot\mathrm{disc} = F(3)\times F(4)\times F(5)$. [Tier N]

---

## Part III: Physics

### 10. Gravity (Three Layers)

**Layer 1 (Scalar, 3D complete).** $L$ on $\mathfrak{gl}(2,\mathbb{R})$ IS the complete 3D gravity operator (0 propagating DOF). $L|_{\mathfrak{sl}(2,\mathbb{R})}(X)=\mathrm{tr}(RX)\cdot I$. Connection $A=N$, curvature $F=-2h$, $\mathrm{tr}(F^2)=8$, $(1/2)[s,h]=N$, $\Lambda=\mathrm{disc}/2$. [Tier A]

**Layer 2 (Two-way dynamics).** $L(\delta s)=0$ (metric in ker), $L(\delta N)=-\{\delta s,N\}$ (connection responds), $\{N,\delta N\}=0$. Center perturbation forces orientation response; orientation constrains center. [Tier N]

**Layer 3 (Recursive disclosure).** The graviton is the K6' transition event. Total ker disclosure at every depth. Area quantum $= 2L = 2\log_2\varphi$ bits. [Tier N]

### 11. Gauge Theory and Matter

**Theorem 11.1.** $\mathrm{SU}(3)$ from $\mathrm{Sym}^2(\mathbb{C}^d)$: $N_c=d(d+1)/2=3$. $\mathrm{SU}(2)$ from $\mathfrak{sl}(2,\mathbb{R})$. $\mathrm{U}(1)$ from $\exp(\theta N)$. [Tier A]

**Theorem 11.2.** 5 field types forced by exchange$\times$isospin$\times$chirality + cubic anomaly split. Hypercharges $\{Y_1,4Y_1,-2Y_1,-3Y_1,-6Y_1\}$ from $18Y_1(9Y_1^2-t^2)=0$. Anomalies $6/6=0$. [Tier A]

**Theorem 11.3.** $\sin^2\theta_W = 3/8$ at GUT. $\beta$-functions $b_1=41/10$, $b_2=-19/6$, $b_3=-7$ from derived matter. [Tier A]

**Theorem 11.4.** $\dim(\mathrm{fund}_\mathrm{GUT})=\mathrm{disc}$: $N_c+d=5=\mathrm{disc}$. All SU(5) reps from disc: adj$=\mathrm{disc}^2-1$, $\Lambda^2=2\cdot\mathrm{disc}$, $\mathrm{Sym}^2=3\cdot\mathrm{disc}$. [Tier A]

### 12. Coupling Constants and Mass Scales

**Theorem 12.1 (K4 → Yang-Mills).** $D_\mathrm{KL}$ at $O(F^2)$ = $(1/4g^2)\mathrm{tr}(F^2)$ = complete renormalizable gauge action. $\theta_\mathrm{QCD}=0$ from K4 minimization. [Tier A / Chain]

**Theorem 12.2.** $\alpha_S = 1/2-\bar\varphi^2 = 0.11803$. Partition function $Z=\varphi$, $\rho_\mathrm{eq}=\bar\varphi^2$. [Tier A]

**Theorem 12.3 (Coupling-contraction identity).** $\alpha_S/|m| = \varphi$ to 0.37%, where $m=f'(y^*)$ is the Canon contraction. The algebra scales the dynamics. [Tier N]

**Theorem 12.4.** $m_\nu = m_e\cdot\bar\varphi^{34}$, $34=2(\dim_\mathrm{gauge}+\mathrm{disc})$. $\delta=\varphi+2$, $\mathrm{dm}^2$ ratio $=32.5$ vs exp 33. [Tier N]

**Theorem 12.5 (Koide from $S_3$).** $Q = d/(d^2-1) = \|N\|^2/\|R\|^2 = 2/3$. $\mathbb{Z}/3 \subset S_3$ forces 3-fold mass structure. [Tier B]

**Theorem 12.6.** $\eta_B\cdot m_e/m_\nu = \bar\varphi^{2\cdot\mathrm{disc}} = \bar\varphi^{\dim(\Lambda^2(\mathrm{fund}))}$. [Tier N]

**Theorem 12.7.** $m_H/v = 1/2 = \ker/A$. $m_p/\Lambda_\mathrm{QCD}=9/2$. [Tier A / N]

### 13. Cosmological Constant

$\Lambda = \mathrm{disc}/2$, depth-invariant. Attenuation $\bar\varphi^{2n}$ per depth. $n\approx 295$ depths $=409$ bits. $2^{409}\approx 10^{123}$. [Tier N]

---

## Part IV: Topology and Quantum

### 14. Jones, Fibonacci, Modular Data

**Theorem 14.1.** $V(4_1)|_{q=\varphi^2}=5=\mathrm{disc}$. $q^{1/2}-q^{-1/2}=1$. [Tier A]

**Theorem 14.2.** $R^2=R+I$ IS $\tau\times\tau=1+\tau$. $d_\tau=\varphi$. SU$(2)_3$ Verlinde recovers Fibonacci fusion. [Tier A]

**Theorem 14.3.** Braiding $e^{4\pi i/5}$, $\cos(4\pi/5)=-\varphi/2$. Fibonacci TQC gate set universal. Braid relation verified. [Tier A]

### 15. Quantum Gates and Bell

**Theorem 15.1.** CNOT $= (I+h)/2\otimes I + (I-h)/2\otimes J$. Hadamard $H=(J+h)/\sqrt{2}$. All from $\{h,J\}$. [Tier A]

**Theorem 15.2.** Bell $S=2\sqrt{2}$ (Tsirelson saturated). 8 quantum algorithms from $\{h,J,N\}$. [Tier A / N]

### 16. Tower Arithmetic and Shor

**Theorem 16.1 (Tower → Peano).** K6' depths with successor satisfy Peano axioms. $\mathbb{N}$ forced. [Tier A]

**Theorem 16.2 (Arithmetic chain).** $\mathbb{N}\to\mathbb{Z}\to\mathbb{Z}/N\mathbb{Z}\to(\mathbb{Z}/N\mathbb{Z})^*$. All forced by quotient grammar. [Tier A]

**Theorem 16.3 (Shor from $P^2=P$).** Every step forced. Every phase $=\exp(\theta N)$. Measurement $=P^2=P$. 15$=3\times 5$. 29 checks. [Tier N]

---

## Part V: The Observer

### 17. Self-Transparency and the Gap

**Theorem 17.1.** $\ker(L_{N,N})=0$ at every depth. $N$ is the ONLY self-transparent generator. [Tier A / N]

**Theorem 17.2 (Explanatory gap).** First person: $\ker=0$. Third person: $\ker=2$. The gap is $0$ vs $2$. [Tier A]

### 18. Consciousness and Two Axes

Axis 1 ($n_\mathrm{eff}$): linear depth, K1' wall, doubly-exponential barrier. Axis 2 ($m$): recursive depth, unbounded. $C(K)=n_\mathrm{eff}\times m\times 2L$. Axis 2 is unattenuated: $\ker(L_{N,N})=0$ is tower-invariant while generation decays. [Tier N]

### 19. Broken Recursion

Three mechanisms: concentrated ker, stalled ascent, backward-branching. Healing $=$ K6' ascent. Requires: Landauer payable, P2 bridge, phase coherence. [Tier N]

---

## Part VI: Closure

### 20. The Orientation Spine

Everything is orientation. $R$ = center, $N$ = orientation, $L$ = center map, $\mathrm{disc}=[R,N]^2/I$ = disagreement. $\Lambda=\mathrm{disc}\cdot(\ker/A)$. $\alpha_S=\ker/A-\bar\varphi^2$. The Bell test is an orientation detector. $P_0\to P$: the birth of orientation. Physics $=\mathrm{im}(L)=$ the center of the naming act.

### 21. The Canon Kernel

$S(x)=\exp(\ln\varphi\cdot\sqrt{|x|}\cdot e^{-|x|/T})\cdot e^{-i\pi|x|}$. $T=e^\varphi/\pi$. $y^*=1.2781$. $m=-0.0727$. $\nu=-y^*/2$. $\alpha_S=\varphi\cdot|m|$ (0.37%). $2\pi/y^*\approx\mathrm{disc}$ (1.7%). Canon depth-invariant.

### 22. The Standing Wave

$\Xi=\Xi(\Xi)$. At every level: $P^2=P$, $D^2=I$, $q\circ q=q$, $R^2=R+I$, $\mathrm{Dist}=P_1\circ P_2\circ P_3$, $M(\mathrm{FRAME})=\mathrm{FRAME}$, $\chi\circ\chi=\chi$. Standing wave. All co-present.

### 23. Reproducibility and Falsification

60 automated tests. Two inputs. Zero free parameters.

| Prediction | Value | Status |
|-----------|-------|--------|
| $\alpha_S$ | $0.11803$ | $0.1\%$ from exp |
| $\sin^2\theta_W$ | $3/8$ | GUT scale |
| $m_\nu$ | $40$ meV | within $[30,60]$ |
| $m_H/v$ | $1/2$ | $1.6\%$ from exp |
| $\mathrm{dm}^2$ ratio | $32.5$ | $1.4\%$ from exp |
| $\eta_B\cdot m_e/m_\nu$ | $\bar\varphi^{10}$ | $4\%$ from exp |
| Bell $S$ | $2\sqrt{2}$ | exact (Tsirelson) |

---

## Appendix A: Taxonomy

See TAXONOMY.md. Universal $\to$ Selected $\to$ Canonicalized $\to$ Reconstructed $\to$ Parent $\to$ Collapsed $\to$ Recursive $\to$ Interpreted. Each layer has its own theorem. Each transition has its own bridge. The bridges are the battleground.

## Appendix B: Open Problems

O-1. Globalize seed selection beyond $(a,b)\in\{1,\ldots,10\}^2$.
O-2. Formalize kernel canonicalization from code to theorem.
O-3. Derive the $\mu=1$ selector from kernel geometry alone.
O-4. $\alpha_S$ comparison scale (framework is dimensionless; $M_Z$ is a bridge).
O-5. Parent-level K6' tower ($\hat{R}$ is a valid seed).
O-6. Structural link between the two 26s (disclosure rank and family disc).
O-7. Separate algebraically forced from interpretation-map dependent.

---

*$P$ is not the primitive. $P$ is the child-collapse of a balanced parent. The parent existed before the occupation. The occupation is not invention. It is reduction. 60 tests. 0 parameters. Everything from $[1,1]$ and $2$.*

◈
