
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Locate project files
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "processed" / "netflix_cleaned.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load cleaned dataset
df = pd.read_csv(DATA_FILE)

# 2. Prepare country information
# Exclude unknown country values from the country ranking.
country_data = df[["show_id", "country"]].copy()

country_data["country"] = country_data["country"].replace(
    ["Not Given", ""], pd.NA
)

country_data = country_data.dropna(subset=["country"])

# Split comma-separated country names into individual rows
country_data["country"] = country_data["country"].str.split(",")

country_data = country_data.explode("country")
country_data["country"] = country_data["country"].str.strip()

# Remove empty entries and count each title once per country
country_data = country_data[
    country_data["country"].notna()
    & country_data["country"].ne("")
]

country_data = country_data.drop_duplicates(
    subset=["show_id", "country"]
)

# 3. Count titles by country
country_counts = (
    country_data.groupby("country")["show_id"]
    .nunique()
    .sort_values(ascending=False)
)

top_10 = country_counts.head(10)

print("TASK 3: COUNTRY-WISE CONTENT ANALYSIS")
print("=" * 45)
print(f"Countries represented: {country_counts.size}")
print("\nTop 10 countries by title count:")
print(top_10.to_string())

# 4. Save ranking
ranking = top_10.rename("title_count").reset_index()
ranking.to_csv(
    OUTPUT_DIR / "task3_top_10_countries.csv",
    index=False
)

# 5. Create chart
sns.set_theme(style="whitegrid")

fig, ax = plt.subplots(figsize=(11, 7))

sns.barplot(
    data=ranking,
    x="title_count",
    y="country",
    hue="country",
    legend=False,
    ax=ax
)

ax.set_title("Top 10 Countries by Netflix Title Count")
ax.set_xlabel("Number of Titles")
ax.set_ylabel("Country")

fig.tight_layout()
fig.savefig(
    OUTPUT_DIR / "task3_top_10_countries.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close(fig)

# 6. Save findings
report = [
    "TASK 3: COUNTRY-WISE CONTENT ANALYSIS",
    "=" * 40,
    f"Countries represented: {country_counts.size}",
    "",
    "TOP 10 COUNTRIES",
    ranking.to_string(index=False),
    "",
    "METHOD",
    "Titles listing multiple countries are counted once",
    "for each listed country. Unknown country values are",
    "excluded from the ranking.",
    "",
    "LIMITATION",
    "These counts describe the supplied dataset. They do",
    "not measure viewing hours, popularity, or current",
    "Netflix availability."
]

(OUTPUT_DIR / "task3_completion_report.txt").write_text(
    "\n".join(report) + "\n",
    encoding="utf-8"
)

print("\nTask 3 outputs saved successfully.")
print(f"Chart: {OUTPUT_DIR / 'task3_top_10_countries.png'}")
print(f"Ranking: {OUTPUT_DIR / 'task3_top_10_countries.csv'}")
print(f"Report: {OUTPUT_DIR / 'task3_completion_report.txt'}")
