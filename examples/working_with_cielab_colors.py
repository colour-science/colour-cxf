"""
Working with CIELab Colors
=========================

This example demonstrates how to work with CIELab color values in CxF files.
"""

import colour_cxf
from colour_cxf.cxf3 import CxF, Resources, ObjectCollection, Object, ColorValues, ColorCielab

print("Example: Working with CIELab Colors")
print("-" * 30)

# Example CxF with CIELab color
xml_string = """<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <cc:Resources>
        <cc:ObjectCollection>
            <cc:Object ObjectType="Target" Name="Sample" Id="1">
                <cc:ColorValues>
                    <cc:ColorCIELab>
                        <cc:L>50.0</cc:L>
                        <cc:A>20.0</cc:A>
                        <cc:B>30.0</cc:B>
                    </cc:ColorCIELab>
                </cc:ColorValues>
            </cc:Object>
        </cc:ObjectCollection>
    </cc:Resources>
</cc:CxF>"""

# Parse the XML string
cxf = colour_cxf.read_cxf(xml_string.encode('utf-8'))

# Access CIELab values
print("Reading CIELab values from XML:")
if cxf.resources and cxf.resources.object_collection and cxf.resources.object_collection.object_value:
    obj = cxf.resources.object_collection.object_value[0]
    if obj.color_values and obj.color_values.choice:
        for color_value in obj.color_values.choice:
            if isinstance(color_value, ColorCielab):
                lab = color_value
                print(f"Object: {obj.name}")
                print(f"CIELab: L={lab.l}, a={lab.a}, b={lab.b}")

print("\nCreating a new CxF object with CIELab values:")
# Create a new CxF object with CIELab values
new_cxf = CxF()
new_cxf.resources = Resources()
new_cxf.resources.object_collection = ObjectCollection()

color_obj = Object(
    object_type="Target",
    name="Red",
    id="1"
)

color_obj.color_values = ColorValues()
color_obj.color_values.choice.append(ColorCielab(
    l=50.0,
    a=60.0,
    b=30.0
))

new_cxf.resources.object_collection.object_value.append(color_obj)

# Write to XML string
xml_bytes = colour_cxf.write_cxf(new_cxf)
xml_string = xml_bytes.decode('utf-8')

# Print the first few lines of the XML
print("Generated XML (first 10 lines):")
print("\n".join(xml_string.split("\n")[:10]))
print("...")

# Verify by reading back the XML
cxf_read = colour_cxf.read_cxf(xml_bytes)
if cxf_read.resources and cxf_read.resources.object_collection and cxf_read.resources.object_collection.object_value:
    obj = cxf_read.resources.object_collection.object_value[0]
    print("\nVerification - CIELab values read back from XML:")
    print(f"Object Name: {obj.name}")
    if obj.color_values and obj.color_values.choice:
        for color_value in obj.color_values.choice:
            if isinstance(color_value, ColorCielab):
                lab = color_value
                print(f"CIELab: L={lab.l}, a={lab.a}, b={lab.b}")

print("-" * 30)
