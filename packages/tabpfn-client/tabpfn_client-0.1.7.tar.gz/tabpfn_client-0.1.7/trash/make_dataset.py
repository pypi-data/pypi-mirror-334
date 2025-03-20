import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Create sample data with missing values
n_samples = 100
data = {
    'product': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Watch'], n_samples),
    'price': np.random.uniform(200, 2000, n_samples),
    'rating': np.random.uniform(1, 5, n_samples),
    'units_sold': np.random.randint(10, 1000, n_samples),
    'in_stock': np.random.choice(['Yes', 'No'], n_samples),
    'category': np.random.choice(['Electronics', 'Accessories'], n_samples)
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Introduce missing values randomly (approximately 15% of data)
for column in ['price', 'rating', 'units_sold']:
    mask = np.random.random(len(df)) < 0.15
    df.loc[mask, column] = None

# Save DataFrame to CSV
df.to_csv('product_data.csv', index=False)

print("Dataset saved to product_data.csv")
print("\nFirst few rows:")
print(df.head())
