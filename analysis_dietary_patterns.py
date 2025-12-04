"""
Section C: Dietary Assessment (Food Frequency Questionnaire)
=============================================================
Analyzes food consumption patterns and Dietary Diversity Score (DDS).
Uses chi-square tests for frequency comparisons and t-test for DDS.
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
print("SECTION C: DIETARY ASSESSMENT (FOOD FREQUENCY QUESTIONNAIRE)")
print("="*80)

# Create results directory
os.makedirs('results/section_c_visualizations', exist_ok=True)

# Load cleaned data
print("\n[1/5] Loading data...")
data = pd.read_csv('cleaned_data.csv')
print(f"   ✓ Loaded {len(data)} participants")

# ============================================================================
# FOOD GROUPS DEFINITION
# ============================================================================
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

frequency_labels = {1: 'Never', 2: 'Occasionally', 3: '1x/week', 4: '2-3x/week', 5: '4-6x/week', 6: 'Daily'}

# ============================================================================
# DESCRIPTIVE STATISTICS - FOOD GROUP CONSUMPTION
# ============================================================================
print("\n[2/5] Analyzing food group consumption patterns...")

group_consumption_results = []

for group_name, items in food_groups.items():
    # Calculate average consumption score for the group
    coded_cols = [f"{item}_coded" for item in items if f"{item}_coded" in data.columns]
    
    if coded_cols:
        # Overall
        overall_mean = data[coded_cols].mean().mean()
        
        # By residence
        urban_mean = data[data['Residence'] == 'urban'][coded_cols].mean().mean()
        rural_mean = data[data['Residence'] == 'rural'][coded_cols].mean().mean()
        
        group_consumption_results.append({
            'Food Group': group_name,
            'Overall Mean Score': round(overall_mean, 2),
            'Urban Mean Score': round(urban_mean, 2),
            'Rural Mean Score': round(rural_mean, 2),
            'Difference': round(urban_mean - rural_mean, 2)
        })

group_consumption_df = pd.DataFrame(group_consumption_results)
print(f"   ✓ Food group consumption patterns calculated")

# ============================================================================
# CHI-SQUARE TESTS FOR INDIVIDUAL FOOD ITEMS
# ============================================================================
print("\n[3/5] Performing chi-square tests for food items...")

chi_square_results = []

# Test selected important food items from each group
important_items = ['Rice', 'Beans', 'Yam', 'Fish', 'Chicken', 'Egg', 'Tomatoes', 
                   'Ugu', 'Orange', 'Banana', 'Milk ', 'Soft drinks', 'Water']

for item in important_items:
    coded_col = f"{item}_coded"
    if coded_col in data.columns:
        # Create contingency table
        contingency = pd.crosstab(data[coded_col], data['Residence'])
        
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
                'Food Item': item.strip(),
                'Chi-square': round(chi2, 3),
                'df': dof,
                'p-value': round(p_value, 4),
                'Significance': significance,
                'Interpretation': 'Significant difference' if p_value < 0.05 else 'No significant difference'
            })
        except:
            pass

chi_square_df = pd.DataFrame(chi_square_results)
print(f"   ✓ Chi-square tests completed for {len(chi_square_results)} food items")
print(f"      Significant differences: {(chi_square_df['Significance'] != 'ns').sum()}")

# ============================================================================
# DIETARY DIVERSITY SCORE (DDS) ANALYSIS
# ============================================================================
print("\n[4/5] Analyzing Dietary Diversity Score (DDS)...")

urban_dds = data[data['Residence'] == 'urban']['DDS'].dropna()
rural_dds = data[data['Residence'] == 'rural']['DDS'].dropna()

# Descriptive statistics
dds_descriptive = pd.DataFrame([
    {
        'Group': 'Overall',
        'N': len(data['DDS'].dropna()),
        'Mean': round(data['DDS'].mean(), 2),
        'SD': round(data['DDS'].std(), 2),
        'Min': int(data['DDS'].min()),
        'Max': int(data['DDS'].max()),
        'Median': round(data['DDS'].median(), 1)
    },
    {
        'Group': 'Urban',
        'N': len(urban_dds),
        'Mean': round(urban_dds.mean(), 2),
        'SD': round(urban_dds.std(), 2),
        'Min': int(urban_dds.min()),
        'Max': int(urban_dds.max()),
        'Median': round(urban_dds.median(), 1)
    },
    {
        'Group': 'Rural',
        'N': len(rural_dds),
        'Mean': round(rural_dds.mean(), 2),
        'SD': round(rural_dds.std(), 2),
        'Min': int(rural_dds.min()),
        'Max': int(rural_dds.max()),
        'Median': round(rural_dds.median(), 1)
    }
])

# T-test for DDS
t_stat, p_value = stats.ttest_ind(urban_dds, rural_dds)

mean_diff = urban_dds.mean() - rural_dds.mean()
se_diff = np.sqrt((urban_dds.var()/len(urban_dds)) + (rural_dds.var()/len(rural_dds)))
ci_lower = mean_diff - 1.96 * se_diff
ci_upper = mean_diff + 1.96 * se_diff

if p_value < 0.001:
    significance = '***'
elif p_value < 0.01:
    significance = '**'
elif p_value < 0.05:
    significance = '*'
else:
    significance = 'ns'

dds_ttest = pd.DataFrame([{
    'Comparison': 'Urban vs Rural DDS',
    'Urban Mean': round(urban_dds.mean(), 2),
    'Rural Mean': round(rural_dds.mean(), 2),
    'Mean Difference': round(mean_diff, 2),
    '95% CI Lower': round(ci_lower, 2),
    '95% CI Upper': round(ci_upper, 2),
    't-statistic': round(t_stat, 3),
    'p-value': round(p_value, 4),
    'Significance': significance,
    'Interpretation': 'Significant difference' if p_value < 0.05 else 'No significant difference'
}])

print(f"   ✓ DDS analysis completed")
print(f"      Urban DDS: {urban_dds.mean():.2f} ± {urban_dds.std():.2f}")
print(f"      Rural DDS: {rural_dds.mean():.2f} ± {rural_dds.std():.2f}")
print(f"      p-value: {p_value:.4f}")

# ============================================================================
# VISUALIZATIONS
# ============================================================================
print("\n[5/5] Creating visualizations...")

viz_count = 0

# 1. Food group consumption comparison
fig, ax = plt.subplots(figsize=(14, 8))
x = np.arange(len(group_consumption_df))
width = 0.35

urban_scores = group_consumption_df['Urban Mean Score']
rural_scores = group_consumption_df['Rural Mean Score']

bars1 = ax.bar(x - width/2, urban_scores, width, label='Urban', color='#3498db', alpha=0.8)
bars2 = ax.bar(x + width/2, rural_scores, width, label='Rural', color='#e74c3c', alpha=0.8)

ax.set_xlabel('Food Group', fontsize=12, weight='bold')
ax.set_ylabel('Mean Consumption Score', fontsize=12, weight='bold')
ax.set_title('Food Group Consumption Patterns by Residence', fontsize=16, weight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(group_consumption_df['Food Group'], rotation=45, ha='right')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('results/section_c_visualizations/food_group_consumption.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 2. DDS distribution
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Box plot
bp = axes[0].boxplot([urban_dds, rural_dds], labels=['Urban', 'Rural'],
                      patch_artist=True, widths=0.6)
colors = ['#3498db', '#e74c3c']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

axes[0].set_title('Dietary Diversity Score by Residence', fontsize=14, weight='bold')
axes[0].set_ylabel('DDS (0-10)', fontsize=12)
axes[0].grid(True, alpha=0.3)

# Histogram
axes[1].hist(urban_dds, bins=11, range=(0, 11), color='#3498db', alpha=0.6, label='Urban', edgecolor='black')
axes[1].hist(rural_dds, bins=11, range=(0, 11), color='#e74c3c', alpha=0.6, label='Rural', edgecolor='black')
axes[1].set_title('DDS Distribution', fontsize=14, weight='bold')
axes[1].set_xlabel('Dietary Diversity Score', fontsize=12)
axes[1].set_ylabel('Frequency', fontsize=12)
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.suptitle('Dietary Diversity Score Analysis', fontsize=16, weight='bold', y=1.02)
plt.tight_layout()
plt.savefig('results/section_c_visualizations/dds_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

# 3. Heatmap of food group consumption
fig, ax = plt.subplots(figsize=(10, 8))

heatmap_data = group_consumption_df[['Food Group', 'Urban Mean Score', 'Rural Mean Score']].set_index('Food Group').T

sns.heatmap(heatmap_data, annot=True, fmt='.2f', cmap='YlOrRd', cbar_kws={'label': 'Mean Score'},
            linewidths=0.5, ax=ax)
ax.set_title('Food Group Consumption Heatmap', fontsize=16, weight='bold', pad=20)
ax.set_xlabel('')
ax.set_ylabel('Residence', fontsize=12, weight='bold')

plt.tight_layout()
plt.savefig('results/section_c_visualizations/consumption_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
viz_count += 1

print(f"   ✓ Created {viz_count} visualizations")

# ============================================================================
# EXPORT RESULTS
# ============================================================================
with pd.ExcelWriter('results/section_c_dietary_patterns.xlsx', engine='openpyxl') as writer:
    group_consumption_df.to_excel(writer, sheet_name='Food Group Consumption', index=False)
    chi_square_df.to_excel(writer, sheet_name='Chi-Square Tests', index=False)
    dds_descriptive.to_excel(writer, sheet_name='DDS Descriptive', index=False)
    dds_ttest.to_excel(writer, sheet_name='DDS T-Test', index=False)

print("\n" + "="*80)
print("SECTION C ANALYSIS COMPLETE!")
print("="*80)
print(f"\nResults saved to:")
print(f"  - results/section_c_dietary_patterns.xlsx")
print(f"  - results/section_c_visualizations/ ({viz_count} charts)")
print(f"\nKey findings:")
print(f"  - {len(food_groups)} food groups analyzed")
print(f"  - {(chi_square_df['Significance'] != 'ns').sum()} food items show significant differences")
print(f"  - DDS difference: {mean_diff:.2f} (p={p_value:.4f})")
