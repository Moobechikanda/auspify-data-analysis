
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Locate project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "processed" / "netflix_cleaned.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load the cleaned dataset
df = pd.read_csv(DATA_FILE)

# 2. Count Movies and TV Shows
content_counts = df["type"].value_counts()

total_titles = len(df)
content_percentages = content_counts / total_titles * 100

# Print the results
print("TASK 2: CONTENT TYPE ANALYSIS")
print("=" * 40)
print(f"Total titles analysed: {total_titles}")
print("\nContent type counts:")

for content_type, count in content_counts.items():
    percentage = content_percentages[content_type]
    print(f"{content_type}: {count:,} ({percentage:.2f}%)")

# Save summary as a CSV file
summary = pd.DataFrame({
    "Content Type": content_counts.index,
    "Count": content_counts.values,
    "Percentage": [
        content_percentages[content_type]
        for content_type in content_counts.index
    ]
})

summary.to_csv(
    OUTPUT_DIR / "task2_content_summary.csv",
    index=False
)

# Use a consistent chart style
sns.set_theme(style="whitegrid")

# 3. Create a bar chart
fig, ax = plt.subplots(figsize=(9, 6))

sns.barplot(
    x=content_counts.index,
    y=content_counts.values,
    hue=content_counts.index,
    legend=False,
    ax=ax
)

ax.set_title("Netflix Content Distribution by Type", fontsize=15)
ax.set_xlabel("Content Type")
ax.set_ylabel("Number of Titles")

for index, count in enumerate(content_counts.values):
    percentage = content_percentages.iloc[index]
    ax.text(
        index,
        count,
        f"{count:,}\n({percentage:.1f}%)",
        ha="center",
        va="bottom"
    )

fig.tight_layout()
fig.savefig(
    OUTPUT_DIR / "task2_content_type_bar.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close(fig)

# 4. Create a pie chart
fig, ax = plt.subplots(figsize=(8, 8))

ax.pie(
    content_counts.values,
    labels=content_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

ax.set_title("Proportion of Movies and TV Shows on Netflix")

fig.tight_layout()
fig.savefig(
    OUTPUT_DIR / "task2_content_type_pie.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close(fig)

# 5. Generate a short findings report
movie_count = int(content_counts.get("Movie", 0))
tv_count = int(content_counts.get("TV Show", 0))

movie_pct = movie_count / total_titles * 100
tv_pct = tv_count / total_titles * 100

report = f"""
TASK 2: CONTENT TYPE ANALYSIS
=============================

Dataset: netflix_cleaned.csv
Total titles analysed: {total_titles:,}

RESULTS
-------
Movies: {movie_count:,} ({movie_pct:.2f}%)
TV Shows: {tv_count:,} ({tv_pct:.2f}%)

KEY FINDINGS
------------
Movies account for {movie_pct:.2f}% of the titles.
TV Shows account for {tv_pct:.2f}% of the titles.

The dataset contains {movie_count - tv_count:,} more
Movies than TV Shows.

LIMITATION
----------
These results describe the content represented in this
dataset. They do not measure viewing hours, popularity,
subscriber preferences, or current Netflix availability.
"""

(OUTPUT_DIR / "task2_completion_report.txt").write_text(
    report.strip() + "\n",
    encoding="utf-8"
)

print("\n" + "=" * 40)
print("TASK 2 OUTPUTS SAVED SUCCESSFULLY")
print(f"Bar chart: {OUTPUT_DIR / 'task2_content_type_bar.png'}")
print(f"Pie chart: {OUTPUT_DIR / 'task2_content_type_pie.png'}")
print(f"Summary CSV: {OUTPUT_DIR / 'task2_content_summary.csv'}")
print(f"Report: {OUTPUT_DIR / 'task2_completion_report.txt'}")
