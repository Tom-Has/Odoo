import os
import base64
import pandas as pd
from pathlib import Path

def pdf_to_base64(pdf_path):
    """Convert PDF file to base64 string"""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            return base64.b64encode(pdf_file.read()).decode('utf-8')
    except Exception as e:
        return f"Error: {str(e)}"

def find_pdfs_and_convert(root_folder):
    """Find all PDFs recursively and convert to base64"""
    data = []
    
    # Walk through directory tree
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                # Get relative path to maintain folder structure info
                relative_path = os.path.relpath(pdf_path, root_folder)
                
                print(f"Processing: {relative_path}")
                base64_string = pdf_to_base64(pdf_path)
                
                data.append({
                    'File Path': relative_path,
                    'Base64': base64_string
                })
    
    return data

def write_to_excel(data, output_file):
    """Write the data to an Excel file"""
    try:
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Write to Excel
        df.to_excel(output_file, index=False)
        print(f"Excel file created successfully at: {output_file}")
    except Exception as e:
        print(f"Error writing to Excel: {str(e)}")

#def main():
# Set your root folder path here
root_folder = "path/to/file"  # Replace with your folder path
output_file = "pdf_base64_output.xlsx"

# Find PDFs and convert to base64
pdf_data = find_pdfs_and_convert(root_folder)

if pdf_data:
    # Write to Excel
    write_to_excel(pdf_data, output_file)
else:
    print("No PDF files found in the specified folder structure.")

#if __name__ == "__main__":
#   main()