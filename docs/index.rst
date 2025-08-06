=================
Colour CxF
=================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   tutorial

Introduction
===========

Colour CxF is a Python library for reading, manipulating, and writing Color Exchange Format (CxF) files. CxF is an XML-based format for exchanging color information between different applications and devices.

Features
========

- Read CxF files from strings or files
- Access and manipulate color data in various formats (RGB, CIELab, spectral)
- Create CxF objects programmatically
- Write CxF objects to XML strings

Installation
===========

You can install Colour CxF using pip:

.. code-block:: bash

    pip install colour-cxf

Quick Start
==========

.. code-block:: python

    import colour_cxf

    # Reading from a string
    xml_string = """<?xml version="1.0" encoding="UTF-8"?>
    <cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <cc:FileInformation>
            <cc:Creator>Colour Developers</cc:Creator>
            <cc:Description>Simple CxF Example</cc:Description>
        </cc:FileInformation>
    </cc:CxF>"""

    # Parse the XML string
    cxf = colour_cxf.read_cxf(xml_string.encode("utf-8"))

    # Access file information
    print(f"Creator: {cxf.file_information.creator}")
    print(f"Description: {cxf.file_information.description}")

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
