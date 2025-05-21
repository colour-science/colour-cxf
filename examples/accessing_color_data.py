"""
Accessing Color Data
===================

This example demonstrates how to access color data from a CxF file.
"""

import colour_cxf

# Example CxF with a simple color object
xml_string = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <cc:Resources>
        <cc:ObjectCollection>
            <cc:Object ObjectType="Target" Name="Red" Id="1">
                <cc:ColorValues>
                    <cc:ColorSRGB>
                        <cc:R>255</cc:R>
                        <cc:G>0</cc:G>
                        <cc:B>0</cc:B>
                    </cc:ColorSRGB>
                </cc:ColorValues>
            </cc:Object>
        </cc:ObjectCollection>
    </cc:Resources>
</cc:CxF>"""

# Parse the XML string
cxf = colour_cxf.read_cxf(xml_string)

print("Example: Accessing Color Data")
print("-" * 30)

# Access the first object in the collection
if cxf.resources and cxf.resources.object_collection:
    obj = cxf.resources.object_collection.object_value[0]
    print(f"Object Name: {obj.name}")
    print(f"Object Type: {obj.object_type}")
    print(f"Object ID: {obj.id}")

    # Access RGB values
    if obj.color_values and obj.color_values.choice:
        rgb = obj.color_values.choice[0]
        # Type checking for RGB values
        from colour_cxf.cxf3.color_srgb import ColorSrgb
        if isinstance(rgb, ColorSrgb) and rgb.r is not None and rgb.g is not None and rgb.b is not None:
            print(f"RGB: ({rgb.r}, {rgb.g}, {rgb.b})")

print("-" * 30)
