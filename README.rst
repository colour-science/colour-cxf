==========
Colour CxF
==========

A Python library for reading, manipulating, and writing Color Exchange Format (CxF) files.

About
=====

Colour CxF provides tools for working with CxF files, which are XML-based files used for exchanging color information between different applications and devices. The library allows you to:

- Read CxF files from strings or files
- Access and manipulate color data in various formats (RGB, CIELab, spectral)
- Create CxF objects programmatically
- Write CxF objects to XML strings

Installation
============

Primary Dependencies
~~~~~~~~~~~~~~~~~~~~

**Colour - CxF** requires some dependencies in order to run:

- `python >= 3.10, < 3.14 <https://www.python.org/download/releases>`__
- `typing-extensions >= 4, < 5 <https://pypi.org/project/typing-extensions>`__
- `xsdata > 25.4 <https://pypi.org/project/xsdata>`__

Pypi
~~~~

Once the dependencies are satisfied, **Colour - CxF** can be installed from
the `Python Package Index <http://pypi.python.org/pypi/colour-cxf>`__ by
issuing this command in a shell::

    pip install --user colour-cxf

The overall development dependencies are installed as follows::

    pip install --user 'colour-cxf[development]'

UV
~~

Using uv you can simply install **Colour - CxF** via::

    uv add colour-cxf

Quick Start
===========

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

Documentation
=============

For more detailed information and examples, see the `tutorial <docs/tutorial.rst>`_.

License
=======

Colour CxF is licensed under the BSD-3-Clause license.
