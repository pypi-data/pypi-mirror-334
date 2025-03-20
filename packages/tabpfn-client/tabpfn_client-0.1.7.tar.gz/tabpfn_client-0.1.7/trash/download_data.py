import openml
import pandas as pd

# Download dataset 4541 from OpenML
dataset = openml.datasets.get_dataset(4541)

# Get the data and convert to pandas DataFrame 
X, y, categorical_indicator, attribute_names = dataset.get_data()
df = pd.DataFrame(X, columns=attribute_names)

# remove nans in Readmitted
df = df[df['readmitted'].notna()]

columns_to_remove = ['race', "encounter_id", "patient_nbr", "glimepiride.pioglitazone",
                     "glyburide", "tolbutamide", "pioglitazone", "rosiglitazone", 
                     "acarbose", "miglitol", "troglitazone", "tolazamide", "examide", "citoglipton",
                     "max_glu_serum", "A1Cresult", "repaglinide", "nateglinide", "chlorpropamide",
                     "payer_code"]
# if metformin in columns, remove it
for column in df.columns:
    if 'metformin' in column:
        columns_to_remove.append(column)

# replace "?" with NaN
df = df.replace("?", pd.NA)

# remove columns_to_remove
df = df.drop(columns=columns_to_remove)

# Keep only top 10 most important features plus target
selected_features = [
    'age',
    "gender",
    "insulin",
    "glipizide",
    'admission_type_id',
    'num_medications',
    'number_diagnoses',
    'discharge_disposition_id',
    'num_procedures',
    'readmitted'  # target variable
]

df = df[selected_features]

# take 1K rows for train and 250 rows for test
train_df = df.sample(n=1000)
test_df = df.sample(n=250)

# Save to CSV
train_df.to_csv('diabetes130US_train.csv', index=False)
test_df.to_csv('diabetes130US_test.csv', index=False)
