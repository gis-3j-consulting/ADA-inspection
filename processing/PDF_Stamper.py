import os
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from pdfrw import PdfReader, PdfWriter
import logging
import fitz


logging.basicConfig(
    filename="pdf_processing_pymupdf.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def fill_pdf_text(record, output_filename, template_pdf, fields, output_dir):
    try:
        output_filepath = os.path.join(output_dir, output_filename)

        pdf_document = fitz.open(template_pdf)
        page = pdf_document[0]

        for field, details in fields.items():
            value = record.get(field, "")
            coordinates_in_inches = details["coordinates"]

            x_pt = coordinates_in_inches[0] * 72
            y_pt = (11 - coordinates_in_inches[1]) * 72

            text_point = fitz.Point(x_pt, y_pt)

            page.insert_text(text_point, str(value), fontsize=12, rotate=90)

        # Save the updated PDF
        pdf_document.save(output_filepath)
        pdf_document.close()

        logging.info(f"Successfully processed {output_filename}.")

    except Exception as e:
        logging.error(f"Failed to process {output_filename}. Error: {str(e)}")
        print(f"Error processing {output_filename}: {str(e)}")
        return False

    return True


# Need to flip x/y
parallel_field_coordinates = {
    "crnr_pstn": {
        "coordinates": (1.38, 7.82),
    },
    "ramp_position": {
        "coordinates": (3.22, 7.82),
    },
    "ntrsctn_cntrl": {
        "coordinates": (7.65, 5.5),
    },
    "nspctn_dt": {"coordinates": (1.07, 5.42)},
}
perpendicular_field_coordinates = {
    "crnr_pstn": {
        "coordinates": (1.5, 7.88),
    },
    "ramp_position": {
        "coordinates": (3.22, 7.88),
    },
    "ntrsctn_cntrl": {
        "coordinates": (7.75, 5.3),
    },
    "nspctn_dt": {"coordinates": (1.14, 5.21)},
}
combination_field_coordinates = {
    "crnr_pstn": {
        "coordinates": (1.25, 7.82),
    },
    "ramp_position": {
        "coordinates": (2.93, 7.82),
    },
    "ntrsctn_cntrl": {
        "coordinates": (8.02, 5.38),
    },
    "nspctn_dt": {"coordinates": (0.96, 5.26)},
}
blended_field_coordinates = {
    "crnr_pstn": {
        "coordinates": (1.58, 7.82),
    },
    "ramp_position": {
        "coordinates": (3.29, 7.82),
    },
    "ntrsctn_cntrl": {
        "coordinates": (7.82, 5.35),
    },
    "nspctn_dt": {"coordinates": (1.07, 5.42)},
}
end_field_coordinates = {
    "crnr_pstn": {
        "coordinates": (1.56, 7.82),
    },
    "ramp_position": {
        "coordinates": (3.25, 7.82),
    },
    "ntrsctn_cntrl": {
        "coordinates": (100, 100),
    },
    "nspctn_dt": {"coordinates": (1.19, 5.26)},
}
cut_field_coordinates = {
    "crnr_pstn": {
        "coordinates": (1.35, 7.82),
    },
    "ramp_position": {
        "coordinates": (2.93, 7.82),
    },
    "ntrsctn_cntrl": {
        "coordinates": (7.08, 5.8),
    },
    "nspctn_dt": {"coordinates": (1.07, 5.42)},
}

input_pdf_dir = r"O:\City of North Plains\City Projects\Misc\ADA Study\GIS\Outputs\unflattened\flattened_fieldsCleared"
output_dir = r"O:\City of North Plains\City Projects\Misc\ADA Study\GIS\Outputs"

data_file = r"O:\City of North Plains\City Projects\Misc\ADA Study\GIS\Tables\combined_processed_output.csv"
df = pd.read_csv(data_file)

for index, row in df.iterrows():
    file_name = str(row["fileName"])
    ramp_type = str(row["type"])

    record = {
        "crnr_pstn": row.get("crnr_pstn", ""),
        "ramp_position": row.get("ramp_position", ""),
        "ntrsctn_cntrl": row.get("ntrsctn_cntrl", ""),
        "nspctn_dt": row.get("nspctn_dt", ""),
    }

    input_pdf_path = os.path.join(input_pdf_dir, f"{file_name}.pdf")
    output_filename = f"{file_name}.pdf"

    if os.path.exists(input_pdf_path):
        if ramp_type == "parallel":
            with open(input_pdf_path, "rb") as input_file:
                fill_pdf_text(
                    record,
                    output_filename,
                    input_file,
                    parallel_field_coordinates,
                    output_dir,
                )
            print(f"Processed {file_name}.pdf as {ramp_type} ramp")
        elif ramp_type == "perpendicular":
            with open(input_pdf_path, "rb") as input_file:
                fill_pdf_text(
                    record,
                    output_filename,
                    input_file,
                    perpendicular_field_coordinates,
                    output_dir,
                )
            print(f"Processed {file_name}.pdf as {ramp_type} ramp")
        elif ramp_type == "combination":
            with open(input_pdf_path, "rb") as input_file:
                fill_pdf_text(
                    record,
                    output_filename,
                    input_file,
                    combination_field_coordinates,
                    output_dir,
                )
            print(f"Processed {file_name}.pdf as {ramp_type} ramp")
        elif ramp_type == "cutthrough":
            with open(input_pdf_path, "rb") as input_file:
                fill_pdf_text(
                    record,
                    output_filename,
                    input_file,
                    cut_field_coordinates,
                    output_dir,
                )
            print(f"Processed {file_name}.pdf as {ramp_type} ramp")
        elif ramp_type == "end-of-walk":
            with open(input_pdf_path, "rb") as input_file:
                fill_pdf_text(
                    record,
                    output_filename,
                    input_file,
                    end_field_coordinates,
                    output_dir,
                )
            print(f"Processed {file_name}.pdf as {ramp_type} ramp")
        elif ramp_type == "blended-transition":
            with open(input_pdf_path, "rb") as input_file:
                fill_pdf_text(
                    record,
                    output_filename,
                    input_file,
                    blended_field_coordinates,
                    output_dir,
                )
            print(f"Processed {file_name}.pdf as {ramp_type} ramp")
        else:
            print(f"{input_pdf_path} has no type")
    else:
        print(f"Warning: PDF file {input_pdf_path} not found.")
