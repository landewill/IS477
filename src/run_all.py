"""
Complete workflow pipeline for College Football Home-Field Advantage Analysis.

This script executes the full data processing and modeling workflow:
1. Loads raw data from Box.com download
2. Merges CFBD and box score datasets
3. Cleans and engineers features
4. Trains three machine learning models (Logistic, Ridge, LASSO)
5. Saves results to reports/ and models/ directories

Usage:
    python run_all.py

Requirements:
    - Data files must be present in data/raw/
    - Run from project root directory
    - Python 3.8+ with required packages (see requirements.txt)
"""

import pandas as pd
import numpy as np
import json
import os
import sys
from pathlib import Path
from rapidfuzz import fuzz
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, Ridge, Lasso
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, roc_auc_score, precision_score, recall_score, f1_score,
    mean_absolute_error, mean_squared_error, r2_score, roc_curve, auc
)
import joblib
import matplotlib.pyplot as plt

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)


# Data merging functions

def prepare_sched(sched):
    """Prepare the schedule dataframe (box scores)."""
    sched = sched.copy()
    sched = (
        sched.reset_index(drop=True)
             .reset_index()
             .rename(columns={'index': 'sched_game_id'})
    )

    sched['game_dt_et'] = pd.to_datetime(
        sched['date'].astype(str) + ' ' + sched['time_et'].astype(str),
        errors='coerce'
    )

    sched['date_key'] = sched['game_dt_et'].dt.date
    sched['time_key'] = sched['game_dt_et'].dt.round('5min')

    sched['season'] = pd.to_numeric(sched['season'], errors='coerce')
    sched['week'] = pd.to_numeric(sched['week'], errors='coerce')

    if 'attendance' in sched.columns:
        sched['attendance'] = pd.to_numeric(
            sched['attendance'], errors='coerce'
        ).round()
    else:
        sched['attendance'] = pd.NA

    return sched


def prepare_cfbd_box(cfbd):
    """Prepare the CFBD games dataframe."""
    cfbd = cfbd.copy()
    cfbd = (
        cfbd.reset_index(drop=True)
            .reset_index()
            .rename(columns={'index': 'cfbd_game_id'})
    )

    cfbd['game_dt_utc'] = pd.to_datetime(
        cfbd['startDate'], utc=True, errors='coerce'
    )
    cfbd['game_dt_et'] = (
        cfbd['game_dt_utc']
            .dt.tz_convert('US/Eastern')
            .dt.tz_localize(None)
    )

    cfbd['date_key'] = cfbd['game_dt_et'].dt.date
    cfbd['time_key'] = cfbd['game_dt_et'].dt.round('5min')

    cfbd['season'] = pd.to_numeric(cfbd['season'], errors='coerce')
    cfbd['week'] = pd.to_numeric(cfbd['week'], errors='coerce')

    if 'attendance' in cfbd.columns:
        cfbd['attendance'] = pd.to_numeric(
            cfbd['attendance'], errors='coerce'
        ).round()
    else:
        cfbd['attendance'] = pd.NA

    return cfbd


def add_team_match_score(candidates):
    """Add fuzzy match score based on home/away team names."""
    def _calc(row):
        home_sched = str(row['home_sched'])
        away_sched = str(row['away_sched'])
        home_cfbd = str(row['home_cfbd'])
        away_cfbd = str(row['away_cfbd'])

        h = fuzz.token_sort_ratio(home_sched, home_cfbd)
        a = fuzz.token_sort_ratio(away_sched, away_cfbd)
        row['match_score'] = (h + a) / 2.0
        return row

    return candidates.apply(_calc, axis=1)


def greedy_match(candidates, score_threshold, used_sched=None, used_cfbd=None):
    """
    1:1 matching: each sched_game_id and cfbd_game_id appears at most once.
    """
    if used_sched is None:
        used_sched = set()
    if used_cfbd is None:
        used_cfbd = set()

    if candidates.empty:
        return pd.DataFrame(), used_sched, used_cfbd

    candidates = candidates.sort_values('match_score', ascending=False).copy()
    rows = []

    for r in candidates.itertuples(index=False):
        if r.match_score < score_threshold:
            continue
        if r.sched_game_id in used_sched or r.cfbd_game_id in used_cfbd:
            continue

        used_sched.add(r.sched_game_id)
        used_cfbd.add(r.cfbd_game_id)
        rows.append(r._asdict())

    if rows:
        matches_df = pd.DataFrame(rows)
    else:
        matches_df = pd.DataFrame(columns=candidates.columns)

    return matches_df, used_sched, used_cfbd


def match_cfbd_box(cfbd_raw, box_raw, time_window_att=15, score_thr_att=80,
                   time_window_time=10, score_thr_time=85):
    """Match CFBD and box dataframes and return merged dataframe."""
    
    sched = prepare_sched(box_raw)
    cfbd = prepare_cfbd_box(cfbd_raw)

    sched_small = sched[['sched_game_id', 'season', 'week', 'date_key', 'time_key',
                         'home', 'away', 'attendance']]
    cfbd_small = cfbd[['cfbd_game_id', 'season', 'week', 'date_key', 'time_key',
                       'homeTeam', 'awayTeam', 'attendance']]

    # Attendance-based candidates
    sched_att = sched_small.dropna(subset=['attendance'])
    cfbd_att = cfbd_small.dropna(subset=['attendance'])

    cand_att = sched_att.merge(
        cfbd_att,
        on=['season', 'week', 'date_key', 'attendance'],
        suffixes=('_sched', '_cfbd')
    )

    if not cand_att.empty:
        cand_att = cand_att.rename(columns={
            'home': 'home_sched',
            'away': 'away_sched',
            'homeTeam': 'home_cfbd',
            'awayTeam': 'away_cfbd'
        })

        cand_att = cand_att.merge(
            sched[['sched_game_id', 'game_dt_et']],
            on='sched_game_id'
        ).merge(
            cfbd[['cfbd_game_id', 'game_dt_et']],
            on='cfbd_game_id',
            suffixes=('_sched_dt', '_cfbd_dt')
        )

        cand_att['time_diff_min'] = (
            (cand_att['game_dt_et_sched_dt'] - cand_att['game_dt_et_cfbd_dt'])
            .abs()
            .dt.total_seconds() / 60.0
        )

        cand_att = cand_att[cand_att['time_diff_min'] <= time_window_att]

        if not cand_att.empty:
            cand_att = add_team_match_score(cand_att)
            matches_att, used_sched, used_cfbd = greedy_match(
                cand_att, score_thr_att
            )
        else:
            matches_att = pd.DataFrame()
            used_sched, used_cfbd = set(), set()
    else:
        matches_att = pd.DataFrame()
        used_sched, used_cfbd = set(), set()

    # Time-based candidates
    sched_small_rem = sched_small[~sched_small['sched_game_id'].isin(used_sched)]
    cfbd_small_rem = cfbd_small[~cfbd_small['cfbd_game_id'].isin(used_cfbd)]

    cand_time = sched_small_rem.merge(
        cfbd_small_rem,
        on=['season', 'week', 'date_key', 'time_key'],
        suffixes=('_sched', '_cfbd')
    )

    if not cand_time.empty:
        cand_time = cand_time.rename(columns={
            'home': 'home_sched',
            'away': 'away_sched',
            'homeTeam': 'home_cfbd',
            'awayTeam': 'away_cfbd'
        })

        cand_time = cand_time.merge(
            sched[['sched_game_id', 'game_dt_et']],
            on='sched_game_id'
        ).merge(
            cfbd[['cfbd_game_id', 'game_dt_et']],
            on='cfbd_game_id',
            suffixes=('_sched_dt', '_cfbd_dt')
        )

        cand_time['time_diff_min'] = (
            (cand_time['game_dt_et_sched_dt'] - cand_time['game_dt_et_cfbd_dt'])
            .abs()
            .dt.total_seconds() / 60.0
        )

        cand_time = cand_time[cand_time['time_diff_min'] <= time_window_time]

        if not cand_time.empty:
            cand_time = add_team_match_score(cand_time)
            matches_time, used_sched, used_cfbd = greedy_match(
                cand_time, score_thr_time, used_sched, used_cfbd
            )
        else:
            matches_time = pd.DataFrame()
    else:
        matches_time = pd.DataFrame()

    # Combine matches
    matches = pd.concat([matches_att, matches_time], ignore_index=True)

    if matches.empty:
        return pd.DataFrame()

    sched_full = sched.set_index('sched_game_id')
    cfbd_full = cfbd.set_index('cfbd_game_id')

    merged = matches.join(
        sched_full, on='sched_game_id', rsuffix='_sched_full'
    ).join(
        cfbd_full, on='cfbd_game_id', rsuffix='_cfbd_full'
    )

    merged = merged.drop(columns=['homeTeam', 'awayTeam'], errors='ignore')

    return merged


# Data cleaning and feature engineering functions

def prepare_model_data(merged):
    """Clean and prepare data for modeling."""
    df = merged.copy()
    
    print(f"Starting with {len(df)} games")
    
    if 'completed' in df.columns:
        df = df[df['completed'] == True].copy()
    
    if 'seasonType' in df.columns:
        df = df[df['seasonType'] == 'regular'].copy()
    
    if 'neutralSite' in df.columns:
        df = df[df['neutralSite'] == False].copy()
    elif 'neutral' in df.columns:
        df = df[df['neutral'] == False].copy()
    
    home_score_col = None
    away_score_col = None
    
    if 'homePoints' in df.columns and 'awayPoints' in df.columns:
        home_score_col = 'homePoints'
        away_score_col = 'awayPoints'
    elif 'score_home' in df.columns and 'score_away' in df.columns:
        home_score_col = 'score_home'
        away_score_col = 'score_away'
    else:
        raise ValueError("Could not find score columns")
    
    df = df.dropna(subset=[home_score_col, away_score_col]).copy()
    print(f"After removing missing scores: {len(df)}")
    
    df[home_score_col] = pd.to_numeric(df[home_score_col], errors='coerce')
    df[away_score_col] = pd.to_numeric(df[away_score_col], errors='coerce')
    df = df.dropna(subset=[home_score_col, away_score_col]).copy()
    
    df['home_margin'] = df[home_score_col] - df[away_score_col]
    df['home_win'] = (df['home_margin'] > 0).astype(int)
    
    df = df.dropna(subset=['home_margin', 'home_win']).copy()
    
    print(f"\nFinal cleaned dataset: {len(df)} games")
    print(f"Home win rate: {df['home_win'].mean():.1%}")
    print(f"Average home margin: {df['home_margin'].mean():.2f} points")
    
    return df


def build_features(df):
    """Engineer features for modeling with missing data handling."""
    feature_df = df.copy()
    
    feature_parts = []
    
    # Exclude game outcomes to prevent data leakage
    EXCLUDE_PATTERNS = [
        'score', 'points', 'margin',
        'q1', 'q2', 'q3', 'q4', 'ot',
        'first_downs', 'third_down', 'fourth_down',
        'pass_comp', 'pass_att', 'pass_yards',
        'rush_att', 'rush_yards', 'total_yards',
        'fum', 'int', 'pen_', 'possession',
        'PostgameWinProbability', 'PostgameElo',
        'excitementIndex',
    ]
    
    def should_exclude_feature(col_name):
        col_lower = col_name.lower()
        for pattern in EXCLUDE_PATTERNS:
            if pattern.lower() in col_lower:
                return True
        return False
    
    # Create difference features for home/away pairs
    home_cols = [c for c in feature_df.columns if c.startswith('home') or c.endswith('_home')]
    away_cols = [c for c in feature_df.columns if c.startswith('away') or c.endswith('_away')]
    
    diff_features = {}
    
    for home_col in home_cols:
        if should_exclude_feature(home_col):
            continue
            
        if home_col.startswith('home'):
            suffix = home_col[4:]
            away_col = 'away' + suffix
        else:
            prefix = home_col.replace('_home', '')
            away_col = prefix + '_away'
        
        if away_col in feature_df.columns and not should_exclude_feature(away_col):
            if pd.api.types.is_numeric_dtype(feature_df[home_col]) and \
               pd.api.types.is_numeric_dtype(feature_df[away_col]):
                feature_name = f'diff_{suffix if home_col.startswith("home") else prefix}'
                diff_features[feature_name] = feature_df[home_col] - feature_df[away_col]
    
    if diff_features:
        diff_df = pd.DataFrame(diff_features)
        
        missing_pct = diff_df.isnull().sum() / len(diff_df)
        
        good_features = missing_pct[missing_pct < 0.5].index.tolist()
        bad_features = missing_pct[missing_pct >= 0.5].index.tolist()
        
        if bad_features:
            print(f"Dropping {len(bad_features)} difference features with >50% missing data")
        
        diff_df = diff_df[good_features]
        
        if len(diff_df.columns) > 0:
            feature_parts.append(diff_df)
            print(f"Created {len(good_features)} difference features")
    
    # Venue features
    venue_features = []
    potential_venue_cols = ['elevation', 'latitude', 'longitude', 'dome', 'grass', 'capacity']
    
    for col in potential_venue_cols:
        if col in feature_df.columns and pd.api.types.is_numeric_dtype(feature_df[col]):
            missing_pct = feature_df[col].isnull().sum() / len(feature_df)
            if missing_pct < 0.5:
                venue_features.append(col)
    
    if venue_features:
        venue_df = feature_df[venue_features].copy()
        feature_parts.append(venue_df)
    
    # One-hot encode categorical features
    categorical_features = []
    
    if 'homeConference' in feature_df.columns:
        missing_pct = feature_df['homeConference'].isnull().sum() / len(feature_df)
        if missing_pct < 0.5:
            categorical_features.append('homeConference')
    
    if 'awayConference' in feature_df.columns:
        missing_pct = feature_df['awayConference'].isnull().sum() / len(feature_df)
        if missing_pct < 0.5:
            categorical_features.append('awayConference')
    
    if 'conf_home' in feature_df.columns:
        missing_pct = feature_df['conf_home'].isnull().sum() / len(feature_df)
        if missing_pct < 0.5:
            categorical_features.append('conf_home')
    
    if 'conf_away' in feature_df.columns:
        missing_pct = feature_df['conf_away'].isnull().sum() / len(feature_df)
        if missing_pct < 0.5:
            categorical_features.append('conf_away')
    
    if categorical_features:
        cat_df = feature_df[categorical_features].copy()
        for col in categorical_features:
            cat_df[col] = cat_df[col].fillna('Unknown')
        
        encoded_df = pd.get_dummies(
            cat_df, 
            drop_first=True,
            prefix=categorical_features
        )
        feature_parts.append(encoded_df)
    
    if not feature_parts:
        raise ValueError("No features were created")
    
    X = pd.concat(feature_parts, axis=1)
    
    # Handle missing values with median imputation
    rows_before = len(X)
    missing_before = X.isnull().sum().sum()
    
    if missing_before > 0:
        print(f"\nImputing {missing_before:,} missing values using median imputation...")
        
        for col in X.columns:
            if X[col].isnull().any():
                median_val = X[col].median()
                if pd.isna(median_val):
                    median_val = 0
                X[col] = X[col].fillna(median_val)
    
    X = X.dropna()
    rows_after = len(X)
    
    if rows_before > rows_after:
        print(f"Dropped {rows_before - rows_after} rows after imputation")
    
    # Extract targets
    y_logit = feature_df.loc[X.index, 'home_win']
    y_reg = feature_df.loc[X.index, 'home_margin']
    
    print(f"Final feature matrix shape: {X.shape}")
    print(f"Number of features: {X.shape[1]}")
    print(f"Data kept: {len(X)/len(df):.1%} of original rows")
    
    return X, y_logit, y_reg


# Model training functions

def train_logistic_model(X, y):
    """Train logistic regression model with cross-validation."""
    print("\nTraining logistic regression model...")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2, 
        random_state=RANDOM_STATE,
        stratify=y
    )
    
    logit_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(max_iter=1000, random_state=RANDOM_STATE))
    ])
    
    param_grid_logit = {
        'classifier__C': [0.001, 0.01, 0.1, 1, 10, 100],
        'classifier__penalty': ['l2'],
        'classifier__solver': ['lbfgs']
    }
    
    grid_search_logit = GridSearchCV(
        logit_pipeline,
        param_grid_logit,
        cv=5,
        scoring='roc_auc',
        n_jobs=-1,
        verbose=1
    )
    
    grid_search_logit.fit(X_train, y_train)
    
    best_logit = grid_search_logit.best_estimator_
    
    # Evaluate on test set
    y_pred = best_logit.predict(X_test)
    y_pred_proba = best_logit.predict_proba(X_test)[:, 1]
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_pred_proba),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
        'best_params': grid_search_logit.best_params_
    }
    
    print("\nLogistic Regression Model - Performance on Test Set")
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"ROC AUC:   {metrics['roc_auc']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1 Score:  {metrics['f1']:.4f}")
    
    return best_logit, metrics, X_test, y_test


def train_ridge_model(X, y):
    """Train Ridge regression model with cross-validation."""
    print("\nTraining Ridge regression model...")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=RANDOM_STATE
    )
    
    ridge_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', Ridge(random_state=RANDOM_STATE))
    ])
    
    param_grid_ridge = {
        'regressor__alpha': [0.001, 0.01, 0.1, 1, 10, 100, 1000]
    }
    
    grid_search_ridge = GridSearchCV(
        ridge_pipeline,
        param_grid_ridge,
        cv=5,
        scoring='neg_mean_absolute_error',
        n_jobs=-1,
        verbose=1
    )
    
    grid_search_ridge.fit(X_train, y_train)
    
    best_reg = grid_search_ridge.best_estimator_
    
    # Evaluate on test set
    y_pred = best_reg.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    metrics = {
        'mae': mae,
        'rmse': rmse,
        'r2': r2,
        'best_params': grid_search_ridge.best_params_
    }
    
    print("\nRidge Regression Model - Test Set Performance")
    print(f"MAE:  {mae:.4f} points")
    print(f"RMSE: {rmse:.4f} points")
    print(f"R^2 Score: {r2:.4f}")
    
    return best_reg, metrics, X_test, y_test


def train_lasso_model(X, y):
    """Train LASSO regression model with cross-validation."""
    print("\nTraining LASSO regression model...")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=RANDOM_STATE
    )
    
    lasso_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', Lasso(random_state=RANDOM_STATE, max_iter=10000))
    ])
    
    param_grid_lasso = {
        'regressor__alpha': [0.001, 0.01, 0.1, 0.5, 1, 5, 10, 50, 100]
    }
    
    grid_search_lasso = GridSearchCV(
        lasso_pipeline,
        param_grid_lasso,
        cv=5,
        scoring='neg_mean_absolute_error',
        n_jobs=-1,
        verbose=1
    )
    
    grid_search_lasso.fit(X_train, y_train)
    
    best_lasso = grid_search_lasso.best_estimator_
    
    # Evaluate on test set
    y_pred = best_lasso.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    # Count non-zero coefficients
    lasso_coefs = best_lasso.named_steps['regressor'].coef_
    n_nonzero = np.sum(lasso_coefs != 0)
    
    metrics = {
        'mae': mae,
        'rmse': rmse,
        'r2': r2,
        'best_params': grid_search_lasso.best_params_,
        'features_selected': int(n_nonzero),
        'features_total': len(X.columns)
    }
    
    print("\nLASSO Regression Model - Test Set Performance")
    print(f"MAE:  {mae:.4f} points")
    print(f"RMSE: {rmse:.4f} points")
    print(f"R^2 Score: {r2:.4f}")
    print(f"\n{n_nonzero}/{len(lasso_coefs)} features selected")
    
    return best_lasso, metrics, X_test, y_test


def quantify_home_advantage_logit(model, X, y):
    """Quantify home-field advantage from logistic model."""
    observed_win_rate = y.mean()
    avg_predicted_prob = model.predict_proba(X)[:, 1].mean()
    
    # Balanced game scenario
    balanced_game = pd.DataFrame([X.median()], columns=X.columns)
    diff_cols = [col for col in balanced_game.columns if col.startswith('diff_')]
    for col in diff_cols:
        balanced_game[col] = 0
    
    balanced_prob = model.predict_proba(balanced_game)[0, 1]
    
    results = {
        'observed_win_rate': observed_win_rate,
        'avg_predicted_prob': avg_predicted_prob,
        'balanced_game_prob': balanced_prob,
        'home_advantage_pct_points': (balanced_prob - 0.5) * 100
    }
    
    summary = f"""
HOME-FIELD ADVANTAGE - Logistic Model Analysis

Observed Data:
  - Home win rate: {observed_win_rate:.1%}

Model Predictions:
  - Average predicted home win probability: {avg_predicted_prob:.1%}
  
Balanced Game Analysis:
  In a perfectly evenly-matched game where all team stats are equal, 
  the model predicts:
  
  - Home team win probability: {balanced_prob:.1%}
  - Away team win probability: {1-balanced_prob:.1%}
  
  Home-field advantage boost: {(balanced_prob - 0.5) * 100:.1f} percentage points
  
INTERPRETATION:
  When two equally-skilled teams play, the home team wins 
  approximately {balanced_prob:.1%} of the time, showing a 
  significant home-field advantage in college football.
"""
    
    return results, summary


def quantify_home_advantage_regression(model, X, y):
    """Quantify home-field advantage from regression model."""
    observed_margin = y.mean()
    avg_predicted_margin = model.predict(X).mean()
    
    # Balanced game scenario
    balanced_game = pd.DataFrame([X.median()], columns=X.columns)
    diff_cols = [col for col in balanced_game.columns if col.startswith('diff_')]
    for col in diff_cols:
        balanced_game[col] = 0
    
    balanced_margin = model.predict(balanced_game)[0]
    
    results = {
        'observed_margin': observed_margin,
        'avg_predicted_margin': avg_predicted_margin,
        'balanced_game_margin': balanced_margin
    }
    
    summary = f"""
HOME-FIELD ADVANTAGE - Regression Model

Observed Data:
  - Average home margin: {observed_margin:+.2f} points

Model Predictions:
  - Average predicted home margin: {avg_predicted_margin:+.2f} points
  
Balanced Game Analysis:
  In a perfectly evenly-matched game, the model predicts:
  
  - Expected home margin: {balanced_margin:+.2f} points
  
INTERPRETATION:
  When two equal teams play, the home team is expected 
  to win by approximately {balanced_margin:.1f} points.
"""
    
    return results, summary


def main():
    """Execute complete workflow."""
    
    print("College Football Home-Field Advantage Analysis")
    print("Complete Workflow Pipeline\n")
    
    # Step 1: Load raw data
    print("Step 1: Loading raw data...")
    cfbd_path = "data/raw/cfbd_merged.csv"
    box_path = "data/raw/cfb_box-scores_2002-2024.csv"
    
    if not os.path.exists(cfbd_path) or not os.path.exists(box_path):
        print("ERROR: Data files not found.")
        print(f"  Expected: {cfbd_path}")
        print(f"  Expected: {box_path}")
        print("\nPlease run: python src/download_data_from_box.py")
        sys.exit(1)
    
    cfbd = pd.read_csv(cfbd_path, low_memory=False)
    box = pd.read_csv(box_path, low_memory=False)
    print(f"Loaded CFBD data: {len(cfbd)} rows")
    print(f"Loaded Box scores: {len(box)} rows")
    
    # Step 2: Merge datasets
    print("\nStep 2: Merging datasets...")
    merged_games = match_cfbd_box(cfbd, box)
    print(f"Merged dataset: {len(merged_games)} games")
    
    # Step 3: Clean and prepare data
    print("\nStep 3: Cleaning and preparing data...")
    clean_df = prepare_model_data(merged_games)
    
    # Step 4: Engineer features
    print("\nStep 4: Engineering features...")
    X, y_logit, y_reg = build_features(clean_df)
    
    # Step 5: Train models
    print("\nStep 5: Training models...")
    
    logit_model, logit_metrics, X_test_logit, y_test_logit = train_logistic_model(X, y_logit)
    ridge_model, ridge_metrics, X_test_reg, y_test_reg = train_ridge_model(X, y_reg)
    lasso_model, lasso_metrics, X_test_lasso, y_test_lasso = train_lasso_model(X, y_reg)
    
    # Step 6: Quantify home-field advantage
    print("\nStep 6: Quantifying home-field advantage...")
    
    logit_adv_results, logit_adv_summary = quantify_home_advantage_logit(logit_model, X, y_logit)
    print(logit_adv_summary)
    
    ridge_adv_results, ridge_adv_summary = quantify_home_advantage_regression(ridge_model, X, y_reg)
    print(ridge_adv_summary)
    
    lasso_adv_results, lasso_adv_summary = quantify_home_advantage_regression(lasso_model, X, y_reg)
    print(lasso_adv_summary)
    
    # Step 7: Save outputs
    print("\nStep 7: Saving outputs...")
    
    # Create output directories
    Path("data/model").mkdir(parents=True, exist_ok=True)
    Path("models").mkdir(parents=True, exist_ok=True)
    Path("reports").mkdir(parents=True, exist_ok=True)
    
    # Save model-ready dataset
    model_ready_df = clean_df.loc[X.index].copy()
    id_cols = []
    for col in ['cfbd_game_id', 'sched_game_id', 'season', 'week', 'date', 'home', 'away']:
        if col in model_ready_df.columns:
            id_cols.append(col)
    
    model_df = pd.concat([
        model_ready_df[id_cols],
        pd.DataFrame({'home_margin': y_reg, 'home_win': y_logit}),
        X
    ], axis=1)
    
    model_df.to_csv('data/model/merged_games_model_ready.csv', index=False)
    print("Saved model-ready dataset")
    
    # Save trained models
    joblib.dump(logit_model, 'models/home_field_logistic.pkl')
    joblib.dump(ridge_model, 'models/home_field_ridge.pkl')
    joblib.dump(lasso_model, 'models/home_field_lasso.pkl')
    print("Saved trained models")
    
    # Save metrics
    all_metrics = {
        'logistic_regression': {
            'test_accuracy': float(logit_metrics['accuracy']),
            'test_roc_auc': float(logit_metrics['roc_auc']),
            'test_precision': float(logit_metrics['precision']),
            'test_recall': float(logit_metrics['recall']),
            'test_f1': float(logit_metrics['f1']),
            'best_params': logit_metrics['best_params'],
            'home_advantage': {
                'observed_win_rate': float(logit_adv_results['observed_win_rate']),
                'avg_predicted_prob': float(logit_adv_results['avg_predicted_prob']),
                'balanced_game_prob': float(logit_adv_results['balanced_game_prob']),
                'home_advantage_pct_points': float(logit_adv_results['home_advantage_pct_points'])
            }
        },
        'ridge_regression': {
            'test_mae': float(ridge_metrics['mae']),
            'test_rmse': float(ridge_metrics['rmse']),
            'test_r2': float(ridge_metrics['r2']),
            'best_params': ridge_metrics['best_params'],
            'features_used': len(X.columns),
            'home_advantage': {
                'observed_margin': float(ridge_adv_results['observed_margin']),
                'avg_predicted_margin': float(ridge_adv_results['avg_predicted_margin']),
                'balanced_game_margin': float(ridge_adv_results['balanced_game_margin'])
            }
        },
        'lasso_regression': {
            'test_mae': float(lasso_metrics['mae']),
            'test_rmse': float(lasso_metrics['rmse']),
            'test_r2': float(lasso_metrics['r2']),
            'best_params': lasso_metrics['best_params'],
            'features_used': int(lasso_metrics['features_selected']),
            'features_total': int(lasso_metrics['features_total']),
            'home_advantage': {
                'observed_margin': float(lasso_adv_results['observed_margin']),
                'avg_predicted_margin': float(lasso_adv_results['avg_predicted_margin']),
                'balanced_game_margin': float(lasso_adv_results['balanced_game_margin'])
            }
        }
    }
    
    with open('reports/model_home_field_metrics.json', 'w') as f:
        json.dump(all_metrics, f, indent=2)
    
    with open('reports/model_home_field_logit_summary.txt', 'w') as f:
        f.write(logit_adv_summary)
    
    with open('reports/model_home_field_ridge_summary.txt', 'w') as f:
        f.write(ridge_adv_summary)
    
    with open('reports/model_home_field_lasso_summary.txt', 'w') as f:
        f.write(lasso_adv_summary)
    
    print("Saved metrics and summaries")
    
    # Generate visualizations
    print("\nGenerating visualizations")
    
    # 1. LASSO Feature Importance
    feature_names = X.columns
    coefficients = lasso_model.named_steps['regressor'].coef_
    
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'coefficient': coefficients
    })
    feature_importance = feature_importance[feature_importance['coefficient'] != 0]
    feature_importance = feature_importance.reindex(
        feature_importance['coefficient'].abs().sort_values(ascending=True).index
    )
    
    plt.figure(figsize=(10, 8))
    plt.barh(range(len(feature_importance)), feature_importance['coefficient'])
    plt.yticks(range(len(feature_importance)), feature_importance['feature'], fontsize=6)
    plt.xlabel('LASSO Coefficient')
    plt.ylabel('Feature')
    plt.title('LASSO Feature Importance')
    plt.axvline(x=0, color='black', linestyle='--', linewidth=0.8)
    plt.tight_layout()
    plt.savefig('reports/lasso_feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. ROC Curve for Logistic Regression
    y_pred_proba = logit_model.predict_proba(X_test_logit)[:, 1]
    fpr, tpr, thresholds = roc_curve(y_test_logit, y_pred_proba)
    roc_auc_val = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC curve (AUC = {roc_auc_val:.3f})')
    plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--', label='Random classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Logistic Regression ROC Curve')
    plt.legend(loc='lower right')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('reports/logistic_roc_curve.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Residual Plot for Ridge Regression
    y_pred_ridge = ridge_model.predict(X_test_reg)
    residuals_ridge = y_test_reg - y_pred_ridge
    
    plt.figure(figsize=(10, 6))
    plt.scatter(y_pred_ridge, residuals_ridge, alpha=0.5, s=10)
    plt.axhline(y=0, color='red', linestyle='--', linewidth=2)
    plt.xlabel('Predicted Score Margin')
    plt.ylabel('Residuals (Actual - Predicted)')
    plt.title('Ridge Regression Residual Plot')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('reports/ridge_residual_plot.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Residual Plot for LASSO Regression
    y_pred_lasso_plot = lasso_model.predict(X_test_lasso)
    residuals_lasso = y_test_lasso - y_pred_lasso_plot
    
    plt.figure(figsize=(10, 6))
    plt.scatter(y_pred_lasso_plot, residuals_lasso, alpha=0.5, s=10, color='green')
    plt.axhline(y=0, color='red', linestyle='--', linewidth=2)
    plt.xlabel('Predicted Score Margin')
    plt.ylabel('Residuals (Actual - Predicted)')
    plt.title('LASSO Regression Residual Plot')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('reports/lasso_residual_plot.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Saved visualizations")
    
    print("\nWorkflow complete.")


if __name__ == '__main__':
    main()
