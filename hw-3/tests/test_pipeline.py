"""
Test: Verify the full pipeline can run on a small sample dataset and produce all expected outputs.
"""

import os
import json
import tempfile
import subprocess
import sys

SAMPLE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SAMPLE_DIR)
SAMPLE_DATA = os.path.join(SAMPLE_DIR, "sample_data.csv")


def get_notebook_path():
    nb_path = os.path.join(PROJECT_DIR, "main.ipynb")
    if not os.path.exists(nb_path):
        raise FileNotFoundError(f"Notebook not found: {nb_path}")
    return nb_path


def get_notebook_code():
    """Extract python code cells from the notebook as a single script."""
    nb_path = get_notebook_path()
    with open(nb_path, "r") as f:
        nb = json.load(f)

    code_lines = []
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            source = "".join(cell["source"])
            # Skip cells that define CONFIG or os.makedirs — we override those
            if "CONFIG =" in source or "os.makedirs(CONFIG" in source:
                continue
            for line in cell["source"]:
                code_lines.append(line)

    return "".join(code_lines)


def build_pipeline_script(output_dir: str):
    """Build a Python script from the notebook code with overridden config."""
    nb_code = get_notebook_code()

    model_dir = os.path.join(output_dir, "models")
    output_dir_inner = os.path.join(output_dir, "outputs")
    override_config = f"""
# ===== OVERRIDDEN CONFIG FOR TESTING =====
import os, json, tempfile
CONFIG = {{
    "train_path": r"{SAMPLE_DATA}",
    "val_path": r"{SAMPLE_DATA}",
    "test_path": r"{SAMPLE_DATA}",
    "target_col": "target",
    "problem_type": "classification",
    "resplit": False,
    "test_size": 0.15,
    "val_size": 0.10,
    "random_seed": 42,
    "model_dir": r"{model_dir}",
    "output_dir": r"{output_dir_inner}",
    "feature_selection": "all",
}}
os.makedirs(CONFIG["model_dir"], exist_ok=True)
os.makedirs(CONFIG["output_dir"], exist_ok=True)
import numpy as np
np.random.seed(CONFIG["random_seed"])
print(f"Test config loaded. Outputs -> {{CONFIG['output_dir']}}/, Models -> {{CONFIG['model_dir']}}/")
# ==========================================
"""
    return override_config + "\n" + nb_code


def test_pipeline_produces_artifacts():
    """Run the full pipeline on sample data and verify all artifacts exist."""
    with tempfile.TemporaryDirectory(prefix="ml_pipeline_test_") as tmpdir:
        script = build_pipeline_script(tmpdir)
        script_path = os.path.join(tmpdir, "run_pipeline.py")

        with open(script_path, "w") as f:
            f.write(script)

        # Execute the pipeline script
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode != 0:
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            raise RuntimeError(f"Pipeline exited with code {result.returncode}")

        # Verify all expected artifacts
        model_dir = os.path.join(tmpdir, "models")
        output_dir = os.path.join(tmpdir, "outputs")

        expected_models = [
            "DecisionTreeClassifier.pkl",
            "AdaBoostClassifier.pkl",
            "RandomForestClassifier.pkl",
            "GradientBoostingClassifier.pkl",
            "XGBClassifier.pkl",
            "preprocessor.pkl",
        ]
        expected_outputs = [
            "metrics.json",
            "eda_summary.json",
            "predictions.csv",
            "classification_report.json",
        ]

        missing_models = [m for m in expected_models if not os.path.exists(os.path.join(model_dir, m))]
        missing_outputs = [o for o in expected_outputs if not os.path.exists(os.path.join(output_dir, o))]

        errors = []
        if missing_models:
            errors.append(f"Missing model files: {missing_models}")
        if missing_outputs:
            errors.append(f"Missing output files: {missing_outputs}")

        # Verify metrics JSON is valid and contains expected keys
        metrics_path = os.path.join(output_dir, "metrics.json")
        if os.path.exists(metrics_path):
            with open(metrics_path) as f:
                metrics = json.load(f)
            if not isinstance(metrics, list) or len(metrics) == 0:
                errors.append("metrics.json should be a non-empty list")
            else:
                required_keys = {"model", "dataset", "accuracy", "precision", "recall", "f1_score"}
                for entry in metrics:
                    if not required_keys.issubset(entry.keys()):
                        errors.append(f"Metrics entry missing keys: {set(entry.keys())} vs {required_keys}")
                        break

        if errors:
            raise AssertionError("\n".join(errors))

        print("PASS: All pipeline artifacts verified.")
        print(f"  Models: {len(expected_models) - 1} trained models + preprocessor")
        print(f"  Outputs: {len(expected_outputs)} artifact files")


if __name__ == "__main__":
    test_pipeline_produces_artifacts()
    print("All pipeline tests passed.")