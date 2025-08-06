"""
Creating CxF Objects
===================

This example demonstrates how to create CxF objects programmatically and write them
to XML.
"""

import colour_cxf
from colour_cxf.cxf3 import (
    ColorSrgb,
    ColorValues,
    CxF,
    FileInformation,
    Object,
    ObjectCollection,
    Resources,
)

print("Example: Creating CxF Objects")
print("-" * 30)

# Create a new CxF object
cxf = CxF()

# Add file information
cxf.file_information = FileInformation(
    creator="Colour Developers", description="Programmatically created CxF file"
)

# Create a color object
color_obj = Object(object_type="Target", name="Blue", id="1")

# Add RGB color values
color_obj.color_values = ColorValues()
color_obj.color_values.choice.append(ColorSrgb(r=0, g=0, b=255))

# Create object collection and add the color object
obj_collection = ObjectCollection()
obj_collection.object_value.append(color_obj)

# Create resources and add the object collection
cxf.resources = Resources()
cxf.resources.object_collection = obj_collection

# Write to XML string
xml_bytes = colour_cxf.write_cxf(cxf)
xml_string = xml_bytes.decode("utf-8")

# Print the first few lines of the XML
print("Generated XML (first 10 lines):")
print("\n".join(xml_string.split("\n")[:10]))
print("...")

# Verify by reading back the XML
cxf_read = colour_cxf.read_cxf(xml_bytes)
if (
    cxf_read.resources
    and cxf_read.resources.object_collection
    and cxf_read.resources.object_collection.object_value
):
    obj = cxf_read.resources.object_collection.object_value[0]
    print("\nVerification - Object read back from XML:")
    print(f"Object Name: {obj.name}")
    print(f"Object Type: {obj.object_type}")

    # Access RGB values
    if obj.color_values and obj.color_values.choice:
        for color_value in obj.color_values.choice:
            if isinstance(color_value, ColorSrgb):
                rgb = color_value
                print(f"RGB: ({rgb.r}, {rgb.g}, {rgb.b})")

print("-" * 30)
