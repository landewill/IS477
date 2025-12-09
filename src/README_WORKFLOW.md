# Source Code Documentation

This directory contains the complete workflow implementation for the College Football Home-Field Advantage Analysis project.

## Overview

The workflow processes raw college football data from two sources (CFBD API and box scores), merges them, engineers features, trains three machine learning models, and quantifies home-field advantage in NCAA FBS football.

## Files

### run_all.py

Main workflow script that orchestrates the complete data pipeline. This script:

1. Loads raw data from the data/raw directory
2. Merges CFBD and box score datasets using fuzzy matching
3. Cleans and filters the data (completed, non-neutral, regular season games)
4. Engineers features while preventing data leakage
5. Trains three models: Logistic Regression, Ridge Regression, and LASSO Regression
6. Quantifies home-field advantage for evenly-matched teams
7. Saves all outputs to data/model, models, and reports directories

### download_data_from_box.py

Script to download pre-processed data from Box.com. Required before running the workflow if you don't have local data files.

## Requirements

### Python Version

Python 3.8 or higher required.

### Required Packages

Install all dependencies using:

```bash
pip install -r requirements.txt
```

Key packages include:
- pandas (data manipulation)
- numpy (numerical operations)
- scikit-learn (machine learning models)
- rapidfuzz (fuzzy string matching for team names)
- python-dateutil (datetime parsing)
- pytz (timezone handling)
- joblib (model persistence)

### Data Requirements

The workflow expects two CSV files in the data/raw directory:

1. cfbd_merged.csv - CFBD API data with game statistics, ELO ratings, venue info
2. cfb_box-scores_2002-2024.csv - Box score data with game results

Download these files using:

```bash
python src/download_data_from_box.py
```

## Usage

### Basic Usage

Run the complete workflow from the project root directory:

```bash
python src/run_all.py
```

This will execute all steps automatically and save outputs.

### Important Notes

Directory Structure: The script must be run from the project root directory (IS477/), not from within the src/ directory. All file paths are relative to the project root.

Example of correct usage:

```bash
cd /path/to/IS477
python src/run_all.py
```

Do not run from src/:

```bash
cd /path/to/IS477/src
python run_all.py  # This will fail
```

The script uses relative paths like "data/raw/..." which assume you're in the project root.

### Output Locations

After running successfully, you will find:

Data:
- data/model/merged_games_model_ready.csv - Feature matrix with targets

Models:
- models/home_field_logistic.pkl - Trained logistic regression model
- models/home_field_ridge.pkl - Trained Ridge regression model
- models/home_field_lasso.pkl - Trained LASSO regression model

Reports:
- reports/model_home_field_metrics.json - Performance metrics for all models
- reports/model_home_field_logit_summary.txt - Home advantage from logistic model
- reports/model_home_field_ridge_summary.txt - Home advantage from Ridge model
- reports/model_home_field_lasso_summary.txt - Home advantage from LASSO model

## Workflow Details

### Step 1: Data Loading

Reads raw CSV files from data/raw directory. Checks for file existence and exits with helpful error message if files are missing.

### Step 2: Data Merging

Matches games between CFBD and box score datasets using:
- Season and week
- Game date and time (with tolerance windows)
- Attendance (when available)
- Fuzzy team name matching (handles variations like "USC" vs "Southern California")

Uses two-pass matching strategy:
1. Attendance-based matching (stricter, for games with attendance data)
2. Time-based matching (for remaining games)

Ensures 1:1 matching - each game appears at most once in the merged dataset.

### Step 3: Data Cleaning

Filters to:
- Completed games only
- Regular season games (excludes bowls, playoffs)
- Non-neutral site games (to measure true home-field advantage)
- Games with valid score data

Creates target variables:
- home_win: Binary indicator (1 if home team won)
- home_margin: Point differential (home score minus away score)

### Step 4: Feature Engineering

Creates features while preventing data leakage:

Difference Features:
- Computes home minus away for all numeric paired columns
- Only includes pre-game features (e.g., pregame ELO, rankings)
- Excludes game outcome features (scores, statistics, postgame metrics)

Missing Data Handling:
- Drops features with more than 50% missing values
- Uses median imputation for remaining missing values
- Ensures no rows are lost due to missing data

Categorical Encoding:
- One-hot encodes conferences (drops first category to avoid multicollinearity)
- Handles missing categories as "Unknown"

### Step 5: Model Training

Trains three models with 80/20 train/test split:

Logistic Regression:
- Predicts home team win probability
- Uses L2 regularization
- Hyperparameters tuned via 5-fold cross-validation
- Optimizes for ROC AUC

Ridge Regression:
- Predicts home team point margin
- Uses L2 regularization
- Hyperparameters tuned via 5-fold cross-validation
- Optimizes for mean absolute error

LASSO Regression:
- Predicts home team point margin
- Uses L1 regularization (automatic feature selection)
- Hyperparameters tuned via 5-fold cross-validation
- Optimizes for mean absolute error
- Reports how many features were selected vs zeroed out

All models use StandardScaler for feature normalization.

### Step 6: Home-Field Advantage Quantification

For each model, computes advantage for an evenly-matched game:

Balanced Game Scenario:
- Sets all difference features to zero (teams are equal)
- Sets other features to median values
- Predicts outcome for this balanced matchup

Logistic Model Output:
- Home team win probability in balanced game
- Percentage point boost from home-field advantage

Regression Model Output:
- Expected point margin in balanced game
- Direct estimate of home-field advantage in points

### Step 7: Output Saving

Saves all artifacts:
- Model-ready dataset with IDs, targets, and features
- Trained model objects (can be loaded with joblib.load)
- Performance metrics in JSON format
- Human-readable summaries in text files

## Reproducibility

This workflow is designed for full reproducibility:

Deterministic Results:
- Random seed set to 42 for all operations
- Train/test splits use same seed
- Model fitting uses same seed

No Manual Steps:
- Entire workflow is automated
- No intermediate files need to be edited
- No hyperparameters need to be manually specified

Version Control:
- All code is in version control
- Data provenance is documented
- Model hyperparameters are saved in output files

## Troubleshooting

Common Issues:

Missing Data Files:
```
ERROR: Data files not found.
```
Solution: Run `python src/download_data_from_box.py` first

Wrong Directory:
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/raw/...'
```
Solution: Make sure you're running from project root, not from src/

Missing Packages:
```
ModuleNotFoundError: No module named 'rapidfuzz'
```
Solution: Run `pip install -r requirements.txt`

Memory Issues:
If you encounter memory errors, the dataset is large. Try:
- Closing other applications
- Using a machine with more RAM
- Running on a subset of years (modify the data loading step)

## Performance Notes

Expected Runtime:
- Data loading: 10-30 seconds
- Data merging: 1-2 minutes
- Feature engineering: 30-60 seconds
- Model training: 5-10 minutes (depends on CPU cores)
- Total: Approximately 10-15 minutes

Memory Usage:
- Peak memory: approximately 2-4 GB
- Requires at least 8 GB system RAM recommended

The script uses all available CPU cores for cross-validation (n_jobs=-1 in GridSearchCV).

## Development Notes

The code in run_all.py is adapted from three Jupyter notebooks:
- Data_merge.ipynb (data merging logic)
- data_clean.ipynb (cleaning and feature engineering)
- model_home_field_advantage.ipynb (modeling and analysis)

The notebooks remain in the repository for development and exploratory analysis, but run_all.py is the production workflow.

Code Style:
- Function-based organization (not class-based)
- Inline comments for complex operations
- Print statements for progress tracking
- Error handling for missing files

## Future Enhancements

Potential improvements:
- Command-line arguments for customization (years, models, hyperparameters)
- Logging to file instead of console output
- Parallel processing for data merging step
- Additional model types (Random Forest, XGBoost)
- Cross-validation results visualization
- Feature importance plots

## Contact

For questions or issues with this workflow, contact the project authors:
- William Lande
- Emil Tomic

See CITATION.cff for complete attribution information.
