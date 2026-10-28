
from pathlib import Path
import pandas as pd

# Locate the project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Load the original dataset
DATA_FILE = PROJECT_DIR / "data" / "raw" / "Dataset.csv"

df = pd.read_csv(DATA_FILE)

# 1. Preview the data
print("\n--- FIRST FIVE ROWS ---")
print(df.head())

# 2. Check the dataset size
print("\n--- DATASET DIMENSIONS ---")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# 3. Inspect column names and data types
print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

print("\n--- DATA TYPES ---")
print(df.dtypes)

# 4. Count missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

# 5. Count duplicate rows
print("\n--- DUPLICATE ROWS ---")
print(df.duplicated().sum())

# 6. Inspect unique values in important text columns
print("\n--- UNIQUE CONTENT TYPES ---")
print(df["type"].value_counts(dropna=False))

print("\n--- UNIQUE RATINGS ---")
print(df["rating"].value_counts(dropna=False))

print("\n--- COUNTRY EXAMPLES ---")
print(df["country"].drop_duplicates().head(15).to_list())

# 7. Check for leading/trailing spaces
print("\n--- TEXT FORMATTING CHECK ---")
for column in ["type", "title", "director", "country", "rating"]:
    if df[column].dtype == "str":
        has_extra_spaces = (
            df[column].dropna()
            .ne(df[column].dropna().str.strip())
            .sum()
        )
        print(f"{column}: {has_extra_spaces} values with extra spaces")

# 8. Check identifier uniqueness
print("\n--- IDENTIFIER CHECK ---")
print("Unique show IDs:", df["show_id"].nunique())
print("Total rows:", len(df))
print("Duplicate show IDs:", df["show_id"].duplicated().sum())

# 9. Check date parsing
parsed_dates = pd.to_datetime(
    df["date_added"], errors="coerce"
)
print("\n--- DATE CHECK ---")
print("Dates that could not be parsed:", parsed_dates.isna().sum())

# 10. Clean and standardize the dataset
df_clean = df.copy()

# Remove completely duplicated rows
df_clean = df_clean.drop_duplicates()

# Remove leading/trailing spaces from text columns
text_columns = df_clean.select_dtypes(include=["str"]).columns

for column in text_columns:
    df_clean[column] = df_clean[column].str.strip()

# Standardize content types
df_clean["type"] = (
    df_clean["type"]
    .str.strip()
    .str.lower()
    .replace({
        "movie": "Movie",
        "tv show": "TV Show"
    })
)

# Standardize country and rating capitalization/spacing
# Preserve "Not Given" because it is an explicit placeholder
# for unavailable country information in this dataset.
df_clean["country"] = df_clean["country"].replace({
    "not given": "Not Given",
    "NOT GIVEN": "Not Given"
})

df_clean["rating"] = df_clean["rating"].str.upper()

# Convert date_added to a proper date type
df_clean["date_added"] = pd.to_datetime(
    df_clean["date_added"],
    errors="coerce"
)

# Report final data quality
print("\n--- FINAL DATA QUALITY REPORT ---")
print("Rows:", len(df_clean))
print("Duplicate rows:", df_clean.duplicated().sum())
print("Missing values:")
print(df_clean.isnull().sum())
print("Unique show IDs:", df_clean["show_id"].nunique())

# Export cleaned dataset
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "netflix_cleaned.csv"

df_clean.to_csv(OUTPUT_FILE, index=False)

print(f"\nCleaned dataset exported to: {OUTPUT_FILE}")
