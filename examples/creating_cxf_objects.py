"""
Creating CxF Objects
===================

This example demonstrates how to create CxF objects programmatically and write them
to XML.
"""

from xsdata.models.datatype import XmlDateTime

import colour_cxf
from colour_cxf.cxf3 import (
    ColorSpecification,
    ColorSpecificationCollection,
    ColorSrgb,
    ColorValues,
    CreationDate,
    CxF,
    EspectrumType,
    EsphereType,
    FileInformation,
    GeometryChoice,
    MeasurementSpec,
    MeasurementType,
    Object,
    ObjectCollection,
    Resources,
)

# Create a new CxF object
cxf = CxF()

# Add file information
cxf.file_information = FileInformation(
    creator="Colour Developers", description="Programmatically created CxF file"
)

# Create a color object
color_obj = Object(object_type="Target", name="Blue", id="blue1")
color_obj.creation_date = CreationDate(value=XmlDateTime(2024, 1, 1, 0, 0, 0))

# Add RGB color values
color_obj.color_values = ColorValues()
color_obj.color_values.choice.append(
    ColorSrgb(r=0, g=0, b=255, color_specification="CIE_D65_2_1931")
)

# Create object collection and add the color object
obj_collection = ObjectCollection()
obj_collection.object_value.append(color_obj)

# Create ColorSpecificationCollection
measurement_spec = MeasurementSpec(
    measurement_type=MeasurementType(value=EspectrumType.SPECTRUM_REFLECTANCE),
    geometry_choice=GeometryChoice(choice=EsphereType.SPECULAR_EXCLUDED),
)
color_spec = ColorSpecification(id="CIE_D65_2_1931", measurement_spec=measurement_spec)

# Create resources and add the collections
cxf.resources = Resources()
cxf.resources.object_collection = obj_collection
cxf.resources.color_specification_collection = ColorSpecificationCollection(
    [color_spec]
)

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
