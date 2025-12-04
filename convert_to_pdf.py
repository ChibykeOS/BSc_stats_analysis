from xhtml2pdf import pisa
import os

def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return True on success and False on errors
    return pisa_status.err

# Read the HTML file
with open('FINAL_ANALYSIS_REPORT.html', 'r', encoding='utf-8') as f:
    source_html = f.read()

# Define output filename
output_filename = "FINAL_ANALYSIS_REPORT_v2.pdf"

# Convert
print(f"Converting 'FINAL_ANALYSIS_REPORT.html' to '{output_filename}'...")
if convert_html_to_pdf(source_html, output_filename) == 0:
    print(f"Successfully created {output_filename}")
else:
    print("Error creating PDF")
