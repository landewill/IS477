# Project Plan – “A Machine Learning Approach to Predicting the AP Top 25”

## Overview
This project applies machine learning to model and predict the weekly **AP Top 25 College Football Poll** using publicly available, ethically sourced data.  
We aim to build a **reproducible pipeline** that ingests team-level performance statistics and historical poll results, cleans and integrates them, then trains predictive models (e.g., Logistic Regression, Random Forest, or Gradient Boosted Trees) to forecast ranking movements.  
The project will demonstrate an end-to-end data lifecycle—from acquisition via APIs to storage, integration, model training, evaluation, and visualization—illustrating how modern analytics can quantify human voting behavior in sports.

---

## Research Questions
1. **Primary Question:**  
   Can team performance metrics (win margin, opponent strength, offensive/defensive stats) accurately predict a team’s AP Top 25 ranking each week?
2. **Secondary Questions:**  
   - Which features are most important for poll ranking decisions?  
   - How consistent are AP voters’ implicit “weights” over multiple seasons?  
   - Does model accuracy vary across Power Five vs. Group of Five conferences?

---

## Team and Roles
| Member | Responsibilities |
|---------|------------------|
| **Will Lande** | Lead data integration, statistical modeling, and workflow automation.  Implement and evaluate machine-learning algorithms; document reproducibility steps. |
| **Emil Tomic** | Lead data acquisition, cleaning, and feature engineering.  Manage API access, metadata documentation, and ensure compliance with data-use policies.  Assist with visualization and reporting. |

Both members will contribute equally to version control (Git commits), Markdown documentation, and presentation.

---

## Datasets
We will integrate at least **two distinct, licensed, and trustworthy datasets**:

1. **College Football Data API (cfbd.io)**  
   - *Access:* [https://api.collegefootballdata.com](https://api.collegefootballdata.com)  
   - *Format:* JSON via HTTPS requests (requires free API key).  
   - *Content:* Team-level stats, game outcomes, opponent ratings, and **AP Poll results** (1998-present).  
   - *Purpose:* Primary source for both model features (performance data) and labels (AP ranks).  

2. **Sports Reference – College Football (“sportsreference” Python package)**  
   - *Access:* [https://www.sports-reference.com/cfb/](https://www.sports-reference.com/cfb/)  
   - *Format:* HTML tables → CSV or via Python library (MIT license).  
   - *Content:* Historical box scores, offensive/defensive efficiency, strength of schedule, and advanced metrics.  
   - *Purpose:* Supplementary features (yards per play, turnover margin, possession time) for integration with cfbd data.

**Integration Plan:**  
Datasets will be joined by `team`, `season`, and `week`.  
All transformations (normalization, feature scaling, missing-value handling) will occur in Python (Pandas/NumPy) prior to modeling.  
Cleaned tables will be stored in a local PostgreSQL database or structured `/data` folder for reproducibility.

---

## Timeline & Task Assignments
| Week | Dates (approx.) | Tasks | Responsible Member(s) |
|------|-----------------|--------|------------------------|
| 1 | Oct 13 – Oct 20 | Finalize project scope, set up GitHub repo, obtain API keys, test endpoints. | Both |
| 2 | Oct 21 – Oct 27 | Write data-acquisition scripts (cfbd + sportsreference); create schema README. | Partner |
| 3 | Oct 28 – Nov 3 | Clean and merge datasets; feature engineering (win margin, strength index, recent form). | Will |
| 4 | Nov 4 – Nov 11 | Prototype ML models (Logistic Regression, Random Forest); draft Status Report. | Both |
| 5 | Nov 12 – Nov 24 | Model tuning (Grid Search CV); add visualizations (feature importance, confusion matrix). | Will |
| 6 | Nov 25 – Dec 5 | Automate pipeline (Snakemake or `run_all.py`); document metadata & dependencies. | Both |
| 7 | Dec 6 – Dec 10 | Finalize report (`README.md`), reproducibility tests, Box upload, final release. | Both |

---

## Constraints
- **API Rate Limits:** cfbd API limits ~60 requests/minute; scripts will include throttling and caching.  
- **Data Coverage:** Some advanced stats missing before 2000; we’ll restrict training years for consistency.  
- **Computation:** Model training may require Colab Pro runtime for larger datasets.  
- **Licensing:** Both APIs allow educational reuse with attribution; licenses will be cited in README.  

---

## Gaps / Areas for Input
- **Model selection:** Need instructor feedback on acceptable model complexity (e.g., tree ensemble vs. neural net).  
- **Feature scope:** Determine whether to include betting lines or recruiting data as predictors (may raise policy issues).  
- **Reproducibility tools:** Decide between Snakemake vs. Makefile workflow depending on course guidance.  

---

## Anticipated Later Modules
- **Data Quality (Module 9):** Check completeness by team/week; handle missing values.  
- **Data Cleaning (Module 10):** Normalize team names, season formats, duplicate entries.  
- **Workflow Automation (Modules 11–12):** Build pipeline that executes end-to-end from API call to model output.  
- **Reproducibility (Module 13):** Include requirements.txt and versioned outputs.  
- **Metadata (Module 15):** Add data dictionary and schema.org JSON-LD metadata block.

---

**Deliverables**
- `ProjectPlan.md` (this document)  
- `data/` folder structure + schema description  
- Initial Python scripts (`get_cfbd.py`, `get_srdata.py`)  
- GitHub tag: `project-plan` for release submission  

---