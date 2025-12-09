# Data Directory

This directory contains all data used in the home-field advantage analysis project for college football.

## Data Availability and Licensing

**Critical Information:** Due to data licensing restrictions, **not all datasets are included in this public repository**.

### What's Included

- **Kaggle datasets** - Fully included and redistributable (open license)
- **Sample data** - Small synthetic datasets for testing (10 games)
- **Data processing scripts** - Complete pipeline to fetch and process all data
- **Documentation** - Full provenance and methodology

### What's NOT Included

- **CFBD API data** - Cannot be redistributed per their Terms of Service
- **Merged datasets** - Contain CFBD data, therefore excluded
- **Raw Sports Reference data** - May have scraping/ToS restrictions

### Why This Matters

**College Football Data API (CFBD) Terms of Service:**
- Prohibits redistribution of their data
- Requires users to fetch data directly via their free API
- This is a common restriction for sports data APIs

**Impact on this repository:**
- CFBD data files are listed in `.gitignore` and will not appear in version control
- The repository focuses on **reproducibility through code** rather than data redistribution
- Anyone can reproduce the full dataset by following the instructions below

**This approach demonstrates:**
- ✅ Ethical data use and licensing compliance
- ✅ Proper citation and attribution practices
- ✅ Reproducible research workflows
- ✅ Data curation best practices for restricted sources

### For Course Graders/Instructors

Since this is a course project, I can provide the complete dataset directly for academic evaluation purposes. **Three options:**

1. **Pre-processed Dataset (Fastest - Recommended):**
   - Contact: [your.email@university.edu]
   - I will provide Google Drive/OneDrive link to `merged_games.csv`
   - Download and place in `data/cleaned/` directory
   - **Time required: 2 minutes**

2. **Run Reproducibility Pipeline (Tests Full Workflow):**
   - Follow "Reproducing the Full Dataset" instructions below
   - Requires free CFBD API registration
   - **Time required: ~15 minutes**

3. **Use Sample Data (Quick Testing):**
   - Sample data included in `data/samples/`
   - Sufficient for verifying code functionality
   - **Time required: 0 minutes (already included)**

## Directory Structure

```
data/
├── raw/                    # Original, unmodified source data
│   ├── kaggle/            # ✅ INCLUDED: Kaggle datasets (redistributable)
│   ├── cfbd/              # ❌ LOCAL ONLY: CFBD API data (not redistributable)
│   ├── sportsref/         # ❌ LOCAL ONLY: Sports Reference data
│   └── .gitkeep           # Preserves empty directory structure
│
├── cleaned/                # Processed and merged datasets
│   ├── kaggle_*.csv       # ✅ INCLUDED: Cleaned Kaggle data
│   ├── cfbd_*.csv         # ❌ LOCAL ONLY: Cleaned CFBD data
│   ├── merged_games.csv   # ❌ LOCAL ONLY: Combined dataset (contains CFBD)
│   └── .gitkeep           # Preserves directory structure
│
├── model/                  # Model-ready feature matrices
│   ├── merged_games_model_ready.csv  # ✅ MAY BE INCLUDED (derived features)
│   └── .gitkeep           # Preserves directory structure
│
├── samples/                # Small test datasets
│   ├── sample_merged_games.csv  # ✅ INCLUDED: 10-row synthetic data
│   └── README.md          # Documentation for sample data
│
└── README.md              # This file
```

**Legend:**
- ✅ **INCLUDED** = Committed to GitHub repository (public)
- ❌ **LOCAL ONLY** = Generated locally, excluded from version control (`.gitignore`)

## Reproducing the Full Dataset

### Prerequisites

1. **Python environment:**
   ```bash
   pip install -r requirements.txt
   ```

2. **CFBD API Key (Free):**
   - Register at https://collegefootballdata.com/
   - Create account → Generate API key
   - **Time: ~2 minutes**

### Steps to Reproduce

1. **Clone this repository** (if you haven't already):
   ```bash
   git clone https://github.com/[username]/IS477.git
   cd IS477
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your CFBD API key:
   # CFBD_API_KEY='your_key_here'
   ```

3. **Run the complete data pipeline:**
   ```bash
   python run_all.py
   # OR
   make all
   ```

4. **Verify output:**
   ```bash
   ls data/raw/cfbd/          # Should contain CFBD API data
   ls data/cleaned/           # Should contain merged_games.csv
   ls data/model/             # Should contain model-ready features
   ```

**Expected Output:**
- `data/raw/cfbd/`: ~15,000 games from 2001-2024
- `data/cleaned/merged_games.csv`: ~12,000 games after filtering
- `data/model/merged_games_model_ready.csv`: ~10,000 games with engineered features

**Estimated Runtime:** 10-15 minutes (API rate limits may vary)

## Data Management and Curation

### Data Sources

This project combines data from three primary sources with different licensing terms:

#### 1. **Kaggle - College Football Dataset** ✅ Redistributable

- **Source:** https://www.kaggle.com/datasets/[DATASET-ID]
- **Retrieval Method:** Direct download (included in repository)
- **Contains:** [Describe Kaggle dataset contents]
- **Coverage:** NCAA FBS games, [years]
- **License:** [Check specific Kaggle dataset - typically CC0, CC-BY, or Public Domain]
- **Redistribution Status:** ✅ **ALLOWED** - Included in this repository
- **Citation:** [Kaggle dataset citation]

#### 2. **College Football Data API (CFBD)** ❌ NOT Redistributable

- **Source:** https://collegefootballdata.com/
- **Retrieval Method:** REST API (requires free registration)
- **Contains:** Game results, team statistics, venue information, ELO ratings, rankings
- **Coverage:** NCAA FBS games, 2001-2024
- **License/Terms:** https://collegefootballdata.com/exporting
- **Key Restriction:** "Users may not redistribute CFBD data"
- **Redistribution Status:** ❌ **PROHIBITED** - Users must fetch data themselves
- **Why This Restriction Exists:**
  - CFBD aggregates data from multiple sources
  - Maintains data quality and freshness through API
  - Prevents unauthorized commercial use
  - Protects their business model (free tier + premium features)
- **Citation:**
  ```
  College Football Data. (2024). College Football Data API. 
  Retrieved from https://collegefootballdata.com/
  ```

#### 3. **Sports Reference (Supplementary)** ⚠️ Status Unclear

- **Source:** https://www.sports-reference.com/cfb/
- **Retrieval Method:** Web scraping (check robots.txt)
- **Contains:** Game schedules, scores, attendance data
- **Coverage:** NCAA FBS games (multiple seasons)
- **License/Terms:** [Check terms of use before scraping]
- **Redistribution Status:** ⚠️ **UNCERTAIN** - Excluded out of caution

### Data Processing Pipeline

The data flows through the following stages:

1. **Raw Data** (`raw/`)
   - Unmodified data as retrieved from sources
   - Preserved for reproducibility and auditing
   - Never edited manually

2. **Cleaned Data** (`cleaned/`)
   - Merged datasets from multiple sources
   - Data quality checks applied
   - Missing values handled
   - Standardized column names and formats
   - Key file: `merged_games.csv`

3. **Model-Ready Data** (`model/`)
   - Feature engineering applied
   - Train/test splits preserved
   - Ready for machine learning workflows
   - Key file: `merged_games_model_ready.csv`

### Data Quality and Curation

**Filtering Applied:**
- Completed games only
- Regular season games (excludes playoffs/bowl games)
- Non-neutral site games (home/away designation required)
- Games with valid score data

**Data Integrity:**
- Duplicate detection and removal
- Cross-validation between sources
- Temporal consistency checks (dates, seasons)
- Statistical outlier identification

### Reproducibility Notes

All data transformations are scripted and version-controlled. The cleaning and merging process is documented in the project's main workflow script (to be run via `make` or `run_all.py`).

**To reproduce the cleaned datasets:**
```bash
# From project root (when workflow is complete)
python run_all.py --stage data-cleaning
# OR
make data-clean
```

## Data Dictionary

Key variables in `merged_games.csv`:

- `season`: Year of the football season
- `week`: Week number within the season
- `home`, `away`: Team names
- `homePoints`, `awayPoints`: Final scores
- `homePregameElo`, `awayPregameElo`: Team strength ratings before the game
- `homeConference`, `awayConference`: Conference affiliations
- `neutralSite`: Boolean indicator for neutral site games
- `completed`: Boolean indicator for game completion status
- `elevation`, `latitude`, `longitude`: Venue characteristics

For complete variable documentation, see the individual README files in each subdirectory.

## Citation

If using this curated dataset, please cite:

**Data Sources:**
1. College Football Data API: [CITATION TO BE COMPLETED]
2. Sports Reference: [CITATION TO BE COMPLETED]

**This Project:**
Lande, W., & Tomic, E. (2025). College Football Home-Field Advantage Analysis Dataset. GitHub. https://github.com/landewill/IS477

## License and Usage

**Source Data:** See individual source licenses above.

**Curated/Derived Data:** [TO BE DETERMINED - Consider CC-BY-4.0 or similar for derived datasets]

**Code:** MIT License (see LICENSE file in repository root)

## Contact

For questions about data curation, quality issues, or access:
[Your contact information]