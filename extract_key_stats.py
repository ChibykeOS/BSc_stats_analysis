import pandas as pd
import os

def print_section(title):
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")

def get_p_col(df):
    # Normalize columns: strip whitespace
    df.columns = df.columns.str.strip()
    
    # Find P-value column (case insensitive)
    for col in df.columns:
        if col.lower() in ['p-value', 'p_value', 'p value', 'sig', 'significance (p)']:
            return col
    return None

try:
    # Section A: Demographics
    print_section("SECTION A: DEMOGRAPHICS")
    df_a = pd.read_excel('results/section_a_sociodemographic.xlsx', sheet_name='Chi-Square Tests')
    p_col = get_p_col(df_a)
    print(f"P-value column detected: {p_col}")
    
    if p_col:
        sig_a = df_a[df_a['Significance'] != 'ns']
        if not sig_a.empty:
            print(sig_a[['Variable', p_col, 'Significance']].to_string(index=False))
        else:
            print("No significant differences found.")
    else:
        print("Could not find P-value column in Section A")

    # Section B: Anthropometry
    print_section("SECTION B: ANTHROPOMETRY")
    df_b_ttest = pd.read_excel('results/section_b_anthropometry.xlsx', sheet_name='T-Tests')
    p_col_b = get_p_col(df_b_ttest)
    print("T-Tests (BMI, Weight, Height):")
    if p_col_b:
        print(df_b_ttest[['Variable', 'Rural Mean', 'Urban Mean', p_col_b, 'Significance']].to_string(index=False))
    
    df_b_chi = pd.read_excel('results/section_b_anthropometry.xlsx', sheet_name='BMI Chi-Square Test')
    print("\nBMI Categories:")
    print(df_b_chi.to_string(index=False))

    # Section C: Dietary Patterns
    print_section("SECTION C: DIETARY PATTERNS")
    df_c_dds = pd.read_excel('results/section_c_dietary_patterns.xlsx', sheet_name='DDS T-Test')
    print("Dietary Diversity Score (DDS):")
    print(df_c_dds.to_string(index=False))
    
    df_c_chi = pd.read_excel('results/section_c_dietary_patterns.xlsx', sheet_name='Chi-Square Tests')
    print("\nTop 5 Significant Food Differences:")
    p_col_c = get_p_col(df_c_chi)
    if p_col_c:
        sig_c = df_c_chi[df_c_chi['Significance'] != 'ns'].sort_values(p_col_c).head(5)
        print(sig_c[['Food Item', p_col_c, 'Significance']].to_string(index=False))

    # Section D: Factors
    print_section("SECTION D: FACTORS AFFECTING DIET")
    df_d = pd.read_excel('results/section_d_diet_factors.xlsx', sheet_name='Chi-Square Tests')
    print("Significant Factors:")
    p_col_d = get_p_col(df_d)
    if p_col_d:
        sig_d = df_d[df_d['Significance'] != 'ns']
        print(sig_d[['Factor', p_col_d, 'Significance']].to_string(index=False))
    
    df_d_corr = pd.read_excel('results/section_d_diet_factors.xlsx', sheet_name='Correlations')
    print("\nTop Correlations with BMI/DDS:")
    print(df_d_corr.head(5).to_string(index=False))

    # Section E: Habits
    print_section("SECTION E: DIETARY HABITS")
    df_e = pd.read_excel('results/section_e_dietary_habits.xlsx', sheet_name='Chi-Square Tests')
    print("Significant Habits:")
    p_col_e = get_p_col(df_e)
    if p_col_e:
        sig_e = df_e[df_e['Significance'] != 'ns']
        print(sig_e[['Variable', p_col_e, 'Significance']].to_string(index=False))

    # Advanced
    print_section("ADVANCED ANALYSIS")
    df_adv_perf = pd.read_excel('results/advanced_analysis.xlsx', sheet_name='Model Performance')
    print(f"Logistic Regression Accuracy: {df_adv_perf.iloc[0]['Value']}")
    
    df_adv_cluster = pd.read_excel('results/advanced_analysis.xlsx', sheet_name='Cluster Profiles')
    print(f"Columns in Cluster Profiles: {df_adv_cluster.columns.tolist()}")
    print(f"\nClusters Identified: {len(df_adv_cluster)}")
    # Print all columns to be safe
    print(df_adv_cluster.to_string(index=False))

except Exception as e:
    print(f"Error extracting stats: {e}")
    import traceback
    traceback.print_exc()
