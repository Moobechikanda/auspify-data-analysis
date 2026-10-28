
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# --------------------------------------------------
# 1. Paths and configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "netflix_cleaned.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")


# --------------------------------------------------
# 2. Load and prepare the dataset
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

required_columns = {"show_id", "type", "rating", "listed_in"}
missing_columns = required_columns.difference(df.columns)

if missing_columns:
    raise ValueError(
        f"The dataset is missing required columns: {sorted(missing_columns)}"
    )

df["type"] = df["type"].astype("string").str.strip()
df["rating"] = df["rating"].astype("string").str.strip()
df["listed_in"] = df["listed_in"].astype("string").str.strip()

# Treat blank strings and common placeholders as missing.
for column in ["rating", "listed_in"]:
    df[column] = df[column].replace(
        ["", "nan", "None", "<NA>", "Not Given"],
        pd.NA
    )

# Use a separate dataset for rating analysis so that missing ratings
# are excluded from rating counts, but remain included in genre analysis.
rating_df = df.dropna(subset=["rating"]).copy()

# Split the genre list into individual genres.
genre_df = df.dropna(subset=["listed_in"])[
    ["show_id", "type", "listed_in"]
].copy()

genre_df["genre"] = genre_df["listed_in"].str.split(",")
genre_df = genre_df.explode("genre")
genre_df["genre"] = genre_df["genre"].str.strip()
genre_df = genre_df[genre_df["genre"].ne("")]
genre_df = genre_df.drop_duplicates(subset=["show_id", "genre"])


# --------------------------------------------------
# 3. Rating category analysis
# --------------------------------------------------

rating_summary = (
    rating_df.groupby("rating")["show_id"]
    .nunique()
    .sort_values(ascending=False)
    .rename("title_count")
    .reset_index()
)

rating_summary["percentage"] = (
    rating_summary["title_count"] / rating_summary["title_count"].sum() * 100
)

rating_summary.to_csv(
    OUTPUT_DIR / "task5_rating_summary.csv", index=False
)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=rating_summary,
    x="title_count",
    y="rating",
)
plt.title("Netflix Titles by Content Rating")
plt.xlabel("Number of Titles")
plt.ylabel("Content Rating")
plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "task5_rating_distribution.png",
    dpi=150,
    bbox_inches="tight",
)
plt.close()


# --------------------------------------------------
# 4. Genre analysis
# --------------------------------------------------

genre_summary = (
    genre_df.groupby("genre")["show_id"]
    .nunique()
    .sort_values(ascending=False)
    .rename("title_count")
    .reset_index()
)

genre_summary["percentage_of_titles"] = (
    genre_summary["title_count"] / df["show_id"].nunique() * 100
)

genre_summary.to_csv(
    OUTPUT_DIR / "task5_genre_summary.csv", index=False
)

top_genres = genre_summary.head(15)

plt.figure(figsize=(11, 7))
sns.barplot(
    data=top_genres,
    x="title_count",
    y="genre",
)
plt.title("Top 15 Netflix Genres")
plt.xlabel("Number of Titles")
plt.ylabel("Genre")
plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "task5_top_genres.png",
    dpi=150,
    bbox_inches="tight",
)
plt.close()


# --------------------------------------------------
# 5. Compare ratings across content types
# --------------------------------------------------

rating_by_type = (
    rating_df.groupby(["rating", "type"])["show_id"]
    .nunique()
    .reset_index(name="title_count")
)

rating_by_type.to_csv(
    OUTPUT_DIR / "task5_rating_by_type.csv", index=False
)

plt.figure(figsize=(12, 7))
sns.barplot(
    data=rating_by_type,
    x="rating",
    y="title_count",
    hue="type",
)
plt.title("Content Ratings: Movies vs TV Shows")
plt.xlabel("Content Rating")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Content Type")
plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "task5_ratings_by_type.png",
    dpi=150,
    bbox_inches="tight",
)
plt.close()


# --------------------------------------------------
# 6. Interactive visualizations using Plotly
# --------------------------------------------------

rating_chart = px.bar(
    rating_summary,
    x="rating",
    y="title_count",
    hover_data=["percentage"],
    title="Interactive Netflix Content Rating Analysis",
    labels={
        "rating": "Content Rating",
        "title_count": "Number of Titles",
        "percentage": "Percentage (%)",
    },
)
rating_chart.write_html(
    OUTPUT_DIR / "task5_interactive_ratings.html"
)

genre_chart = px.bar(
    top_genres.sort_values("title_count"),
    x="title_count",
    y="genre",
    orientation="h",
    title="Interactive Top 15 Netflix Genres",
    labels={
        "genre": "Genre",
        "title_count": "Number of Titles",
    },
)
genre_chart.write_html(
    OUTPUT_DIR / "task5_interactive_genres.html"
)

comparison_chart = px.bar(
    rating_by_type,
    x="rating",
    y="title_count",
    color="type",
    barmode="group",
    title="Interactive Rating Comparison by Content Type",
    labels={
        "rating": "Content Rating",
        "title_count": "Number of Titles",
        "type": "Content Type",
    },
)
comparison_chart.write_html(
    OUTPUT_DIR / "task5_interactive_rating_comparison.html"
)


# --------------------------------------------------
# 7. Generate a completion report
# --------------------------------------------------

total_titles = df["show_id"].nunique()
rated_titles = rating_df["show_id"].nunique()
unrated_titles = total_titles - rated_titles

top_rating = rating_summary.iloc[0]
top_genre = genre_summary.iloc[0]

report_lines = [
    "TASK 5: CONTENT RATING & GENRE ANALYSIS",
    "=" * 48,
    f"Total unique titles: {total_titles:,}",
    f"Titles with a recorded rating: {rated_titles:,}",
    f"Titles without a recorded rating: {unrated_titles:,}",
    f"Distinct rating categories: {rating_summary['rating'].nunique()}",
    f"Distinct genres identified: {genre_summary['genre'].nunique()}",
    "",
    "MOST COMMON CONTENT RATINGS",
    "-" * 30,
]

for _, row in rating_summary.head(10).iterrows():
    report_lines.append(
        f"{row['rating']}: {row['title_count']:,} titles "
        f"({row['percentage']:.2f}%)"
    )

report_lines.extend([
    "",
    "TOP 10 GENRES",
    "-" * 30,
])

for _, row in genre_summary.head(10).iterrows():
    report_lines.append(
        f"{row['genre']}: {row['title_count']:,} titles"
    )

report_lines.extend([
    "",
    "KEY FINDINGS",
    "-" * 30,
    (
        f"The most common rating is {top_rating['rating']} "
        f"({top_rating['title_count']:,} titles)."
    ),
    (
        f"The most common genre is {top_genre['genre']} "
        f"({top_genre['title_count']:,} titles)."
    ),
    (
        "A title may belong to multiple genres, so genre counts "
        "can add up to more than the total number of titles."
    ),
    (
        "Content ratings indicate classification categories; "
        "they do not directly measure viewership or popularity."
    ),
    "",
    "OUTPUTS",
    "-" * 30,
    "task5_rating_summary.csv",
    "task5_genre_summary.csv",
    "task5_rating_by_type.csv",
    "task5_rating_distribution.png",
    "task5_top_genres.png",
    "task5_ratings_by_type.png",
    "task5_interactive_ratings.html",
    "task5_interactive_genres.html",
    "task5_interactive_rating_comparison.html",
])

(OUTPUT_DIR / "task5_completion_report.txt").write_text(
    "\n".join(report_lines),
    encoding="utf-8",
)

print("TASK 5 COMPLETED")
print("=" * 40)
print(f"Total unique titles: {total_titles:,}")
print(f"Titles with ratings: {rated_titles:,}")
print(f"Titles without ratings: {unrated_titles:,}")
print(f"Distinct genres: {genre_summary['genre'].nunique()}")
print()
print("Top 5 ratings:")
print(rating_summary.head(5).to_string(index=False))
print()
print("Top 10 genres:")
print(genre_summary.head(10).to_string(index=False))
print()
print(f"All Task 5 outputs saved to: {OUTPUT_DIR}")
