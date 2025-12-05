import pandas as pd
import os

base_dir = r'c:/Users/USER/Desktop/Vivian Project/Vivian_analysis/results'

files = {
    'Section A (Sociodemographic)': 'section_a_sociodemographic.xlsx',
    'Section B (Anthropometry)': 'section_b_anthropometry.xlsx',
    'Section C (Dietary Patterns)': 'section_c_dietary_patterns.xlsx',
    'Advanced Analysis': 'advanced_analysis.xlsx',
    'Section D (Diet Factors)': 'section_d_diet_factors.xlsx',
    'Section E (Dietary Habits)': 'section_e_dietary_habits.xlsx'
}

def print_stats(df, name):
    print(f"\n--- {name} ---")
    for col in df.columns:
        print(f"\nVariable: {col}")
        if df[col].dtype == 'object' or df[col].nunique() < 20:
            counts = df[col].value_counts()
            percents = df[col].value_counts(normalize=True) * 100
            stats = pd.DataFrame({'Count': counts, 'Percent': percents})
            print(stats)
        else:
            print(df[col].describe())

with open('stats_output_utf8.txt', 'w', encoding='utf-8') as f:
    for name, filename in files.items():
        path = os.path.join(base_dir, filename)
        if os.path.exists(path):
            try:
                df = pd.read_excel(path)
                f.write(f"\n--- {name} ---\n")
                f.write(df.to_string() + "\n")
            except Exception as e:
                f.write(f"Error reading {name}: {e}\n")
        else:
            f.write(f"File not found: {path}\n")
