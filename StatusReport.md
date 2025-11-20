# Status Report: Quantifying Home Field Advantage in College Football

**Course:** IS 477  
**Team:** Emil Tomic, Will Lande  
**Date:** 2025-11-20  
**Repository Artifacts Referenced:** `ProjectPlan.md`, `StatusReport.md`, `notebooks/API_CFBD.ipynb`, `notebooks/kaggle_data.ipynb`, `notebooks/Data_merge.ipynb`, `data/raw/*`

---

## 1. Project Overview and Scope Changes

### 1.1 Original Plan (Milestone 2)

In our original `ProjectPlan.md`, the project goal was:

> *Apply a machine learning model to predict the weekly AP Top 25 College Football Poll.*

The focus was on:
- Collecting team and game data from cfbd.io and Sports Reference.  
- Engineering features (margin of victory, opponent strength, other stats).  
- Training a model to predict AP Top 25 rankings each week, and see if we can outperform the real AP Poll.

### 1.2 Updated Research Question and Goals

After working with the data and considering time constraints, we switched to a more focused problem:

> **New goal:** Quantify home field advantage in FBS college football using a logistic regression model.

We now aim to:
- Build a game level dataset from 2002–2024 containing:
  - Home/away designation, final scores, and game metadata (date, time, venue, attendance).  
  - Team-level performance features (season stats, ELO/AP ranking features).  
- Define an outcome:
  - \(Y = 1\) if the home team wins, \(Y = 0\) otherwise.  
- Fit logistic regression models to estimate how much playing at home increases win probability, controlling for team strength and a small set of covariates.

---

## 2. Progress Update by Original Project Plan Tasks

### 2.1 Data Acquisition

**Planned:**  
Use cfbd.io and SportsReference (or similar) for historical team/game data.

**Completed work:**

- **CFBD API (games + venues)** – `notebooks/API_CFBD.ipynb`  
  - Pulled games for seasons 2002–2024 from `https://api.collegefootballdata.com/games`.  
  - Pulled venues from `https://api.collegefootballdata.com/venues`.  
  - Merged to create dataset with venue/location info.  
  - Saved outputs in `data/raw/` (`cfbd_games_2002_2024.csv`, `cfbd_venues.csv`, `cfbd_merged.csv`).

- **Team Stats via Kaggle** – `notebooks/kaggle_data.ipynb`  
  - Dataset: `college-football-team-stats-2002-to-january-2024` on Kaggle.  
  - We attempted to use the NCAA API (`https://ncaa-api.henrygd.me/openapi`) but it is inactive/outdated and did not return data.  
  - Kaggle provides season-level team stats from 2002–Jan 2024.  
  - Saved cleaned stats to `data/raw/kaggle_team_stats_2002_2024.csv`.
  - `cfb_box-scores_2002-2024.csv` used as the schedule/box-score side of our merge (home/away, date, time, attendance).

**Status:**  
- Game- and venue-level data from CFBD: complete.  
- Team-season stats from Kaggle: downloaded and loaded.  
- NCAA API: evaluated but not used.

---

### 2.2 Data Cleaning, Integration, and Feature Engineering

**Planned:**  
Standardize data sources, merge them, and construct features.

**Work to date – `notebooks/Data_merge.ipynb`:**

- **Time and Date Standardization**
  - `prepare_sched(sched)`  
    - Takes the box-score schedule (`cfb_box-scores_2002-2024.csv`).  
    - Builds a local Eastern Time datetime from `date` + `time_et`.  
    - Creates `sched_game_id`, `date_key`, `time_key` (rounded to 5-minute buckets).  
  - `prepare_cfbd_box(cfbd)`  
    - Parses `startDate` (UTC) from CFBD, converts to US/Eastern, then drops timezone.  
    - Creates `cfbd_game_id`, `date_key`, `time_key` compatible with schedule data.

- **Fuzzy Team-Name Matching and Alignment**
  - Team names differ across datasets (e.g., *“Cal Poly”* vs *“Cal Poly SLO”*).  
  - `add_team_match_score(candidates)`  
    - Uses `rapidfuzz.fuzz.token_sort_ratio` to compute similarity between home and away team names across datasets and averages them into a `match_score`.
    - Sorts candidate pairs by `match_score`.  
    - Enforces a one-to-one match between `sched_game_id` and `cfbd_game_id` above a chosen threshold.
  - `match_cfbd_box(cfbd_raw, box_raw, ...)`  
    - Stage 1: Attendance-based matching(season/week/date/attendance + time window + fuzzy names).  
    - Stage 2: Time-based matching (season/week/date/time_key + tighter time window + fuzzy names).  
    - Combines matches, joins back to the full dataframes.
    - Target merged output: `data/interim/merged_games_cfbd_box_2002_2024.csv`.

- **Mismatch Investigation**
  - One source has ~45k games; the other ~15k.  
  - We are:
    - Logging matched vs. unmatched games by season.  
    - Paying attention to 2002–2003, where full box stats appear less consistent.

**Status:**  
- Time/ID standardization: complete.  
- Fuzzy matching pipeline: implemented and tested on subsets  
- Full 2002–2024 merge: in progress, with remaining work on mismatches and whats going wrong with early 2000s seasons.

---

### 2.3 Modeling and Variable Selection

**Original plan:** AP Top 25 prediction with more complex ML.  
**Current plan:** Logistic regression for home field advantage.

**Status:**  
- Variable selection and model design: in progress conceptually.  
- Modeling implementation: not started, pending final merged dataset (need to fix issues with early 2000 seasons first).

---

### 2.4 Evaluation, Visualization, Automation, and Documentation

- **Evaluation, Visualization, Automation:**
  - Notebooks:  
    - `notebooks/evaluation_and_visualization.ipynb`  
  - Outputs (planned):  
    - Plots of estimated home field advantage over time / by conference.
  - No full workflow system yet; likely to use Snakefile/Snakemake. Need to convert notebooks to python scripts before we can do this effectively.

- **Documentation**
  - `ProjectPlan.md`: original plan (will be updated with new research question and design).  
  - `StatusReport.md`: this document.  
  - We plan to add a brief “How to run” section once the pipeline is fully defined.

---

## 3. Updated Timeline and Task Status

| Task                                             | Original Target | Current Status        | Revised Target Date |
|--------------------------------------------------|-----------------|-----------------------|---------------------|
| Data acquisition (games, venues, team stats)     | Oct 27          | **Completed**         | Done                |
| Initial cleaning & exploratory analysis          | Nov 3           | **Completed (basic)** | Done                |
| Robust merge of CFBD + box-score datasets        | Nov 10          | **In progress**       | Nov 25              |
| Diagnose & resolve mismatches (coverage issues)  | Nov 10          | **In progress**       | Nov 27              |
| Feature engineering for logistic regression      | Nov 17          | **Not started**       | Dec 1               |
| Fit baseline logistic regression model           | Nov 24          | **Not started**       | Dec 5               |
| Extend model & sensitivity analyses              | Dec 1           | **Not started**       | Dec 8               |
| Visualizations & interpretation of home advantage| Dec 3           | **Not started**       | Dec 10              |
| Final documentation & updated ProjectPlan        | Dec 10          | **In progress**       | Dec 10              |

We spent more time than planned on data integration and fuzzy matching, which delayed modeling. The revised timeline reflects this.

---

## 5. Team Member Contribution Summaries


### 5.1 Emil – Contribution Summary

Write your reflection here.

### 5.2 Will – Contribution Summary

During this milestone, I focused on external team stats and dataset integration. I attempted to download data from `sportsreference`, but realized that the website wasn't updated and therefore didn't work. This presented an issue since there weren't too many other data sources to use, but thankfully I found a Kaggle dataset for AP rankings and other stats, some of which were not in our CFBD data already. I Created `kaggle_data.ipynb` to download and inspect the Kaggle team stats dataset from 2002–Jan 2024. I then implemented `Data_merge.ipynb`, including `prepare_sched` and `prepare_cfbd_box` for standardizing timestamps and keys. Fuzzy team-name matching was used, using RapidFuzz to align inconsistent school names.  From here, a two-stage (attendance-based then time-based) matching pipeline plus greedy one-to-one matching. I tried to be as overkill as possible, since that data was quite large and I figured there would be mismatch cases I didn't initially consider. I also helped redefine the project scope toward home field advantage and sketched the initial logistic regression modeling plan.

---

## 6. Next Steps

In the next milestone, we plan to:

1. **Finalize the merged game-level dataset**
   - Run the matching pipeline for all seasons 2002–2024.  
   - Find source of unmatched games and decide how to treat seasons with sparse data (especially 2002–2003).

2. **Engineer modeling features**
   - Merge Kaggle team-season stats into the merged game dataset.  
   - Construct the response variable (home win indicator) and covariates.

3. **Fit and evaluate logistic regression models**
   - Estimate the overall home field advantage effect.  
   - Explore variation by time period and/or conference, other interesting factors if time permits.

4. **Update documentation**
   - Revise documentation with the new research question and updated design.  
   - Add brief run instructions and results/plots
   - Need to create documentation on data quality (FAIR Principles, other topics that are required for project).

