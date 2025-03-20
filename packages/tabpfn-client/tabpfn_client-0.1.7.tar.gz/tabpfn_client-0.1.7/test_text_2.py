import pandas as pd
from tabpfn_client import TabPFNRegressor

df = pd.read_csv("/Users/leo/Downloads/anime_reviews-train.csv").sample(1000)

target_column = "rating"

X = df.drop(columns=[target_column])
y = df[target_column]

model = TabPFNRegressor(
)


model.fit(X, y)

print(model.predict(X))
