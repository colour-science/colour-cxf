import pprint
from enum import Enum
from typing import List
import datetime as dt
from pydantic_xml import BaseXmlModel, element, attr

__author__ = "Colour Developers"
__copyright__ = "Copyright 2024 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__application_name__ = "Colour - CxF"

__major_version__ = "0"
__minor_version__ = "1"
__change_version__ = "0"
__version__ = f"{__major_version__}.{__minor_version__}.{__change_version__}"

from xsdata.formats.dataclass.serializers import XmlSerializer

from .generated.com.colorexchangeformat import *

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.context import XmlContext

from .generated.com.colorexchangeformat.cx_f3_core.cx_f import CxF


def read_cxf(source_path) -> CxF:
    context = XmlContext()
    parser = XmlParser(context=context)
    return parser.from_bytes(source_path, CxF)

def write_cxf(cxf):
    serializer = XmlSerializer()
    return serializer.render(cxf).encode("utf-8")
