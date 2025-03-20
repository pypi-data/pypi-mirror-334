import openml
import pandas as pd

# Download dataset 4541 from OpenML
dataset = openml.datasets.get_dataset(57)

# Get the data and convert to pandas DataFrame 
X, y, categorical_indicator, attribute_names = dataset.get_data()
df = pd.DataFrame(X, columns=attribute_names)

# Save to CSV
# shuffle
df = df.sample(frac=1).reset_index(drop=True)
# split 80% train, 20% test
train_df = df.iloc[:int(0.8*len(df))]
test_df = df.iloc[int(0.8*len(df)):]

# Save to CSV
train_df.to_csv('hypothyroid_train.csv', index=False)
test_df.to_csv('hypothyroid_test.csv', index=False)
