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

# from catboost import CatBoostClassifier, CatBoostRegressor
from tabpfn import TabPFNRegressor as TabPFNRegressorLocal

logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    # Patch webbrowser.open to prevent browser login
    with patch("webbrowser.open", return_value=False):
        use_server = True
        # use_server = False

        # X, y = load_breast_cancer(return_X_y=True)
        # use openml task 9951
        import openml
        from sklearn.preprocessing import LabelEncoder
        from sklearn.metrics import r2_score

        openml_regression_tasks = [361073, 361074, 361076, 361077, 361279, 361078]
        openml_classification_tasks = [3663, 9951, 3011]
        # for task_id in openml_classification_tasks:
        #     task = openml.tasks.get_task(task_id)
        #     X, y, categorical_indicator, feature_names = task.get_dataset().get_data(target=task.target_name)
        #     # label encode y
        #     le = LabelEncoder()
        #     y = le.fit_transform(y)
        #     X_train, X_test, y_train, y_test = train_test_split(
        #         X, y, test_size=0.33, random_state=42
        #     )

        #     # TabPFN Classification
        #     print("\n=== Classification Task ===")
        #     print(f"Task ID: {task_id}")
        #     print(f"Dataset: {task.get_dataset().name}")
        #     tabpfn = TabPFNClassifier(n_estimators=8, random_state=43)
        #     tabpfn.fit(X_train[:99], y_train[:99])
        #     tabpfn_preds = tabpfn.predict(X_test)
        #     tabpfn_acc = accuracy_score(y_test, tabpfn_preds)
        #     print(f"TabPFN Accuracy: {tabpfn_acc:.4f}")

        #     # # XGBoost Classification
        #     # xgb_clf = XGBClassifier(random_state=43)
        #     # xgb_clf.fit(X_train[:99], y_train[:99])
        #     # xgb_preds = xgb_clf.predict(X_test)
        #     # xgb_acc = accuracy_score(y_test, xgb_preds)
        #     # print(f"XGBoost Accuracy: {xgb_acc:.4f}")

        #     # CatBoost Classification
        #     cat_clf = CatBoostClassifier(random_state=43, verbose=False)
        #     cat_clf.fit(X_train[:99], y_train[:99], cat_features=[i for i in range(X_train.shape[1]) if categorical_indicator[i]])
        #     cat_preds = cat_clf.predict(X_test)
        #     cat_acc = accuracy_score(y_test, cat_preds)
        #     print(f"CatBoost Accuracy: {cat_acc:.4f}")

        for task_id in openml_regression_tasks:
            task = openml.tasks.get_task(task_id)
            X, y, categorical_indicator, feature_names = task.get_dataset().get_data(
                target=task.target_name
            )
            # subsample to 2000
            idx = np.random.choice(len(X), 2000, replace=False)
            X = X.iloc[idx]
            y = y.iloc[idx]
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.33, random_state=42
            )

            # TabPFN Regression
            print("\n=== Regression Task ===")
            tabpfn = TabPFNRegressor(n_estimators=2, random_state=43)
            tabpfn.fit(X_train, y_train)
            tabpfn_reg_preds = tabpfn.predict(X_test, output_type="mean")
            tabpfn_mse = mean_squared_error(y_test, tabpfn_reg_preds)
            tabpfn_r2 = r2_score(y_test, tabpfn_reg_preds)
            print(f"TabPFN MSE: {tabpfn_mse:.4f}")
            print(f"TabPFN R2: {tabpfn_r2:.4f}")

            # local TabPFN
            tabpfn_local = TabPFNRegressorLocal(
                n_estimators=2, random_state=43, n_jobs=1
            )
            tabpfn_local.fit(X_train, y_train)
            tabpfn_local_reg_preds = tabpfn_local.predict(X_test, output_type="mean")
            tabpfn_local_mse = mean_squared_error(y_test, tabpfn_local_reg_preds)
            tabpfn_local_r2 = r2_score(y_test, tabpfn_local_reg_preds)
            print(f"Local TabPFN MSE: {tabpfn_local_mse:.4f}")
            print(f"Local TabPFN R2: {tabpfn_local_r2:.4f}")

            # XGBoost Regression
            xgb_reg = XGBRegressor(random_state=43)
            xgb_reg.fit(X_train, y_train)
            xgb_reg_preds = xgb_reg.predict(X_test)
            xgb_mse = mean_squared_error(y_test, xgb_reg_preds)
            xgb_r2 = r2_score(y_test, xgb_reg_preds)
            print(f"XGBoost MSE: {xgb_mse:.4f}")
            print(f"XGBoost R2: {xgb_r2:.4f}")

            # # CatBoost Regression
            # cat_reg = CatBoostRegressor(random_state=43, verbose=False)
            # cat_reg.fit(X_train, y_train)
            # cat_reg_preds = cat_reg.predict(X_test)
            # cat_mse = mean_squared_error(y_test, cat_reg_preds)
            # cat_r2 = r2_score(y_test, cat_reg_preds)
            # print(f"CatBoost MSE: {cat_mse:.4f}")
            # print(f"CatBoost R2: {cat_r2:.4f}")
