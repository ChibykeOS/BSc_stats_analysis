"""
Section B: Anthropometric Analysis
===================================
Analyzes weight, height, and BMI data.
Uses t-tests for continuous variables and chi-square for BMI categories.
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
print("SECTION B: ANTHROPOMETRIC ANALYSIS")
print("="*80)

# Create results directory
os.makedirs('results/section_b_visualizations', exist_ok=True)

# Load cleaned data
print("\n[1/4] Loading data...")
data = pd.read_csv('cleaned_data.csv')
print(f"   ✓ Loaded {len(data)} participants")

# ============================================================================
# DESCRIPTIVE STATISTICS
# ============================================================================
print("\n[2/4] Calculating descriptive statistics...")

anthropometric_vars = ['Weight (kg)', 'Height (m)', 'BMI_final']
var_labels = {'Weight (kg)': 'Weight (kg)', 'Height (m)': 'Height (m)', 'BMI_final': 'BMI'}

descriptive_results = []

for var in anthropometric_vars:
    if var in data.columns:
        # Overall statistics
        overall_data = data[var].dropna()
        urban_data = data[data['Residence'] == 'urban'][var].dropna()
        rural_data = data[data['Residence'] == 'rural'][var].dropna()
        
        descriptive_results.append({
            'Variable': var_labels.get(var, var),
            'Group': 'Overall',
            'N': len(overall_data),
            'Mean': round(overall_data.mean(), 2),
            'SD': round(overall_data.std(), 2),
            'Min': round(overall_data.min(), 2),
            'Max': round(overall_data.max(), 2),
            'Median': round(overall_data.median(), 2)
        })
        
        descriptive_results.append({
            'Variable': var_labels.get(var, var),
            'Group': 'Urban',
            'N': len(urban_data),
            'Mean': round(urban_data.mean(), 2),
            'SD': round(urban_data.std(), 2),
            'Min': round(urban_data.min(), 2),
            'Max': round(urban_data.max(), 2),
            'Median': round(urban_data.median(), 2)
        })
        
        descriptive_results.append({
            'Variable': var_labels.get(var, var),
            'Group': 'Rural',
            'N': len(rural_data),
            'Mean': round(rural_data.mean(), 2),
            'SD': round(rural_data.std(), 2),
            'Min': round(rural_data.min(), 2),
            'Max': round(rural_data.max(), 2),
            'Median': round(rural_data.median(), 2)
        })

descriptive_df = pd.DataFrame(descriptive_results)
print(f"   ✓ Descriptive statistics calculated")

# ============================================================================
# INDEPENDENT T-TESTS
# ============================================================================
print("\n[3/4] Performing independent t-tests...")

ttest_results = []

for var in anthropometric_vars:
    if var in data.columns:
        urban_data = data[data['Residence'] == 'urban'][var].dropna()
        rural_data = data[data['Residence'] == 'rural'][var].dropna()
        
        # Perform t-test
        t_stat, p_value = stats.ttest_ind(urban_data, rural_data)
        
        # Calculate mean difference and 95% CI
        mean_diff = urban_data.mean() - rural_data.mean()
        se_diff = np.sqrt((urban_data.var()/len(urban_data)) + (rural_data.var()/len(rural_data)))
        ci_lower = mean_diff - 1.96 * se_diff
        ci_upper = mean_diff + 1.96 * se_diff
        
        # Determine significance
        if p_value < 0.001:
            significance = '***'
        elif p_value < 0.01:
            significance = '**'
        elif p_value < 0.05:
            significance = '*'
        else:
            significance = 'ns'
        
        ttest_results.append({
            'Variable': var_labels.get(var, var),
            'Urban Mean': round(urban_data.mean(), 2),
            'Rural Mean': round(rural_data.mean(), 2),
            'Mean Difference': round(mean_diff, 2),
            '95% CI Lower': round(ci_lower, 2),
            '95% CI Upper': round(ci_upper, 2),
            't-statistic': round(t_stat, 3),
            'p-value': round(p_value, 4),
            'Significance': significance,
            'Interpretation': 'Significant difference' if p_value < 0.05 else 'No significant difference'
        })

ttest_df = pd.DataFrame(ttest_results)
print(f"   ✓ T-tests completed")
print(f"      Significant differences: {(ttest_df['Significance'] != 'ns').sum()}")

# BMI Category Analysis
print("\n   Analyzing BMI categories...")

bmi_category_freq = pd.crosstab(data['BMI_category'], data['Residence'], margins=True)
bmi_category_pct = pd.crosstab(data['BMI_category'], data['Residence'], normalize='columns') * 100

# Chi-square test for BMI categories
contingency = pd.crosstab(data['BMI_category'], data['Residence'])
# Remove 'Unknown' category if present
if 'Unknown' in contingency.index:
    contingency = contingency.drop('Unknown')

chi2, p_value, dof, expected = stats.chi2_contingency(contingency)

if p_value < 0.001:
    significance = '***'
elif p_value < 0.01:
    significance = '**'
elif p_value < 0.05:
    significance = '*'
else:
    significance = 'ns'

bmi_chi_square = pd.DataFrame([{
    'Test': 'BMI Category Distribution',
    'Chi-square': round(chi2, 3),
    'df': dof,
    'p-value': round(p_value, 4),
    'Significance': significance,
    'Interpretation': 'Significant difference' if p_value < 0.05 else 'No significant difference'
}])

print(f"      BMI category chi-square: χ²={chi2:.3f}, p={p_value:.4f}")

# ============================================================================
# VISUALIZATIONS
# ============================================================================
print("\n[4/4] Creating visualizations...")

viz_count = 0

# 1. Box plots for anthropometric measures
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for idx, var in enumerate(anthropometric_vars):
    if var in data.columns:
        urban_data = data[data['Residence'] == 'urban'][var].dropna()
        rural_data = data[data['Residence'] == 'rural'][var].dropna()
        
        bp = axes[idx].boxplot([urban_data, rural_data], labels=['Urban', 'Rural'],
                               patch_artist=True, widths=0.6)
        
        # Color the boxes
        colors = ['#3498db', '#e74c3c']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        axes[idx].set_title(var_labels.get(var, var), fontsize=14, weight='bold')
        axes[idx].set_ylabel('Value', fontsize=12)
        axes[idx].grid(True, alpha=0.3)

plt.suptitle('Anthropometric Measures by Residence', fontsize=16, weight='bold', y=1.02)
plt.tight_layout()
plt.savefig('results/section_b_visualizations/anthropometric_boxplots.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 2. BMI distribution histogram
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

urban_bmi = data[data['Residence'] == 'urban']['BMI_final'].dropna()
rural_bmi = data[data['Residence'] == 'rural']['BMI_final'].dropna()

axes[0].hist(urban_bmi, bins=20, color='#3498db', alpha=0.7, edgecolor='black')
axes[0].axvline(urban_bmi.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {urban_bmi.mean():.2f}')
axes[0].set_title('Urban BMI Distribution', fontsize=14, weight='bold')
axes[0].set_xlabel('BMI', fontsize=12)
axes[0].set_ylabel('Frequency', fontsize=12)
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].hist(rural_bmi, bins=20, color='#e74c3c', alpha=0.7, edgecolor='black')
axes[1].axvline(rural_bmi.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {rural_bmi.mean():.2f}')
axes[1].set_title('Rural BMI Distribution', fontsize=14, weight='bold')
axes[1].set_xlabel('BMI', fontsize=12)
axes[1].set_ylabel('Frequency', fontsize=12)
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.suptitle('BMI Distribution by Residence', fontsize=16, weight='bold', y=1.02)
plt.tight_layout()
plt.savefig('results/section_b_visualizations/bmi_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 3. BMI category distribution
fig, ax = plt.subplots(figsize=(12, 6))

# Filter out 'Unknown' and 'All' for visualization
bmi_pct_plot = bmi_category_pct.drop('Unknown', errors='ignore')
bmi_pct_plot.plot(kind='bar', ax=ax, color=['#e74c3c', '#3498db'], width=0.7)

ax.set_title('BMI Category Distribution by Residence', fontsize=16, weight='bold', pad=20)
ax.set_xlabel('BMI Category', fontsize=12, weight='bold')
ax.set_ylabel('Percentage (%)', fontsize=12, weight='bold')
ax.legend(title='Residence', title_fontsize=12, fontsize=11)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('results/section_b_visualizations/bmi_categories.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

print(f"   ✓ Created {viz_count} visualizations")

# ============================================================================
# EXPORT RESULTS
# ============================================================================
with pd.ExcelWriter('results/section_b_anthropometry.xlsx', engine='openpyxl') as writer:
    descriptive_df.to_excel(writer, sheet_name='Descriptive Statistics', index=False)
    ttest_df.to_excel(writer, sheet_name='T-Tests', index=False)
    bmi_category_freq.to_excel(writer, sheet_name='BMI Category Frequency')
    bmi_category_pct.to_excel(writer, sheet_name='BMI Category Percentage')
    bmi_chi_square.to_excel(writer, sheet_name='BMI Chi-Square Test', index=False)

print("\n" + "="*80)
print("SECTION B ANALYSIS COMPLETE!")
print("="*80)
print(f"\nResults saved to:")
print(f"  - results/section_b_anthropometry.xlsx")
print(f"  - results/section_b_visualizations/ ({viz_count} charts)")
print(f"\nKey findings:")
print(f"  - Mean BMI: Urban={urban_bmi.mean():.2f}, Rural={rural_bmi.mean():.2f}")
print(f"  - {(ttest_df['Significance'] != 'ns').sum()} anthropometric measures show significant differences")
