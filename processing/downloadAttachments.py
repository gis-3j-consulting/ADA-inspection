from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import os
import getpass

username = input("Enter your ArcGIS Online username: ")

password = getpass.getpass("Enter your ArcGIS Online password: ")

gis = GIS("https://3j.maps.arcgis.com", username, password)


def downloadAttachments(feature_layer_url, output_folder, last_download):
    layer = FeatureLayer(feature_layer_url)

    image_output = os.path.join(output_folder, "attachments")
    os.makedirs(image_output, exist_ok=True)

    features = layer.query().features
    object_id_field = "objectid"

    table_extensions = [".xlsx", ".xls"]
    image_extensions = [".png"]

    if features:
        for feature in features:
            try:
                feature_id = feature.attributes[object_id_field]
                attachments = layer.attachments.get_list(feature_id)

                if feature_id > last_download:
                    for attachment in attachments:
                        attachment_name = attachment["name"]
                        attachment_extension = os.path.splitext(attachment_name)[
                            1
                        ].lower()
                        attachment_id = attachment["id"]
                        if attachment_extension in image_extensions:
                            final_output = os.path.join(
                                image_output,
                                f"{feature_id}-{attachment_id}{attachment_extension}",
                            )
                            temp_output = os.path.join(image_output, "temp")

                            print(
                                f"Attempting to download attachment {attachment_id} for feature {feature_id}"
                            )

                            attachment_url = layer.attachments.download(
                                feature_id, attachment_id, save_path=temp_output
                            )

                            if os.path.exists(temp_output):
                                print(
                                    f"Downloaded attachment {attachment_id} to {temp_output}"
                                )
                                os.rename(
                                    os.path.join(temp_output, attachment_name),
                                    final_output,
                                )
                                print(
                                    f"Saved as {feature_id}-{attachment_id}{attachment_extension}"
                                )
                            else:
                                print(
                                    f"Failed to download or locate the file at {temp_output}"
                                )

                        elif attachment_extension in table_extensions:
                            temp_output = os.path.join(output_folder, "temp")
                            table_output = os.path.join(
                                output_folder, f"{feature_id}.xlsx"
                            )

                            print(
                                f"Attempting to download table attachment {attachment_name} for feature {feature_id}"
                            )

                            attachment_url = layer.attachments.download(
                                feature_id, attachment_id, save_path=temp_output
                            )

                            if os.path.exists(temp_output):
                                print(
                                    f"Downloaded table attachment {attachment_name} to {temp_output}"
                                )
                                os.rename(
                                    os.path.join(temp_output, attachment_name),
                                    table_output,
                                )
                                print(f"Saved table as {table_output}")
                            else:
                                print(
                                    f"Failed to download or locate the table file at {temp_output}"
                                )
                else:
                    print(f"Skipping feature {feature_id}")

            except Exception as e:
                print(f"Error processing feature {feature_id}: {e}")
    else:
        print("No features found in the layer.")

    print("All specified attachments have been downloaded.")


feature_layer_url = "https://services3.arcgis.com/pZZTDhBBLO3B9dnl/arcgis/rest/services/survey123_64d4f78251234606b2b8bfd0e29ffde6_results/FeatureServer/0"
output_folder = r"C:\3japps\ADA-Inspection\processing\downloads"
last_download = 455

downloadAttachments(feature_layer_url, output_folder, last_download)
