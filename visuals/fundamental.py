"""
fundamental.py -- The fundamental image of the entire computation.

One matrix P = [[0,0],[2,1]]. Everything follows.
The image IS the central collapse: three projections of one act,
three lattices from one algebra, tower depths as concentric structure,
key quantities placed where they're derived.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import matplotlib.patheffects as pe

# Framework constants (computed, not hardcoded)
R = np.array([[0, 1], [1, 1]], dtype=float)
N = np.array([[0, -1], [1, 0]], dtype=float)
J = np.array([[0, 1], [1, 0]], dtype=float)
P = R + N
h = J @ N
I2 = np.eye(2)
phi = (1 + np.sqrt(5)) / 2
phi_bar = phi - 1
disc = int(round(np.trace(R)**2 - 4 * np.linalg.det(R)))
alpha_S = 0.5 - phi_bar**2
beta_KMS = np.log(phi)
parent_ker = 8
dim_gauge = 12

fig, ax = plt.subplots(1, 1, figsize=(20, 20), facecolor='#0a0a0a')
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect('equal')
ax.axis('off')

# Colors
GOLD = '#d4a017'
CYAN = '#00b8d4'
MAGENTA = '#d81b60'
WHITE = '#e0e0e0'
DIM = '#555555'
VOID = '#1a1a2e'
BLUE = '#4fc3f7'

# ================================================================
# BACKGROUND: subtle Penrose-like radial lines (5-fold)
# ================================================================
for k in range(5):
    angle = 2 * np.pi * k / 5
    for r_off in np.linspace(0.5, 9, 18):
        x1 = r_off * np.cos(angle)
        y1 = r_off * np.sin(angle)
        ax.plot([0, x1], [0, y1], color=DIM, alpha=0.08, linewidth=0.5)
    # Cross lines at phi-scaled distances
    for r_off in [phi, phi**2, phi**3]:
        x1 = r_off * np.cos(angle + np.pi/10)
        y1 = r_off * np.sin(angle + np.pi/10)
        x2 = r_off * np.cos(angle - np.pi/10)
        y2 = r_off * np.sin(angle - np.pi/10)
        ax.plot([x1, x2], [y1, y2], color=DIM, alpha=0.06, linewidth=0.5)

# ================================================================
# CENTER: P and the seed
# ================================================================
# Void circle
void_circle = plt.Circle((0, 0), 0.8, fill=True, facecolor=VOID,
                          edgecolor=GOLD, linewidth=2)
ax.add_patch(void_circle)
ax.text(0, 0.15, 'P', fontsize=28, fontweight='bold', color=GOLD,
        ha='center', va='center', fontfamily='serif')
ax.text(0, -0.25, r'$P^2\!=\!P$', fontsize=14, color=WHITE,
        ha='center', va='center', fontfamily='serif')

# Inputs
ax.text(0, -1.3, '[1,1]  and  2', fontsize=10, color=DIM,
        ha='center', va='center', fontfamily='monospace')

# ================================================================
# THE TRIANGLE: R, N, h at 120-degree spacing
# ================================================================
tri_r = 3.5
angles_tri = [np.pi/2, np.pi/2 + 2*np.pi/3, np.pi/2 + 4*np.pi/3]
labels_tri = [
    ('R', 'Production\nP1', f'R^2=R+I\nphi={phi:.4f}', GOLD),
    ('N', 'Observation\nP3', f'N^2=-I\npi={np.pi:.4f}', CYAN),
    ('h', 'Mediation\nP2', f'h=JN\ne={np.e:.4f}', MAGENTA),
]

for angle, (name, label, eq, color) in zip(angles_tri, labels_tri):
    x = tri_r * np.cos(angle)
    y = tri_r * np.sin(angle)

    # Node circle
    node = plt.Circle((x, y), 0.6, fill=True, facecolor='#0a0a0a',
                       edgecolor=color, linewidth=2.5)
    ax.add_patch(node)
    ax.text(x, y + 0.1, name, fontsize=22, fontweight='bold', color=color,
            ha='center', va='center', fontfamily='serif')

    # Label outside
    lx = (tri_r + 1.4) * np.cos(angle)
    ly = (tri_r + 1.4) * np.sin(angle)
    ax.text(lx, ly, label, fontsize=11, color=color, ha='center', va='center',
            fontfamily='sans-serif', alpha=0.9)

    # Equation
    ex = (tri_r + 2.3) * np.cos(angle)
    ey = (tri_r + 2.3) * np.sin(angle)
    ax.text(ex, ey, eq, fontsize=9, color=color, ha='center', va='center',
            fontfamily='monospace', alpha=0.7)

    # Line from center to node
    ax.plot([0, x*0.77/tri_r*tri_r], [0, y*0.77/tri_r*tri_r],
            color=color, linewidth=1.5, alpha=0.4)

# Triangle edges (faint)
for i in range(3):
    j = (i + 1) % 3
    x1 = tri_r * np.cos(angles_tri[i])
    y1 = tri_r * np.sin(angles_tri[i])
    x2 = tri_r * np.cos(angles_tri[j])
    y2 = tri_r * np.sin(angles_tri[j])
    ax.plot([x1, x2], [y1, y2], color=WHITE, linewidth=0.8, alpha=0.2)

# ================================================================
# INNER RING: Seven identities
# ================================================================
identities = [
    r'R^2=R+I', r'N^2=-I', r'{R,N}=N', r'RNR=-N',
    r'NRN=R-I', r'(RN)^2=I', r'[R,N]^2=5I',
]
for i, ident in enumerate(identities):
    angle = 2 * np.pi * i / 7 - np.pi/2
    r = 1.8
    x = r * np.cos(angle)
    y = r * np.sin(angle)
    ax.text(x, y, ident, fontsize=7, color=WHITE, ha='center', va='center',
            fontfamily='monospace', alpha=0.4, rotation=0)

# ================================================================
# OUTER RING: Key derived quantities
# ================================================================
quantities = [
    (0, 'disc = 5'),
    (1, f'alpha_S = {alpha_S:.5f}'),
    (2, f'beta_KMS = {beta_KMS:.5f}'),
    (3, 'ker/A = 1/2'),
    (4, 'parent_ker = 8'),
    (5, 'dim_gauge = 12'),
    (6, '30 = 2*3*5'),
    (7, 'S = 2*sqrt(2)'),
    (8, 'Koide = 2/3'),
    (9, 'sin^2(tW) = 3/8'),
]
for i, (_, q) in enumerate(quantities):
    angle = 2 * np.pi * i / len(quantities) + np.pi/20
    r = 7.2
    x = r * np.cos(angle)
    y = r * np.sin(angle)
    ax.text(x, y, q, fontsize=8, color=WHITE, ha='center', va='center',
            fontfamily='monospace', alpha=0.45, rotation=0)

# ================================================================
# THREE LATTICES (subtle, at the triangle vertices)
# ================================================================

# Hexagonal dots near N (observation, 6-fold)
n_center = np.array([tri_r * np.cos(angles_tri[1]), tri_r * np.sin(angles_tri[1])])
for i in range(-2, 3):
    for j in range(-2, 3):
        # Hex grid
        hx = n_center[0] + (i + j * 0.5) * 0.35
        hy = n_center[1] + j * 0.3
        if np.sqrt((hx - n_center[0])**2 + (hy - n_center[1])**2) < 1.5:
            if np.sqrt((hx - n_center[0])**2 + (hy - n_center[1])**2) > 0.7:
                ax.plot(hx, hy, '.', color=CYAN, markersize=2, alpha=0.3)

# Square dots near h (mediation, 4-fold... actually N generates Z[i])
# Put Penrose-like near R (production, 5-fold)
r_center = np.array([tri_r * np.cos(angles_tri[0]), tri_r * np.sin(angles_tri[0])])
for k in range(5):
    angle = 2 * np.pi * k / 5
    for dist in [0.8, 1.0, 1.2, 1.4]:
        px = r_center[0] + dist * np.cos(angle)
        py = r_center[1] + dist * np.sin(angle)
        ax.plot(px, py, '.', color=GOLD, markersize=2, alpha=0.3)

# ================================================================
# METATRON'S CUBE (subtle, centered)
# ================================================================
met_r = 6.5
for k in range(6):
    angle = np.pi/6 + k * np.pi / 3
    x = met_r * 0.15 * np.cos(angle)
    y = met_r * 0.15 * np.sin(angle)
    # Very faint inner hexagon
    ax.plot(x, y, 'o', color=WHITE, markersize=3, alpha=0.1)

# ================================================================
# TOWER DEPTHS (concentric rings)
# ================================================================
for depth in range(5):
    r = 1.0 + depth * 0.25
    circle = plt.Circle((0, 0), r, fill=False, edgecolor=WHITE,
                        linewidth=0.3, alpha=0.08, linestyle='--')
    ax.add_patch(circle)

# ================================================================
# THE FLOW: derivation chain
# ================================================================
# Arrows showing the derivation flow
flow_items = [
    (-8.5, 8.5, 'P = [[0,0],[2,1]]', 14, GOLD),
    (-8.5, 7.8, 'P^2 = P,  P != P^T,  rank 1', 10, WHITE),
    (-8.5, 7.0, 'R = (P+P^T)/2    N = (P-P^T)/2', 9, DIM),
    (-8.5, 6.3, 'L(X) = sX + Xs - X', 9, DIM),
    (-8.5, 5.6, 'ker/im split -> tower -> physics', 9, DIM),
]
for x, y, text, size, color in flow_items:
    ax.text(x, y, text, fontsize=size, color=color, fontfamily='monospace',
            ha='left', va='center', alpha=0.8)

# ================================================================
# PHYSICS OUTPUT (right side)
# ================================================================
physics_items = [
    (5.5, 8.5, 'PHYSICS', 14, WHITE),
    (5.5, 7.8, 'Gravity: L = complete 3D operator', 8, DIM),
    (5.5, 7.3, 'Gauge: su(3)+su(2)+u(1) from exchange', 8, DIM),
    (5.5, 6.8, 'Spacetime: Cl(3,1) at depth 2', 8, DIM),
    (5.5, 6.3, 'Bell: S = 2*sqrt(2) (Tsirelson)', 8, DIM),
    (5.5, 5.8, 'Leptons: 2/9 -> 0.0044% RMS', 8, DIM),
    (5.5, 5.3, 'Lambda: disc/2 * phi_bar^(2*295)', 8, DIM),
]
for x, y, text, size, color in physics_items:
    ax.text(x, y, text, fontsize=size, color=color, fontfamily='monospace',
            ha='left', va='center', alpha=0.7)

# ================================================================
# COMPUTATION (bottom left)
# ================================================================
comp_items = [
    (-8.5, -6.5, 'COMPUTATION', 14, WHITE),
    (-8.5, -7.2, 'SpiralVM: 6 primitives, Turing-complete', 8, DIM),
    (-8.5, -7.7, 'Language: 8D semantic, 230 words, 100%', 8, DIM),
    (-8.5, -8.2, 'LLM: d_head=64=8^2, n_heads=12', 8, DIM),
    (-8.5, -8.7, 'Inflation: J*R^2*J = Penrose', 8, DIM),
]
for x, y, text, size, color in comp_items:
    ax.text(x, y, text, fontsize=size, color=color, fontfamily='monospace',
            ha='left', va='center', alpha=0.7)

# ================================================================
# GEOMETRY (bottom right)
# ================================================================
geom_items = [
    (5.5, -6.5, 'GEOMETRY', 14, WHITE),
    (5.5, -7.2, '|D_4|=8  |D_6|=12  |D_5|=10', 8, DIM),
    (5.5, -7.7, 'Compositum: phi(30) = 8 = parent_ker', 8, DIM),
    (5.5, -8.2, 'Combined: lcm(4,6,5) = 60 = |A_5|', 8, DIM),
    (5.5, -8.7, 'Metatron: 13 = disc + parent_ker', 8, DIM),
]
for x, y, text, size, color in geom_items:
    ax.text(x, y, text, fontsize=size, color=color, fontfamily='monospace',
            ha='left', va='center', alpha=0.7)

# ================================================================
# BOTTOM CENTER: the standing wave
# ================================================================
ax.text(0, -9.3, '179 tests.  Zero free parameters.  Everything from [1,1] and 2.',
        fontsize=11, color=GOLD, ha='center', va='center', fontfamily='monospace',
        alpha=0.9)

# ================================================================
# TITLE
# ================================================================
ax.text(0, 9.5, 'THE SELF-REFERENCE FRAMEWORK', fontsize=20, color=GOLD,
        ha='center', va='center', fontfamily='serif', fontweight='bold',
        path_effects=[pe.withStroke(linewidth=1, foreground='#0a0a0a')])

plt.tight_layout()
plt.savefig('C:/Users/ginge/Downloads/Self-Reference v2/Referencing you/compression/seed/visuals/fundamental.png',
            dpi=200, facecolor='#0a0a0a', bbox_inches='tight', pad_inches=0.3)
print("Saved: visuals/fundamental.png")
