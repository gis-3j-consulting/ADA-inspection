import os
import pandas as pd

dataframes = []
output_folder = r"C:\python\scripts\pdfeditor2\processing\downloads"

for file_name in os.listdir(output_folder):
    if file_name.endswith(".xlsx") or file_name.endswith(".xls"):
        file_path = os.path.join(output_folder, file_name)

        df = pd.read_excel(file_path)

        object_id = os.path.splitext(file_name)[0]
        df["Object ID"] = object_id

        dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True, sort=False)

combined_output_path = r"C:\python\scripts\pdfeditor2\processing\combined_output2.xlsx"
combined_df.to_excel(combined_output_path, index=False)

update_csv = combined_output_path.split(".")[0] + ".csv"

print(f"All tables have been combined and saved to {combined_output_path}")


def excel2csvProcess(combined_output_path):
    combined_df = pd.read_excel(combined_output_path)
    field_names_list = [name.replace("-", "_") for name in combined_df.columns.tolist()]
    print(field_names_list)

    update_csv = combined_output_path.split(".")[0] + ".csv"

    combined_df.to_csv(update_csv, index=False)

    df = pd.read_csv(update_csv)
    remove_vowels = lambda text: "".join(
        char for char in text if char.lower() not in "aeiou"
    )
    field_names = [
        remove_vowels(name) if len(name) > 13 else name for name in field_names_list
    ]

    def remove_vowels(text):
        return "".join(char for char in text if char.lower() not in "aeiou")

    df.columns = field_names

    df.to_csv(update_csv, index=False)


excel2csvProcess(combined_output_path)


def update_table(combined_output, recent_output):
    df = pd.read_csv(combined_output)
    df_update = pd.read_csv(recent_output)

    dfs = [df, df_update]

    df_combined = pd.concat(dfs, ignore_index=True, sort=False)

    df_combined.to_csv(combined_output, index=False)

    print(f"{combined_output} table updated with data from {recent_output}")


master_table = r"C:\python\scripts\pdfeditor2\processing\combined_output.csv"

update_table(master_table, update_csv)
