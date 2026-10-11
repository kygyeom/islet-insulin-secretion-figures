"""
Random-forest feature importance for insulin secretion (synthetic example data).
"""
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("synthetic_results.csv")
df["S"] = LabelEncoder().fit_transform(df["structure"])

features = ["G", "K", "Pb", "D", "S"]
labels = {"G": "G", "K": "K", "Pb": r"$P_{\beta}$", "D": "D", "S": "S"}

rf = RandomForestRegressor(n_estimators=300, random_state=42).fit(df[features], df["IC"])
imp = pd.Series(rf.feature_importances_, index=[labels[f] for f in features]).sort_values()

fig, ax = plt.subplots(figsize=(4, 3))
ax.barh(imp.index, imp.values, color="#4C78A8")
ax.set_xlabel("Feature importance")
ax.text(0.98, 0.04, "synthetic example data", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=8, style="italic", color="gray")
fig.tight_layout()
fig.savefig("examples/feature_importance.png", dpi=200)
