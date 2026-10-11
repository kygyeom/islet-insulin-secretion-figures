"""
Core vs Mix cell arrangement of an islet, drawn from generated coordinates
(synthetic example; no structural data from the manuscript is used).
"""
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(1)
N, RADIUS = 2500, 45.0
FRACTION = {"beta": 0.70, "alpha": 0.20, "delta": 0.10}
COLOR = {"beta": "blue", "alpha": "red", "delta": "green"}


def sample_ball(n):
    pts = rng.normal(size=(n, 3))
    pts /= np.linalg.norm(pts, axis=1, keepdims=True)
    return pts * RADIUS * rng.random((n, 1)) ** (1 / 3)


def assign(pts, structure):
    n = len(pts)
    n_beta = int(FRACTION["beta"] * n)
    n_alpha = int(FRACTION["alpha"] * n)
    kinds = np.empty(n, dtype=object)
    if structure == "core":      # beta cells inside, alpha/delta in the outer shell
        order = np.argsort(np.linalg.norm(pts, axis=1))
    else:                        # mix: random placement with the same fractions
        order = rng.permutation(n)
    kinds[order[:n_beta]] = "beta"
    kinds[order[n_beta:n_beta + n_alpha]] = "alpha"
    kinds[order[n_beta + n_alpha:]] = "delta"
    return kinds


pts = sample_ball(N)
fig = plt.figure(figsize=(8, 4))
for i, structure in enumerate(("core", "mix")):
    ax = fig.add_subplot(1, 2, i + 1, projection="3d")
    kinds = assign(pts, structure)
    for kind, color in COLOR.items():
        m = (kinds == kind)
        cut = np.abs(pts[:, 2]) <= 8                # central slab shows the interior
        ax.scatter(*pts[m & cut].T, c=color, s=40, alpha=1.0, edgecolors="black", linewidths=0.3)
        ax.scatter(*pts[m & ~cut].T, c=color, s=10, alpha=0.05)
    ax.set_title(structure.capitalize(), fontsize=11)
    ax.view_init(elev=60, azim=-60)
    ax.set_axis_off()
fig.text(0.99, 0.01, "synthetic example", ha="right", va="bottom",
         fontsize=8, style="italic", color="gray")
fig.tight_layout()
fig.savefig("examples/islet_structure_3d.png", dpi=200)
