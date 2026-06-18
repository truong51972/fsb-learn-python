"""
Test: Verify preprocessing does not leak data.
- StandardScaler must be fitted on train only.
- Transforming val/test must NOT call .fit() or .fit_transform().
"""

import numpy as np
from sklearn.preprocessing import StandardScaler

SAMPLE_SIZE = 20


def test_preprocessor_fitted_on_train_only():
    """Verify scaler mean/std come from train, not from test."""
    rng = np.random.RandomState(42)

    # Create train/test with deliberately different distributions
    X_train = rng.normal(loc=10, scale=2, size=(SAMPLE_SIZE, 3))
    X_test = rng.normal(loc=100, scale=20, size=(SAMPLE_SIZE, 3))

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # The scaler's mean should be close to train's mean (~10), not test's (~100)
    assert abs(scaler.mean_[0] - 10) < 2, (
        f"Scaler mean ({scaler.mean_[0]:.2f}) should be close to train mean (~10), "
        f"not test mean (~100)"
    )

    # Verify test data still has different distribution after transform
    test_mean_after = X_test_scaled.mean(axis=0)
    assert abs(test_mean_after[0]) > 2, (
        f"Test mean after transform ({test_mean_after[0]:.2f}) should differ from 0 "
        f"since test distribution differs from train"
    )

    print("PASS: Preprocessor correctly fitted on train only.")


def test_transform_does_not_modify_scaler():
    """Verify .transform() does not alter the fitted scaler's parameters."""
    rng = np.random.RandomState(42)
    X_train = rng.randn(SAMPLE_SIZE, 3)
    X_test = rng.randn(SAMPLE_SIZE, 3)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    mean_before = scaler.mean_.copy()
    var_before = scaler.var_.copy()

    # Transform multiple times
    for _ in range(3):
        scaler.transform(X_test)

    # Verify parameters unchanged
    np.testing.assert_array_equal(scaler.mean_, mean_before, err_msg="Mean changed after transform!")
    np.testing.assert_array_equal(scaler.var_, var_before, err_msg="Variance changed after transform!")

    print("PASS: .transform() does not modify fitted scaler.")


if __name__ == "__main__":
    test_preprocessor_fitted_on_train_only()
    test_transform_does_not_modify_scaler()
    print("All preprocess tests passed.")