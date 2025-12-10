# Reports

This directory contains the analysis outputs and model evaluation metrics from the home-field advantage study.

## Contents

### Model Performance Metrics
- `model_home_field_metrics.json` - Complete metrics for all three models (accuracy, ROC AUC, MAE, RMSE, R², etc.)

### Home Advantage Summaries
- `model_home_field_logit_summary.txt` - Home-field advantage quantification from logistic regression (win probability)
- `model_home_field_ridge_summary.txt` - Home-field advantage quantification from Ridge regression (point margin)
- `model_home_field_lasso_summary.txt` - Home-field advantage quantification from LASSO regression (point margin)

### Visualizations
- `lasso_feature_importance.png` - Bar chart of non-zero feature coefficients from LASSO model
- `logistic_roc_curve.png` - ROC curve for logistic regression classifier
- `ridge_residual_plot.png` - Residual plot for Ridge regression predictions
- `lasso_residual_plot.png` - Residual plot for LASSO regression predictions

## How They Were Generated

All reports are created by running:
```bash
python src/run_all.py
```

Metrics and summaries are generated in the main workflow, and visualizations are created using matplotlib in the final step of the pipeline.
