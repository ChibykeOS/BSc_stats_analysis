import pandas as pd
import numpy as np

def clean_print(title, df, f):
    print(f"\n### {title}", file=f)
    print(df.to_string(index=False), file=f)

try:
    with open('chapter4_data_final.txt', 'w', encoding='utf-8') as f:
        # Section A
        df_a = pd.read_excel('results/section_a_sociodemographic.xlsx', sheet_name='Chi-Square Tests')
        df_a.columns = df_a.columns.str.strip()
        p_col = next((c for c in df_a.columns if c.lower().startswith('p-val')), 'P-value')
        sig_a = df_a[df_a['Significance'] != 'ns']
        clean_print("Significant Demographics", sig_a[['Variable', p_col, 'Significance']], f)

        # Section B
        df_b = pd.read_excel('results/section_b_anthropometry.xlsx', sheet_name='T-Tests')
        df_b.columns = df_b.columns.str.strip()
        p_col_b = next((c for c in df_b.columns if c.lower().startswith('p-val')), 'P-value')
        clean_print("Anthropometry T-Tests", df_b[['Variable', 'Rural Mean', 'Urban Mean', p_col_b, 'Significance']], f)

        df_b_chi = pd.read_excel('results/section_b_anthropometry.xlsx', sheet_name='BMI Chi-Square Test')
        clean_print("BMI Categories", df_b_chi, f)

        # Section C
        df_c = pd.read_excel('results/section_c_dietary_patterns.xlsx', sheet_name='DDS T-Test')
        clean_print("DDS T-Test", df_c, f)

        # Section D
        df_d = pd.read_excel('results/section_d_diet_factors.xlsx', sheet_name='Chi-Square Tests')
        df_d.columns = df_d.columns.str.strip()
        p_col_d = next((c for c in df_d.columns if c.lower().startswith('p-val')), 'P-value')
        sig_d = df_d[df_d['Significance'] != 'ns']
        clean_print("Significant Diet Factors", sig_d[['Factor', p_col_d, 'Significance']], f)

        # Section E
        df_e = pd.read_excel('results/section_e_dietary_habits.xlsx', sheet_name='Chi-Square Tests')
        df_e.columns = df_e.columns.str.strip()
        p_col_e = next((c for c in df_e.columns if c.lower().startswith('p-val')), 'P-value')
        sig_e = df_e[df_e['Significance'] != 'ns']
        clean_print("Significant Habits", sig_e[['Variable', p_col_e, 'Significance']], f)

        # Advanced
        df_adv = pd.read_excel('results/advanced_analysis.xlsx', sheet_name='Cluster Profiles')
        clean_print("Cluster Profiles", df_adv, f)

except Exception as e:
    print(f"Error: {e}")

