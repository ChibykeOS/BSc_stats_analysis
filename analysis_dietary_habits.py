"""
Section E: Dietary Habits Analysis
===================================
Analyzes meal patterns, meal skipping, eating out frequency, and snack preferences.
Uses chi-square tests for categorical comparisons.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("="*80)
print("SECTION E: DIETARY HABITS ANALYSIS")
print("="*80)

# Create results directory
os.makedirs('results/section_e_visualizations', exist_ok=True)

# Load cleaned data
print("\n[1/4] Loading data...")
data = pd.read_csv('cleaned_data.csv')

# FAIL-SAFE: Explicitly standardize text columns for this analysis
cols_to_fix = ['Do you skip meals', 'Prefer snacks over food? (Yes/No)']
for col in cols_to_fix:
    if col in data.columns:
        data[col] = data[col].astype(str).str.strip().str.title()
        data[col] = data[col].replace('Nan', np.nan)

print(f"   ✓ Loaded {len(data)} participants")

# ============================================================================
# DIETARY HABITS VARIABLES
# ============================================================================
habits_vars = {
    'Meals per Day': 'Meals per Day',
    'Do you skip meals': 'Meal Skipping',
    'Which meal skipped': 'Meal Skipped',
    'Reason for skipping meals': 'Reason for Skipping',
    'Source of food': 'Food Source',
    'Eating Out Frequency': 'Eating Out Frequency',
    'Prefer snacks over food? (Yes/No)': 'Snack Preference',
    'Reason for snack preference': 'Reason for Snack Preference'
}

# ============================================================================
# DESCRIPTIVE STATISTICS
# ============================================================================
print("\n[2/4] Generating descriptive statistics...")

descriptive_results = []

for var_col, var_label in habits_vars.items():
    if var_col in data.columns:
        # Overall frequency
        freq_overall = data[var_col].value_counts()
        pct_overall = (freq_overall / len(data) * 100).round(1)
        
        # By residence
        freq_urban = data[data['Residence'] == 'urban'][var_col].value_counts()
        pct_urban = (freq_urban / (data['Residence'] == 'urban').sum() * 100).round(1)
        
        freq_rural = data[data['Residence'] == 'rural'][var_col].value_counts()
        pct_rural = (freq_rural / (data['Residence'] == 'rural').sum() * 100).round(1)
        
        # Combine results
        for category in freq_overall.index:
            descriptive_results.append({
                'Variable': var_label,
                'Category': category,
                'Overall_n': freq_overall.get(category, 0),
                'Overall_%': pct_overall.get(category, 0),
                'Urban_n': freq_urban.get(category, 0),
                'Urban_%': pct_urban.get(category, 0),
                'Rural_n': freq_rural.get(category, 0),
                'Rural_%': pct_rural.get(category, 0)
            })

descriptive_df = pd.DataFrame(descriptive_results)
print(f"   ✓ Descriptive statistics calculated for {len(habits_vars)} variables")

# ============================================================================
# CHI-SQUARE TESTS
# ============================================================================
print("\n[3/4] Performing chi-square tests...")

chi_square_results = []

for var_col, var_label in habits_vars.items():
    if var_col in data.columns:
        # Create contingency table
        contingency = pd.crosstab(data[var_col], data['Residence'])
        
        try:
            chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
            
            if p_value < 0.001:
                significance = '***'
            elif p_value < 0.01:
                significance = '**'
            elif p_value < 0.05:
                significance = '*'
            else:
                significance = 'ns'
            
            chi_square_results.append({
                'Variable': var_label,
                'Chi-square': round(chi2, 3),
                'df': dof,
                'p-value': round(p_value, 4),
                'Significance': significance,
                'Interpretation': 'Significant difference' if p_value < 0.05 else 'No significant difference'
            })
        except:
            chi_square_results.append({
                'Variable': var_label,
                'Chi-square': 'N/A',
                'df': 'N/A',
                'p-value': 'N/A',
                'Significance': 'N/A',
                'Interpretation': 'Could not compute'
            })

chi_square_df = pd.DataFrame(chi_square_results)
print(f"   ✓ Chi-square tests completed")
print(f"      Significant differences: {(chi_square_df['Significance'] != 'ns').sum()}")

# ============================================================================
# VISUALIZATIONS
# ============================================================================
print("\n[4/4] Creating visualizations...")

viz_count = 0

# 1. Meals per day
if 'Meals per Day' in data.columns:
    fig, ax = plt.subplots(figsize=(12, 6))
    meals_data = pd.crosstab(data['Meals per Day'], data['Residence'], normalize='columns') * 100
    meals_data.plot(kind='bar', ax=ax, color=['#e74c3c', '#3498db'], width=0.7)
    ax.set_title('Meals per Day by Residence', fontsize=16, weight='bold', pad=20)
    ax.set_xlabel('Number of Meals', fontsize=12, weight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=12, weight='bold')
    ax.legend(title='Residence', title_fontsize=12, fontsize=11)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('results/section_e_visualizations/meals_per_day.png', dpi=300, bbox_inches='tight')
    plt.close()
    viz_count += 1

# 2. Meal skipping
if 'Do you skip meals' in data.columns:
    fig, ax = plt.subplots(figsize=(10, 6))
    skip_data = pd.crosstab(data['Residence'], data['Do you skip meals'], normalize='index') * 100
    skip_data.plot(kind='bar', ax=ax, color=['#2ecc71', '#e74c3c'], width=0.6)
    ax.set_title('Meal Skipping Prevalence by Residence', fontsize=16, weight='bold', pad=20)
    ax.set_xlabel('Residence', fontsize=12, weight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=12, weight='bold')
    ax.legend(title='Skip Meals?', title_fontsize=12, fontsize=11)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('results/section_e_visualizations/meal_skipping.png', dpi=300, bbox_inches='tight')
    plt.close()
    viz_count += 1

# 3. Which meal skipped
if 'Which meal skipped' in data.columns:
    fig, ax = plt.subplots(figsize=(12, 6))
    meal_skipped_data = pd.crosstab(data['Which meal skipped'], data['Residence'], normalize='columns') * 100
    meal_skipped_data.plot(kind='bar', ax=ax, color=['#e74c3c', '#3498db'], width=0.7)
    ax.set_title('Type of Meal Skipped by Residence', fontsize=16, weight='bold', pad=20)
    ax.set_xlabel('Meal Type', fontsize=12, weight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=12, weight='bold')
    ax.legend(title='Residence', title_fontsize=12, fontsize=11)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('results/section_e_visualizations/meal_type_skipped.png', dpi=300, bbox_inches='tight')
    plt.close()
    viz_count += 1

# 4. Eating out frequency
if 'Eating Out Frequency' in data.columns:
    fig, ax = plt.subplots(figsize=(12, 6))
    eating_out_data = pd.crosstab(data['Eating Out Frequency'], data['Residence'], normalize='columns') * 100
    eating_out_data.plot(kind='bar', ax=ax, color=['#e74c3c', '#3498db'], width=0.7)
    ax.set_title('Eating Out Frequency by Residence', fontsize=16, weight='bold', pad=20)
    ax.set_xlabel('Frequency', fontsize=12, weight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=12, weight='bold')
    ax.legend(title='Residence', title_fontsize=12, fontsize=11)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('results/section_e_visualizations/eating_out_frequency.png', dpi=300, bbox_inches='tight')
    plt.close()
    viz_count += 1

# 5. Snack preference
if 'Prefer snacks over food? (Yes/No)' in data.columns:
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Bar chart
    snack_pref_data = pd.crosstab(data['Residence'], data['Prefer snacks over food? (Yes/No)'], normalize='index') * 100
    snack_pref_data.plot(kind='bar', ax=axes[0], color=['#e74c3c', '#2ecc71'], width=0.6)
    axes[0].set_title('Snack Preference by Residence', fontsize=14, weight='bold')
    axes[0].set_xlabel('Residence', fontsize=12, weight='bold')
    axes[0].set_ylabel('Percentage (%)', fontsize=12, weight='bold')
    axes[0].legend(title='Prefer Snacks?', title_fontsize=11, fontsize=10)
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=0)
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # Pie chart for overall
    overall_snack = data['Prefer snacks over food? (Yes/No)'].value_counts()
    axes[1].pie(overall_snack, labels=overall_snack.index, autopct='%1.1f%%',
                colors=['#2ecc71', '#e74c3c'], startangle=90, textprops={'fontsize': 12, 'weight': 'bold'})
    axes[1].set_title('Overall Snack Preference', fontsize=14, weight='bold')
    
    plt.suptitle('Snack Preference Analysis', fontsize=16, weight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('results/section_e_visualizations/snack_preference.png', dpi=300, bbox_inches='tight')
    plt.close()
    viz_count += 1

# 6. Reason for skipping meals
if 'Reason for skipping meals' in data.columns:
    fig, ax = plt.subplots(figsize=(14, 6))
    reason_data = pd.crosstab(data['Reason for skipping meals'], data['Residence'], normalize='columns') * 100
    reason_data.plot(kind='bar', ax=ax, color=['#e74c3c', '#3498db'], width=0.7)
    ax.set_title('Reasons for Meal Skipping by Residence', fontsize=16, weight='bold', pad=20)
    ax.set_xlabel('Reason', fontsize=12, weight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=12, weight='bold')
    ax.legend(title='Residence', title_fontsize=12, fontsize=11)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('results/section_e_visualizations/reasons_for_skipping.png', dpi=300, bbox_inches='tight')
    plt.close()
    viz_count += 1

print(f"   ✓ Created {viz_count} visualizations")

# ============================================================================
# EXPORT RESULTS
# ============================================================================
with pd.ExcelWriter('results/section_e_dietary_habits.xlsx', engine='openpyxl') as writer:
    descriptive_df.to_excel(writer, sheet_name='Descriptive Statistics', index=False)
    chi_square_df.to_excel(writer, sheet_name='Chi-Square Tests', index=False)

print("\n" + "="*80)
print("SECTION E ANALYSIS COMPLETE!")
print("="*80)
print(f"\nResults saved to:")
print(f"  - results/section_e_dietary_habits.xlsx")
print(f"  - results/section_e_visualizations/ ({viz_count} charts)")
print(f"\nKey findings:")
print(f"  - {len(habits_vars)} dietary habit variables analyzed")
print(f"  - {(chi_square_df['Significance'] != 'ns').sum()} variables show significant differences")
