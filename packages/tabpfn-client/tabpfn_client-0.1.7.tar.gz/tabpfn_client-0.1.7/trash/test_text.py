from tabpfn_client import TabPFNClassifier
import pandas as pd

# load the dataset
df = pd.read_csv('/Users/leo/Downloads/fake_job_postings2.csv')

X = df.drop(columns=['fraudulent'])
y = df['fraudulent']
# remove the description column
print(X.head())

#classifier = TabPFNClassifier(paper_version=True)
#classifier.fit(X, y)

