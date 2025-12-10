# Data Directory

This directory contains all data used in the home-field advantage analysis project for college football.

## Data Availability and Licensing

**Critical Information:** Due to data licensing restrictions, **we store all data, including all of our raw data, in Box**.

### What's Included in Box.com Download

**For course graders:** The Box.com shared folder contains this entire `data/` directory with **all datasets included**:
- CFBD data files 
- Merged datasets (`merged_games.csv`)
- Kaggle data
- Model data
- This README file

**Simply download the Box folder and place it in your local repository to have all data ready.**


### Why This Matters

**College Football Data API (CFBD) Terms of Service:**
- Prohibits redistribution of their data
- Requires users to fetch data directly via their free API
- This is a common restriction for sports data APIs

**Impact on this repository:**
- CFBD data files are listed in `.gitignore` and will not appear in version control
- The repository focuses on reproducibility through code rather than data redistribution
- Anyone can reproduce the full dataset by following the instructions below

**This approach demonstrates:**
- Ethical data use and licensing compliance
- Proper citation and attribution practices
- Reproducible research workflows
- Data curation best practices for restricted sources

### For Course Graders/Instructors

**Quick Start:**
1. Download the complete `data/` folder from Box.com (link provided via course submission)
2. Place it in your cloned repository to replace the empty `data/` directory
3. All datasets are now ready - proceed to run `python src/run_all.py` or explore the data directly

**Note:** The Box download includes all CFBD data, merged datasets, and Kaggle data. No additional data fetching required.

## Directory Structure

```
data/
├── raw/                    # Original, unmodified source data
│   ├── cfb_box-scores_2002-2024.csv  # Kaggle datasets (redistributable)
│   └── cfbd_merged.csv   # CFBD API data (not redistributable)
│
├── cleaned/                # Processed and merged datasets
│   └── merged_games.csv   # Combined dataset 
│
├── model/                  # Model-ready feature matrices
│   └── merged_games_model_ready.csv  # MAY BE INCLUDED (derived features)
│
└── README.md              # This file
```

## Reproducing the Analysis

### Use Pre-Downloaded Data from Box

1. **Clone this repository:**
   ```bash
   git clone https://github.com/landewill/IS477.git
   cd IS477
   ```

2. **Download complete data directory from Box.com:**
   - Access the Box.com shared folder (link provided via course submission)
   - Download the entire `data/` folder
   - Place into repository/replace the empty `data/` directory in your local repository
   - Verify: `ls data/raw/` should show `cfbd_merged.csv` and `cfb_box-scores_2002-2024.csv`

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the complete analysis pipeline:**
   ```bash
   python src/run_all.py
   ```

5. **Verify output:**
   ```bash
   ls models/                 # Should contain trained models
   ls reports/                # Should contain home advantage analysis
   ```

**Expected Output:**
- `models/*.joblib`: Trained Logistic, Ridge, and LASSO models
- `reports/*.csv`: Home field advantage quantification results

## Data Management and Curation

### Data Sources

This project combines data from two primary sources with different licensing terms:

#### 1. **Kaggle - College Football Dataset** Redistributable

- **Source:** https://www.kaggle.com/datasets/cviaxmiwnptr/college-football-team-stats-2002-to-january-2024/data
- **Retrieval Method:** Direct download (included in repository)
- **Contains:** Dataset includes every game that involves an FBS (Division I-A) NCAA football team
- **Coverage:** NCAA FBS games, away teams, date, attendence, etc
- **License:** CC0: Public Domain
- **Redistribution Status:** **ALLOWED** - Included in this repository
- **Citation:** 
```
Cviaxmiwnptr. (2025, January 24). College Football Game Stats: 2002 to January 2025. Kaggle. https://www.kaggle.com/datasets/cviaxmiwnptr/college-football-team-stats-2002-to-january-2024/data 
```

#### 2. **College Football Data API (CFBD)** Not Redistributable

- **Source:** https://collegefootballdata.com/
- **Retrieval Method:** Downloaded from Box.com (for academic evaluation)
- **Original Source:** REST API (requires free registration)
- **Contains:** Game results, team statistics, venue information, ELO ratings, rankings
- **Coverage:** NCAA FBS games, 2001-2024
- **License/Terms:** https://collegefootballdata.com/exporting
- **Key Restriction:** "Users may not redistribute CFBD data"
- **Redistribution Status:** Prohibited
- **Academic Access:** Available via Box.com for course evaluation purposes only
- **Citation:**
  ```
  College Football Data. (2024). College Football Data API. 
  Retrieved from https://collegefootballdata.com/
  ```

### Data Processing Pipeline

The data flows through the following stages:

1. **Raw Data** (`raw/`)
   - Unmodified data as retrieved from sources
   - Preserved for reproducibility and auditing

2. **Cleaned Data** (`cleaned/`)
   - Merged datasets from multiple sources
   - Data quality checks applied
   - Missing values handled
   - Standardized column names and formats
   - Key file: `merged_games.csv`

3. **Model-Ready Data** (`model/`)
   - Feature engineering applied
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

All data transformations are scripted and version-controlled. The cleaning and merging process is documented in the project's main workflow script.

**To reproduce the cleaned datasets:**
```bash
# From project root
python src/run_all.py
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
1. College Football Data API: ```
  College Football Data. (2024). College Football Data API. 
  Retrieved from https://collegefootballdata.com/
  ```
2. Kaggle: 
```
Cviaxmiwnptr. (2025, January 24). College Football Game Stats: 2002 to January 2025. Kaggle. https://www.kaggle.com/datasets/cviaxmiwnptr/college-football-team-stats-2002-to-january-2024/data 
```
**This Project:**
Lande, W., & Tomic, E. (2025). College Football Home-Field Advantage Analysis Dataset. GitHub. https://github.com/landewill/IS477

## License and Usage
- MIT License (see LICENSE file in repository root)

**Source Data:** See individual source licenses above.

## Contact

For questions about data curation, quality issues, or access:
[emilt2@illinois.edu] OR [willl2@illinois.edu]