# main.py
import os

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Heart Disease Prediction Demo",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# -----------------------------
# Feature order expected by preprocessor.pkl
# (Must match the EXACT order used in training — eda.ipynb Cell 9-10)
# -----------------------------
# The StandardScaler (preprocessor.pkl) was fitted on RAW values for these 10 features
# in the order below. Inference must pass raw values in the SAME order.
SELECTED_FEATURES = [
    "age",
    "trestbps",
    "thalach",
    "sex",
    "cp",
    "restecg",
    "exang",
    "slope",
    "ca",
    "thal",
]

MODEL_NAMES = [
    "DecisionTreeClassifier",
    "AdaBoostClassifier",
    "RandomForestClassifier",
    "GradientBoostingClassifier",
    "XGBClassifier",
]

# -----------------------------
# Demo data
# -----------------------------
EXAMPLES = {
    "Example 1 (No Heart Disease)": {
        "age": 58,
        "sex": 1,
        "cp": 2,
        "trestbps": 130,
        "chol": 250,
        "fbs": 0,
        "restecg": 1,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 1.0,
        "slope": 1,
        "ca": 0,
        "thal": 3,
    },
    "Example 2 (Mild Heart Disease)": {
        "age": 63,
        "sex": 1,
        "cp": 4,
        "trestbps": 145,
        "chol": 233,
        "fbs": 1,
        "restecg": 2,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 2.3,
        "slope": 3,
        "ca": 0,
        "thal": 6,
    },
    "Example 3 (High Risk)": {
        "age": 68,
        "sex": 1,
        "cp": 4,
        "trestbps": 160,
        "chol": 280,
        "fbs": 1,
        "restecg": 2,
        "thalach": 100,
        "exang": 1,
        "oldpeak": 4.0,
        "slope": 3,
        "ca": 3,
        "thal": 7,
    },
    "Example 4 (Young Healthy)": {
        "age": 35,
        "sex": 0,
        "cp": 1,
        "trestbps": 110,
        "chol": 180,
        "fbs": 0,
        "restecg": 0,
        "thalach": 180,
        "exang": 0,
        "oldpeak": 0.0,
        "slope": 1,
        "ca": 0,
        "thal": 3,
    },
    "Example 5 (Borderline)": {
        "age": 52,
        "sex": 1,
        "cp": 3,
        "trestbps": 138,
        "chol": 220,
        "fbs": 0,
        "restecg": 1,
        "thalach": 130,
        "exang": 1,
        "oldpeak": 1.8,
        "slope": 2,
        "ca": 1,
        "thal": 6,
    },
}


# -----------------------------
# Load artifacts with cache
# -----------------------------
@st.cache_resource
def load_artifacts():
    model_dir = os.path.join(os.path.dirname(__file__), "models")
    # Models
    models = {}
    for name in MODEL_NAMES:
        path = os.path.join(model_dir, f"{name}.pkl")
        models[name] = joblib.load(path)
    # Preprocessor: StandardScaler fitted on RAW selected features during training
    preprocessor = joblib.load(os.path.join(model_dir, "preprocessor.pkl"))
    return models, preprocessor


# -----------------------------
# Preprocessing: raw patient dict -> raw DataFrame (same format as training input)
# -----------------------------
def preprocess_patient(patient: dict) -> pd.DataFrame:
    """Extract the 10 selected raw features from patient dict in training order.

    NOTE: "chol", "fbs", "oldpeak" were dropped during EDA-based feature selection
    (see outputs/feature_selection.json) and are NOT used by the models.
    They are collected in the UI for display/reference purposes only.
    """
    raw_df = pd.DataFrame([{col: patient[col] for col in SELECTED_FEATURES}])
    return raw_df


# -----------------------------
# Prediction
# -----------------------------
def get_model_predictions(patient: dict) -> dict:
    models, preprocessor = load_artifacts()

    # Extract raw features (same as training input before scaling)
    X_raw = preprocess_patient(patient)
    # Scale exactly as done during training (single StandardScaler on all raw features)
    X_scaled = preprocessor.transform(X_raw)

    result = {}
    probs = []

    for name in MODEL_NAMES:
        model = models[name]
        prob_class1 = model.predict_proba(X_scaled)[0, 1]
        confidence = round(float(prob_class1), 2)
        label = "Heart Disease" if prob_class1 >= 0.5 else "No Heart Disease"
        result[name] = {"confidence": confidence, "label": label}
        probs.append(prob_class1)

    # Ensemble (Soft Voting): average probabilities
    ensemble_prob = float(np.mean(probs))
    ensemble_confidence = round(ensemble_prob, 2)
    ensemble_label = "Heart Disease" if ensemble_prob >= 0.5 else "No Heart Disease"
    result["Ensemble (Soft Voting)"] = {
        "confidence": ensemble_confidence,
        "label": ensemble_label,
    }

    return result


# -----------------------------
# Chart
# -----------------------------
def draw_prediction_chart(predictions: dict):
    models = list(predictions.keys())
    confidence = [v["confidence"] for v in predictions.values()]
    labels = [v["label"] for v in predictions.values()]

    # Majority voting among individual models (exclude Ensemble)
    individual_models = [k for k in predictions.keys() if k != "Ensemble (Soft Voting)"]
    votes_hd = sum(
        1 for k in individual_models if predictions[k]["label"] == "Heart Disease"
    )
    votes_no_hd = len(individual_models) - votes_hd
    majority_label = "Heart Disease" if votes_hd >= votes_no_hd else "No Heart Disease"

    # Green if model matches majority, red if not
    colors = ["#2e7d32" if label == majority_label else "#c92f4f" for label in labels]

    fig, ax = plt.subplots(figsize=(8.4, 5.1))

    x = np.arange(len(models))
    bars = ax.bar(x, confidence, color=colors, edgecolor="black", linewidth=1.0)

    ax.set_title("Model Predictions", fontsize=15, pad=12)
    ax.set_ylabel("Prediction Confidence", fontsize=12)
    ax.set_xlabel("Model", fontsize=12, labelpad=18)
    ax.set_ylim(0, 1.12)

    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=-35, ha="left", fontsize=10)

    ax.set_yticks(np.linspace(0, 1, 6))
    ax.set_yticklabels([f"{v:g}" for v in np.linspace(0, 1, 6)])

    for bar, value, label in zip(bars, confidence, labels):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.04,
            f"{int(value * 100)}%",
            ha="center",
            va="bottom",
            fontsize=11,
        )

        inner_text = (
            "✓ No Heart Disease" if label == "No Heart Disease" else "⚕ Heart Disease"
        )
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value / 2,
            inner_text,
            ha="center",
            va="center",
            rotation=270,
            color="white",
            fontsize=9,
            fontweight="bold",
        )

    for spine in ax.spines.values():
        spine.set_color("black")
        spine.set_linewidth(1.0)

    ax.grid(False)
    fig.tight_layout()
    return fig


left_col, right_col = st.columns([1.05, 1.0], gap="large")

with left_col:
    st.markdown(
        '<div class="section-title">✍️ Enter Patient Features</div>',
        unsafe_allow_html=True,
    )

    # Initialize session state for example selection (used at bottom of form)
    if "example_select" not in st.session_state:
        st.session_state.example_select = list(EXAMPLES.keys())[0]

    defaults = EXAMPLES[st.session_state.example_select]

    with st.form("patient_form"):
        row1 = st.columns(4)
        with row1[0]:
            age = st.number_input(
                "age (years)", min_value=1, max_value=120, value=defaults["age"]
            )
        with row1[1]:
            sex = st.selectbox("sex (0=female, 1=male)", [0, 1], index=defaults["sex"])
        with row1[2]:
            cp = st.selectbox(
                "cp (chest pain type 1..4)", [1, 2, 3, 4], index=defaults["cp"] - 1
            )
        with row1[3]:
            trestbps = st.number_input(
                "trestbps (resting BP mmHg)",
                min_value=60,
                max_value=250,
                value=defaults["trestbps"],
            )

        st.divider()

        row2 = st.columns(4)
        with row2[0]:
            chol = st.number_input(
                "chol (serum cholesterol mg/dl) — not used by model",
                min_value=80,
                max_value=700,
                value=defaults["chol"],
            )
        with row2[1]:
            fbs = st.selectbox(
                "fbs (>120 mg/dl? 1/0) — not used by model",
                [0, 1],
                index=defaults["fbs"],
            )
        with row2[2]:
            restecg = st.selectbox(
                "restecg (0..2)", [0, 1, 2], index=defaults["restecg"]
            )
        with row2[3]:
            thalach = st.number_input(
                "thalach (max heart rate)",
                min_value=60,
                max_value=250,
                value=defaults["thalach"],
            )

        st.divider()

        row3 = st.columns(4)
        with row3[0]:
            exang = st.selectbox(
                "exang (exercise angina 1/0)", [0, 1], index=defaults["exang"]
            )
        with row3[1]:
            oldpeak = st.number_input(
                "oldpeak (ST depression) — not used by model",
                min_value=0.0,
                max_value=10.0,
                value=float(defaults["oldpeak"]),
                step=0.1,
            )
        with row3[2]:
            slope = st.selectbox("slope (1..3)", [1, 2, 3], index=defaults["slope"] - 1)
        with row3[3]:
            ca = st.selectbox(
                "ca (major vessels 0..3)", [0, 1, 2, 3], index=defaults["ca"]
            )

        st.divider()

        thal_options = [3, 6, 7]
        thal = st.selectbox(
            "thal (3=normal, 6=fixed, 7=reversible)",
            thal_options,
            index=thal_options.index(defaults["thal"]),
        )

        action_row = st.columns([2.2, 1])
        with action_row[0]:
            st.selectbox(
                "Select Example Patient",
                options=list(EXAMPLES.keys()),
                key="example_select",
            )
        with action_row[1]:
            submitted = st.form_submit_button("🔍 Predict", use_container_width=True)

    patient = {
        "age": age,
        "sex": sex,
        "cp": cp,
        "trestbps": trestbps,
        "chol": chol,
        "fbs": fbs,
        "restecg": restecg,
        "thalach": thalach,
        "exang": exang,
        "oldpeak": oldpeak,
        "slope": slope,
        "ca": ca,
        "thal": thal,
    }

with right_col:
    if submitted:
        predictions = get_model_predictions(patient)

        with st.expander("📉 Model Predictions Overview", expanded=True):
            fig = draw_prediction_chart(predictions)
            st.pyplot(fig, use_container_width=True)
    else:
        st.info("👈 Select an example or enter values and click **Predict**")
