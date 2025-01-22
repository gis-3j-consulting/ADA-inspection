import os
import pandas as pd
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName

########## Create extra data columns for use in dashboards
df = pd.read_csv(r"C:\python\scripts\pdfeditor2\processing\combined_output.csv")

df["fail_count"] = df.apply(lambda row: (row == "fail").sum(), axis=1)

df["intersection_name"] = df.apply(
    lambda row: f"{row['ns_road']} & {row['ew_road']}", axis=1
)

df["file_link"] = df.apply(
    lambda row: f"O:\\City of North Plains\\City Projects\\Misc\\ADA Study\\GIS\\Outputs\\{row['fileName']}.pdf",
    axis=1,
)

df["failing_test"] = "none"

for index, row in df.iterrows():
    failing_tests = []
    for col in df.columns:
        if row[col] == "fail":
            failing_tests.append(col)

    if failing_tests:
        df.at[index, "failing_test"] = ", ".join(failing_tests)

df["failing_test"] = df["failing_test"].apply(
    lambda x: x.replace("none, ", "") if x.startswith("none, ") else x
)

print(df)

df.to_csv(
    r"C:\python\scripts\pdfeditor2\processing\combined_processed_output2.csv",
    index=False,
)

#### Replacing default fail field values with expanded lookup table values

import pandas as pd
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

df = pd.read_csv(
    r"C:\python\scripts\pdfeditor2\processing\combined_processed_output2.csv"
)
lookup_values = pd.read_excel(
    r"O:\City of North Plains\City Projects\Misc\ADA Study\GIS\Tables\csvTextOutput1.xlsx"
)

lookup_values["csvField"] = lookup_values["csvField"].str.strip()


def process_shorthand(shorthand):
    shorthand_clean = shorthand.strip()
    if shorthand_clean.endswith("_pf"):
        shorthand_clean = shorthand_clean[:-3]
        logging.debug(f"Removed '_pf' from shorthand: {shorthand} -> {shorthand_clean}")
    return shorthand_clean


for index, row in df.iterrows():
    failing_tests = row["failing_test"]
    logging.info(f"Working on index {index}: {failing_tests}")

    if pd.notna(failing_tests):
        tests_list = failing_tests.split(",")
        expanded_tests = []

        for shorthand in tests_list:
            shorthand_clean = process_shorthand(shorthand)
            logging.debug(f"Processing shorthand: {shorthand_clean}")

            match = lookup_values[
                lookup_values["csvField"].str.lower() == shorthand_clean.lower()
            ]

            if not match.empty:
                expanded_version = match["Text Output"].values[0]
                logging.debug(
                    f"Found expanded version: {expanded_version} for {shorthand_clean}"
                )
                expanded_tests.append(expanded_version)
            else:
                logging.warning(
                    f"Shorthand not found in lookup table: {shorthand_clean}"
                )
                expanded_tests.append(shorthand_clean)

        df.at[index, "failing_test"] = ", ".join(expanded_tests)

output_path = r"C:\python\scripts\pdfeditor2\processing\updated_output.csv"
df.to_csv(output_path, index=False)
logging.info(f"Updated CSV saved to {output_path}")


############ For double checking and fixing comment fields. Some pdfs don't work due to corruption, so need to exclude them.
def update_comments_in_pdf(input_pdf_path, comments, output_folder):
    input_pdf = PdfReader(input_pdf_path)

    for page in input_pdf.pages:
        annotations = page.get("/Annots")
        if annotations:
            for annotation in annotations:
                field = annotation.get("/T")
                if field and (field == "(ADA2_COMNT)" or field == "(ADA_COMNT)"):
                    annotation.update(PdfDict(V=comments, AP=PdfDict()))
                    print(f"\nComments field updated with: \n{comments}")
                    break

    output_path = os.path.join(output_folder, os.path.basename(input_pdf_path))
    PdfWriter().write(output_path, input_pdf)
    print(f"Saved updated PDF to {output_path}")


def loop_folder_comments(input_folder, csv_path, output_path):
    file_list = os.listdir(input_folder)
    df = pd.read_csv(csv_path, dtype=str)

    for file in file_list:
        if file.endswith(".pdf") and file not in ["170.pdf", "171.pdf", "354.pdf"]:
            print(f"Processing {file}")
            file_name = os.path.splitext(file)[0]
            row = df[df["fileName"] == file_name]

            if not row.empty:
                should_value = str(row["comments"].values[0])
                first_line = should_value.split("\n")[0]

                update_comments_in_pdf(
                    os.path.join(input_folder, file), first_line, output_path
                )
                print(f"{file} updated with comment {first_line}")


input_folder = r"C:\Users\ianm\Desktop\3J\ADA_Outputs\processing2"
output_path = r"C:\Users\ianm\Desktop\3J\ADA_Outputs\processing2\added_comments"
csv_path = r"C:\python\scripts\pdfeditor2\processing\combined_processed_output.csv"

loop_folder_comments(input_folder, csv_path, output_path)

######## Function to double check the checkbox fields in the PDF forms


def check_checkbox(input_number, field_name):
    input_pdf = rf"C:\Users\ianm\Desktop\3J\ADA_Outputs\processing2\added_comments\{input_number}.pdf"
    output_pdf = rf"C:\Users\ianm\Desktop\3J\ADA_Outputs\processing2\added_comments\checked\{input_number}.pdf"

    pdf = PdfReader(input_pdf)
    for page in pdf.pages:
        annotations = page.Annots
        if annotations:
            for annotation in annotations:
                if annotation.get("/T") == f"({field_name})":  # Find the checkbox field
                    annotation.update(
                        PdfDict(
                            AS=PdfName("Yes"),
                            V=PdfName("Yes"),
                        )  # Mark it as checked
                    )
    PdfWriter(output_pdf, trailer=pdf).write()

    print(f"Saved {output_pdf}")


turn_space_array = [
    436,
    437,
    438,
    439,
    440,
    441,
    442,
    443,
    444,
    445,
    446,
    447,
    448,
    449,
    451,
    452,
    453,
]

landing_array = []

pdf_folder = r"C:\Users\ianm\Desktop\3J\ADA_Outputs\processing2\added_comments"

for pdf in os.listdir(pdf_folder):
    pdf_name = os.path.splitext(pdf)[0]
    try:
        pdf_number = int(pdf_name)  # Convert to integer
    except ValueError:
        print(f"Skipping {pdf_name}, not a number.")
        continue

    print(f"Checking {pdf_name}")
    if pdf_number in turn_space_array:
        check_checkbox(pdf_number, "TURN_SPACE_PRSNT")
    elif pdf_number in landing_array:
        check_checkbox(pdf_number, "LANDING_PRSNT")
    else:
        pass

#### Following reduction (should be last step due to interfering with script editing) remove suffix

folder_path = (
    r"C:\Users\ianm\Desktop\3J\ADA_Outputs\processing2\added_comments\checked\reduced"
)

for filename in os.listdir(folder_path):
    new_filename = filename.replace("_red", "")
    old_file = os.path.join(folder_path, filename)
    new_file = os.path.join(folder_path, new_filename)
    os.rename(old_file, new_file)

    print(f"{old_file} renamed to {new_file}")

print("Files have been renamed successfully!")
