"""
Reading CxF Files
================

This example demonstrates how to read CxF files from strings and files, and access basic
information.
"""

import os
import tempfile

import colour_cxf

# Reading from a string
xml_string = """<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <cc:FileInformation>
        <cc:Creator>Colour Developers</cc:Creator>
        <cc:CreationDate>2023-01-01T00:00:00</cc:CreationDate>
        <cc:Description>Simple CxF Example</cc:Description>
    </cc:FileInformation>
</cc:CxF>"""

# Parse the XML string
cxf = colour_cxf.read_cxf(xml_string.encode("utf-8"))

if cxf.file_information:
    print(f"Creator: {cxf.file_information.creator}")
    # Format the creation date for better readability
    if cxf.file_information.creation_date:
        date_obj = cxf.file_information.creation_date.value
        if date_obj:
            formatted_date = (
                f"{date_obj.year}-{date_obj.month:02d}-{date_obj.day:02d} "
                f"{date_obj.hour:02d}:{date_obj.minute:02d}:{date_obj.second:02d}"
            )
            print(f"Creation Date: {formatted_date}")
    print(f"Description: {cxf.file_information.description}")

print("\nReading from a file:")
print("-" * 30)

# Create a temporary file to demonstrate file reading
with tempfile.NamedTemporaryFile(mode="w", suffix=".cxf", delete=False) as temp_file:
    temp_file.write(xml_string)
    temp_file_path = temp_file.name

try:
    # Read from the temporary file
    cxf_from_file = colour_cxf.read_cxf_from_file(temp_file_path)

    if cxf_from_file.file_information:
        print(f"Creator (from file): {cxf_from_file.file_information.creator}")
        # Format the creation date for better readability
        if cxf_from_file.file_information.creation_date:
            date_obj = cxf_from_file.file_information.creation_date.value
            if date_obj:
                formatted_date = (
                    f"{date_obj.year}-{date_obj.month:02d}-{date_obj.day:02d} "
                    f"{date_obj.hour:02d}:{date_obj.minute:02d}:{date_obj.second:02d}"
                )
                print(f"Creation Date (from file): {formatted_date}")
        print(f"Description (from file): {cxf_from_file.file_information.description}")
finally:
    # Clean up the temporary file
    os.unlink(temp_file_path)
