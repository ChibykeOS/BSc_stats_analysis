"""
Section D: Factors Affecting Dietary Habits
============================================
Analyzes factors influencing dietary choices using Likert scale responses.
Uses chi-square tests and optional Spearman correlations.
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
plt.rcParams['figure.figsize'] = (14, 8)

print("="*80)
print("SECTION D: FACTORS AFFECTING DIETARY HABITS")
print("="*80)

# Create results directory
os.makedirs('results/section_d_visualizations', exist_ok=True)

# Load cleaned data
print("\n[1/4] Loading data...")
data = pd.read_csv('cleaned_data.csv')
print(f"   ✓ Loaded {len(data)} participants")

# ============================================================================
# FACTORS DEFINITION
# ============================================================================
factors = {
    'Food availability': 'Food Availability',
    'Individual preferences': 'Individual Preferences',
    'Culture/Tradition': 'Culture/Tradition',
    'Socio-economic status': 'Socio-economic Status',
    'Nutritional knowledge': 'Nutritional Knowledge',
    'Geographical location (SA/A/D/SD)': 'Geographical Location',
    'Peer influence': 'Peer Influence',
    'Cost of food': 'Cost of Food',
    'Health status': 'Health Status',
    'Educational level of parents': 'Parental Education',
    'Season': 'Seasonality'
}

# ============================================================================
# DESCRIPTIVE STATISTICS
# ============================================================================
print("\n[2/4] Generating descriptive statistics...")

descriptive_results = []

for factor_col, factor_label in factors.items():
    if factor_col in data.columns:
        # Overall frequency
        freq_overall = data[factor_col].value_counts()
        pct_overall = (freq_overall / len(data) * 100).round(1)
        
        # By residence
        freq_urban = data[data['Residence'] == 'urban'][factor_col].value_counts()
        pct_urban = (freq_urban / (data['Residence'] == 'urban').sum() * 100).round(1)
        
        freq_rural = data[data['Residence'] == 'rural'][factor_col].value_counts()
        pct_rural = (freq_rural / (data['Residence'] == 'rural').sum() * 100).round(1)
        
        # Combine results
        for category in freq_overall.index:
            descriptive_results.append({
                'Factor': factor_label,
                'Response': category,
                'Overall_n': freq_overall.get(category, 0),
                'Overall_%': pct_overall.get(category, 0),
                'Urban_n': freq_urban.get(category, 0),
                'Urban_%': pct_urban.get(category, 0),
                'Rural_n': freq_rural.get(category, 0),
                'Rural_%': pct_rural.get(category, 0)
            })

descriptive_df = pd.DataFrame(descriptive_results)
print(f"   ✓ Descriptive statistics calculated for {len(factors)} factors")

# ============================================================================
# CHI-SQUARE TESTS
# ============================================================================
print("\n[3/4] Performing chi-square tests...")

chi_square_results = []

for factor_col, factor_label in factors.items():
    if factor_col in data.columns:
        # Create contingency table
        contingency = pd.crosstab(data[factor_col], data['Residence'])
        
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
                'Factor': factor_label,
                'Chi-square': round(chi2, 3),
                'df': dof,
                'p-value': round(p_value, 4),
                'Significance': significance,
                'Interpretation': 'Significant difference' if p_value < 0.05 else 'No significant difference'
            })
        except:
            chi_square_results.append({
                'Factor': factor_label,
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
# OPTIONAL: SPEARMAN CORRELATIONS
# ============================================================================
print("\n   Computing Spearman correlations with DDS and BMI...")

# Code Likert responses numerically
likert_mapping = {
    'Strongly Agree': 4,
    'Agree': 3,
    'Disagree': 2,
    'Strongly Disagree': 1,
    'SA': 4,
    'A': 3,
    'D': 2,
    'SD': 1
}

correlation_results = []

for factor_col, factor_label in factors.items():
    if factor_col in data.columns:
        # Code the factor
        factor_coded = data[factor_col].map(likert_mapping)
        
        if factor_coded.notna().sum() > 0:
            # Correlation with DDS
            if 'DDS' in data.columns:
                corr_dds, p_dds = stats.spearmanr(factor_coded.dropna(), 
                                                   data.loc[factor_coded.notna(), 'DDS'])
            else:
                corr_dds, p_dds = np.nan, np.nan
            
            # Correlation with BMI
            if 'BMI_final' in data.columns:
                valid_idx = factor_coded.notna() & data['BMI_final'].notna()
                if valid_idx.sum() > 0:
                    corr_bmi, p_bmi = stats.spearmanr(factor_coded[valid_idx], 
                                                      data.loc[valid_idx, 'BMI_final'])
                else:
                    corr_bmi, p_bmi = np.nan, np.nan
            else:
                corr_bmi, p_bmi = np.nan, np.nan
            
            correlation_results.append({
                'Factor': factor_label,
                'Correlation_with_DDS': round(corr_dds, 3) if not np.isnan(corr_dds) else 'N/A',
                'p-value_DDS': round(p_dds, 4) if not np.isnan(p_dds) else 'N/A',
                'Correlation_with_BMI': round(corr_bmi, 3) if not np.isnan(corr_bmi) else 'N/A',
                'p-value_BMI': round(p_bmi, 4) if not np.isnan(p_bmi) else 'N/A'
            })

correlation_df = pd.DataFrame(correlation_results)
print(f"      Correlations calculated for {len(correlation_results)} factors")

# ============================================================================
# VISUALIZATIONS
# ============================================================================
print("\n[4/4] Creating visualizations...")

viz_count = 0

# Create stacked bar charts for key factors
key_factors = ['Food availability', 'Nutritional knowledge', 'Peer influence', 
               'Cost of food', 'Socio-economic status']

for factor_col in key_factors:
    if factor_col in data.columns:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create percentage crosstab
        ct = pd.crosstab(data['Residence'], data[factor_col], normalize='index') * 100
        
        ct.plot(kind='bar', stacked=True, ax=ax, colormap='RdYlGn', width=0.6)
        
        factor_label = factors.get(factor_col, factor_col)
        ax.set_title(f'{factor_label} by Residence', fontsize=16, weight='bold', pad=20)
        ax.set_xlabel('Residence', fontsize=12, weight='bold')
        ax.set_ylabel('Percentage (%)', fontsize=12, weight='bold')
        ax.legend(title='Response', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        filename = factor_label.lower().replace(' ', '_').replace('/', '_')
        plt.savefig(f'results/section_d_visualizations/{filename}.png', dpi=300, bbox_inches='tight')
        plt.close()
        viz_count += 1

# Correlation heatmap
if len(correlation_df) > 0:
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Prepare data for heatmap
    corr_data = correlation_df.copy()
    corr_data['DDS_corr'] = pd.to_numeric(corr_data['Correlation_with_DDS'], errors='coerce')
    corr_data['BMI_corr'] = pd.to_numeric(corr_data['Correlation_with_BMI'], errors='coerce')
    
    heatmap_data = corr_data[['Factor', 'DDS_corr', 'BMI_corr']].set_index('Factor')
    heatmap_data.columns = ['DDS', 'BMI']
    
    sns.heatmap(heatmap_data, annot=True, fmt='.3f', cmap='coolwarm', center=0,
                vmin=-1, vmax=1, cbar_kws={'label': 'Spearman Correlation'},
                linewidths=0.5, ax=ax)
    ax.set_title('Correlation of Factors with DDS and BMI', fontsize=16, weight='bold', pad=20)
    ax.set_ylabel('')
    
    plt.tight_layout()
    plt.savefig('results/section_d_visualizations/correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    viz_count += 1

print(f"   ✓ Created {viz_count} visualizations")

# ============================================================================
# EXPORT RESULTS
# ============================================================================
with pd.ExcelWriter('results/section_d_diet_factors.xlsx', engine='openpyxl') as writer:
    descriptive_df.to_excel(writer, sheet_name='Descriptive Statistics', index=False)
    chi_square_df.to_excel(writer, sheet_name='Chi-Square Tests', index=False)
    correlation_df.to_excel(writer, sheet_name='Correlations', index=False)

print("\n" + "="*80)
print("SECTION D ANALYSIS COMPLETE!")
print("="*80)
print(f"\nResults saved to:")
print(f"  - results/section_d_diet_factors.xlsx")
print(f"  - results/section_d_visualizations/ ({viz_count} charts)")
print(f"\nKey findings:")
print(f"  - {len(factors)} factors analyzed")
print(f"  - {(chi_square_df['Significance'] != 'ns').sum()} factors show significant differences")
