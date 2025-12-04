import pandas as pd

# Load the dataset
df = pd.read_excel('complete_data.xlsx')

print("="*80)
print("DATASET OVERVIEW")
print("="*80)
print(f"Total Rows: {df.shape[0]}")
print(f"Total Columns: {df.shape[1]}")

print("\n" + "="*80)
print("ALL COLUMN NAMES")
print("="*80)
for i, col in enumerate(df.columns, 1):
    print(f"{i:3d}. {col}")

print("\n" + "="*80)
print("FIRST 5 ROWS")
print("="*80)
print(df.head())

print("\n" + "="*80)
print("DATA TYPES")
print("="*80)
print(df.dtypes)

print("\n" + "="*80)
print("MISSING VALUES")
print("="*80)
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({'Missing': missing, 'Percentage': missing_pct})
print(missing_df[missing_df['Missing'] > 0].sort_values('Missing', ascending=False))

print("\n" + "="*80)
print("RESIDENCE DISTRIBUTION")
print("="*80)
print(df['Residence'].value_counts())
