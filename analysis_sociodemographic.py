"""
Section A: Socio-Demographic Analysis
======================================
Compares socio-demographic characteristics between rural and urban adolescent girls.
Uses chi-square tests for categorical variables.
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
print("SECTION A: SOCIO-DEMOGRAPHIC ANALYSIS")
print("="*80)

# Create results directory
os.makedirs('results/section_a_visualizations', exist_ok=True)

# Load cleaned data
print("\n[1/4] Loading data...")
data = pd.read_csv('cleaned_data.csv')
print(f"   ✓ Loaded {len(data)} participants")

# ============================================================================
# SOCIO-DEMOGRAPHIC VARIABLES
# ============================================================================
sociodem_vars = {
    'Age Group ': 'Age Group',
    'Living With': 'Living Arrangement',
    'Family Size': 'Family Size',
    'Education Level of Guardian': 'Guardian Education',
    'Father Occupation': 'Father Occupation',
    'Mother Occupation': 'Mother Occupation',
    'Marital Status of Parents': 'Parental Marital Status',
    'Family Monthly Income': 'Monthly Income',
    'Religion': 'Religion',
    'Ethnic Group': 'Ethnicity'
}

# ============================================================================
# DESCRIPTIVE STATISTICS
# ============================================================================
print("\n[2/4] Generating descriptive statistics...")

results_list = []

for var, label in sociodem_vars.items():
    if var in data.columns:
        # Overall frequency
        freq_overall = data[var].value_counts()
        pct_overall = (freq_overall / len(data) * 100).round(1)
        
        # By residence
        freq_urban = data[data['Residence'] == 'urban'][var].value_counts()
        pct_urban = (freq_urban / (data['Residence'] == 'urban').sum() * 100).round(1)
        
        freq_rural = data[data['Residence'] == 'rural'][var].value_counts()
        pct_rural = (freq_rural / (data['Residence'] == 'rural').sum() * 100).round(1)
        
        # Combine into dataframe
        for category in freq_overall.index:
            results_list.append({
                'Variable': label,
                'Category': category,
                'Overall_n': freq_overall.get(category, 0),
                'Overall_%': pct_overall.get(category, 0),
                'Urban_n': freq_urban.get(category, 0),
                'Urban_%': pct_urban.get(category, 0),
                'Rural_n': freq_rural.get(category, 0),
                'Rural_%': pct_rural.get(category, 0)
            })

descriptive_df = pd.DataFrame(results_list)
print(f"   ✓ Descriptive statistics calculated for {len(sociodem_vars)} variables")

# ============================================================================
# CHI-SQUARE TESTS
# ============================================================================
print("\n[3/4] Performing chi-square tests...")

chi_square_results = []

for var, label in sociodem_vars.items():
    if var in data.columns:
        # Create contingency table
        contingency = pd.crosstab(data[var], data['Residence'])
        
        # Perform chi-square test
        try:
            chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
            
            # Determine significance
            if p_value < 0.001:
                significance = '***'
            elif p_value < 0.01:
                significance = '**'
            elif p_value < 0.05:
                significance = '*'
            else:
                significance = 'ns'
            
            chi_square_results.append({
                'Variable': label,
                'Chi-square': round(chi2, 3),
                'df': dof,
                'p-value': round(p_value, 4),
                'Significance': significance,
                'Interpretation': 'Significant difference' if p_value < 0.05 else 'No significant difference'
            })
        except:
            chi_square_results.append({
                'Variable': label,
                'Chi-square': 'N/A',
                'df': 'N/A',
                'p-value': 'N/A',
                'Significance': 'N/A',
                'Interpretation': 'Could not compute'
            })

chi_square_df = pd.DataFrame(chi_square_results)
print(f"   ✓ Chi-square tests completed")
print(f"      Significant differences found: {(chi_square_df['Significance'] != 'ns').sum()}")

# ============================================================================
# VISUALIZATIONS
# ============================================================================
print("\n[4/4] Creating visualizations...")

viz_count = 0

# 1. Residence distribution (Pie chart)
plt.figure(figsize=(8, 8))
residence_counts = data['Residence'].value_counts()
colors = ['#3498db', '#e74c3c']
plt.pie(residence_counts, labels=residence_counts.index, autopct='%1.1f%%', 
        colors=colors, startangle=90, textprops={'fontsize': 14, 'weight': 'bold'})
plt.title('Distribution of Participants by Residence', fontsize=16, weight='bold', pad=20)
plt.savefig('results/section_a_visualizations/residence_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 2. Age group distribution
if 'Age Group ' in data.columns:
    fig, ax = plt.subplots(figsize=(12, 6))
    age_data = pd.crosstab(data['Age Group '], data['Residence'], normalize='columns') * 100
    age_data.plot(kind='bar', ax=ax, color=['#e74c3c', '#3498db'], width=0.7)
    ax.set_title('Age Group Distribution by Residence', fontsize=16, weight='bold', pad=20)
    ax.set_xlabel('Age Group', fontsize=12, weight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=12, weight='bold')
    ax.legend(title='Residence', title_fontsize=12, fontsize=11)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('results/section_a_visualizations/age_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    viz_count += 1

# 3. Education level of guardian
if 'Education Level of Guardian' in data.columns:
    fig, ax = plt.subplots(figsize=(14, 6))
    edu_data = pd.crosstab(data['Education Level of Guardian'], data['Residence'], normalize='columns') * 100
    edu_data.plot(kind='bar', ax=ax, color=['#e74c3c', '#3498db'], width=0.7)
    ax.set_title('Guardian Education Level by Residence', fontsize=16, weight='bold', pad=20)
    ax.set_xlabel('Education Level', fontsize=12, weight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=12, weight='bold')
    ax.legend(title='Residence', title_fontsize=12, fontsize=11)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('results/section_a_visualizations/guardian_education.png', dpi=300, bbox_inches='tight')
    plt.close()
    viz_count += 1

# 4. Family income
if 'Family Monthly Income' in data.columns:
    fig, ax = plt.subplots(figsize=(12, 6))
    income_data = pd.crosstab(data['Family Monthly Income'], data['Residence'], normalize='columns') * 100
    income_data.plot(kind='bar', ax=ax, color=['#e74c3c', '#3498db'], width=0.7)
    ax.set_title('Family Monthly Income by Residence', fontsize=16, weight='bold', pad=20)
    ax.set_xlabel('Income Level', fontsize=12, weight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=12, weight='bold')
    ax.legend(title='Residence', title_fontsize=12, fontsize=11)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('results/section_a_visualizations/family_income.png', dpi=300, bbox_inches='tight')
    plt.close()
    viz_count += 1

# 5. Religion
if 'Religion' in data.columns:
    fig, ax = plt.subplots(figsize=(10, 6))
    religion_data = pd.crosstab(data['Religion'], data['Residence'], normalize='columns') * 100
    religion_data.plot(kind='bar', ax=ax, color=['#e74c3c', '#3498db'], width=0.7)
    ax.set_title('Religion Distribution by Residence', fontsize=16, weight='bold', pad=20)
    ax.set_xlabel('Religion', fontsize=12, weight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=12, weight='bold')
    ax.legend(title='Residence', title_fontsize=12, fontsize=11)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('results/section_a_visualizations/religion.png', dpi=300, bbox_inches='tight')
    plt.close()
    viz_count += 1

print(f"   ✓ Created {viz_count} visualizations")

# ============================================================================
# EXPORT RESULTS
# ============================================================================
with pd.ExcelWriter('results/section_a_sociodemographic.xlsx', engine='openpyxl') as writer:
    descriptive_df.to_excel(writer, sheet_name='Descriptive Statistics', index=False)
    chi_square_df.to_excel(writer, sheet_name='Chi-Square Tests', index=False)

print("\n" + "="*80)
print("SECTION A ANALYSIS COMPLETE!")
print("="*80)
print(f"\nResults saved to:")
print(f"  - results/section_a_sociodemographic.xlsx")
print(f"  - results/section_a_visualizations/ ({viz_count} charts)")
print(f"\nKey findings:")
print(f"  - {len(sociodem_vars)} socio-demographic variables analyzed")
print(f"  - {(chi_square_df['Significance'] != 'ns').sum()} variables show significant differences")
