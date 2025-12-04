"""
Generate Comprehensive Analysis Report
=======================================
Compiles all analysis results and visualizations into a single HTML report.
"""

import pandas as pd
import os
import datetime
import base64

def get_image_base64(path):
    """Convert image to base64 string"""
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    return ""

def create_html_report():
    print("="*80)
    print("GENERATING COMPREHENSIVE REPORT")
    print("="*80)
    
    # Load results
    print("\n[1/3] Loading analysis results...")
    
    try:
        # Section A
        df_socio = pd.read_excel('results/section_a_sociodemographic.xlsx', sheet_name='Chi-Square Tests')
        
        # Section B
        df_anthro = pd.read_excel('results/section_b_anthropometry.xlsx', sheet_name='T-Tests')
        df_bmi = pd.read_excel('results/section_b_anthropometry.xlsx', sheet_name='BMI Chi-Square Test')
        
        # Section C
        df_diet = pd.read_excel('results/section_c_dietary_patterns.xlsx', sheet_name='Chi-Square Tests')
        df_dds = pd.read_excel('results/section_c_dietary_patterns.xlsx', sheet_name='DDS T-Test')
        
        # Section D
        df_factors = pd.read_excel('results/section_d_diet_factors.xlsx', sheet_name='Chi-Square Tests')
        df_corr = pd.read_excel('results/section_d_diet_factors.xlsx', sheet_name='Correlations')
        
        # Section E
        df_habits = pd.read_excel('results/section_e_dietary_habits.xlsx', sheet_name='Chi-Square Tests')
        
        # Advanced
        df_logistic = pd.read_excel('results/advanced_analysis.xlsx', sheet_name='Logistic Regression')
        df_perf = pd.read_excel('results/advanced_analysis.xlsx', sheet_name='Model Performance')
        df_cluster = pd.read_excel('results/advanced_analysis.xlsx', sheet_name='Cluster Profiles')
        
    except Exception as e:
        print(f"Error loading results: {e}")
        return

    # HTML Template
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Nutritional Status Analysis Report</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 1200px; margin: 0 auto; padding: 20px; }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            h2 {{ color: #2980b9; margin-top: 40px; border-bottom: 1px solid #eee; padding-bottom: 5px; }}
            h3 {{ color: #16a085; margin-top: 25px; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; font-size: 0.9em; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #f2f2f2; color: #333; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            .significant {{ color: #e74c3c; font-weight: bold; }}
            .img-container {{ text-align: center; margin: 30px 0; }}
            img {{ max-width: 100%; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-radius: 5px; }}
            .summary-box {{ background-color: #e8f6f3; padding: 20px; border-radius: 5px; border-left: 5px solid #1abc9c; margin: 20px 0; }}
            .footer {{ margin-top: 50px; text-align: center; color: #7f8c8d; font-size: 0.8em; }}
        </style>
    </head>
    <body>
        <h1>Nutritional Status and Dietary Patterns of Adolescent Girls</h1>
        <p><strong>Comparison of Rural vs Urban Areas in Nigeria</strong></p>
        <p>Date: {datetime.datetime.now().strftime('%Y-%m-%d')}</p>
        
        <div class="summary-box">
            <h3>Executive Summary</h3>
            <p>This report presents the findings from a comparative analysis of {len(pd.read_csv('cleaned_data.csv'))} adolescent girls (Urban vs Rural). 
            The analysis covers socio-demographics, anthropometry, dietary patterns, factors affecting diet, and dietary habits.</p>
        </div>

        <!-- SECTION A -->
        <h2>Section A: Socio-Demographic Characteristics</h2>
        <p>Comparison of socio-demographic variables between rural and urban participants.</p>
        
        <div class="img-container">
            <img src="data:image/png;base64,{get_image_base64('results/section_a_visualizations/residence_distribution.png')}" alt="Residence Distribution" style="width:45%">
            <img src="data:image/png;base64,{get_image_base64('results/section_a_visualizations/age_distribution.png')}" alt="Age Distribution" style="width:45%">
        </div>
        
        <h3>Statistical Comparison (Chi-Square Tests)</h3>
        {df_socio.to_html(index=False, classes='table')}

        <!-- SECTION B -->
        <h2>Section B: Anthropometric Status</h2>
        <p>Analysis of Weight, Height, and BMI.</p>
        
        <div class="img-container">
            <img src="data:image/png;base64,{get_image_base64('results/section_b_visualizations/bmi_categories.png')}" alt="BMI Categories">
        </div>
        
        <h3>BMI Category Comparison</h3>
        {df_bmi.to_html(index=False, classes='table')}
        
        <h3>Anthropometric Measures (T-Tests)</h3>
        {df_anthro.to_html(index=False, classes='table')}

        <!-- SECTION C -->
        <h2>Section C: Dietary Patterns</h2>
        <p>Food frequency analysis and Dietary Diversity Score (DDS).</p>
        
        <div class="img-container">
            <img src="data:image/png;base64,{get_image_base64('results/section_c_visualizations/food_group_consumption.png')}" alt="Food Group Consumption">
        </div>
        
        <h3>Dietary Diversity Score (DDS) Comparison</h3>
        {df_dds.to_html(index=False, classes='table')}
        
        <div class="img-container">
            <img src="data:image/png;base64,{get_image_base64('results/section_c_visualizations/dds_analysis.png')}" alt="DDS Analysis">
        </div>

        <!-- SECTION D -->
        <h2>Section D: Factors Affecting Diet</h2>
        <p>Analysis of factors influencing dietary choices.</p>
        
        <div class="img-container">
            <img src="data:image/png;base64,{get_image_base64('results/section_d_visualizations/correlation_heatmap.png')}" alt="Correlation Heatmap">
        </div>
        
        <h3>Significant Factors (Chi-Square Tests)</h3>
        {df_factors[df_factors['Significance'] != 'ns'].to_html(index=False, classes='table')}

        <!-- SECTION E -->
        <h2>Section E: Dietary Habits</h2>
        <p>Meal skipping, eating out, and snacking habits.</p>
        
        <div class="img-container">
            <img src="data:image/png;base64,{get_image_base64('results/section_e_visualizations/meal_skipping.png')}" alt="Meal Skipping">
            <img src="data:image/png;base64,{get_image_base64('results/section_e_visualizations/snack_preference.png')}" alt="Snack Preference">
        </div>
        
        <h3>Habit Comparisons</h3>
        {df_habits.to_html(index=False, classes='table')}

        <!-- ADVANCED ANALYSIS -->
        <h2>Advanced Analysis</h2>
        
        <h3>1. Logistic Regression: Predicting Undernutrition</h3>
        <p>Model Accuracy: <strong>{df_perf.iloc[0]['Value']}</strong></p>
        
        <div class="img-container">
            <img src="data:image/png;base64,{get_image_base64('results/advanced_analysis_visualizations/logistic_regression_coefficients.png')}" alt="Coefficients">
        </div>
        
        {df_logistic.to_html(index=False, classes='table')}
        
        <h3>2. Cluster Analysis: Dietary Patterns</h3>
        <p>Identified {len(df_cluster)} distinct dietary patterns.</p>
        
        <div class="img-container">
            <img src="data:image/png;base64,{get_image_base64('results/advanced_analysis_visualizations/cluster_profiles.png')}" alt="Cluster Profiles">
        </div>
        
        {df_cluster.to_html(index=False, classes='table')}

        <div class="footer">
            <p>Generated by Antigravity AI | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </body>
    </html>
    """
    
    # Save report
    print("\n[2/3] Saving report...")
    with open('FINAL_ANALYSIS_REPORT.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"   ✓ Report saved to 'FINAL_ANALYSIS_REPORT.html'")
    print("\n" + "="*80)
    print("REPORT GENERATION COMPLETE!")
    print("="*80)

if __name__ == "__main__":
    create_html_report()
