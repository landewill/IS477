# Models

This directory contains the trained machine learning models for predicting college football game outcomes and quantifying home-field advantage.

## Contents

- `home_field_logistic.pkl` - Logistic regression model for predicting home team win probability
- `home_field_ridge.pkl` - Ridge regression model for predicting point margin (L2 regularization)
- `home_field_lasso.pkl` - LASSO regression model for predicting point margin (L1 regularization with feature selection)

## Model Details

All models were trained using scikit-learn pipelines that include:
- StandardScaler for feature normalization
- GridSearchCV for hyperparameter tuning with 5-fold cross-validation
- Random state = 42 for reproducibility

## How They Were Generated

These models are created by running:
```bash
python src/run_all.py
```

The training process is implemented in the `train_logistic_model()`, `train_ridge_model()`, and `train_lasso_model()` functions in `src/run_all.py`.

## Usage

Load models using joblib:
```python
import joblib
model = joblib.load('models/home_field_logistic.pkl')
```
