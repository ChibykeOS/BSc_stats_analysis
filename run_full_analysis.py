"""
Master Script: Run Full Nutritional Status Analysis
====================================================
Executes all analysis sections in sequence:
1. Data Preparation
2. Section A: Socio-demographic Analysis
3. Section B: Anthropometric Analysis
4. Section C: Dietary Assessment
5. Section D: Factors Affecting Diet
6. Section E: Dietary Habits
7. BONUS: Advanced Analysis

Author: Vivian BSc Project
Date: December 2025
"""

import os
import sys
import time
from datetime import datetime

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*80)
    print(text.center(80))
    print("="*80 + "\n")

def print_section(text):
    """Print section header"""
    print("\n" + "-"*80)
    print(text)
    print("-"*80)

def run_script(script_name, description):
    """Run a Python script and track time"""
    print_section(f"Running: {description}")
    start_time = time.time()
    
    try:
        # Run the script
        exit_code = os.system(f'python {script_name}')
        
        elapsed_time = time.time() - start_time
        
        if exit_code == 0:
            print(f"\n✓ {description} completed successfully in {elapsed_time:.1f} seconds")
            return True
        else:
            print(f"\n✗ {description} failed with exit code {exit_code}")
            return False
    except Exception as e:
        print(f"\n✗ Error running {description}: {str(e)}")
        return False

def main():
    """Main execution function"""
    print_header("NUTRITIONAL STATUS AND DIETARY PATTERN ANALYSIS")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Working Directory: {os.getcwd()}")
    
    overall_start = time.time()
    results = {}
    
    # List of scripts to run
    scripts = [
        ('data_preparation.py', 'Data Preparation'),
        ('analysis_sociodemographic.py', 'Section A: Socio-demographic Analysis'),
        ('analysis_anthropometry.py', 'Section B: Anthropometric Analysis'),
        ('analysis_dietary_patterns.py', 'Section C: Dietary Assessment (FFQ & DDS)'),
        ('analysis_diet_factors.py', 'Section D: Factors Affecting Diet'),
        ('analysis_dietary_habits.py', 'Section E: Dietary Habits'),
        ('advanced_analysis.py', 'BONUS: Advanced Analysis (Logistic Regression & Clustering)'),
        ('generate_report.py', 'Report Generation')
    ]
    
    # Run each script
    for script_name, description in scripts:
        if os.path.exists(script_name):
            success = run_script(script_name, description)
            results[description] = 'Success' if success else 'Failed'
        else:
            print(f"\n✗ Script not found: {script_name}")
            results[description] = 'Not Found'
    
    # Summary
    overall_time = time.time() - overall_start
    
    print_header("ANALYSIS SUMMARY")
    print(f"Total Execution Time: {overall_time:.1f} seconds ({overall_time/60:.1f} minutes)\n")
    
    print("Results by Section:")
    print("-" * 80)
    for section, status in results.items():
        status_symbol = "✓" if status == "Success" else "✗"
        print(f"{status_symbol} {section}: {status}")
    
    # Check if all succeeded
    all_success = all(status == 'Success' for status in results.values())
    
    if all_success:
        print("\n" + "="*80)
        print("ALL ANALYSES COMPLETED SUCCESSFULLY!".center(80))
        print("="*80)
        print("\nResults Location:")
        print("  - Cleaned Data: cleaned_data.csv")
        print("  - All Results: results/ folder")
        print("    • section_a_sociodemographic.xlsx")
        print("    • section_b_anthropometry.xlsx")
        print("    • section_c_dietary_patterns.xlsx")
        print("    • section_d_diet_factors.xlsx")
        print("    • section_e_dietary_habits.xlsx")
        print("    • advanced_analysis.xlsx")
        print("  - Visualizations: results/section_*_visualizations/")
        print("\nNext Steps:")
        print("  1. Review all Excel files in the results/ folder")
        print("  2. Examine visualizations for your presentation")
        print("  3. Use findings for your BSc project report")
    else:
        print("\n" + "="*80)
        print("SOME ANALYSES FAILED - PLEASE REVIEW ERRORS ABOVE".center(80))
        print("="*80)
    
    print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
