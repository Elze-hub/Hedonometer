"""Plot Yelp review stars vs happiness score (labMT)"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path

# ========== 路径配置 ==========
# 假设你的项目根目录是 hedonometer-project
ROOT = Path(__file__).resolve().parents[1]  # 回到项目根目录
LABMT_PATH = ROOT / "data" / "raw" / "Data_Set_S1.txt"
YELP_REVIEWS_PATH = ROOT / "data" / "raw" / "yelp_academic_dataset_review.json"
SAMPLE_SIZE = 5000  # 先取 5000 条评论，避免内存太大

# ========== 1. 加载 labMT 词表 ==========
labmt = pd.read_csv(LABMT_PATH, sep="\t", skiprows=3, na_values=["--"])
labmt = labmt[["word", "happiness_average"]].dropna()
happiness_dict = dict(zip(labmt["word"], labmt["happiness_average"]))

print(f"Loaded {len(happiness_dict)} words from labMT")

# ========== 2. 从 Yelp 读取部分评论 ==========
stars = []
texts = []

print(f"Reading {SAMPLE_SIZE} reviews from {YELP_REVIEWS_PATH}...")
with open(YELP_REVIEWS_PATH, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i >= SAMPLE_SIZE:
            break
        data = json.loads(line)
        stars.append(data["stars"])
        texts.append(data["text"])

print(f"Read {len(stars)} reviews")

# ========== 3. 计算每条评论的幸福感分数 ==========
def compute_happiness(text):
    words = text.lower().split()
    scores = [happiness_dict.get(w) for w in words if w in happiness_dict]
    if not scores:
        return np.nan
    return np.mean(scores)

happiness_scores = []
for i, txt in enumerate(texts):
    if i % 1000 == 0:
        print(f"  Processed {i}/{len(texts)}")
    happiness_scores.append(compute_happiness(txt))

df = pd.DataFrame({"stars": stars, "happiness": happiness_scores}).dropna()
print(f"After removing NaNs: {len(df)} reviews")

# ========== 4. 画散点图 + 趋势线 ==========
plt.figure(figsize=(8, 6))
plt.scatter(df["stars"], df["happiness"], alpha=0.3, s=10, color="blue")

# 计算线性回归趋势线
from scipy import stats
slope, intercept, r_value, p_value, std_err = stats.linregress(df["stars"], df["happiness"])
x_line = np.linspace(df["stars"].min(), df["stars"].max(), 100)
y_line = slope * x_line + intercept
plt.plot(x_line, y_line, color="red", linewidth=2, label=f"Trend line (r = {r_value:.2f})")

plt.title("Star Rating vs. Happiness Score (Yelp Reviews)")
plt.xlabel("Star Rating (1–5)")
plt.ylabel("Happiness Score (labMT)")
plt.legend()
plt.tight_layout()

# 保存图片
figures_dir = ROOT / "figures"
figures_dir.mkdir(exist_ok=True)
plt.savefig(figures_dir / "stars_vs_happiness.png", dpi=150)
print("Saved figure to", figures_dir / "stars_vs_happiness.png")
plt.show()

# ========== Bootstrap 估计相关系数的置信区间 ==========
print("\n--- Bootstrap resampling for correlation confidence interval ---")

# 原始数据（df 已经包含 stars 和 happiness 两列，且已去掉了 NaN）
data = df[["stars", "happiness"]].values  # 转成 NumPy 数组，方便抽样
n = len(data)                              # 样本量
n_bootstrap = 1000                         # 重复抽样次数（1000 次足够）

# 用来存储每次抽样计算出的相关系数
boot_r = []

# 设置随机种子，让结果可重复（方便检查）
np.random.seed(42)

for i in range(n_bootstrap):
    # 从原始数据中随机抽取 n 行（有放回）
    idx = np.random.choice(n, size=n, replace=True)
    sample = data[idx]
    # 计算抽样数据的相关系数
    r_sample, _ = stats.pearsonr(sample[:, 0], sample[:, 1])
    boot_r.append(r_sample)

# 计算 95% 置信区间（取 2.5 和 97.5 百分位数）
ci_lower = np.percentile(boot_r, 2.5)
ci_upper = np.percentile(boot_r, 97.5)

print(f"Bootstrap 95% confidence interval for correlation: [{ci_lower:.3f}, {ci_upper:.3f}]")
print(f"Original r = {r_value:.3f} lies inside the interval? {'Yes' if ci_lower <= r_value <= ci_upper else 'No'}")

# （可选）画出 bootstrap 得到的 r 分布直方图
plt.figure(figsize=(6, 4))
plt.hist(boot_r, bins=40, color="skyblue", edgecolor="black", alpha=0.7)
plt.axvline(r_value, color="red", linestyle="--", label=f"Original r = {r_value:.3f}")
plt.axvline(ci_lower, color="gray", linestyle=":")
plt.axvline(ci_upper, color="gray", linestyle=":")
plt.title("Bootstrap Distribution of Correlation Coefficient")
plt.xlabel("Pearson r")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()

# 保存直方图到 figures 文件夹
bootstrap_fig_path = figures_dir / "bootstrap_r_distribution.png"
plt.savefig(bootstrap_fig_path, dpi=150)
print(f"Bootstrap histogram saved to {bootstrap_fig_path}")

plt.show()