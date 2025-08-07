"""
Working with Multiple Objects
============================

This example demonstrates how to work with multiple color objects in a single CxF file,
which is a common real-world scenario for color palettes or measurement sets.
"""

import colour_cxf
from colour_cxf.cxf3 import (
    ColorCielab,
    ColorSrgb,
    ColorValues,
    CxF,
    FileInformation,
    Object,
    ObjectCollection,
    ReflectanceSpectrum,
    Resources,
)

# Create a CxF object with multiple color objects (a simple color palette)
cxf = CxF()

# Add file information
cxf.file_information = FileInformation(
    creator="Colour Developers", description="Color palette with multiple objects"
)

# Create resources and object collection
cxf.resources = Resources()
cxf.resources.object_collection = ObjectCollection()

# Create multiple color objects representing a palette
colors = [
    {"name": "Red", "rgb": (255, 0, 0), "lab": (53.24, 80.09, 67.20)},
    {"name": "Green", "rgb": (0, 255, 0), "lab": (87.73, -86.18, 83.18)},
    {"name": "Blue", "rgb": (0, 0, 255), "lab": (32.30, 79.19, -107.86)},
    {"name": "Yellow", "rgb": (255, 255, 0), "lab": (97.14, -21.55, 94.48)},
    {"name": "Magenta", "rgb": (255, 0, 255), "lab": (60.32, 98.23, -60.82)},
]

# Add each color as a separate object
for i, color_data in enumerate(colors, 1):
    color_obj = Object(object_type="Target", name=color_data["name"], id=str(i))
    color_obj.color_values = ColorValues()

    # Add RGB values
    rgb = color_data["rgb"]
    color_obj.color_values.choice.append(ColorSrgb(r=rgb[0], g=rgb[1], b=rgb[2]))

    # Add CIELab values
    lab = color_data["lab"]
    color_obj.color_values.choice.append(ColorCielab(l=lab[0], a=lab[1], b=lab[2]))

    # Add a simple spectral representation (for demonstration)
    # In real scenarios, this would be measured spectral data
    spectral_values = [0.1 + (i * 0.05) % 0.8 for _ in range(21)]
    color_obj.color_values.choice.append(
        ReflectanceSpectrum(start_wl=400, value=spectral_values)
    )

    cxf.resources.object_collection.object_value.append(color_obj)

# Write to XML
xml_bytes = colour_cxf.write_cxf(cxf)
xml_string = xml_bytes.decode("utf-8")

print(f"Created CxF file with {len(colors)} color objects")
print("Generated XML (first 15 lines):")
print("\n".join(xml_string.split("\n")[:15]))
print("...")

# Read back and demonstrate accessing multiple objects
print("\nReading back and accessing all objects:")
cxf_read = colour_cxf.read_cxf(xml_bytes)

if (
    cxf_read.resources
    and cxf_read.resources.object_collection
    and cxf_read.resources.object_collection.object_value
):
    objects = cxf_read.resources.object_collection.object_value
    print(f"Found {len(objects)} objects in the CxF file:")

    for obj in objects:
        print(f"\nObject: {obj.name} (ID: {obj.id})")

        if obj.color_values and obj.color_values.choice:
            rgb_values = None
            lab_values = None
            spectral_count = 0

            # Analyze available color representations
            for color_value in obj.color_values.choice:
                if isinstance(color_value, ColorSrgb):
                    rgb_values = (color_value.r, color_value.g, color_value.b)
                elif isinstance(color_value, ColorCielab):
                    lab_values = (color_value.l, color_value.a, color_value.b)
                elif isinstance(color_value, ReflectanceSpectrum):
                    spectral_count = len(color_value.value)

            # Display the color information
            if rgb_values:
                print(f"  RGB: {rgb_values}")
            if lab_values:
                print(
                    f"  CIELab: L={lab_values[0]:.2f}, "
                    f"a={lab_values[1]:.2f}, b={lab_values[2]:.2f}"
                )
            if spectral_count > 0:
                print(f"  Spectral data: {spectral_count} values")

print("\nDemonstrating how to find a specific object by name:")
# Demonstrate finding a specific object by name
target_name = "Blue"
if (
    cxf_read.resources
    and cxf_read.resources.object_collection
    and cxf_read.resources.object_collection.object_value
):
    for obj in cxf_read.resources.object_collection.object_value:
        if obj.name == target_name:
            print(f"Found object '{target_name}' with ID: {obj.id}")
            break
    else:
        print(f"Object '{target_name}' not found")
else:
    print(f"Object '{target_name}' not found")
