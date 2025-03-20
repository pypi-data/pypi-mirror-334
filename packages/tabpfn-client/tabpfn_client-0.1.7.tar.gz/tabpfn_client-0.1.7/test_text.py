from tabpfn_client import TabPFNClassifier
import pandas as pd
from unittest.mock import patch

with patch("webbrowser.open", return_value=False):
    # load the dataset
    df = pd.read_csv('/Users/leo/Downloads/fake_job_postings2.csv')
    print(df.head())
    # remove commas in column description
    # ... existing code ...

    # Clean the description column
    # df['description'] = (df['description']
    #     .str.lower()  # convert to lowercase
    #     .str.replace(r'[^\w\s]', '', regex=True)  # remove special characters and punctuation
    #     .str.replace(r'\s+', ' ', regex=True)  # replace multiple spaces with single space
    #     .str.strip()  # remove leading/trailing whitespace
    # )

    # ... existing code ...
    X = df.drop(columns=['fraudulent'])
    y = df['fraudulent']
    # remove the description column
    # make it numpy array
    X = X.to_numpy()
    y = y.to_numpy()

    classifier = TabPFNClassifier(paper_version=True)
    classifier.fit(X, y)

