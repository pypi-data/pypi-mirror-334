import numpy as np
import time
from sklearn.model_selection import train_test_split
from tabpfn_client import TabPFNClassifier
from sklearn.model_selection import cross_val_score

from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

def make_prediction(i):
    try:
        # Generate random dataset
        # sleep for i seconds
        #time.sleep(i)
        X = np.random.randn(100, 10) 
        y = (X[:, 0] + X[:, 1] > 0).astype(int) # Simple binary classification rule
        # Split data for this iteration
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=i)

        classifier = TabPFNClassifier(n_estimators=1)

        
        # Fit and predict
        classifier.fit(X_train, y_train)
        score = classifier.score(X_test, y_test)
        return f"Request {i}: Score = {score}"
    except Exception as e:
        return f"Request {i} failed: {str(e)}"

# Make 100 parallel requests using ThreadPoolExecutor
total_requests = 20
completed_requests = 0
failed_requests = 0

with ThreadPoolExecutor(max_workers=200) as executor:
    future_to_request = {executor.submit(make_prediction, i): i for i in range(total_requests)}
    
    for future in concurrent.futures.as_completed(future_to_request):
        request_id = future_to_request[future]
        try:
            result = future.result()
            completed_requests += 1
            remaining = total_requests - completed_requests
            print(f"{result} | Completed: {completed_requests}, Failed: {failed_requests}, Remaining: {remaining}")
        except Exception as e:
            completed_requests += 1
            failed_requests += 1
            remaining = total_requests - completed_requests
            print(f"Request {request_id} generated an exception: {str(e)} | Completed: {completed_requests}, Failed: {failed_requests}, Remaining: {remaining}")
