import numpy as np
from sklearn.model_selection import train_test_split
from tabpfn_client import TabPFNClassifier
from sklearn.model_selection import cross_val_score

# Generate random dataset
X = np.random.randn(5000, 10) 
y = (X[:, 0] + X[:, 1] > 0).astype(int) # Simple binary classification rule

# Convert X to list of lists for string manipulation
# X_list = X.tolist()
# for i in range(len(X_list)):
#     for j in range(len(X_list[i])):
#         X_list[i][j] = f"{X_list[i][j]}_{i}"

#X = np.array(X_list)
# add a numerical column
X = np.hstack((X, np.arange(len(X)).reshape(-1, 1)))
# add a categorical column
X = np.hstack((X, np.random.choice(['A', 'B', 'C'], size=len(X)).reshape(-1, 1)))
# make it into a pandas dataframe
import pandas as pd
X = pd.DataFrame(X)
print(X.head())

# Initialize TabPFN
classifier = TabPFNClassifier(paper_version=False)

# Perform 5-fold cross validation
#cv_scores = cross_val_score(classifier, X, y, cv=5, error_score='raise', n_jobs=5)
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import time

def run_iteration(i):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=i)
    classifier.fit(X_train, y_train)
    score = classifier.score(X_test, y_test)
    return f"Score {i}: {score}"

times = []
for i in range(15):
    try:
        start_time = time.time()
        print(run_iteration(i))
        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")
        times.append(end_time - start_time)
    except Exception as e:
        print(f"Iteration {i} failed: {str(e)}")

print(f"Average time taken: {np.mean(times)} seconds")
