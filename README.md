# Quantifying Home-Field Advantage in NCAA FBS College Football Using Machine Learning

## Contributors

- **William Lande** ([ORCID: 0000-0002-3055-7198](https://orcid.org/0000-0002-3055-7198))
- **Emil Tomic**

## Summary

This project quantifies home-field advantage in NCAA Football Bowl Subdivision (FBS) college football using machine learning models trained on comprehensive game data from 2002-2024. The central research question investigates: **How much does playing at home influence game outcomes in college football when controlling for team strength and other factors?**

Home field advantage is a phenomenon in sports, but quantifying its magnitude takes statistical modeling to seperate venue effects from differences in team quality. This project addresses that challenge by integrating two complementary datasets containing over 15,000 FBS games and training three machine learning models: Logistic Regression (for win probability), Ridge Regression, and LASSO Regression for point margin prediction.

The motivation stems from both practical and academic interests. For sports analysts, coaches, and bettors, understanding home-field advantage provides insights for game predictions. From a data science perspective, this project demonstrates end-to-end reproducible research practices.

Our analysis pipeline begins by merging game-level data from the College Football Data (CFBD) API with box score statistics from Kaggle. The CFBD dataset provides game outcomes, venue information, team ELO ratings, and AP poll rankings, while the Kaggle dataset contributes detailed box scores including attendance, game times, and team identifiers. Merging these datasets required fuzzy string matching to deal with inconsistent team naming across sources and datetime alignment to match games across datasets.

After data integration, we engineered 83 features capturing team strength (ELO ratings, AP rankings), game context (attendance, venue type), and matchup characteristics (ranking differential). It was important to prevent data leakage by ensuring no future information contaminated the training data.

We trained three complementary models using scikit-learn with hyperparameter tuning via grid search cross-validation:

1. **Logistic Regression**: Predicts binary home team win probability. This model achieved 75.7% test accuracy and 0.825 ROC-AUC, indicating strong predictive performance. For games where team statistics are equal, the model estimates the home team wins 69.0% of the time, representing a 19 percentage point advantage over the expected 50% for neutral venues.

2. **Ridge Regression**: Predicts home team point margin using L2 regularization. This model achieved an R^2 of 0.439 and RMSE of 16.6 points on test data. For evenly matched teams, it predicts the home team wins by 14.4 points on average.

3. **LASSO Regression**: Predicts point margin using L1 regularization for automatic feature selection. With R^2 of 0.438 and selecting 76 of 83 features, this model estimates a 16.8 point home advantage for balanced games while identifying the most predictive factors.

Key findings reveal substantial and consistent home field advantage across all models. The logistic model shows home teams win nearly 70% of evenly-matched contests, while regression models estimate home teams score 14-17 more points than equal away opponents.

Visualizations generated as part of this analysis include ROC curves , residual plots showing model fit quality, and feature importance charts from the LASSO model. These diagnostic outputs confirm model assumptions and provide interpretable insights into the factors influencing game outcomes.

This project represents a complete, reproducible data science workflow from acquisition through analysis. The workflow is fully automated via the `run_all.py` script. We provide comprehensive documentation enabling independent reproduction of our results.

Beyond academic rigor, this project demonstrates practical skills in data curation, integration, quality assessment, machine learning, and workflow automation. The findings contribute quantitative evidence to the sports analytics literature while the methodology provides a template for reproducible research in computational social science.

## Data Profile

This project integrates two primary datasets covering NCAA FBS college football games from 2002-2024. Each dataset serves complementary purposes and operates under different ethical and legal constraints.

### Dataset 1: College Football Data (CFBD) API

**Source**: [https://collegefootballdata.com/](https://collegefootballdata.com/)

**Description**: The CFBD API provides comprehensive college football data including game results, team statistics, venue information, ELO ratings, and AP poll rankings. Data was retrieved via REST API endpoint s for games and venues across seasons 2002-2024.

**Coverage**: 
- Over 15,000 FBS games spanning 23 seasons
- Game-level outcomes (scores, dates, locations)
- Team performance metrics (ELO ratings, rankings)
- Venue information (capacity, location, grass/turf)
- Weekly AP Top 25 poll rankings

**Format**: Originally JSON via HTTPS requests, converted to CSV for analysis

**Retrieval Method**: API access requires free registration at collegefootballdata.com. Data was fetched using Python requests library with appropriate rate limiting (60 requests/minute) to comply with API terms.

**Ethical and Legal Constraints**:
- **Licensing**: CFBD Terms of Service explicitly prohibit redistribution of their data. Users must fetch data directly from the API. Data is provided through the Box link in the release as well, and this is the prefered method for grading.
- **Attribution**: CFBD requires citation in any publications or projects using their data.
- **Commercial Use**: Free tier is for educational/personal use.

**Citation**:
```
College Football Data. (2024). College Football Data API. 
Retrieved from https://collegefootballdata.com/
```

**Data Quality Notes**:
- CFBD data is well-maintained with minimal missing values
- ELO ratings and rankings not available for all teams in early years
- Venue information occasionally missing or inconsistent for neutral site games

### Dataset 2: Kaggle College Football Box Scores (2002-2024)

**Source**: [https://www.kaggle.com/datasets/cviaxmiwnptr/college-football-team-stats-2002-to-january-2024/data](https://www.kaggle.com/datasets/cviaxmiwnptr/college-football-team-stats-2002-to-january-2024/data)

**Description**: This dataset contains box score information for NCAA FBS games including team names, dates, times, attendance figures, and final scores. It provides complementary scheduling and attendance data not available in CFBD.

**Coverage**:
- Over 45,000 games (includes FCS and other divisions beyond FBS)
- Game scheduling information (dates, times in Eastern Time)
- Attendance figures
- Home/away team designations
- Final scores

**Format**: CSV file (`cfb_box-scores_2002-2024.csv`)

**Retrieval Method**: Direct download from Kaggle (included in Box.com data distribution for this project)

**Ethical and Legal Constraints**:
- **License**: CC0: Public Domain - no restrictions on use or redistribution
- **Attribution**: We cite the dataset creator as best practice
- **Privacy**: Contains only aggregated game-level data, no personal information

**Citation**:
```
Cviaxmiwnptr. (2025, January 24). College Football Game Stats: 2002 to January 2025. 
Kaggle. https://www.kaggle.com/datasets/cviaxmiwnptr/college-football-team-stats-2002-to-january-2024/data
```

**Data Quality Notes**:
- Includes games beyond FBS level, requiring filtering
- Team naming inconsistencies compared to CFBD dataset
- Some missing attendance values for smaller games
- Time zone standardization required (all times provided in Eastern Time, not UTC)

### Data Integration Considerations

Merging these datasets presented significant challenges:

1. **Team Name Harmonization**: Different naming conventions required fuzzy string matching using `rapidfuzz` library to align team identifiers across datasets.

2. **Temporal Alignment**: Game times required conversion from UTC (CFBD) and Eastern Time (Kaggle) to a common timezone with bucketing to 5-minute intervals to account for small recording differences.

3. **Coverage Discrepancies**: CFBD focuses on FBS games (~15k) while Kaggle includes all college levels (~45k), necessitating careful filtering and match validation.

4. **Missing Data**: Early seasons (2002-2003) have less complete statistics, particularly for non-power conference teams.

The final merged dataset contains approximately 12,000 games with complete feature coverage after filtering for regular season, non-neutral site, FBS games with complete statistics.

### Ethical Considerations

Both datasets contain only aggregated statistics without personal information, eliminating privacy concerns. The primary ethical consideration is compliance with CFBD's redistribution prohibition. Our solution—hosting data on Box.com. 

## Data Quality

Ensuring high data quality was critical to producing reliable home-field advantage estimates. We conducted systematic quality assessment across multiple dimensions: completeness, accuracy, consistency, and validity. This section summarizes our profiling methodology, findings, and remediation steps.

### Quality Assessment Methodology

Our quality assessment focused on:

1. **Integration Validation**: After merging datasets, assessed match quality and logical consistency of joined records.

2. **Feature Engineering Checks**: Validated derived features for data leakage and excluded features with >50% missing data.

3. **Model Input Validation**: Final verification that training data contains no missing values and features are properly scaled.

### Dataset-Specific Quality Findings

#### CFBD API Data (`cfbd_merged.csv`)

**Completeness**:
- Game outcomes (scores, dates): >99% complete
- ELO ratings: ~85% complete (missing for lower-tier teams, especially pre-2010)
- AP rankings: ~60% complete (only ranked teams have values)
- Venue information: ~95% complete

**Accuracy**:
- Date/time stamps occasionally show timezone inconsistencies (UTC vs local time)

**Consistency**:
- Team naming generally consistent within dataset
- Some venues have multiple name variations (e.g., stadium renames)

**Issues Identified**:
- Neutral site games flagged inconsistently (some bowl games marked as home games)
- ELO ratings occasionally missing for teams in transition years (conference realignment)
- Overtime games not explicitly flagged, this impacts margin calculations

#### Kaggle Box Scores (`cfb_box-scores_2002-2024.csv`)

**Completeness**:
- Game identifiers, dates, teams: 100% complete
- Attendance: ~80% complete (missing for smaller games)
- Game times: ~95% complete

**Accuracy**:
- Game dates and scores appear consistent across sources

**Consistency**:
- Team naming highly inconsistent (e.g., "Miami" vs "Miami (FL)", "USC" ambiguity)
- Time zones mixed
- Date formats inconsistent across years

**Issues Identified**:
- Includes FCS and lower division games not in CFBD
- Some games have placeholder "TBD" or "0" for attendance

**Remediation**:
- Filtered to completed, regular season, non-neutral site games
- Standardized all times to Eastern Time, rounded to 5-minute buckets

### Integration Quality Assessment

Merging CFBD and Kaggle datasets required sophisticated matching algorithms due to inconsistent team naming and time recording. We validated merge quality through multiple approaches:

**Match Validation**:
- **Fuzzy Matching Threshold**: Set token sort ratio ≥ 80 for team name matches after testing on hand-labeled sample (F1 = 0.94)
- **Temporal Windows**: Allowed ±15 minute window for game start times to account for recording differences
- **Attendance Validation**: For attendance-based matching, required exact attendance match plus date/season/week alignment
- **Score Consistency**: Verified final scores agree between datasets (99.1% agreement in matched games)

**Match Statistics**:
- Successfully matched: 12,347 games (82% of CFBD data)
- Unmatched CFBD games: 2,653 (primarily early seasons, conference realignment years)
- Unmatched Kaggle games: 32,847 (primarily FCS/Division II/III games)

**Quality Flags**:
- Neutral site games excluded from analysis by filtering neutralSite == False

### Feature Engineering Quality Checks

Engineered features introduced new quality concerns, particularly around data leakage:

**Temporal Consistency**:
- Train/test splits use random sampling with fixed seed for reproducibility

**Data Leakage Prevention**:
- Fitted StandardScaler exclusively on training data
- Computed opponent strength using only games available at prediction time
- Excluded concurrent-week rankings from features

**Statistical Properties**:
- Features with >50% missing data automatically excluded during feature engineering

### Missing Data Handling

Missing data patterns varied by variable type:

**Missing Value Strategy**:
- Features with >50% missing data excluded from analysis
- Remaining missing values imputed using median for numeric features
- Categorical features with missing values filled with 'Unknown' category

### Final Dataset Quality Summary

After all cleaning and integration steps, our model-ready dataset contains:

- **12,347 games** with complete feature coverage
- **83 features** (including engineered features, team stats, game context)
- **0% missing values** in final dataset (all handled via imputation or filtering)
- **Temporal range**: 2002-2024 regular season games
- **Games excluded**: Neutral site games (bowl games, conference championships), games with incomplete statistics, non-FBS matchups

**Quality Metrics**:
- Data completeness: 100% (after filtering)
- Target variable balance: 62.8% home wins (reasonable given home advantage exists)
- Temporal coverage: 23 seasons with >400 games per season average

### Quality Assurance Process

To maintain quality throughout the workflow:

1. **Print Statements**: Script outputs progress messages showing games filtered and features created
2. **Reproducibility**: Fixed random seed (42) ensures consistent train/test splits and CV folds
3. **Documentation**: All quality decisions documented in code comments and this report

The resulting dataset provides a high-quality foundation for modeling home-field advantage with confidence in the reliability and validity of our findings.

## Findings

Our analysis quantified home-field advantage in NCAA FBS college football using three machine learning models, revealing consistent and substantial advantages for home teams across multiple metrics.

### Model Performance

#### Logistic Regression (Win Probability)

The logistic regression classifier achieved strong predictive performance:
- **Test Accuracy**: 75.7%
- **ROC-AUC**: 0.825
- **Precision**: 78.3%
- **Recall**: 84.9%
- **F1 Score**: 0.814

These metrics indicate the model reliably distinguishes between home wins and losses. The ROC curve (see `reports/logistic_roc_curve.png`) shows excellent discrimination ability, with the curve well above the diagonal baseline.

**Best Hyperparameters** (via 5-fold cross-validation):
- Penalty: L2 regularization
- C: 0.01 (inverse regularization strength)
- Solver: LBFGS

#### Ridge Regression (Point Margin)

The Ridge regression model predicting home team point margin achieved:
- **Test MAE**: 13.2 points
- **Test RMSE**: 16.6 points
- **Test R²**: 0.439

An R² of 0.439 indicates the model explains 44% of variance in game outcomes, a solid result given the inherent unpredictability of sports. The residual plot (`reports/ridge_residual_plot.png`) shows residuals approximately centered at zero with consistent variance, confirming model assumptions.

**Best Hyperparameter**: α = 10 (regularization strength)

#### LASSO Regression (Point Margin with Feature Selection)

The LASSO model with L1 regularization performed similarly while automatically selecting features:
- **Test MAE**: 13.2 points
- **Test RMSE**: 16.6 points
- **Test R²**: 0.438
- **Features Selected**: 76 of 83 total features

**Best Hyperparameter**: α = 0.001

LASSO's feature importance analysis (`reports/lasso_feature_importance.png`) reveals the most predictive variables:
- **Top Predictors**: Home/away ELO ratings, season win percentages, AP poll rankings, historical head-to-head records
- **Moderate Predictors**: Opponent strength, conference affiliation, time of season
- **Weak Predictors**: Attendance, game time, weather-related proxies

Seven features received zero weight and were effectively excluded, including redundant team statistics and highly correlated variables.

### Home-Field Advantage Quantification

The central finding is a **substantial and consistent home-field advantage**:

#### Logistic Model Results

- **Observed Home Win Rate**: 62.8% across all games in dataset
- **Model-Predicted Average**: 62.8% (excellent calibration)
- **Balanced Game Prediction**: When all team statistics are set to equal (evenly-matched teams), the home team has a **69.0% win probability**
- **Home Advantage**: **19 percentage points** above the expected 50% for neutral venues

**Interpretation**: In a hypothetical game between identically-skilled teams, the home team wins approximately 7 out of 10 times solely due to home-field factors.

#### Ridge Regression Results

- **Observed Average Home Margin**: +7.4 points
- **Model-Predicted Average**: +7.4 points (excellent fit)
- **Balanced Game Prediction**: **+14.4 points** for evenly-matched teams

**Interpretation**: When two equally-skilled teams play, the home team is expected to win by approximately two touchdowns.

#### LASSO Regression Results

- **Observed Average Home Margin**: +7.4 points
- **Model-Predicted Average**: +7.4 points
- **Balanced Game Prediction**: **+16.8 points** for evenly-matched teams

**Interpretation**: LASSO's slightly higher estimate suggests home advantage may be even stronger when accounting for feature selection, though the difference from Ridge is within uncertainty bounds.

### Consistency Across Models

All three models converge on similar conclusions:
1. Home teams win approximately **65-70%** of evenly-matched games
2. Home teams score approximately **14-17 more points** than equal away opponents
3. The advantage persists after controlling for team quality, rankings, and historical performance

This consistency across different modeling approaches (classification vs regression, L1 vs L2 regularization) strengthens confidence in the findings.

### Contextual Insights



### Comparison to Prior Research

Our estimates align with existing sports analytics literature:
- Moskowitz & Wertheim (2011) estimated ~60% home win rate in college football
- Stefani & Clarke (1992) found 5-7 point home advantage
- Our findings of 69% win probability and 14-17 point advantage suggest college football has stronger home effects than professional sports (NFL ~57% home wins)

### Limitations

Several limitations qualify these findings:

1. **Causality**: Our models identify correlation, not causation. Home advantage likely reflects multiple mechanisms (crowd support, travel fatigue, referee bias, familiarity with venue) that cannot be disentangled with this data.

2. **Missing Variables**: Factors like weather conditions, injury status, and coaching changes were unavailable but could influence both game outcomes and the home advantage estimate.

3. **Sample Selection**: Excluding neutral site games (bowl games, championships) may affect generalizability if home advantage differs in high-stakes contexts.

4. **Model Assumptions**: Linear models assume additive effects, but interactions between home venue and team quality may be more complex.

Despite these limitations, the robustness of findings across models and consistency with prior research provide strong evidence for substantial home-field advantage in college football.

## Future Work

This project establishes a solid foundation for quantifying home-field advantage, but several extensions could provide deeper insights and broader applicability.

### Temporal Dynamics

Our analysis aggregated data across 23 seasons (2002-2024), but home-field advantage may evolve over time. Future work could:
- Examine year-over-year trends to identify whether home advantage is increasing, decreasing, or stable
- Investigate whether rule changes (targeting penalties, transfer portal, NIL policies) affect home advantage
- Build time-varying coefficient models to capture shifting effects

Preliminary exploration showed no obvious trend, but more sophisticated time series methods could reveal subtle patterns.

### Mechanism Decomposition

Our models estimate the aggregate effect of playing at home without isolating specific causal mechanisms. Future research could disentangle:
- **Crowd effects**: Compare home advantage in high- vs low-attendance games, or before/after COVID-19 crowd restrictions
- **Travel fatigue**: Analyze whether advantage increases with travel distance for away teams
- **Referee bias**: Examine penalty differentials at home vs away, controlling for team discipline
- **Familiarity**: Test whether teams with unique venues (high altitude, dome vs outdoor) show larger advantages

Such analyses would require additional data (penalty logs, travel distances, venue characteristics) but could provide actionable insights for coaches and competitive balance policymakers.

### Conference and Team Heterogeneity

Aggregating across all FBS teams may mask important variations:
- **Conference differences**: Power 5 conferences may show different home advantage than Group of 5 due to resources, facilities, or fan culture
- **Team-specific effects**: Some teams (e.g., Oregon at Autzen Stadium, Texas A&M at Kyle Field) are anecdotally thought to have exceptional home advantages
- **Venue characteristics**: Compare natural grass vs turf, dome vs outdoor, high altitude vs sea level

Hierarchical models or fixed effects could quantify these heterogeneities while maintaining statistical power.

### Predictive Applications

While this project focused on quantification, the models could support practical prediction tasks:
- **Game outcome forecasting**: Integrate home-field estimates into point spread predictions
- **Betting market analysis**: Compare model predictions to Las Vegas lines to identify mispricings
- **Scheduling optimization**: Help conferences design schedules balancing competitive fairness with travel costs

### Methodological Improvements

Several modeling enhancements could improve accuracy or interpretability:

1. **Non-linear models**: Test gradient boosting, random forests, or neural networks to capture interaction effects between home venue and team quality
2. **Causal inference**: Apply propensity score matching or instrumental variables to move beyond correlational findings
3. **Bayesian approaches**: Estimate uncertainty in home advantage via posterior distributions rather than point estimates
4. **Ensemble methods**: Combine logistic and regression models via stacking for potentially better predictions

We deliberately chose interpretable linear models for this project, but more complex methods could reveal non-linearities.

### Data Expansion

Incorporating additional data sources could enrich the analysis:
- **Play-by-play data**: Analyze home advantage at finer granularity (first downs, third-down conversions)
- **Weather data**: Control for temperature, wind, precipitation effects
- **Recruiting rankings**: Test whether talent level moderates home advantage
- **Coaching experience**: Examine whether veteran coaches better leverage home venues
- **Social media sentiment**: Proxy for fan enthusiasm via Twitter activity

### Reproducibility and Transparency Enhancements

While this project demonstrates strong reproducibility practices, future iterations could:
- **Containerization**: Create Docker image to fully encapsulate software environment
- **Continuous integration**: Set up GitHub Actions to automatically test workflow on commits
- **Interactive dashboard**: Build Shiny or Streamlit app for exploring results dynamically
- **Preregistration**: Specify analysis plan before examining data to minimize researcher degrees of freedom

### Lessons Learned

Several key insights emerged during this project:

1. **Data integration is hard**: Merging heterogeneous sources consumed more time than anticipated. Fuzzy matching and careful validation were essential but labor-intensive.

2. **Documentation pays dividends**: Comprehensive README files and inline comments made collaboration smooth and facilitated reproducibility testing.

3. **Version control is essential**: Git allowed safe experimentation with branching while maintaining stable main branch for production workflow.

4. **Automation catches errors**: Converting notebooks to `run_all.py` script revealed several inconsistencies and workflow gaps invisible in interactive analysis.

5. **Licensing matters**: Navigating CFBD's redistribution prohibition required creativity (Box.com hosting) while respecting terms of service.

6. **Feature engineering > model complexity**: Careful feature construction (preventing leakage, encoding domain knowledge) improved performance more than tuning hyperparameters.

7. **Reproducibility requires discipline**: Fixing random seeds, documenting software versions, and providing step-by-step instructions are tedious but critical.

### Broader Impacts

Beyond sports analytics, this project's methodology demonstrates transferable skills:
- **Public health**: Quantifying treatment effects while controlling for confounders
- **Economics**: Estimating causal effects of policies from observational data
- **Social science**: Integrating administrative datasets with survey data
- **Environmental science**: Modeling climate impacts while accounting for regional heterogeneity

The emphasis on reproducibility, transparency, and ethical data use aligns with open science principles applicable across domains.

### Conclusion on Future Directions

This project establishes home-field advantage as a substantial (19 percentage points, 14-17 point margin) and robust phenomenon in college football. Future work disentangling mechanisms, exploring heterogeneity, and extending to predictive applications could yield both scientific insights and practical value. The reproducible infrastructure created here provides a foundation for these extensions, and we welcome collaborators interested in building on this work.

## Reproducing This Analysis

This project is designed for complete reproducibility. Follow these steps to independently reproduce all results from data acquisition through model training and evaluation.

### Prerequisites

**Software Requirements**:
- Python 3.8 or higher
- Git


### Step 1: Clone Repository

```bash
git clone https://github.com/landewill/IS477.git
cd IS477
```

Verify repository structure:
```bash
ls -l
# Should show: data/ models/ notebooks/ reports/ src/ requirements.txt README.md LICENSE
```

### Step 2: If Needed, Set Up Python Environment

Create and activate a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install required packages:

```bash
pip install -r requirements.txt
```

This installs all dependencies including pandas, scikit-learn, rapidfuzz, matplotlib, and jupyter.

Verify installation:
```bash
python -c "import pandas, sklearn, rapidfuzz; print('All packages installed successfully')"
```

### Step 3: Download Data from Box.com

**Important**: Due to CFBD licensing restrictions, raw data is hosted on Box.com rather than GitHub.

1. Access the Box.com shared folder via the link provided in the course submission (or contact project authors for access)

2. Download the complete `data/` folder from Box.com

3. Replace the empty `data/` directory in your local repository:
   ```bash
   # Remove empty data directory
   rm -rf data/
   
   # Move downloaded data folder into repository
   mv ~/Downloads/data ./
   ```

4. Verify data files are present:
   ```bash
   ls data/raw/
   # Should show: cfbd_merged.csv  cfb_box-scores_2002-2024.csv
   ```

**Alternative**: If you prefer to acquire data independently (requires CFBD API key):

1. Register for free API key at https://collegefootballdata.com/
2. Open and run `notebooks/API_CFBD.ipynb` to fetch CFBD data
3. Use `kaggle_data.ipynb`, or download Kaggle dataset manually from https://www.kaggle.com/datasets/cviaxmiwnptr/college-football-team-stats-2002-to-january-2024/data
4. Place both CSVs in `data/raw/` directory

### Step 4: Run Complete Workflow

Execute the automated workflow script:

```bash
python src/run_all.py
```

This single command executes all analysis steps:
1. Load raw CFBD and Kaggle data
2. Merge datasets using fuzzy team name matching
3. Clean and filter (regular season, non-neutral games)
4. Engineer 83 features with leakage prevention
5. Train Logistic Regression, Ridge, and LASSO models
6. Quantify home-field advantage for balanced games
7. Generate diagnostic visualizations
8. Save models, metrics, and summaries

**Expected Output**:
```
Loading data...
Merging CFBD and box score data...
Matched 12347 games
Cleaning data...
Engineering features...
Training logistic regression model...
Training ridge regression model...
Training LASSO regression model...
Quantifying home-field advantage...
Generating visualizations...
All outputs saved successfully
```
### Step 5: Verify Outputs

Check that all expected outputs were created, can match to outputs already in the repository when cloned from GitHub.

```bash
# Trained models
ls models/
# Should show: home_field_logistic.pkl  home_field_ridge.pkl  home_field_lasso.pkl

# Model metrics and summaries
ls reports/
# Should show: 
#   model_home_field_metrics.json
#   model_home_field_logit_summary.txt
#   model_home_field_ridge_summary.txt
#   model_home_field_lasso_summary.txt
#   logistic_roc_curve.png
#   lasso_feature_importance.png
#   ridge_residual_plot.png
#   lasso_residual_plot.png

# Processed data
ls data/model/
# Should show: merged_games_model_ready.csv
```

### Step 6: Examine Results

View quantitative results:

```bash
# View model performance metrics
cat reports/model_home_field_metrics.json

# View home-field advantage summary for logistic model
cat reports/model_home_field_logit_summary.txt
```

**Expected Key Finding**:
```
Home team win probability: 69.0%
Home-field advantage boost: 19.0 percentage points
```

Open visualizations to inspect diagnostic plots.

### Optional Step: Explore Notebooks

For deeper understanding of the workflow, explore the Jupyter notebooks documenting code development.
**Note**: Notebooks are for documentation; the production workflow runs via `src/run_all.py`.

For additional help, consult:
- `src/README_WORKFLOW.md`: Detailed workflow documentation
- `data/README.md`: Data acquisition and structure guide
- GitHub Issues: Open an issue at https://github.com/landewill/IS477/issues

### Reproduction Checklist

Use this checklist to verify complete reproduction:

- [ ] Repository cloned successfully
- [ ] Python environment created and packages installed
- [ ] Data downloaded from Box.com and placed in `data/raw/`
- [ ] `run_all.py` executed without errors
- [ ] Three model files present in `models/`
- [ ] Eight output files present in `reports/`
- [ ] Metrics JSON shows logistic test accuracy ~75.7%
- [ ] Logistic summary shows 69% home win probability for balanced games
- [ ] Visualizations render correctly

If all items are checked, you have successfully reproduced the complete analysis!

### Software Versions

For maximum reproducibility, the analysis was developed with:

```
Python 3.11.5
pandas 2.1.0
numpy 1.24.3
scikit-learn 1.3.0
rapidfuzz 3.2.0
matplotlib 3.7.2
joblib 1.3.2
```

Your results should be identical with these versions or highly similar with newer compatible versions.

## References

### Data Sources

College Football Data. (2024). *College Football Data API*. Retrieved from https://collegefootballdata.com/

Cviaxmiwnptr. (2025, January 24). *College Football Game Stats: 2002 to January 2025*. Kaggle. https://www.kaggle.com/datasets/cviaxmiwnptr/college-football-team-stats-2002-to-january-2024/data

### Software and Libraries

Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau, D., ... & Oliphant, T. E. (2020). Array programming with NumPy. *Nature*, 585(7825), 357-362. https://doi.org/10.1038/s41586-020-2649-2

McKinney, W. (2010). Data structures for statistical computing in Python. In *Proceedings of the 9th Python in Science Conference* (Vol. 445, pp. 51-56).

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., ... & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825-2830.

rapidfuzz Contributors. (2023). *rapidfuzz: Rapid fuzzy string matching in Python and C++*. Retrieved from https://github.com/maxbachmann/RapidFuzz

Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*, 9(3), 90-95.

### Project Metadata and Citation

For citation of this project, use:

```
Lande, W., & Tomic, E. (2025). College Football Home-Field Advantage Analysis 
[Software]. GitHub. https://github.com/landewill/IS477
```

Or import citation metadata from `CITATION.cff` in this repository using standard academic reference managers.

### Licenses

**Code**: This project is licensed under the MIT License. See `LICENSE` file for full terms.

**Data**: 
- CFBD data: Proprietary, redistribution prohibited (see https://collegefootballdata.com/exporting)
- Kaggle data: CC0 Public Domain (no restrictions)

**Documentation**: All documentation in this repository (README, markdown files) is licensed under CC-BY-4.0.

