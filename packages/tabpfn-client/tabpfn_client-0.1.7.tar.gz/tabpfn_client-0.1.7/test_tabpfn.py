import numpy as np
from tabpfn_client import TabPFNClassifier
from sklearn.metrics import accuracy_score
import pytest

def test_tabpfn_classifier():
    # Print version
    #print(f"TabPFN version: {tabpfn.__version__}")
    
    # Generate random data
    np.random.seed(42)
    X = np.random.randn(100, 10)  # 100 samples, 10 features
    y = np.random.randint(0, 2, 100)  # Binary classification
    
    # Split into train and test
    train_size = 80
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    
    # Initialize and train classifier
    classifier = TabPFNClassifier(device='cpu')
    classifier.fit(X_train, y_train)
    
    # Make predictions
    y_pred = classifier.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test accuracy: {accuracy:.3f}")
    
    # Basic assertions
    assert y_pred.shape == y_test.shape
    assert 0 <= accuracy <= 1

if __name__ == "__main__":
    test_tabpfn_classifier()
