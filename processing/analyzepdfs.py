import os
from PyPDF2 import PdfReader, PdfWriter
import pandas as pd


def update_pdf_fields(csv_path, pdf_folder):
    """
    Updates PDF form fields based on values from a CSV file.

    Parameters:
    csv_path (str): Path to the CSV file containing filename and date values
    pdf_folder (str): Path to the folder containing PDF files
    """
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Track results
    results = []

    for index, row in df.iterrows():
        filename = row["filename"]
        new_date = row["ADA2_CAL_DATE"]  # Assumes column name is 'intended_date'
        print(f"processing {filename}")

        pdf_path = os.path.join(pdf_folder, filename)
        if not os.path.exists(pdf_path):
            results.append(
                {"filename": filename, "status": "File not found", "success": False}
            )
            continue

        try:
            # Create output filename
            output_path = os.path.join(pdf_folder, f"updated_{filename}")

            # Read the PDF
            reader = PdfReader(pdf_path)
            writer = PdfWriter()

            # Copy all pages to writer
            for page in reader.pages:
                writer.add_page(page)

            # Get form fields
            if reader.get_form_text_fields() is not None:
                writer.update_page_form_field_values(
                    writer.pages[0],  # Assumes field is on first page
                    {"ADA2_CAL_DATE": str(new_date)},
                )

                # Save the modified PDF
                with open(output_path, "wb") as output_file:
                    writer.write(output_file)

                results.append(
                    {
                        "filename": filename,
                        "status": "Successfully updated",
                        "success": True,
                    }
                )
            else:
                results.append(
                    {
                        "filename": filename,
                        "status": "No form fields found",
                        "success": False,
                    }
                )

        except Exception as e:
            results.append(
                {"filename": filename, "status": f"Error: {str(e)}", "success": False}
            )

    # Create results DataFrame
    results_df = pd.DataFrame(results)
    return results_df


if __name__ == "__main__":
    # Replace these paths with your actual paths
    csv_path = r"C:\Users\ianm\Desktop\3J\ADA_Outputs\processing2\added_comments\checked\reduced\pdf_analysis_results.csv"
    pdf_folder = r"O:\City of North Plains\City Projects\Misc\ADA Study\GIS\Outputs"

    # Update PDFs and get results
    results_df = update_pdf_fields(csv_path, pdf_folder)

    # Display results
    print("\nUpdate Results:")
    print(f"Total files processed: {len(results_df)}")
    print(f"Successfully updated: {len(results_df[results_df['success'] == True])}")
    print(f"Failed updates: {len(results_df[results_df['success'] == False])}")
    print("\nDetailed Results:")
    print(results_df)

    # Save results to CSV
    results_df.to_csv(
        r"C:\Users\ianm\Desktop\3J\ADA_Outputs\processing2\added_comments\checked\reduced\pdf_update_results.csv",
        index=False,
    )


def remove_updated_prefix(folder_path):
    """
    Removes 'updated_' prefix from all files in the specified folder.
    Returns list of processed files.
    """
    processed_files = []

    # Get list of files with 'updated_' prefix
    files_to_rename = [f for f in os.listdir(folder_path) if f.startswith("updated_")]

    if not files_to_rename:
        print("No files with 'updated_' prefix found!")
        return processed_files

    # Show files that will be renamed
    print(f"Found {len(files_to_rename)} files to rename:")
    for file in files_to_rename:
        print(f"  {file} -> {file[8:]}")

    # Ask for confirmation
    confirm = input("\nProceed with renaming? (yes/no): ").lower()
    if confirm != "yes":
        print("Operation cancelled.")
        return processed_files

    # Perform renaming
    for old_name in files_to_rename:
        try:
            old_path = os.path.join(folder_path, old_name)
            new_name = old_name[8:]  # Remove 'updated_' prefix
            new_path = os.path.join(folder_path, new_name)

            # Check if destination file exists
            if os.path.exists(new_path):
                print(f"Warning: {new_name} already exists, skipping...")
                continue

            os.rename(old_path, new_path)
            processed_files.append((old_name, new_name))
            print(f"Renamed: {old_name} -> {new_name}")

        except Exception as e:
            print(f"Error renaming {old_name}: {str(e)}")

    return processed_files


if __name__ == "__main__":
    folder_path = r"O:\City of North Plains\City Projects\Misc\ADA Study\GIS\Outputs\9999"  # Replace with your folder path

    print("PDF Prefix Removal Tool")
    print("-" * 20)

    processed = remove_updated_prefix(folder_path)

    if processed:
        print(f"\nSuccessfully renamed {len(processed)} files.")
    else:
        print("\nNo files were renamed.")
