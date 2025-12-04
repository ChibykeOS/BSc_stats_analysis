"""
BONUS: Advanced Analysis - Logistic Regression & Cluster Analysis
==================================================================
1. Logistic Regression: Predicts undernutrition based on various factors
2. Cluster Analysis: Identifies dietary pattern groups
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, silhouette_score
import os
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

print("="*80)
print("BONUS: ADVANCED ANALYSIS")
print("="*80)

# Create results directory
os.makedirs('results/advanced_analysis_visualizations', exist_ok=True)

# Load cleaned data
print("\n[1/3] Loading data...")
data = pd.read_csv('cleaned_data.csv')
print(f"   ✓ Loaded {len(data)} participants")

# ============================================================================
# PART 1: LOGISTIC REGRESSION FOR UNDERNUTRITION
# ============================================================================
print("\n" + "="*80)
print("PART 1: LOGISTIC REGRESSION - PREDICTING UNDERNUTRITION")
print("="*80)

print("\n[1/4] Preparing data for logistic regression...")

# Create binary outcome: Undernutrition (Yes/No)
data['Undernutrition'] = (data['BMI_category'] == 'Underweight').astype(int)

print(f"   ✓ Undernutrition prevalence: {data['Undernutrition'].sum()} ({data['Undernutrition'].mean()*100:.1f}%)")

# Prepare predictors
# Code categorical variables
data['Residence_coded'] = (data['Residence'] == 'urban').astype(int)
data['Meal_skipping_coded'] = (data['Do you skip meals'] == 'Yes').astype(int) if 'Do you skip meals' in data.columns else 0

# Income coding (if available)
income_mapping = {
    'Below ₦30,000': 1,
    '₦30,000 - ₦50,000': 2,
    '₦50,000 - ₦100,000': 3,
    'Above ₦100,000': 4
}

if 'Family Monthly Income' in data.columns:
    data['Income_coded'] = data['Family Monthly Income'].map(income_mapping)
else:
    data['Income_coded'] = np.nan

# Select predictors
predictor_cols = ['Residence_coded', 'DDS', 'Meal_skipping_coded', 'Income_coded']
available_predictors = [col for col in predictor_cols if col in data.columns and data[col].notna().sum() > 0]

# Create dataset for regression (remove missing values)
regression_data = data[available_predictors + ['Undernutrition']].dropna()

print(f"   ✓ Regression dataset: {len(regression_data)} observations")
print(f"   ✓ Predictors: {', '.join(available_predictors)}")

# Fit logistic regression
X = regression_data[available_predictors]
y = regression_data['Undernutrition']

log_reg = LogisticRegression(random_state=42, max_iter=1000)
log_reg.fit(X, y)

# Get predictions
y_pred = log_reg.predict(X)
y_pred_proba = log_reg.predict_proba(X)[:, 1]

print("\n[2/4] Logistic regression results...")

# Coefficients and odds ratios
coefficients = pd.DataFrame({
    'Predictor': available_predictors,
    'Coefficient': log_reg.coef_[0],
    'Odds Ratio': np.exp(log_reg.coef_[0]),
    'Log Odds': log_reg.coef_[0]
})
coefficients = coefficients.round(3)

print("\n   Coefficients and Odds Ratios:")
print(coefficients.to_string(index=False))

# Model performance
print("\n[3/4] Model performance...")
print("\n   Classification Report:")
print(classification_report(y, y_pred, target_names=['Normal/Overweight', 'Underweight']))

# Confusion matrix
cm = confusion_matrix(y, y_pred)
print("\n   Confusion Matrix:")
print(f"   True Negatives: {cm[0,0]}, False Positives: {cm[0,1]}")
print(f"   False Negatives: {cm[1,0]}, True Positives: {cm[1,1]}")

# Visualizations
print("\n[4/4] Creating visualizations...")

# Coefficients plot
fig, ax = plt.subplots(figsize=(10, 6))
coefficients_sorted = coefficients.sort_values('Coefficient')
colors = ['#e74c3c' if x < 0 else '#2ecc71' for x in coefficients_sorted['Coefficient']]
ax.barh(coefficients_sorted['Predictor'], coefficients_sorted['Coefficient'], color=colors, alpha=0.7)
ax.axvline(x=0, color='black', linestyle='--', linewidth=1)
ax.set_xlabel('Coefficient', fontsize=12, weight='bold')
ax.set_title('Logistic Regression Coefficients for Undernutrition', fontsize=14, weight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('results/advanced_analysis_visualizations/logistic_regression_coefficients.png', dpi=300, bbox_inches='tight')
plt.close()

# Confusion matrix heatmap
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax,
            xticklabels=['Normal/Overweight', 'Underweight'],
            yticklabels=['Normal/Overweight', 'Underweight'])
ax.set_xlabel('Predicted', fontsize=12, weight='bold')
ax.set_ylabel('Actual', fontsize=12, weight='bold')
ax.set_title('Confusion Matrix - Undernutrition Prediction', fontsize=14, weight='bold', pad=20)
plt.tight_layout()
plt.savefig('results/advanced_analysis_visualizations/confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# PART 2: CLUSTER ANALYSIS FOR DIETARY PATTERNS
# ============================================================================
print("\n" + "="*80)
print("PART 2: CLUSTER ANALYSIS - DIETARY PATTERN IDENTIFICATION")
print("="*80)

print("\n[1/4] Preparing data for cluster analysis...")

# Use food group consumption scores for clustering
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
    'Snacks': ['Biscuits ', 'Chin-chin', 'Buns', 'Doughnut', 'Peanut', 'Plantain', 
               'Chocolate', 'Eggrolls', 'Snack_Other']
}

# Calculate mean consumption score for each food group
cluster_features = []
for group_name, items in food_groups.items():
    coded_cols = [f"{item}_coded" for item in items if f"{item}_coded" in data.columns]
    if coded_cols:
        data[f'{group_name}_score'] = data[coded_cols].mean(axis=1)
        cluster_features.append(f'{group_name}_score')

# Prepare clustering dataset
cluster_data = data[cluster_features].dropna()
print(f"   ✓ Clustering dataset: {len(cluster_data)} observations")
print(f"   ✓ Features: {len(cluster_features)} food groups")

# Standardize features
scaler = StandardScaler()
cluster_data_scaled = scaler.fit_transform(cluster_data)

print("\n[2/4] Determining optimal number of clusters...")

# Elbow method
inertias = []
silhouette_scores = []
K_range = range(2, 7)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(cluster_data_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(cluster_data_scaled, kmeans.labels_))

# Plot elbow curve
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
axes[0].set_xlabel('Number of Clusters', fontsize=12, weight='bold')
axes[0].set_ylabel('Inertia', fontsize=12, weight='bold')
axes[0].set_title('Elbow Method', fontsize=14, weight='bold')
axes[0].grid(True, alpha=0.3)

axes[1].plot(K_range, silhouette_scores, 'ro-', linewidth=2, markersize=8)
axes[1].set_xlabel('Number of Clusters', fontsize=12, weight='bold')
axes[1].set_ylabel('Silhouette Score', fontsize=12, weight='bold')
axes[1].set_title('Silhouette Score', fontsize=14, weight='bold')
axes[1].grid(True, alpha=0.3)

plt.suptitle('Optimal Number of Clusters', fontsize=16, weight='bold', y=1.02)
plt.tight_layout()
plt.savefig('results/advanced_analysis_visualizations/optimal_clusters.png', dpi=300, bbox_inches='tight')
plt.close()

# Use 3 clusters (typical for dietary patterns)
optimal_k = 3
print(f"   ✓ Using {optimal_k} clusters")

print("\n[3/4] Performing K-means clustering...")

kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(cluster_data_scaled)

# Add cluster labels to data
data_with_clusters = data.loc[cluster_data.index].copy()
data_with_clusters['Cluster'] = cluster_labels

# Analyze cluster characteristics
print("\n[4/4] Analyzing cluster characteristics...")

cluster_profiles = []
for cluster in range(optimal_k):
    cluster_subset = data_with_clusters[data_with_clusters['Cluster'] == cluster]
    
    profile = {
        'Cluster': f'Cluster {cluster + 1}',
        'N': len(cluster_subset),
        'Percentage': f"{len(cluster_subset)/len(data_with_clusters)*100:.1f}%"
    }
    
    # Add mean scores for each food group
    for feature in cluster_features:
        profile[feature.replace('_score', '')] = round(cluster_subset[feature].mean(), 2)
    
    # Add residence distribution
    profile['Urban_%'] = f"{(cluster_subset['Residence'] == 'urban').sum() / len(cluster_subset) * 100:.1f}%"
    profile['Rural_%'] = f"{(cluster_subset['Residence'] == 'rural').sum() / len(cluster_subset) * 100:.1f}%"
    
    cluster_profiles.append(profile)

cluster_profile_df = pd.DataFrame(cluster_profiles)

print("\n   Cluster Profiles:")
print(cluster_profile_df.to_string(index=False))

# Visualize cluster profiles
fig, ax = plt.subplots(figsize=(14, 8))

# Prepare data for radar chart
categories = [f.replace('_score', '') for f in cluster_features]
N = len(categories)

# Create radar chart
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

ax = plt.subplot(111, projection='polar')

for cluster in range(optimal_k):
    cluster_subset = data_with_clusters[data_with_clusters['Cluster'] == cluster]
    values = [cluster_subset[f].mean() for f in cluster_features]
    values += values[:1]
    
    ax.plot(angles, values, 'o-', linewidth=2, label=f'Cluster {cluster + 1}')
    ax.fill(angles, values, alpha=0.15)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, size=10)
ax.set_ylim(0, 6)
ax.set_title('Dietary Pattern Clusters', size=16, weight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
ax.grid(True)

plt.tight_layout()
plt.savefig('results/advanced_analysis_visualizations/cluster_profiles.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# EXPORT RESULTS
# ============================================================================
with pd.ExcelWriter('results/advanced_analysis.xlsx', engine='openpyxl') as writer:
    coefficients.to_excel(writer, sheet_name='Logistic Regression', index=False)
    
    # Add model performance metrics
    performance_df = pd.DataFrame([{
        'Metric': 'Accuracy',
        'Value': f"{(y == y_pred).mean():.3f}"
    }])
    performance_df.to_excel(writer, sheet_name='Model Performance', index=False)
    
    cluster_profile_df.to_excel(writer, sheet_name='Cluster Profiles', index=False)

print("\n" + "="*80)
print("ADVANCED ANALYSIS COMPLETE!")
print("="*80)
print(f"\nResults saved to:")
print(f"  - results/advanced_analysis.xlsx")
print(f"  - results/advanced_analysis_visualizations/")
print(f"\nKey findings:")
print(f"  - Logistic regression model accuracy: {(y == y_pred).mean():.1%}")
print(f"  - {optimal_k} dietary pattern clusters identified")
cluster_sizes = [str(len(data_with_clusters[data_with_clusters['Cluster'] == i])) for i in range(optimal_k)]
print(f"  - Cluster sizes: {', '.join(cluster_sizes)}")
