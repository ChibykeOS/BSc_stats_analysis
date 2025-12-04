# Nutritional Status and Dietary Patterns Analysis
**BSc Project: Comparative Analysis of Adolescent Girls in Rural and Urban Nigeria**

## 📌 Project Overview
This project analyzes the nutritional status, dietary patterns, and eating habits of 367 adolescent girls (207 Urban, 160 Rural). It uses statistical methods to identify significant differences and trends between the two populations.

## 📂 Project Structure
```
Vivian_analysis/
├── data_preparation.py         # Cleans raw data, codes frequencies, calculates BMI/DDS
├── analysis_sociodemographic.py # Section A: Demographics analysis
├── analysis_anthropometry.py   # Section B: BMI, Weight, Height analysis
├── analysis_dietary_patterns.py # Section C: Food frequency & DDS analysis
├── analysis_diet_factors.py    # Section D: Factors affecting diet
├── analysis_dietary_habits.py  # Section E: Eating habits analysis
├── advanced_analysis.py        # Logistic Regression & Cluster Analysis
├── generate_report.py          # Generates the HTML report
├── convert_to_pdf.py           # Converts HTML report to PDF
├── run_full_analysis.py        # MASTER SCRIPT: Runs everything
│
├── cleaned_data.csv            # Processed dataset used for analysis
├── chapter_4.md                # Generated Thesis Chapter 4 (Results)
├── chapter_5.md                # Generated Thesis Chapter 5 (Discussion)
│
└── results/                    # All output files
    ├── section_*_visualizations/ # Charts and graphs (PNG)
    ├── *.xlsx                    # Statistical tables (Excel)
    └── advanced_analysis.xlsx    # Advanced stats results
```

## 🚀 How to Run the Analysis
You can reproduce the entire analysis and generate all reports by running the master script:

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Analysis**:
    ```bash
    python run_full_analysis.py
    ```
    *This will execute all analysis scripts in order, generate the visualizations, and create the HTML report.*

3.  **Generate PDF Report** (Optional):
    ```bash
    python convert_to_pdf.py
    ```

## 📊 Outputs
After running the analysis, you will find:
*   **`FINAL_ANALYSIS_REPORT_v2.pdf`**: The complete, printable report with all charts and tables.
*   **`chapter_4.md`**: The text for your thesis Chapter 4 (Results & Discussion).
*   **`chapter_5.md`**: The text for your thesis Chapter 5 (Conclusion & Recommendations).
*   **Excel Files**: Detailed statistical tables in the `results/` folder (useful for appendices).

## 🧪 Key Analyses Performed
*   **Chi-Square Tests**: For categorical comparisons (e.g., Urban vs Rural BMI categories).
*   **Independent T-Tests**: For continuous variables (e.g., Mean BMI, Mean DDS).
*   **Dietary Diversity Score (DDS)**: Calculated based on 10 food groups.
*   **Cluster Analysis**: Identified 3 distinct dietary patterns ("Modern", "Limited", "Average").
*   **Logistic Regression**: Predictors of undernutrition.

## 📝 Authors
*   **Vivian** - BSc Project Researcher
*   **Antigravity AI** - Data Analysis & Technical Implementation
