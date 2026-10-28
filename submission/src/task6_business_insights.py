
from pathlib import Path
import html

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ============================================================
# TASK 6: NETFLIX BUSINESS INSIGHTS REPORT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "netflix_cleaned.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")


# ------------------------------------------------------------
# 1. Load and validate data
# ------------------------------------------------------------

df = pd.read_csv(DATA_PATH)

required_columns = {
    "show_id", "type", "title", "country", "release_year",
    "rating", "duration", "listed_in", "date_added"
}

missing_columns = required_columns.difference(df.columns)

if missing_columns:
    raise ValueError(
        f"Missing required columns: {sorted(missing_columns)}"
    )

df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")

total_rows = len(df)
unique_titles = df["show_id"].nunique()
duplicate_rows = int(df.duplicated().sum())
missing_cells = int(df.isna().sum().sum())

type_summary = (
    df.groupby("type")["show_id"]
    .nunique()
    .sort_values(ascending=False)
    .rename("title_count")
    .reset_index()
)
type_summary["percentage"] = (
    type_summary["title_count"] / unique_titles * 100
)

rating_df = df.dropna(subset=["rating"]).copy()
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

genre_df = df.dropna(subset=["listed_in"])[
    ["show_id", "listed_in"]
].copy()
genre_df["genre"] = genre_df["listed_in"].str.split(",")
genre_df = genre_df.explode("genre")
genre_df["genre"] = genre_df["genre"].str.strip()
genre_df = genre_df[genre_df["genre"].ne("")]
genre_df = genre_df.drop_duplicates(subset=["show_id", "genre"])

genre_summary = (
    genre_df.groupby("genre")["show_id"]
    .nunique()
    .sort_values(ascending=False)
    .rename("title_count")
    .reset_index()
)
genre_summary["percentage_of_titles"] = (
    genre_summary["title_count"] / unique_titles * 100
)

country_df = df.dropna(subset=["country"])[
    ["show_id", "country"]
].copy()
country_df["country"] = country_df["country"].replace(
    ["Not Given", "", "nan"], pd.NA
)
country_df = country_df.dropna(subset=["country"])
country_df["country"] = country_df["country"].str.split(",")
country_df = country_df.explode("country")
country_df["country"] = country_df["country"].str.strip()
country_df = country_df[country_df["country"].ne("")]
country_df = country_df.drop_duplicates(subset=["show_id", "country"])

country_summary = (
    country_df.groupby("country")["show_id"]
    .nunique()
    .sort_values(ascending=False)
    .rename("title_count")
    .reset_index()
)

year_df = df.dropna(subset=["release_year"]).copy()
year_df["release_year"] = year_df["release_year"].astype(int)

year_summary = (
    year_df.groupby("release_year")["show_id"]
    .nunique()
    .sort_index()
    .rename("title_count")
    .reset_index()
)

# Export the main analytical tables.
type_summary.to_csv(OUTPUT_DIR / "task6_content_type_summary.csv", index=False)
rating_summary.to_csv(OUTPUT_DIR / "task6_rating_summary.csv", index=False)
genre_summary.to_csv(OUTPUT_DIR / "task6_genre_summary.csv", index=False)
country_summary.to_csv(OUTPUT_DIR / "task6_country_summary.csv", index=False)
year_summary.to_csv(OUTPUT_DIR / "task6_yearly_summary.csv", index=False)

quality_summary = pd.DataFrame({
    "metric": [
        "Total rows",
        "Unique titles",
        "Duplicate rows",
        "Missing cells",
        "Titles with missing ratings",
        "Titles with missing countries",
        "Titles with missing release years",
        "Titles with missing date_added",
    ],
    "value": [
        total_rows,
        unique_titles,
        duplicate_rows,
        missing_cells,
        int(df["rating"].isna().sum()),
        int(df["country"].isna().sum()),
        int(df["release_year"].isna().sum()),
        int(df["date_added"].isna().sum()),
    ],
})
quality_summary.to_csv(OUTPUT_DIR / "task6_data_quality_summary.csv", index=False)


# ------------------------------------------------------------
# 2. Create interactive charts
# ------------------------------------------------------------

type_fig = px.pie(
    type_summary,
    names="type",
    values="title_count",
    hole=0.45,
    title="Catalogue Composition by Content Type",
)
type_fig.update_traces(textposition="inside", textinfo="label+percent")
type_fig.write_html(OUTPUT_DIR / "task6_content_type.html", include_plotlyjs="cdn")

rating_fig = px.bar(
    rating_summary.sort_values("title_count", ascending=False),
    x="rating",
    y="title_count",
    title="Titles by Content Rating",
    labels={"rating": "Rating", "title_count": "Titles"},
)
rating_fig.write_html(OUTPUT_DIR / "task6_ratings.html", include_plotlyjs="cdn")

genre_fig = px.bar(
    genre_summary.head(15).sort_values("title_count"),
    x="title_count",
    y="genre",
    orientation="h",
    title="Top 15 Genres",
    labels={"genre": "Genre", "title_count": "Titles"},
)
genre_fig.write_html(OUTPUT_DIR / "task6_genres.html", include_plotlyjs="cdn")

country_fig = px.bar(
    country_summary.head(10).sort_values("title_count"),
    x="title_count",
    y="country",
    orientation="h",
    title="Top 10 Countries by Number of Associated Titles",
    labels={"country": "Country", "title_count": "Titles"},
)
country_fig.write_html(OUTPUT_DIR / "task6_countries.html", include_plotlyjs="cdn")

year_fig = px.line(
    year_summary,
    x="release_year",
    y="title_count",
    markers=True,
    title="Netflix Titles by Release Year",
    labels={"release_year": "Release Year", "title_count": "Titles"},
)
year_fig.write_html(OUTPUT_DIR / "task6_release_years.html", include_plotlyjs="cdn")

# Create a single dashboard page containing all charts.
dashboard = make_subplots(
    rows=3,
    cols=2,
    specs=[
        [{"type": "domain"}, {"type": "xy"}],
        [{"type": "xy"}, {"type": "xy"}],
        [{"type": "xy", "colspan": 2}, None],
    ],
    subplot_titles=[
        "Content Type Composition",
        "Content Ratings",
        "Top 15 Genres",
        "Top 10 Countries",
        "Titles by Release Year",
    ],
    vertical_spacing=0.12,
    horizontal_spacing=0.12,
)

dashboard.add_trace(
    go.Pie(
        labels=type_summary["type"],
        values=type_summary["title_count"],
        hole=0.45,
        name="Content Type",
    ),
    row=1, col=1,
)

dashboard.add_trace(
    go.Bar(
        x=rating_summary["rating"],
        y=rating_summary["title_count"],
        name="Ratings",
    ),
    row=1, col=2,
)

dashboard.add_trace(
    go.Bar(
        x=genre_summary.head(15)["title_count"],
        y=genre_summary.head(15)["genre"],
        orientation="h",
        name="Genres",
    ),
    row=2, col=1,
)

dashboard.add_trace(
    go.Bar(
        x=country_summary.head(10)["title_count"],
        y=country_summary.head(10)["country"],
        orientation="h",
        name="Countries",
    ),
    row=2, col=2,
)

dashboard.add_trace(
    go.Scatter(
        x=year_summary["release_year"],
        y=year_summary["title_count"],
        mode="lines+markers",
        name="Release Year",
    ),
    row=3, col=1,
)

dashboard.update_layout(
    title="Netflix Catalogue: Business Intelligence Dashboard",
    height=1200,
    template="plotly_white",
    showlegend=False,
)
dashboard.write_html(
    OUTPUT_DIR / "task6_business_dashboard.html",
    include_plotlyjs="cdn",
)


# ------------------------------------------------------------
# 3. Create a static chart for the submission folder
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))
sns.barplot(
    data=type_summary,
    x="type",
    y="title_count",
)
plt.title("Netflix Catalogue by Content Type")
plt.xlabel("Content Type")
plt.ylabel("Number of Titles")
plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "task6_content_type_chart.png",
    dpi=150,
    bbox_inches="tight",
)
plt.close()


# ------------------------------------------------------------
# 4. Generate evidence-based business insights
# ------------------------------------------------------------

top_type = type_summary.iloc[0]
top_rating = rating_summary.iloc[0]
top_genre = genre_summary.iloc[0]
top_country = country_summary.iloc[0]
top_year = year_summary.loc[year_summary["title_count"].idxmax()]

movie_count = int(
    type_summary.loc[type_summary["type"].eq("Movie"), "title_count"].sum()
)
tv_count = int(
    type_summary.loc[type_summary["type"].eq("TV Show"), "title_count"].sum()
)

insights = [
    (
        f"The dataset contains {unique_titles:,} unique titles. "
        f"It has {total_rows:,} rows, {duplicate_rows:,} duplicate rows "
        f"and {missing_cells:,} missing cells in the loaded cleaned file."
    ),
    (
        f"{top_type['type']} is the most common content type, with "
        f"{int(top_type['title_count']):,} titles "
        f"({top_type['percentage']:.2f}% of the catalogue)."
    ),
    (
        f"{top_rating['rating']} is the most common recorded rating, "
        f"covering {int(top_rating['title_count']):,} titles "
        f"({top_rating['percentage']:.2f}% of titles with ratings)."
    ),
    (
        f"{top_genre['genre']} is the most common genre, associated with "
        f"{int(top_genre['title_count']):,} titles. Titles can have multiple "
        f"genres, so genre counts overlap."
    ),
    (
        f"{top_country['country']} is the country associated with the most "
        f"titles ({int(top_country['title_count']):,}). A title can be "
        f"associated with more than one country."
    ),
    (
        f"The release year with the highest number of titles in this dataset "
        f"is {int(top_year['release_year'])}, with "
        f"{int(top_year['title_count']):,} titles. This is based on release "
        f"year, not the date Netflix added each title."
    ),
]

recommendations = [
    (
        "Catalogue planning: use the genre and content-type summaries to "
        "understand the composition of the available catalogue. Validate "
        "investment decisions against viewing and cost data before acting."
    ),
    (
        "Audience strategy: use content ratings to plan classification-aware "
        "content discovery and messaging, while validating the intended "
        "audience with actual audience research."
    ),
    (
        "International catalogue analysis: use country associations to "
        "identify areas for further investigation. Country counts alone do "
        "not establish demand, profitability, or local audience size."
    ),
    (
        "Trend analysis: compare release years with Netflix addition dates "
        "in future analysis to distinguish content age from acquisition "
        "or catalogue-addition timing."
    ),
    (
        "Data improvement: join this catalogue data with viewership, "
        "completion rates, subscription, licensing-cost, and revenue data "
        "before making financial or performance recommendations."
    ),
]


# ------------------------------------------------------------
# 5. Write the final report
# ------------------------------------------------------------

report = [
    "TASK 6: NETFLIX BUSINESS INSIGHTS REPORT",
    "=" * 55,
    "",
    "EXECUTIVE SUMMARY",
    "-" * 25,
    (
        f"This analysis explores {unique_titles:,} unique Netflix titles "
        "in the supplied dataset. It examines catalogue composition, "
        "content ratings, genres, country associations, and release-year "
        "patterns."
    ),
    "",
    "DATA QUALITY OVERVIEW",
    "-" * 25,
    f"Rows: {total_rows:,}",
    f"Unique titles: {unique_titles:,}",
    f"Duplicate rows: {duplicate_rows:,}",
    f"Missing cells in loaded cleaned dataset: {missing_cells:,}",
    f"Titles with missing ratings: {int(df['rating'].isna().sum()):,}",
    f"Titles with missing countries: {int(df['country'].isna().sum()):,}",
    f"Titles with missing release years: {int(df['release_year'].isna().sum()):,}",
    f"Titles with missing date_added: {int(df['date_added'].isna().sum()):,}",
    "",
    "KEY FINDINGS",
    "-" * 25,
]

report.extend(f"{i}. {insight}" for i, insight in enumerate(insights, start=1))
report.extend(["", "BUSINESS RECOMMENDATIONS", "-" * 25])
report.extend(
    f"{i}. {item}" for i, item in enumerate(recommendations, start=1)
)
report.extend([
    "",
    "LIMITATIONS",
    "-" * 25,
    (
        "This dataset describes catalogue titles. It does not provide "
        "viewership, subscriber demographics, revenue, licensing costs, "
        "or profitability. Therefore, the analysis cannot establish which "
        "titles are most watched or most profitable."
    ),
    (
        "Country and genre counts overlap because a title can have multiple "
        "country and genre associations."
    ),
    (
        "Release-year counts measure the years titles were released, not "
        "the dates they were added to Netflix or produced."
    ),
    (
        "Findings describe this dataset and should not automatically be "
        "treated as a complete representation of Netflix's current catalogue."
    ),
    "",
    "OUTPUT FILES",
    "-" * 25,
    "task6_data_quality_summary.csv",
    "task6_content_type_summary.csv",
    "task6_rating_summary.csv",
    "task6_genre_summary.csv",
    "task6_country_summary.csv",
    "task6_yearly_summary.csv",
    "task6_content_type_chart.png",
    "task6_content_type.html",
    "task6_ratings.html",
    "task6_genres.html",
    "task6_countries.html",
    "task6_release_years.html",
    "task6_business_dashboard.html",
])

(OUTPUT_DIR / "task6_business_insights_report.txt").write_text(
    "\n".join(report),
    encoding="utf-8",
)

print("TASK 6 COMPLETED")
print("=" * 50)
print(f"Total rows: {total_rows:,}")
print(f"Unique titles: {unique_titles:,}")
print(f"Duplicate rows: {duplicate_rows:,}")
print(f"Missing cells: {missing_cells:,}")
print()
print("Top content type:")
print(type_summary.head(1).to_string(index=False))
print()
print("Top rating:")
print(rating_summary.head(1).to_string(index=False))
print()
print("Top genre:")
print(genre_summary.head(1).to_string(index=False))
print()
print("Top country:")
print(country_summary.head(1).to_string(index=False))
print()
print("Year with the highest title count:")
print(top_year.to_string())
print()
print(f"Report saved to: {OUTPUT_DIR / 'task6_business_insights_report.txt'}")
print(f"Dashboard saved to: {OUTPUT_DIR / 'task6_business_dashboard.html'}")
