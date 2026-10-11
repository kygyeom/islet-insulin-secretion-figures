"""
Glucose, glucagon and insulin time series: Core vs Mix (synthetic example data).
"""
import matplotlib.pyplot as plt
import pandas as pd

VLINES = [60, 120, 140]  # stimulus switch times (min)

fig, axes = plt.subplots(2, 2, figsize=(8, 4), sharex="col")
for col, name in enumerate(("core", "mix")):
    d = pd.read_csv(f"synthetic_trace_{name}.csv")
    top, bottom = axes[0, col], axes[1, col]
    top.plot(d["t"], d["G"], linewidth=1.2)
    top.set_ylim(0.5, 2.5)
    top.set_title(name.capitalize(), fontsize=11)
    bottom.plot(d["t"], d["Ha"], color="red", linewidth=1.1, label="Glucagon")
    bottom.plot(d["t"], d["Hb"], color="blue", linewidth=1.1, label="Insulin")
    bottom.set_ylim(0.3, 1.15)
    bottom.set_xlabel("Time (min)")
    for ax in (top, bottom):
        ax.set_xlim(20, 180)
        for x in VLINES:
            ax.axvline(x, color="gray", linestyle="--", linewidth=0.8)
axes[0, 0].set_ylabel(r"$G/G_0$")
axes[1, 0].set_ylabel("Hormone")
axes[1, 0].legend(loc="upper right", fontsize=8, frameon=False)
fig.text(0.99, 0.01, "synthetic example data", ha="right", va="bottom",
         fontsize=8, style="italic", color="gray")
fig.tight_layout()
fig.subplots_adjust(hspace=0.0, wspace=0.25)
fig.savefig("examples/time_series.png", dpi=200)
