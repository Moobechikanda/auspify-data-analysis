
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "processed" / "netflix_cleaned.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load cleaned dataset
df = pd.read_csv(DATA_FILE)

# 2. Prepare release-year data
df["release_year"] = pd.to_numeric(
    df["release_year"], errors="coerce"
)

year_data = df.dropna(subset=["release_year"]).copy()
year_data["release_year"] = year_data["release_year"].astype(int)

# Count titles released in each year
yearly_counts = (
    year_data.groupby("release_year")["show_id"]
    .nunique()
    .sort_index()
)

# 3. Display key results
print("TASK 4: RELEASE YEAR TREND ANALYSIS")
print("=" * 45)
print(f"Titles analysed: {year_data['show_id'].nunique()}")
print(f"Years covered: {yearly_counts.index.min()}–{yearly_counts.index.max()}")

print("\nTop 10 release years by title count:")
print(
    yearly_counts.sort_values(ascending=False)
    .head(10)
    .to_string()
)

# Save yearly counts
yearly_counts.rename("title_count").rename_axis(
    "release_year"
).reset_index().to_csv(
    OUTPUT_DIR / "task4_yearly_counts.csv",
    index=False
)

# 4. Create a trend chart
sns.set_theme(style="whitegrid")

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    yearly_counts.index,
    yearly_counts.values,
    linewidth=2
)

ax.set_title("Netflix Titles by Release Year")
ax.set_xlabel("Release Year")
ax.set_ylabel("Number of Titles")
ax.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig(
    OUTPUT_DIR / "task4_release_year_trend.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close(fig)

# 5. Create a report
peak_year = int(yearly_counts.idxmax())
peak_count = int(yearly_counts.max())

report = f"""
TASK 4: RELEASE YEAR TREND ANALYSIS
===================================

Titles analysed: {year_data['show_id'].nunique():,}
Release years covered: {yearly_counts.index.min()}–{yearly_counts.index.max()}

Peak release year in the dataset: {peak_year}
Titles released in that year: {peak_count:,}

INTERPRETATION
--------------
The chart shows how many titles in this dataset were
originally released in each year.

These are release years, not the dates when Netflix
added titles to its catalogue.

LIMITATIONS
-----------
The dataset describes titles available in the supplied
file. It does not by itself establish why releases rose
or fell, nor does it measure audience demand.
"""

(OUTPUT_DIR / "task4_completion_report.txt").write_text(
    report.strip() + "\n",
    encoding="utf-8"
)

print("\nTask 4 outputs saved successfully.")
print(f"Chart: {OUTPUT_DIR / 'task4_release_year_trend.png'}")
print(f"Yearly counts: {OUTPUT_DIR / 'task4_yearly_counts.csv'}")
print(f"Report: {OUTPUT_DIR / 'task4_completion_report.txt'}")
