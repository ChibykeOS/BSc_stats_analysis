import pandas as pd
import json

# Load the dataset
df = pd.read_excel('complete_data.xlsx')

# Save column names to JSON for easy viewing
columns_info = {
    'total_rows': df.shape[0],
    'total_columns': df.shape[1],
    'columns': df.columns.tolist(),
    'residence_counts': df['Residence'].value_counts().to_dict() if 'Residence' in df.columns else {}
}

with open('columns_info.json', 'w') as f:
    json.dump(columns_info, f, indent=2)

print("Column information saved to columns_info.json")
print(f"\nDataset: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"\nResidence distribution:")
if 'Residence' in df.columns:
    print(df['Residence'].value_counts())
