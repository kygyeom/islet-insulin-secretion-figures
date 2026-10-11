"""
Generate synthetic example data for the figure scripts.

All values are produced by arbitrary functions plus noise. They are NOT simulation
output and do NOT reproduce any result of the manuscript.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(0)


# ---------------------------------------------------------------- results table
# One row per (structure, K, Pb, D, G) condition with several repeats.
rows = []
for structure in ("core", "mix"):
    for K in (0.2, 0.4, 0.6):
        for Pb in (20, 40, 60):
            for D in (90, 160, 200):
                for G in (0.5, 1.0, 1.5, 2.2):
                    for _ in range(3):
                        base = 1.0 / (1.0 + np.exp(-(G - 1.2) * 3.0))
                        size = 0.5 + 0.004 * D
                        mix_bonus = 0.15 if structure == "mix" else 0.0
                        ic = base * size * (0.6 + 0.01 * Pb) * (0.8 + 0.5 * K) + mix_bonus
                        rows.append(
                            dict(structure=structure, K=K, Pb=Pb, D=D, G=G,
                                 IC=ic + rng.normal(0, 0.05))
                        )
pd.DataFrame(rows).to_csv("synthetic_results.csv", index=False)


# ---------------------------------------------------------------- time series
# Stepwise glucose input and first-order hormone responses with arbitrary constants.
t = np.arange(20, 181, 1.0)
steps = [(0, 1.0), (60, 2.2), (120, 1.0), (140, 1.8)]


def glucose(t):
    g = np.full_like(t, 1.0)
    for t0, level in steps:
        g[t >= t0] = level
    return g


def lag(x, tau):
    y = np.empty_like(x)
    y[0] = x[0]
    for i in range(1, len(x)):
        y[i] = y[i - 1] + (x[i] - y[i - 1]) / tau
    return y


g = glucose(t)
for name, tau_b, tau_a, amp in (("core", 9.0, 14.0, 0.60), ("mix", 5.0, 7.0, 0.75)):
    hb = 0.35 + amp * (lag(g, tau_b) - 1.0) / 1.2
    ha = 0.95 - 0.55 * (lag(g, tau_a) - 1.0) / 1.2
    out = pd.DataFrame(dict(t=t, G=lag(g, 3.0), Ha=ha, Hb=hb))
    out.iloc[:, 1:] += rng.normal(0, 0.004, size=(len(t), 3))
    out.to_csv(f"synthetic_trace_{name}.csv", index=False)

print("wrote synthetic_results.csv, synthetic_trace_core.csv, synthetic_trace_mix.csv")
