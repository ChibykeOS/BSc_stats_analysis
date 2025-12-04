"""
Data Preparation Script for Nutritional Status Analysis
========================================================
This script prepares the raw data for statistical analysis by:
1. Loading the dataset
2. Coding food frequency variables (Daily=6 to Never=1)
3. Calculating BMI categories
4. Computing Dietary Diversity Scores (DDS)
5. Exporting cleaned dataset
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("DATA PREPARATION FOR NUTRITIONAL STATUS ANALYSIS")
print("="*80)

# ============================================================================
# 1. LOAD DATASET
# ============================================================================
print("\n[1/5] Loading dataset...")
df = pd.read_excel('complete_data.xlsx')
print(f"   ✓ Loaded {df.shape[0]} rows and {df.shape[1]} columns")

# Create a copy for processing
data = df.copy()

# Standardize text columns to Title Case to fix "yes"/"Yes" inconsistencies
text_columns = ['Do you skip meals', 'Prefer snacks over food? (Yes/No)', 'Residence', 
                'Living With', 'Marital Status of Parents', 'Religion', 'Ethnic Group',
                'Which meal skipped', 'Reason for skipping meals', 'Source of food',
                'Reason for snack preference']

print("\n[1.5/5] Standardizing text variables...")
for col in text_columns:
    if col in data.columns:
        # Convert to string, strip whitespace, and capitalize first letter
        data[col] = data[col].astype(str).str.strip().str.title()
        # Replace 'Nan' (from string conversion of NaN) back to actual NaN
        data[col] = data[col].replace('Nan', np.nan)
        print(f"   ✓ Standardized {col}")

# ============================================================================
# 2. CODE FOOD FREQUENCY VARIABLES
# ============================================================================
print("\n[2/5] Coding food frequency variables...")

# Define frequency mapping
frequency_mapping = {
    'daily': 6,
    'Daily': 6,
    'DAILY': 6,
    '4-6x': 5,
    '4-6X': 5,
    '2-3x': 4,
    '2-3X': 4,
    '1x': 3,
    '1X': 3,
    'occ': 2,
    'Occ': 2,
    'OCC': 2,
    'occasionally': 2,
    'Occasionally': 2,
    '0x': 1,
    '0X': 1,
    'never': 1,
    'Never': 1,
    'NEVER': 1
}

# Identify food frequency columns (all food items)
food_groups = {
    'Dairy': ['Milk ', 'Yoghurt', 'Ice cream', 'Dairy_Other'],
    'Tubers': ['Yam', 'Cocoyam', 'Water yam', 'Sweet Potatoe', 
               'Irish Potatoes (Daily/1wk/2-3x/4-6x/Occasional/Never)', 'Tubers_Other'],
    'Legumes': ['Beans', 'Pigeon pea', 'Bambara nut', 'Soybean products',
                'Breadfruit (Daily/1wk/2-3x/4-6x/Occasional/Never)', 
                'Groundnut', 'African yam bean', 'Legumes_Other'],
    'Cereals': ['Rice', 'Maize', 'Millet', 'Guinea corn', 'Wheat', 'Oats', 'Cereals_Other'],
    'Meats': ['Beef', 'Goat meat', 'Chicken', 'Turkey', 'Egg', 'Fish', 'Pork meat', 'Snail', 'Kpomo'],
    'Vegetables': ['Tomatoes', 'Ugu', 'Scent leaf', 'Water leaf', 'Green', 'Bitter leaf ',
                   'Carrot', 'Cabbage', 'Cucumber', 'Garden', 'Okro', 'Pumpkin', 'Veg_Other'],
    'Fruits': ['Apple', 'Orange', 'Grapes', 'Banana', 'Soursop', 'Avocado', 'African pear',
               'Forest pear', 'Watermelon', 'Pineapple', 'Agbalumo', 'Pawpaw', 'Mango', 
               'Guava', 'Cashew', 'Fruit_Other'],
    'Spices': ['Garlic ', 'Rosemary', 'Thyme', 'Turmeric', 'Nutmeg', 'Okpei', 'Ogiri', 'Spice_Other'],
    'Drinks': ['Water', 'Soft drinks', 'Alcoholic beverages', 'Wines', 'Palm wine', 'Beer', 'Drink_Other'],
    'Snacks': ['Biscuits ', 'Chin-chin', 'Buns', 'Doughnut', 'Peanut', 'Plantain', 
               'Chocolate', 'Eggrolls', 'Snack_Other']
}

# Flatten all food items
all_food_items = []
for group, items in food_groups.items():
    all_food_items.extend(items)

# Code frequency variables
coded_count = 0
for col in all_food_items:
    if col in data.columns:
        # Create coded column
        coded_col = f"{col}_coded"
        data[coded_col] = data[col].map(frequency_mapping)
        
        # If mapping failed, try to handle numeric values
        if data[coded_col].isna().any():
            # Check if already numeric
            try:
                data[coded_col] = data[coded_col].fillna(pd.to_numeric(data[col], errors='coerce'))
            except:
                pass
        
        coded_count += 1

print(f"   ✓ Coded {coded_count} food frequency variables")

# ============================================================================
# 3. CALCULATE BMI CATEGORIES
# ============================================================================
print("\n[3/5] Calculating BMI categories...")



# BMI column has no missing values, so we use it directly
data['BMI_final'] = pd.to_numeric(data['BMI'], errors='coerce')

# Define BMI categories for adolescents (using standard WHO cutoffs)
# For adolescents, we use: <18.5 (Underweight), 18.5-24.9 (Normal), 25-29.9 (Overweight), ≥30 (Obese)
def categorize_bmi(bmi):
    if pd.isna(bmi):
        return 'Unknown'
    elif bmi < 18.5:
        return 'Underweight'
    elif bmi < 25:
        return 'Normal'
    elif bmi < 30:
        return 'Overweight'
    else:
        return 'Obese'

data['BMI_category'] = data['BMI_final'].apply(categorize_bmi)

print(f"   ✓ BMI categories created")
print(f"      Distribution:")
for category in ['Underweight', 'Normal', 'Overweight', 'Obese', 'Unknown']:
    count = (data['BMI_category'] == category).sum()
    pct = (count / len(data)) * 100
    print(f"      - {category}: {count} ({pct:.1f}%)")

# ============================================================================
# 4. CALCULATE DIETARY DIVERSITY SCORE (DDS)
# ============================================================================
print("\n[4/5] Calculating Dietary Diversity Score (DDS)...")

# DDS: Count how many food groups consumed at least "once per week" (coded value ≥ 3)
def calculate_dds(row, food_groups):
    score = 0
    for group, items in food_groups.items():
        # Check if any item in the group is consumed ≥ once per week
        group_consumed = False
        for item in items:
            coded_col = f"{item}_coded"
            if coded_col in row.index:
                if pd.notna(row[coded_col]) and row[coded_col] >= 3:
                    group_consumed = True
                    break
        if group_consumed:
            score += 1
    return score

data['DDS'] = data.apply(lambda row: calculate_dds(row, food_groups), axis=1)

print(f"   ✓ DDS calculated (range: {data['DDS'].min():.0f} - {data['DDS'].max():.0f})")
print(f"      Mean DDS: {data['DDS'].mean():.2f} ± {data['DDS'].std():.2f}")

# ============================================================================
# 5. EXPORT CLEANED DATASET
# ============================================================================
print("\n[5/5] Exporting cleaned dataset...")

# Select relevant columns for analysis
# Keep original columns + coded columns + new calculated columns
data.to_csv('cleaned_data.csv', index=False)
print(f"   ✓ Cleaned dataset saved to 'cleaned_data.csv'")

# Create a summary report
summary = {
    'Total Participants': len(data),
    'Urban': (data['Residence'] == 'urban').sum(),
    'Rural': (data['Residence'] == 'rural').sum(),
    'Mean Age': data['Age Group '].value_counts().to_dict() if 'Age Group ' in data.columns else 'N/A',
    'BMI Categories': data['BMI_category'].value_counts().to_dict(),
    'Mean DDS': f"{data['DDS'].mean():.2f} ± {data['DDS'].std():.2f}",
    'DDS Range': f"{data['DDS'].min():.0f} - {data['DDS'].max():.0f}"
}

# Save summary
with open('data_preparation_summary.txt', 'w') as f:
    f.write("DATA PREPARATION SUMMARY\n")
    f.write("="*80 + "\n\n")
    for key, value in summary.items():
        f.write(f"{key}: {value}\n")

print(f"   ✓ Summary saved to 'data_preparation_summary.txt'")

print("\n" + "="*80)
print("DATA PREPARATION COMPLETE!")
print("="*80)
print(f"\nCleaned dataset: cleaned_data.csv ({len(data)} rows)")
print(f"Summary report: data_preparation_summary.txt")
print("\nNext steps:")
print("  1. Run Section A analysis: python analysis_sociodemographic.py")
print("  2. Or run full analysis: python run_full_analysis.py")
