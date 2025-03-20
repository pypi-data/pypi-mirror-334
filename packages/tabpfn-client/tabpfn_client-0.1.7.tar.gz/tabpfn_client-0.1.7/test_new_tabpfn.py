import numpy as np
from tabpfn_client import TabPFNClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Load and prepare the electricity_small dataset
def load_electricity_data():
    df = pd.read_csv('electricity.csv')  # Adjust path as needed
    # subsample to 30000
    df = df.sample(n=3000, random_state=42)
    X = df.drop('target', axis=1)
    y = df['target']
    return X, y

def main():
    # Load data
    X, y = load_electricity_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train and evaluate TabPFN
    tabpfn = TabPFNClassifier()  # Use 'cuda' if GPU available
    tabpfn.fit(X_train, y_train)
    tabpfn_pred = tabpfn.predict(X_test)
    tabpfn_pred_proba = tabpfn.predict_proba(X_test)
    
    # Train and evaluate XGBoost
    xgb = XGBClassifier(random_state=42)
    xgb.fit(X_train, y_train)
    xgb_pred = xgb.predict(X_test)
    xgb_pred_proba = xgb.predict_proba(X_test)

    # Calculate metrics
    print("TabPFN Results:")
    print(f"Accuracy: {accuracy_score(y_test, tabpfn_pred):.4f}")
    print(f"ROC AUC: {roc_auc_score(y_test, tabpfn_pred_proba[:, 1]):.4f}")
    
    print("\nXGBoost Results:")
    print(f"Accuracy: {accuracy_score(y_test, xgb_pred):.4f}")
    print(f"ROC AUC: {roc_auc_score(y_test, xgb_pred_proba[:, 1]):.4f}")

if __name__ == "__main__":
    main()
