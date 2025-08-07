"""
Error Handling and Validation
=============================

This example demonstrates proper error handling when working with CxF files,
including handling malformed XML, missing data, and validation scenarios.
"""

import colour_cxf
from colour_cxf.cxf3 import ColorSrgb, CxF, Object, ReflectanceSpectrum

# Example 1: Handling malformed XML
print("1. Handling malformed XML:")
malformed_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:Resources>
        <cc:ObjectCollection>
            <cc:Objects ObjectType="Target" Name="Test" Id="1">
                <!-- Objects instead of Object -->
        </cc:ObjectCollection>
    </cc:Resources>
</cc:CxF>"""

try:
    cxf = colour_cxf.read_cxf(malformed_xml)
    print("  Successfully parsed malformed XML (unexpected)")
except (ValueError, TypeError, AttributeError) as e:
    print(f"  Expected error caught: {type(e).__name__}: {str(e)[:100]}...")

# Example 2: Handling empty or minimal CxF files
print("\n2. Handling minimal CxF files:")
minimal_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
</cc:CxF>"""

try:
    cxf = colour_cxf.read_cxf(minimal_xml)
    print("  Successfully parsed minimal CxF file")
    print(f"  Has resources: {cxf.resources is not None}")
    print(f"  Has file information: {cxf.file_information is not None}")
except (ValueError, TypeError, AttributeError) as e:
    print(f"  Error: {type(e).__name__}: {e}")

# Example 3: Safe access patterns for CxF data
print("\n3. Safe access patterns for CxF data:")
safe_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:Resources>
        <cc:ObjectCollection>
            <cc:Object ObjectType="Target" Name="SafeTest" Id="1">
                <cc:ColorValues>
                    <cc:ColorSRGB>
                        <cc:R>255</cc:R>
                        <cc:G>128</cc:G>
                        <cc:B>0</cc:B>
                    </cc:ColorSRGB>
                </cc:ColorValues>
            </cc:Object>
        </cc:ObjectCollection>
    </cc:Resources>
</cc:CxF>"""

try:
    cxf = colour_cxf.read_cxf(safe_xml)

    # Safe way to access nested data with proper null checks
    def safe_get_first_object(cxf_obj: CxF) -> Object | None:
        """Safely get the first object from a CxF file."""
        if not cxf_obj.resources:
            return None
        if not cxf_obj.resources.object_collection:
            return None
        if not cxf_obj.resources.object_collection.object_value:
            return None
        return cxf_obj.resources.object_collection.object_value[0]

    def safe_get_color_values(obj: Object | None) -> list:
        """Safely get color values from an object."""
        if not obj or not obj.color_values:
            return []
        return obj.color_values.choice or []

    # Demonstrate safe access
    first_obj = safe_get_first_object(cxf)
    if first_obj:
        print(f"  Found object: {first_obj.name}")

        color_values = safe_get_color_values(first_obj)
        print(f"  Number of color representations: {len(color_values)}")

        # Safe type checking and value access
        for color_value in color_values:
            if isinstance(color_value, ColorSrgb):
                # Check for None values before using
                r = color_value.r if color_value.r is not None else 0
                g = color_value.g if color_value.g is not None else 0
                b = color_value.b if color_value.b is not None else 0
                print(f"  RGB: ({r}, {g}, {b})")
            elif isinstance(color_value, ReflectanceSpectrum):
                if color_value.value:
                    print(f"  Spectral data: {len(color_value.value)} values")
                else:
                    print("  Spectral data: No values")
    else:
        print("  No objects found in CxF file")

except (ValueError, TypeError, AttributeError) as e:
    print(f"  Error: {type(e).__name__}: {e}")

# Example 4: Handling file I/O errors
print("\n5. Handling file I/O errors:")
try:
    # Try to read from a non-existent file
    cxf = colour_cxf.read_cxf_from_file("non_existent_file.cxf")
except FileNotFoundError as e:
    print(f"  File not found error caught: {e}")
except (ValueError, TypeError, AttributeError) as e:
    print(f"  Other error caught: {type(e).__name__}: {e}")
