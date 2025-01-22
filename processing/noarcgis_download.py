import os
import requests
from getpass import getpass

username = input("Enter your ArcGIS Online username: ")
password = getpass("Enter your ArcGIS Online password: ")

# Define the base URL and login credentials for ArcGIS REST API
base_url = "https://3j.maps.arcgis.com"
feature_layer_url = "https://services3.arcgis.com/pZZTDhBBLO3B9dnl/arcgis/rest/services/survey123_64d4f78251234606b2b8bfd0e29ffde6_results/FeatureServer/0"
output_folder = r"C:\python\scripts\pdfeditor2\downloads"
last_download = 172


# Authenticate and get token
def get_token(username, password, base_url):
    token_url = f"{base_url}/sharing/rest/generateToken"
    params = {
        "username": username,
        "password": password,
        "referer": base_url,
        "f": "json",
    }
    response = requests.post(token_url, data=params, verify=False)
    response_json = response.json()
    if "token" in response_json:
        return response_json["token"]
    else:
        raise Exception("Unable to get token. Check your credentials.")


token = get_token(username, password, base_url)


def download_attachments(feature_layer_url, output_folder, last_download, token):
    image_output = os.path.join(output_folder, "attachments")
    os.makedirs(image_output, exist_ok=True)

    # Query the layer to get all features
    query_url = f"{feature_layer_url}/query"
    params = {"where": "1=1", "outFields": "*", "f": "json", "token": token}
    response = requests.get(query_url, params=params, verify=False)
    features = response.json()["features"]

    object_id_field = "objectid"

    # Specify the file types to download
    table_extensions = [".xlsx", ".xls"]
    image_extensions = [".jpg", ".jpeg"]

    # Download the allowed attachments
    for feature in features:
        feature_id = feature["attributes"][object_id_field]

        if feature_id > last_download:
            attachments_url = f"{feature_layer_url}/{feature_id}/attachments"
            params = {"f": "json", "token": token}
            attachments_response = requests.get(attachments_url, params=params)
            attachments = attachments_response.json().get("attachmentInfos", [])

            for attachment in attachments:
                attachment_name = attachment["name"]
                attachment_extension = os.path.splitext(attachment_name)[1].lower()
                attachment_id = attachment["id"]
                download_url = (
                    f"{feature_layer_url}/{feature_id}/attachments/{attachment_id}"
                )

                if attachment_extension in image_extensions:
                    final_output = os.path.join(
                        image_output,
                        f"{feature_id}-{attachment_id}{attachment_extension}",
                    )

                    print(
                        f"Attempting to download attachment {attachment_id} for feature {feature_id}"
                    )

                    # Download the file
                    file_response = requests.get(
                        download_url, params={"token": token}, verify=False
                    )
                    if file_response.status_code == 200:
                        with open(final_output, "wb") as file:
                            file.write(file_response.content)
                        print(f"Saved as {final_output}")
                    else:
                        print(f"Failed to download {attachment_name}")

                elif attachment_extension in table_extensions:
                    table_output = os.path.join(output_folder, f"{feature_id}.xlsx")

                    print(
                        f"Attempting to download attachment {attachment_name} for feature {feature_id}"
                    )

                    file_response = requests.get(
                        download_url, params={"token": token}, verify=False
                    )
                    if file_response.status_code == 200:
                        with open(table_output, "wb") as file:
                            file.write(file_response.content)
                        print(f"Saved table as {table_output}")
                    else:
                        print(f"Failed to download {attachment_name}")

        else:
            print(f"Skipping feature {feature_id}")

    print("All specified attachments have been downloaded.")


download_attachments(feature_layer_url, output_folder, last_download, token)
