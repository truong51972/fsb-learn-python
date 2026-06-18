# HW-3: Heart Disease ML Training Pipeline

This repository contains a complete ML training pipeline for heart disease classification (binary classification). The pipeline is implemented as a Jupyter notebook (`main.ipynb`) with clear, step-by-step cells.

## Dataset

**Source**: Heart Disease (UCI) dataset

**Input**: CSV files with 13 features and a binary `target` column (0 = no disease, 1 = disease)

The data is already pre-split:
| Split | File | Samples |
|---|---|---|
| Train | `data/raw_train.csv` | 243 |
| Validation | `data/raw_val.csv` | 31 |
| Test | `data/raw_test.csv` | 32 |

**Features**: age, trestbps, chol, thalach, oldpeak, sex, cp, fbs, restecg, exang, slope, ca, thal

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate
```

### Dependencies

- Python >= 3.11
- scikit-learn
- xgboost
- pandas, numpy
- matplotlib, seaborn
- joblib
- jupyter / notebook

## Pipeline

The pipeline in `main.ipynb` follows this flow:

1. **Imports** — Load all libraries
2. **Configuration** — All configurable parameters in one cell
3. **Load Data** — Read train/val/test CSVs
4. **EDA** — Shape, missing values, target distribution, statistics, correlation heatmap
5. **Split Features/Target** — Separate X and y
6. **Preprocess** — `StandardScaler` fitted on **train only**, transforms val + test
7. **Define Models** — 5 classifiers ready for training
8. **Train** — Fit all 5 models, measure training time
9. **Evaluate** — Accuracy, precision, recall, F1 on val + test
10. **Error Analysis** — Confusion matrices for all models
11. **Save Models** — Each model saved as `.pkl`
12. **Predictions** — CSV with actual + all model predictions
13. **Best Model Report** — Classification report for top model
14. **Summary** — Comparison table and artifact locations

## Trained Models

| Model | File |
|---|---|
| DecisionTreeClassifier | `models/DecisionTreeClassifier.pkl` |
| AdaBoostClassifier | `models/AdaBoostClassifier.pkl` |
| RandomForestClassifier | `models/RandomForestClassifier.pkl` |
| GradientBoostingClassifier | `models/GradientBoostingClassifier.pkl` |
| XGBClassifier | `models/XGBClassifier.pkl` |
| Preprocessor (StandardScaler) | `models/preprocessor.pkl` |

## How to Run

### Option 1: Interactive (recommended)

Open `main.ipynb` in VS Code or Jupyter and run all cells.

### Option 2: Headless execution

```bash
uv run jupyter nbconvert --to notebook --execute main.ipynb --output main_executed.ipynb
```

### Configuration

Edit the `CONFIG` dictionary in **Cell 2** to change:

| Parameter | Default | Description |
|---|---|---|
| `train_path` | `data/raw_train.csv` | Path to training CSV |
| `val_path` | `data/raw_val.csv` | Path to validation CSV |
| `test_path` | `data/raw_test.csv` | Path to test CSV |
| `target_col` | `target` | Name of target column |
| `random_seed` | `42` | Random seed for reproducibility |
| `model_dir` | `models` | Directory to save trained models |
| `output_dir` | `outputs` | Directory to save artifacts |

## Output Artifacts

After running the pipeline, the following files are generated:

### `models/` — Trained models + preprocessor
- `DecisionTreeClassifier.pkl`
- `AdaBoostClassifier.pkl`
- `RandomForestClassifier.pkl`
- `GradientBoostingClassifier.pkl`
- `XGBClassifier.pkl`
- `preprocessor.pkl`

### `outputs/` — Reports and visualizations
| File | Description |
|---|---|
| `eda_summary.json` | Basic EDA statistics |
| `metrics.json` | Evaluation metrics for all models on val + test |
| `predictions.csv` | Actual labels + predictions from all models |
| `classification_report.json` | Detailed report for best model |
| `correlation_heatmap.png` | Feature correlation matrix |
| `confusion_matrices.png` | Confusion matrices for all models |

## Data Leakage Prevention

- `StandardScaler` is fitted **exclusively on the training set**
- Validation and test sets are only **transformed** (never used for fitting)
- All preprocessing happens after the train/val/test split

## Running Tests

```bash
# Run all tests
uv run python -m pytest tests/ -v

# Run specific test
uv run python -m pytest tests/test_preprocess.py -v
```

## Project Structure

```
hw-3/
├── main.ipynb              # Main ML pipeline notebook
├── data/
│   ├── raw_train.csv       # Training data
│   ├── raw_val.csv         # Validation data
│   └── raw_test.csv        # Test data
├── models/                 # Saved models (generated)
├── outputs/                # Reports & metrics (generated)
├── tests/
│   ├── __init__.py
│   ├── sample_data.csv     # Small sample for testing
│   ├── test_preprocess.py  # Data leakage tests
│   └── test_pipeline.py    # Integration test
├── pyproject.toml          # Project config & dependencies
├── README.md               # This file
└── .python-version         # Python 3.11