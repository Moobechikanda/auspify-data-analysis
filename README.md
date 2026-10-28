# Netflix Data Analysis Using Python

## Project Overview

This project analyses a Netflix titles dataset using Python, pandas, Matplotlib, Seaborn, and Plotly. It was completed as part of the Auspify Technologies Data Analysis Using Python internship tasks.

The project explores data cleaning, content-type distribution, country associations, release-year trends, content ratings, genres, and catalogue-level business insights.

## Objectives

- Clean and prepare the dataset for analysis.
- Compare the distribution of Movies and TV Shows.
- Identify countries associated with the largest number of titles.
- Examine the distribution of titles by release year.
- Analyse content ratings and common genres.
- Present findings through charts, interactive visualizations, and a written report.

## Technology Stack

- Python
- pandas
- Matplotlib
- Seaborn
- Plotly
- Visual Studio Code

## Project Structure

```text
auspify-data-analysis/
├── data/
│   ├── raw/
│   │   └── Dataset.csv
│   └── processed/
│       └── netflix_cleaned.csv
├── src/
│   ├── task1_cleaning.py
│   ├── task2_content_types.py
│   ├── task3_country_analysis.py
│   ├── task4_release_trends.py
│   ├── task5_rating_genre_analysis.py
│   └── task6_business_insights.py
├── outputs/
├── screenshots/
│   ├── task1/
│   ├── task2/
│   ├── task3/
│   ├── task4/
│   ├── task5/
│   └── task6/
├── .venv/
└── README.md
```

## Dataset

The analysis uses the Netflix titles dataset stored in `data/raw/Dataset.csv`. The cleaned dataset is stored in `data/processed/netflix_cleaned.csv`.

The analysed dataset contains 8,790 unique titles and 10 columns. The fields include content type, title, director, country, date added, release year, rating, duration, and genre classifications.

## Tasks Completed

### Task 1 — Netflix Data Cleaning and Preparation

- Inspected dataset dimensions, data types, missing values, and duplicates.
- Standardized selected text fields.
- Prepared and exported the cleaned dataset.

### Task 2 — Content Type Analysis

- Compared Movies and TV Shows.
- Generated distribution charts and a summary report.

**Finding:** Movies account for 6,126 titles (69.69%), while TV Shows account for 2,664 titles (30.31%).

### Task 3 — Country-Wise Content Analysis

- Split multi-country entries into individual country associations.
- Ranked countries by the number of associated titles.
- Generated a top-10 country chart and summary.

**Finding:** The United States is associated with 3,240 titles in the dataset.

### Task 4 — Trend Analysis by Release Year

- Counted titles by release year.
- Generated a yearly trend visualization and CSV summary.

**Finding:** 2018 has the highest title count in this dataset, with 1,146 titles.

### Task 5 — Content Rating and Genre Analysis

- Analysed content-rating categories.
- Identified common genres.
- Compared ratings across content types.
- Created static and interactive visualizations.

**Findings:** TV-MA is the most common recorded rating, with 3,205 titles. International Movies is the most common genre, associated with 2,752 titles.

### Task 6 — Netflix Business Insights Report

- Conducted exploratory data analysis.
- Combined catalogue, rating, genre, country, and release-year findings.
- Created interactive charts and a combined dashboard.
- Prepared a written business insights report and data-quality summary.

The combined dashboard is available at `outputs/task6_business_dashboard.html`.

## How to Run

### 1. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install pandas matplotlib seaborn plotly
```

### 3. Run the analysis scripts

Run from the project root:

```powershell
python src/task1_cleaning.py
python src/task2_content_types.py
python src/task3_country_analysis.py
python src/task4_release_trends.py
python src/task5_rating_genre_analysis.py
python src/task6_business_insights.py
```

### 4. Open the interactive dashboard

```powershell
Start-Process .\outputs\task6_business_dashboard.html
```

Some interactive charts use Plotly's CDN and may require an internet connection to render.

## Key Limitations

This dataset describes titles in a catalogue. It does not include viewing hours, subscriber demographics, revenue, licensing costs, or profitability.

Country and genre counts can overlap because a title may be associated with multiple countries and genres. Release-year counts describe the titles' release years, not when they were added to Netflix.

Business recommendations should therefore be treated as directions for further investigation, not conclusions about actual viewing behaviour or financial performance.

## Project Deliverables

- Python source scripts for six tasks.
- Cleaned dataset.
- CSV analytical summaries.
- Static charts.
- Interactive HTML visualizations.
- Business insights report.
- Screenshots documenting completed work.

## Author

Prepared for the Auspify Technologies Data Analysis Using Python internship.
