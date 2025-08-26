"""
Combining Multiple Color Representations
======================================

This example demonstrates how to work with multiple color representations for the
same object in CxF files.
"""

from xsdata.models.datatype import XmlDateTime

import colour_cxf
from colour_cxf.cxf3 import (
    ColorCielab,
    ColorSpecification,
    ColorSpecificationCollection,
    ColorSrgb,
    ColorValues,
    CreationDate,
    CxF,
    EspectrumType,
    EsphereType,
    GeometryChoice,
    MeasurementSpec,
    MeasurementType,
    Object,
    ObjectCollection,
    ReflectanceSpectrum,
    Resources,
)

# Create a CxF object with multiple color representations
cxf = CxF()
cxf.resources = Resources()
cxf.resources.object_collection = ObjectCollection()

# Create ColorSpecificationCollection
measurement_spec = MeasurementSpec(
    measurement_type=MeasurementType(value=EspectrumType.SPECTRUM_REFLECTANCE),
    geometry_choice=GeometryChoice(choice=EsphereType.SPECULAR_EXCLUDED),
)
color_spec = ColorSpecification(id="CIE_D65_2_1931", measurement_spec=measurement_spec)
cxf.resources.color_specification_collection = ColorSpecificationCollection(
    [color_spec]
)

# Create a color object with RGB, CIELab, and spectral values
color_obj = Object(object_type="Target", name="Purple", id="purple1")
color_obj.creation_date = CreationDate(value=XmlDateTime(2024, 1, 1, 0, 0, 0))

color_obj.color_values = ColorValues()

# Add RGB values
color_obj.color_values.choice.append(
    ColorSrgb(r=128, g=0, b=128, color_specification="CIE_D65_2_1931")
)

# Add CIELab values
color_obj.color_values.choice.append(
    ColorCielab(l=30.0, a=58.0, b=-36.0, color_specification="CIE_D65_2_1931")
)

# Add spectral values (a simple example spectrum)
spectral_values = [0.1 + (i % 5) * 0.05 for i in range(21)]
color_obj.color_values.choice.append(
    ReflectanceSpectrum(value=spectral_values, color_specification="CIE_D65_2_1931")
)

cxf.resources.object_collection.object_value.append(color_obj)

# Write to XML string
xml_bytes = colour_cxf.write_cxf(cxf)
xml_string = xml_bytes.decode("utf-8")

# Print the first few lines of the XML
print("Generated XML (first 10 lines):")
print("\n".join(xml_string.split("\n")[:10]))
print("...")

# Reading back and accessing all representations
print("\nReading back and accessing all representations:")
cxf_read = colour_cxf.read_cxf(xml_bytes)
if (
    cxf_read.resources
    and cxf_read.resources.object_collection
    and cxf_read.resources.object_collection.object_value
):
    obj = cxf_read.resources.object_collection.object_value[0]
    print(f"Object Name: {obj.name}")

    # Access color values
    if obj.color_values and obj.color_values.choice:
        for color_value in obj.color_values.choice:
            if isinstance(color_value, ColorSrgb):
                rgb = color_value
                print(f"RGB: ({rgb.r}, {rgb.g}, {rgb.b})")
            elif isinstance(color_value, ColorCielab):
                lab = color_value
                print(f"CIELab: L={lab.l}, a={lab.a}, b={lab.b}")
            elif isinstance(color_value, ReflectanceSpectrum):
                spectrum = color_value
                print(
                    f"""First few spectral values: {
                    ' '.join(map(str, spectrum.value[:5]))
                    }..."""
                )

print("\nDemonstrating how to check which color representations are available:")
# Demonstrate how to check which color representations are available
if (
    cxf_read.resources
    and cxf_read.resources.object_collection
    and cxf_read.resources.object_collection.object_value
):
    obj = cxf_read.resources.object_collection.object_value[0]
    representations = []
    if obj.color_values and obj.color_values.choice:
        for color_value in obj.color_values.choice:
            if isinstance(color_value, ColorSrgb):
                representations.append("RGB")
            elif isinstance(color_value, ColorCielab):
                representations.append("CIELab")
            elif isinstance(color_value, ReflectanceSpectrum):
                representations.append("Spectral")

        print(
            f"""Available color representations for {obj.name}: {
            ', '.join(representations)
            }"""
        )
