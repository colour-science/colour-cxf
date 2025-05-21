"""
Reading CxF Files
================

This example demonstrates how to read CxF files from strings and access basic information.
"""

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
cxf = colour_cxf.read_cxf(xml_string.encode('utf-8'))

# Access file information
print("Example: Reading CxF Files")
print("-" * 30)
if cxf.file_information:
    print(f"Creator: {cxf.file_information.creator}")
    print(f"Creation Date: {cxf.file_information.creation_date}")
    print(f"Description: {cxf.file_information.description}")
print("-" * 30)
