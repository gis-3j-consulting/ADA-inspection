import pandas as pd
import geopandas as gpd
import fiona


#### workaround script (run in python window) ###

import arcpy

# Set input and output paths
input_fc = r"P:\21713-North Plains\GIS\mxd\21713 North Plains.gdb\ADA_Ramp_Inspections"
output_fc = (
    r"P:\21713-North Plains\GIS\mxd\21713 North Plains.gdb\ADA_Ramp_Inspections2"
)
prefix_to_remove = "combined_processed_output_csv_"

# Create a copy of the feature class
arcpy.CopyFeatures_management(input_fc, output_fc)

# List all fields in the copied feature class
fields = arcpy.ListFields(output_fc)

# Create a dictionary to store the old and new field names
field_mappings = {}

# Loop through the fields
for field in fields:
    field_name = field.name
    # Check if the field name starts with the prefix
    if field_name.startswith(prefix_to_remove):
        # Create a new field name by removing the prefix
        new_field_name = field_name.replace(prefix_to_remove, "")
        field_mappings[field_name] = new_field_name

# Rename the fields
for old_field, new_field in field_mappings.items():
    print(f"Renaming field '{old_field}' to '{new_field}'")
    arcpy.AlterField_management(output_fc, old_field, new_field)

print("Field renaming complete.")


##### Currently non-functional due to conflicts with geopandas ####

input_fc = r"P:\21713-North Plains\GIS\mxd\21713 North Plains.gdb\survey_Clip3"
output_shapefile = (
    r"P:\21713-North Plains\GIS\Infrastructure\Utilities\ADA_Ramp_Inspections.shp"
)
prefix_to_remove = "combined_processed_output_csv_"

gdb_path = "P:/21713-North Plains/GIS/mxd/21713 North Plains.gdb"
input_feature = "survey_Clip3"
layers = fiona.listlayers(gdb_path)

try:
    gdf = gpd.read_file(gdb_path, layer=input_feature, crs="EPSG:4326")
    print("GDF loaded successfully")
except Exception as e:
    print(f"Error: {e}")

for field in gdf.columns:
    print(field)

gdf.columns = [
    col[len(prefix_to_remove) :] if col.startswith(prefix_to_remove) else col
    for col in gdf.columns
]

datetime_fields = gdf.select_dtypes(
    include=["datetime64[ns, UTC]", "datetime64[ns]"]
).columns
print(f"Datetime fields detected and will be dropped: {list(datetime_fields)}")
gdf = gdf.drop(columns=datetime_fields)

gdf.to_file(output_shapefile)


from osgeo import ogr
import datetime

# Paths
input_gdb = r"P:\21713-North Plains\GIS\mxd\21713 North Plains.gdb"
input_layer = "survey_Clip3"
output_shapefile = (
    r"P:\21713-North Plains\GIS\Infrastructure\Utilities\ADA_Ramp_Inspections.shp"
)

# Prefix to remove
prefix_to_remove = "combined_processed_output_csv_"

# Open geodatabase
driver = ogr.GetDriverByName("FileGDB")
print(driver)
datasource = driver.Open(input_gdb)
layer = datasource.GetLayerByName(input_layer)

# Create output shapefile
out_driver = ogr.GetDriverByName("ESRI Shapefile")
out_datasource = out_driver.CreateDataSource(output_shapefile)
out_layer = out_datasource.CreateLayer(
    "ADA_Ramp_Inspections", geom_type=layer.GetGeomType()
)

# Process layer definition
in_layer_defn = layer.GetLayerDefn()
for i in range(in_layer_defn.GetFieldCount()):
    field_defn = in_layer_defn.GetFieldDefn(i)

    # Remove prefix from field name
    new_field_name = field_defn.GetName()
    if new_field_name.startswith(prefix_to_remove):
        new_field_name = new_field_name[len(prefix_to_remove) :]

    # Skip datetime fields
    if field_defn.GetType() in [ogr.OFTDate, ogr.OFTDateTime]:
        continue

    # Create field with new name
    new_field = ogr.FieldDefn(new_field_name, field_defn.GetType())
    out_layer.CreateField(new_field)

# Copy features
out_layer_defn = out_layer.GetLayerDefn()
for feature in layer:
    out_feature = ogr.Feature(out_layer_defn)

    for i in range(out_layer_defn.GetFieldCount()):
        field_defn = out_layer_defn.GetFieldDefn(i)

        # Get original field name (with prefix)
        orig_field_name = field_defn.GetName()
        if not orig_field_name.startswith(prefix_to_remove):
            orig_field_name = prefix_to_remove + orig_field_name

        value = feature.GetField(orig_field_name)
        out_feature.SetField(field_defn.GetName(), value)

    out_feature.SetGeometry(feature.GetGeometryRef())
    out_layer.CreateFeature(out_feature)

# Close datasources
out_datasource = None
datasource = None
