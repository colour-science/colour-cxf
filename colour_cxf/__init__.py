__author__ = "Colour Developers"
__copyright__ = "Copyright 2024 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__application_name__ = "Colour - CxF"

__major_version__ = "0"
__minor_version__ = "1"
__change_version__ = "1"
__version__ = f"{__major_version__}.{__minor_version__}.{__change_version__}"


__all__ = [
    "cxf3",
    "read_cxf_from_file",
    "read_cxf",
    "write_cxf",
]

from io import BytesIO
from os import PathLike

from lxml import etree
from xsdata.exceptions import ParserError
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer

import colour_cxf.cxf3


def read_cxf_from_file(
    source_path: str | PathLike[str], validate_schema: bool = True
) -> colour_cxf.cxf3.CxF:
    """
    Read a CxF file from a file path.

    Parameters
    ----------
    source_path : str or PathLike[str]
        Path to the CxF file to read.
    validate_schema : bool, optional
        Whether to validate the schema before parsing the file.

    Returns
    -------
    colour_cxf.cxf3.CxF
        CxF object containing the parsed data.

    Raises
    ------
    ParserError
        If the CxF document does not match the CxF schema.

    Examples
    --------
    >>> import colour_cxf
    >>> cxf = colour_cxf.read_cxf_from_file("path/to/file.cxf")  # doctest: +SKIP
    """
    with open(source_path, "rb") as file:
        doc = file.read()

        if validate_schema:
            _validate_schema(doc)

        return read_cxf(doc)


def _validate_schema(doc: bytes) -> None:
    """
    Validate the CxF document against the XSD schema.

    Parameters
    ----------
    doc : bytes
        Bytes data containing the CxF XML content.


    Raises
    ------
    ParserError
        If the CxF document does not match the CxF schema.
    """
    try:
        parsed_xml = etree.parse(BytesIO(doc))
    except etree.XMLSyntaxError as e:
        msg = f"XML is not well-formed: {e}"
        raise ParserError(msg) from e

    try:
        with open("CxF3_Core.xsd") as schema_file:
            xmlschema_doc = etree.parse(schema_file)
            xmlschema = etree.XMLSchema(xmlschema_doc)

            if not xmlschema.validate(parsed_xml):
                errors = xmlschema.error_log
                msg = f"Schema validation failed: {errors}"
                raise ParserError(msg)
    except (etree.XMLSyntaxError, etree.XSLTParseError) as e:
        msg = f"Schema validation error: {e}"
        raise ParserError(msg) from e


def read_cxf(doc: bytes, validate_schema: bool = True) -> colour_cxf.cxf3.CxF:
    """
    Read a CxF object from bytes data.

    Parameters
    ----------
    doc : bytes
        Bytes data containing the CxF XML content.
    validate_schema : bool, optional
        Whether to validate the schema before parsing the file.

    Returns
    -------
    colour_cxf.cxf3.CxF
        CxF object containing the parsed data.

    Raises
    ------
    ParserError
        If the CxF document does not match the CxF schema.

    Examples
    --------
    >>> import colour_cxf
    >>> with open("path/to/file.cxf", "rb") as f:  # doctest: +SKIP
    ...     data = f.read()
    >>> cxf = colour_cxf.read_cxf(data)  # doctest: +SKIP
    """

    if validate_schema:
        _validate_schema(doc)

    context = XmlContext()
    parser = XmlParser(context=context)
    return parser.from_bytes(doc, colour_cxf.cxf3.CxF)


def write_cxf(cxf: colour_cxf.cxf3.CxF) -> bytes:
    """
    Write a CxF object to bytes.

    Parameters
    ----------
    cxf : colour_cxf.cxf3.CxF
        CxF object to serialize.

    Returns
    -------
    bytes
        UTF-8 encoded XML bytes representing the CxF object.

    Examples
    --------
    >>> import colour_cxf
    >>> cxf = colour_cxf.read_cxf_from_file("path/to/file.cxf")  # doctest: +SKIP
    >>> # Modify cxf object...
    >>> xml_bytes = colour_cxf.write_cxf(cxf)  # doctest: +SKIP
    >>> with open("path/to/output.cxf", "wb") as f:  # doctest: +SKIP
    ...     f.write(xml_bytes)
    """
    serializer = XmlSerializer()
    return serializer.render(cxf).encode("utf-8")
