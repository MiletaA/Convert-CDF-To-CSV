import os
import pandas as pd
from spacepy import pycdf

def process_cdf_file(cdf_file_path, output_csv_path):
    try:
        print(f"Processing file: {cdf_file_path}")
        # Open the CDF file
        with pycdf.CDF(cdf_file_path) as cdf:
            # Extract 'epoch' and 'electric_field' data
            epoch_data = cdf['epoch'][:]
            electric_field_data = cdf['electric_field'][:]

            # Create a DataFrame with 'epoch' as index and 'electric_field' as columns
            df = pd.DataFrame(electric_field_data, index=epoch_data)

            # Rename columns
            columns = [str(freq) + ' Hz' for freq in cdf['frequency'][:]]
            df.columns = columns

            # Export the DataFrame to a CSV file
            df.to_csv(output_csv_path)
        print(f"Saved CSV to: {output_csv_path}")
    except Exception as e:
        print(f"Failed to process {cdf_file_path}: {e}")

def process_directory(parent_dir, output_csv_dir):
    cdf_count = 0
    csv_count = 0
    
    # Walk through all directories and subdirectories
    for root, _, files in os.walk(parent_dir):
        for file in files:
            if file.endswith('.cdf'):
                cdf_count += 1
                # Construct full file path
                cdf_file_path = os.path.join(root, file)
                
                # Create the corresponding directory structure in the output directory
                relative_path = os.path.relpath(root, parent_dir)
                output_dir_path = os.path.join(output_csv_dir, relative_path)
                os.makedirs(output_dir_path, exist_ok=True)
                
                # Define the output CSV file path
                output_csv_path = os.path.join(output_dir_path, os.path.splitext(file)[0] + '.csv')
                
                # Process the CDF file and save to CSV
                process_cdf_file(cdf_file_path, output_csv_path)
                if os.path.exists(output_csv_path):
                    csv_count += 1

    print(f"Total CDF files found: {cdf_count}")
    print(f"Total CSV files created: {csv_count}")

if __name__ == "__main__":
    # Specify the parent directory containing CDF files
    parent_directory = ''
    
    # Specify the output directory for CSV files
    output_csv_directory = ''
    
    print(f"Processing directory: {parent_directory}")
    print(f"Output will be saved to: {output_csv_directory}")
    
    # Process all CDF files in the parent directory
    process_directory(parent_directory, output_csv_directory)
    
    print("Processing complete.")
