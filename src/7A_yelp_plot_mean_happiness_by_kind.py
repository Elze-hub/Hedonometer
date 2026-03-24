#Asena

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load happiness scores with 'kind' column
data = pd.read_csv("data/processed/yelp_happiness_averages_scores.csv")

# 2. Compute mean happiness per kind
grouped = data.groupby("kind")["happiness_average"]
means = grouped.mean()

# (Optional but recommended) compute standard error for error bars
counts = grouped.count()
stds = grouped.std()
se = stds / np.sqrt(counts)  # standard error

print("Mean happiness by kind:")
print(means)

# 3. Make barplot
kinds = ["review", "tip"]  # ensure a consistent order
mean_values = [means[k] for k in kinds]
se_values = [se[k] for k in kinds]

fig, ax = plt.subplots(figsize=(6, 4))

bars = ax.bar(kinds, mean_values, yerr=se_values, capsize=5, color=["steelblue", "orange"])

ax.set_ylabel("Mean hedonometer happiness score")
ax.set_xlabel("Kind of text")
ax.set_title("Average happiness of Yelp tips vs reviews")
ax.set_ylim(min(mean_values) - 0.2, max(mean_values) + 0.2)

# Add value labels on top of bars
for bar, m in zip(bars, mean_values):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height, f"{m:.2f}",
            ha="center", va="bottom", fontsize=9)

# 4. Save figure
figures_dir = "figures"
os.makedirs(figures_dir, exist_ok=True)
out_path = os.path.join(figures_dir, "yelp_mean_happiness_tips_vs_reviews.png")
plt.tight_layout()
plt.savefig(out_path, dpi=300)
plt.show()

print(f"Saved barplot to {out_path}")