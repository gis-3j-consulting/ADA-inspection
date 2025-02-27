from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName, PdfString
import pandas as pd
import os


def format_choice_value(value):
    return str(value).strip().lower()


def combobox(annotation, value):
    export = None
    formatted_value = format_choice_value(value)
    for each in annotation["/Opt"]:
        if isinstance(each, list) and len(each) > 1:
            if format_choice_value(each[1].to_unicode()) == formatted_value:
                export = each[0].to_unicode()
        elif isinstance(each, PdfString):
            if format_choice_value(each.to_unicode()) == formatted_value:
                export = each.to_unicode()
    if export is None:
        print(f"Warning: Export Value for '{value}' Not Found. Using the value as is.")
        export = value
    pdfstr = PdfString.encode(export)
    annotation.update(PdfDict(V=pdfstr, AS=pdfstr))


def fill_pdf_form(pdf_template_path, data, lookup, output_path):
    template_pdf = PdfReader(pdf_template_path)
    fields_updated = False
    comments = ""

    print("\nProcessing PDF fields:")
    for page in template_pdf.pages:
        annotations = page.get("/Annots")
        if annotations:
            for annotation in annotations:
                if annotation.get("/Subtype") == "/Widget":
                    field = annotation.get("/T")
                    if field:
                        field_name = (
                            field[1:-1]
                            if field.startswith("(") and field.endswith(")")
                            else field
                        )
                        field_type = annotation.get("/FT")
                        print(f"\nField: {field_name}")
                        print(f"  Type: {field_type}")

                        if field_name in lookup:
                            data_field_name = lookup[field_name]
                            print(f"  Mapped to CSV column: {data_field_name}")
                            if data_field_name in data and pd.notna(
                                data[data_field_name]
                            ):
                                field_value = str(data[data_field_name])

                                if field_type == PdfName("Tx"):  # Text field
                                    annotation.update(
                                        PdfDict(V=field_value, AP=PdfDict())
                                    )
                                    fields_updated = True
                                    print(f"  Text value filled: {field_value}")

                                elif field_type == PdfName(
                                    "Ch"
                                ):  # Choice field (combobox/dropdown)
                                    try:
                                        combobox(annotation, field_value)
                                        fields_updated = True
                                        print(
                                            f"  Combobox value selected: {field_value}"
                                        )
                                        # Append to comments string
                                        comments += f"{field_name}: {field_value}\n"
                                    except Exception as e:
                                        print(
                                            f"  Error setting combobox value: {str(e)}"
                                        )

                                elif field_type == PdfName("Btn"):  # Checkbox
                                    if field_name.endswith("_PASS"):
                                        if (
                                            field_value.lower() == "pass"
                                            or field_value.lower() == "y"
                                        ):
                                            annotation.update(
                                                PdfDict(
                                                    AS=PdfName("Yes"), V=PdfName("Yes")
                                                )
                                            )
                                            fields_updated = True
                                            print(f"  Checkbox selected: {field_name}")
                                        else:

                                            fail_field_name = field_name.replace(
                                                "_PASS", "_FAIL"
                                            )
                                            print(
                                                f"  Looking for corresponding fail field: {fail_field_name}"
                                            )
                                            for fail_annotation in annotations:
                                                fail_field = fail_annotation.get("/T")
                                                if (
                                                    fail_field
                                                    and fail_field_name
                                                    in str(fail_field)
                                                ):
                                                    fail_annotation.update(
                                                        PdfDict(
                                                            AS=PdfName("Yes"),
                                                            V=PdfName("Yes"),
                                                        )
                                                    )
                                                    fields_updated = True
                                                    print(
                                                        f"  Checkbox selected for fail: {fail_field_name}"
                                                    )
                                                    break
                                            else:
                                                print(
                                                    f"  Corresponding fail field not found for: {fail_field_name}"
                                                )

                                    elif field_name.endswith("TRVRSBLE"):
                                        if field_value == "Y":
                                            annotation.update(
                                                PdfDict(
                                                    AS=PdfName("Yes"), V=PdfName("Yes")
                                                )
                                            )
                                            fields_updated = True
                                            print(f"   Checkbox selected: {field_name}")
                                    elif field_name.endswith("_PRSNT"):
                                        if field_value.lower() == "none":
                                            annotation.update(
                                                PdfDict(
                                                    AS=PdfName("Yes"), V=PdfName("Yes")
                                                )
                                            )
                                            fields_updated = True
                                            print(f"   Checkbox selected: {field_name}")
                                        elif field_value.lower() == "turn-space":
                                            turn_space_field = "TURN_SPACE_PRSNT"
                                            for turn_space_annotation in annotations:
                                                turn_space = turn_space_annotation.get(
                                                    "/T"
                                                )
                                                if (
                                                    turn_space
                                                    and turn_space_field
                                                    == str(turn_space)
                                                ):
                                                    turn_space_annotation.update(
                                                        PdfDict(
                                                            AS=PdfName("Yes"),
                                                            V=PdfName("Yes"),
                                                        )
                                                    )
                                                    fields_updated = True
                                                    print(
                                                        f"Turn space selected for {turn_space_field}"
                                                    )
                                                    break
                                            else:
                                                print(
                                                    f"Failed to find turn space field: {turn_space_field}"
                                                )
                                        elif field_value.lower() == "landing":
                                            landing_field = "LANDING_PRSNT"
                                            for landing_annotation in annotations:
                                                landing = landing_annotation.get("/T")
                                                if landing and landing_field == str(
                                                    landing
                                                ):
                                                    landing_annotation.update(
                                                        PdfDict(
                                                            AS=PdfName("Yes"),
                                                            V=PdfName("Yes"),
                                                        )
                                                    )
                                                    fields_updated = True
                                                    print(
                                                        f"Landing selected for {landing_field}"
                                                    )
                                                    break
                                            else:
                                                print(
                                                    f"Failed to find landing field: {landing_field}"
                                                )

                                        else:
                                            print(
                                                f"Error finding value for {field_name}"
                                            )
                                    else:
                                        print(
                                            f"  Checkbox field doesn't match with existing protocols: {field_name}"
                                        )

                                else:
                                    print(f"  Unsupported field type: {field_type}")
                            else:
                                print(f"  No data found in CSV for this field")
                        else:
                            print(f"  Not found in lookup table")

    # Update comments field with accumulated string
    if comments:
        for page in template_pdf.pages:
            annotations = page.get("/Annots")
            if annotations:
                for annotation in annotations:
                    field = annotation.get("/T")
                    if field and field == "(ADA2_COMNT)":
                        existing_comments = annotation.get("/V")
                        if existing_comments:
                            existing_comments = str(existing_comments)
                        else:
                            existing_comments = ""

                        updated_comments = existing_comments + " \n" + comments

                        annotation.update(PdfDict(V=updated_comments, AP=PdfDict()))
                        print(f"\nComments field updated with: \n{updated_comments}")
                        fields_updated = True
                        break

    if not fields_updated:
        print(
            "\nNo fields were updated. Please check the PDF form fields and the lookup table."
        )

    PdfWriter().write(output_path, template_pdf)


combined_csv_path = r"O:\City of North Plains\City Projects\Misc\ADA Study\GIS\Tables\combined_processed_output.csv"
data_df = pd.read_csv(combined_csv_path)

lookup_path = (
    r"O:\City of North Plains\City Projects\Misc\ADA Study\GIS\Tables\lookup.csv"
)
lookup_df = pd.read_csv(lookup_path)

output_folder = r"C:\3japps\ADA-Inspection\processing\output"

lookup_df = lookup_df.dropna(subset=["pdfField"])
lookup_dict = pd.Series(lookup_df.csvField.values, index=lookup_df.pdfField).to_dict()

print(lookup_dict)


# Process each row in the combined CSV file
def process_csv_rows(data_df, output_folder):
    for index, row in data_df.iterrows():
        ramp_type = row["type"]
        file_name = row["fileName"]

        if pd.isna(file_name):
            print(f"Skipping row {index} due to missing fileName")
            continue

        try:
            output_file_name = f"{int(file_name)}.pdf"
        except ValueError:
            print(
                f"Warning: Invalid fileName '{file_name}' in row {index}. Using index as filename."
            )
            output_file_name = f"output_{index}.pdf"

        pdf_template_path = f"C:\\python\\scripts\\pdfeditor2\\docs\\{ramp_type}.pdf"
        output_path = os.path.join(output_folder, output_file_name)

        print(f"Now processing {file_name}")
        fill_pdf_form(pdf_template_path, row, lookup_dict, output_path)


process_csv_rows(data_df, output_folder)
print(f"All rows in {combined_csv_path} processed and saved in {output_folder}")


def process_specific_row(data_df, output_folder, row_index):
    try:
        row = data_df.iloc[row_index]
    except IndexError:
        print(f"Error: Row index {row_index} is out of bounds.")
        return

    ramp_type = row["type"]
    file_name = row["fileName"]

    if pd.isna(file_name):
        print(f"Skipping row {row_index} due to missing fileName")
        return

    try:
        output_file_name = f"{int(file_name)}.pdf"
    except ValueError:
        print(
            f"Warning: Invalid fileName '{file_name}' in row {row_index}. Using index as filename."
        )
        output_file_name = f"output_{row_index}.pdf"

    pdf_template_path = f"C:\\python\\scripts\\pdfeditor2\\docs\\{ramp_type}.pdf"
    output_path = os.path.join(output_folder, output_file_name)

    print(f"Now processing row {row_index} with fileName '{file_name}'")
    fill_pdf_form(pdf_template_path, row, lookup_dict, output_path)

process_specific_row(data_df, output_folder, 392)

def process_rows_by_objectid(data_df, output_folder, objectid_threshold):
    data_df["fileName"] = pd.to_numeric(data_df["fileName"], errors="coerce")

    filtered_rows = data_df[data_df["fileName"] > objectid_threshold]

    if filtered_rows.empty:
        print(f"No rows found with ObjectID greater than {objectid_threshold}.")
        return

    for index, row in filtered_rows.iterrows():
        ramp_type = row["type"]
        file_name = row["fileName"]

        if pd.isna(file_name):
            print(f"Skipping row {index} due to missing or invalid fileName")
            continue

        try:
            output_file_name = f"{int(file_name)}.pdf"
        except ValueError:
            print(
                f"Warning: Invalid fileName '{file_name}' in row {index}. Using index as filename."
            )
            output_file_name = f"output_{index}.pdf"

        pdf_template_path = f"C:\\python\\scripts\\pdfeditor2\\docs\\{ramp_type}.pdf"
        output_path = os.path.join(output_folder, output_file_name)

        print(f"Now processing row {index} with ObjectID '{row['fileName']}'")
        fill_pdf_form(pdf_template_path, row, lookup_dict, output_path)


process_rows_by_objectid(data_df, output_folder, 455)
