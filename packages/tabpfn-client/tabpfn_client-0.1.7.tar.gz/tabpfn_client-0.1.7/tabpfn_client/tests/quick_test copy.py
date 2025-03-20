"""
TabPFN Client Example Usage
--------------------------
Toy script to check that the TabPFN client is working.
Use the breast cancer dataset for classification and the diabetes dataset for regression,
and try various prediction types.
"""

import logging
from unittest.mock import patch

from sklearn.datasets import load_breast_cancer, load_diabetes
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier, XGBRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
import numpy as np

from tabpfn_client import UserDataClient
from tabpfn_client.estimator import TabPFNClassifier, TabPFNRegressor
from tabpfn import TabPFNClassifier as TabPFNClassifierLocal
from tabpfn import TabPFNRegressor as TabPFNRegressorLocal

# from catboost import CatBoostClassifier, CatBoostRegressor
from sklearn.datasets import fetch_openml
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    # Patch webbrowser.open to prevent browser login
    with patch("webbrowser.open", return_value=False):
        df = fetch_openml("diabetes", version=1)
        X, y = df.data, df.target

        # Encode target labels to classes
        le = LabelEncoder()
        y = le.fit_transform(y)

        # Convert all categorical columns to numeric
        for col in X.select_dtypes(["category"]).columns:
            X[col] = X[col].cat.codes

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=42
        )

        # Compare different machine learning models by training each one multiple times
        # on different parts of the data and averaging their performance scores for a
        # more reliable performance estimate

        # Define models
        models = [
            # ('TabPFN-Local', TabPFNClassifierLocal(random_state=42, n_estimators=8)),
            (
                "TabPFN-API-Paper",
                TabPFNClassifier(random_state=42, n_estimators=8, paper_version=True),
            ),
            ("RandomForest", RandomForestClassifier(random_state=42)),
            ("XGBoost", XGBClassifier(random_state=42)),
            # ('CatBoost', CatBoostClassifier(random_state=42, verbose=0))
        ]

        # Calculate scores
        scoring = "roc_auc_ovr" if len(np.unique(y)) > 2 else "roc_auc"
        scores = {
            name: cross_val_score(model, X, y, cv=5, scoring=scoring, n_jobs=-1).mean()
            for name, model in models
        }

        # Plot results
        df = pd.DataFrame(list(scores.items()), columns=["Model", "ROC AUC"])
        ax = df.plot(x="Model", y="ROC AUC", kind="bar", figsize=(10, 6))
        ax.set_ylim(df["ROC AUC"].min() * 0.99, df["ROC AUC"].max() * 1.01)
        ax.set_title("Model Comparison - 5-fold Cross-validation")
        plt.show()
