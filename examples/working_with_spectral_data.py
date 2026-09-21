"""
Working with Spectral Data
=========================

This example demonstrates how to work with reflectance spectra in CxF files.
"""

from xsdata.models.datatype import XmlDateTime

import colour_cxf
from colour_cxf.cxf3 import (
    ColorSpecification,
    ColorSpecificationCollection,
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

# Example CxF with spectral data
xml_string = """<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <cc:Resources>
        <cc:ObjectCollection>
            <cc:Object ObjectType="Target" Name="Sample" Id="sample1">
                <cc:CreationDate>2024-01-01T00:00:00</cc:CreationDate>
                <cc:ColorValues>
                    <cc:ReflectanceSpectrum StartWL="400" ColorSpecification="CIE_D65_2_1931">
                        0.05 0.06 0.07 0.08 0.10 0.12 0.15 0.20 0.30 0.40 0.50 0.60 0.70 0.80 0.85 0.90 0.92 0.94 0.95 0.96 0.97
                    </cc:ReflectanceSpectrum>
                </cc:ColorValues>
            </cc:Object>
        </cc:ObjectCollection>
        <cc:ColorSpecificationCollection>
            <cc:ColorSpecification Id="CIE_D65_2_1931">
                <cc:MeasurementSpec>
                    <cc:MeasurementType>Spectrum_Reflectance</cc:MeasurementType>
                    <cc:GeometryChoice>
                        <cc:SphereGeometry>Specular_Excluded</cc:SphereGeometry>
                    </cc:GeometryChoice>
                </cc:MeasurementSpec>
            </cc:ColorSpecification>
        </cc:ColorSpecificationCollection>
    </cc:Resources>
</cc:CxF>"""  # noqa: E501

# Parse the XML string
cxf = colour_cxf.read_cxf(xml_string.encode("utf-8"))

# Access spectral data
print("Reading spectral data from XML:")
if (
    cxf.resources
    and cxf.resources.object_collection
    and cxf.resources.object_collection.object_value
):
    obj = cxf.resources.object_collection.object_value[0]
    if obj.color_values and obj.color_values.choice:
        for color_value in obj.color_values.choice:
            if isinstance(color_value, ReflectanceSpectrum):
                spectrum = color_value
                print(f"Object: {obj.name}")
                print(f"Start Wavelength: {spectrum.start_wl} nm")
                print(f"Number of spectral values: {len(spectrum.value)}")
                print(
                    f"""First few spectral values: {
                        " ".join(map(str, spectrum.value[:5]))
                    }..."""
                )

print("\nCreating a new CxF object with spectral data:")
# Create a new CxF object with spectral data
new_cxf = CxF()
new_cxf.resources = Resources()
new_cxf.resources.object_collection = ObjectCollection()

# Create ColorSpecificationCollection
measurement_spec = MeasurementSpec(
    measurement_type=MeasurementType(value=EspectrumType.SPECTRUM_REFLECTANCE),
    geometry_choice=GeometryChoice(choice=EsphereType.SPECULAR_EXCLUDED),
)
color_spec = ColorSpecification(id="CIE_D65_2_1931", measurement_spec=measurement_spec)
new_cxf.resources.color_specification_collection = ColorSpecificationCollection(
    [color_spec]
)

color_obj = Object(object_type="Target", name="Sample", id="sample1")
color_obj.creation_date = CreationDate(value=XmlDateTime(2024, 1, 1, 0, 0, 0))

# Create a simple linear ramp spectrum from 0.05 to 0.97
# (21 values to match the original)
spectral_values = [0.05 + i * 0.044 for i in range(21)]

color_obj.color_values = ColorValues()
color_obj.color_values.choice.append(
    ReflectanceSpectrum(
        start_wl=400, value=spectral_values, color_specification="CIE_D65_2_1931"
    )
)

new_cxf.resources.object_collection.object_value.append(color_obj)

# Write to XML string
xml_bytes = colour_cxf.write_cxf(new_cxf)
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
    print("\nVerification - Spectral data read back from XML:")
    print(f"Object Name: {obj.name}")
    if obj.color_values and obj.color_values.choice:
        for color_value in obj.color_values.choice:
            if isinstance(color_value, ReflectanceSpectrum):
                spectrum = color_value
                print(f"Start Wavelength: {spectrum.start_wl} nm")
                print(f"Number of spectral values: {len(spectrum.value)}")
                print(
                    f"""First few spectral values: {
                        " ".join(map(str, spectrum.value[:5]))
                    }..."""
                )
