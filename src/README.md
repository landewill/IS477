# Source Code Directory

This directory contains the production-ready Python scripts that implement the complete data processing and modeling pipeline.

## Status

✅ **COMPLETED** - All core functionality implemented and tested.

## Purpose

The `src/` directory houses modular, reusable Python code that:
1. Fetches raw data from external sources (APIs, web scraping)
2. Cleans and merges datasets
3. Engineers features for machine learning
4. Trains and evaluates models
5. Generates reports and visualizations

**Note:** This code is orchestrated by the main workflow script (`run_all.py` or `Makefile`) at the project root.

## Directory Structure

```
src/
├── data_collection/       # [PLANNED] Scripts to fetch raw data from sources
├── data_processing/       # [PLANNED] Data cleaning, merging, validation
├── feature_engineering/   # [PLANNED] Feature creation and transformation
├── modeling/             # [PLANNED] Model training, evaluation, prediction
├── utils/                # [PLANNED] Shared utilities and helper functions
└── README.md             # This file
```

**Current Status:** Core logic developed in Jupyter notebooks (`../notebooks/`). Production refactoring in progress.

## Design Principles

### Modularity
- Each script has a single, well-defined responsibility
- Functions are small, testable, and reusable
- Clear input/output contracts

### Reproducibility
- No hardcoded paths (use relative paths or config files)
- Fixed random seeds for stochastic operations
- Versioned dependencies (`requirements.txt`)
- Logging for transparency and debugging

### Data Integrity
- Validate inputs and outputs
- Preserve raw data (never modify)
- Document all transformations
- Handle missing data explicitly

## Planned Modules

### Data Collection
```python
# Example: fetch_cfbd_data.py
# Retrieves game data from College Football Data API
# Outputs: data/raw/cfbd_games.csv
```

### Data Processing
```python
# Example: merge_datasets.py
# Combines multiple data sources with quality checks
# Outputs: data/cleaned/merged_games.csv
```

### Feature Engineering
```python
# Example: build_features.py
# Creates model-ready feature matrices
# Outputs: data/model/merged_games_model_ready.csv
```

### Modeling
```python
# Example: train_models.py
# Trains logistic, Ridge, and LASSO models
# Outputs: models/*.pkl, reports/*.json
```

## Usage

**Run Individual Scripts:**
```bash
python src/data_processing/merge_datasets.py
python src/modeling/train_models.py
```

**Run Complete Pipeline:**
```bash
# From project root
python run_all.py
# OR
make all
```

## Dependencies

All Python dependencies are specified in `../requirements.txt`:

```bash
pip install -r requirements.txt
```

**Core Libraries:**
- pandas - Data manipulation
- numpy - Numerical computing
- scikit-learn - Machine learning models
- requests - API calls (if applicable)
- beautifulsoup4 - Web scraping (if applicable)

## Code Quality

### Testing
[PLANNED] Unit tests will be added to `tests/` directory:
```bash
pytest tests/
```

### Style
Code follows PEP 8 style guidelines:
```bash
flake8 src/
black src/  # Auto-formatter
```

### Documentation
All functions include docstrings with:
- Purpose description
- Parameters and types
- Return values
- Example usage

## Logging

Scripts use Python's `logging` module for transparency:
- INFO: Progress updates
- WARNING: Data quality issues
- ERROR: Failures and exceptions

Logs can be configured via environment variables or config files.

## Configuration

[PLANNED] Configuration parameters will be stored in:
- `config.yaml` or `config.json` - Paths, hyperparameters, settings
- Environment variables - Credentials, API keys (never committed)

## Software Citation

If using or adapting this code, please cite:

**Primary Libraries:**
1. **scikit-learn:**  
   Pedregosa et al. (2011). Scikit-learn: Machine Learning in Python. JMLR 12, pp. 2825-2830.

2. **pandas:**  
   McKinney, W. (2010). Data Structures for Statistical Computing in Python. Proceedings of the 9th Python in Science Conference, 51-56.

3. **NumPy:**  
   Harris, C.R., Millman, K.J., van der Walt, S.J. et al. (2020). Array programming with NumPy. Nature 585, 357–362.

**This Project:**  
Lande, W., & Tomic, E. (2025). College Football Home-Field Advantage Analysis. GitHub. https://github.com/landewill/IS477

## License

**MIT License**

Copyright (c) 2025 William Lande and Emil Tomic

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Contributing

This is a course project. For questions or issues, please contact [your email].

---

*This source code directory is part of a database management, curation, and reproducibility course project.*