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


ns_args = {
    "nsmap": {
    "": "http://colorexchangeformat.com/CxF3-core",
}
}

class Tag(BaseXmlModel, tag="Tag", **ns_args):
    name: str = attr(name="Name")
    value: str = attr(name="Value")

class FileInformation(BaseXmlModel, tag="FileInformation",  **ns_args):
    creator: str | None = element(tag="Creator", default=None)
    creation_date : dt.date | None = element(tag="CreationDate", default=None)
    description: str | None = element(tag="Description", default=None)
    tags: list[Tag] | None = element(default=[])

class CustomResources(BaseXmlModel):
    pass

class ColorSRGB(BaseXmlModel, tag="ColorSRGB", **ns_args):
    r: float = element(tag="R")
    g: float = element(tag="G")
    b: float = element(tag="B")
    name: str | None = element(tag="Name", default=None)
    color_specification: str | None = element(tag="ColorSpecification", default=None)

class ColorCIELab(BaseXmlModel, tag="ColorCIELab", **ns_args):
    l: float = element(tag="L")
    a: float = element(tag="A")
    b: float = element(tag="B")
    name: str | None = element(tag="Name", default=None)
    color_specification: str | None = element(tag="ColorSpecification", default=None)

class ReflectanceSpectrum(BaseXmlModel, tag="ReflectanceSpectrum", **ns_args):
    value: str | None = element(tag="Value", default=None)
    name: str | None = element(tag="Name", default=None)
    measureDate: dt.date | None = element(tag="MeasureDate", default=None)
    start_wl: str | None = element(tag="StartWL", default=None)
    color_specification: str | None = element(tag="ColorSpecification", default=None)


class TransmittanceSpectrum(BaseXmlModel, tag="TransmittanceSpectrum", **ns_args):
    value: str | None = element(tag="Value", default=None)
    name: str | None = element(tag="Name", default=None)
    measureDate: dt.date | None = element(tag="MeasureDate", default=None)
    start_wl: str | None = element(tag="StartWL", default=None)
    color_specification: str | None = element(tag="ColorSpecification", default=None)



class ColorValues(BaseXmlModel, tag="ColorValues",  **ns_args):
    root: list[ColorCIELab | ColorSRGB| ReflectanceSpectrum] = element()




class DeltaCIELab(BaseXmlModel, tag="DeltaCIELab", **ns_args):
    dL: float | None = element(name="dL")
    dA: float | None = element(name="dA")
    dB: float | None = element(name="dB")
    dC: float | None = element(name="dC")
    dH: float | None = element(name="dH")
    dE: float | None = element(name="dE")
    dEcmc: DEcmcType | None = element(name="dEcmc")
    dE94: DE94Type | None = element(name="dE94")
    dE2000: DE2000Type | None = element(name="dE2000")

    name: str = attr(name="Name", default=None)
    color_specification: str = attr(name="ColorSpecification")
    standard_ref: str = attr(name="StandardRef")

class ColorDifferenceValues(BaseXmlModel, tag="ColorDifferenceValues", **ns_args):
    pass

class TagCollection(BaseXmlModel, tag="TagCollection", **ns_args):
    pass

class TargetType(str, Enum):
    IT8_7_1 = "IT8.7/1"
    IT8_7_2 = "IT8.7/2"
    IT8_7_3 = "IT8.7/3"
    IT8_7_4 = "IT8.7/4"
    ECI2002 = "ECI2002"
    OTHER = "Other"

class FinishType(str, Enum):
    COATED = "Cated"
    UNCOATED = "Uncoated"
    MATTE = "Matte"
    POLISHED = "Polished"
    GLOSSY = "Glossy"
    SATIN = "Satin"
    OTHER = "Other"

"""
            <xs:enumeration value="Film"/>
            <xs:enumeration value="Leather"/>
            <xs:enumeration value="Metal"/>
            <xs:enumeration value="Paint"/>
            <xs:enumeration value="Paper"/>
            <xs:enumeration value="Plastic"/>
            <xs:enumeration value="Textile"/>
            <xs:enumeration value="Tile"/>
            <xs:enumeration value="Vinyl"/>
            <xs:enumeration value="Wood"/>
            <xs:enumeration value="Other"/>"""

class SubstrateType(str, Enum):
    FILM = "Film"
    LEATHER = "Leather"
    METAL = "Metal"
    PAINT = "Paint"
    PAPER = "Paper"
    PLASTIC = "Plastic"
    TEXTILE = "Textile"
    TILE = "Tile"
    VINYL = "Vinyl"
    WOOD = "Wood"
    OTHER = "Other"

class Quantity(BaseXmlModel, tag="Quantity", **ns_args):
    value: float
    unit: str | None = attr(name="Unit", default=None)

class Height(BaseXmlModel, tag="Height", **ns_args):
    value: float
    unit: str | None = attr(name="Unit", default=None)

class Width(BaseXmlModel, tag="Width", **ns_args):
    value: float
    unit: str | None = attr(name="Unit", default=None)

class Length(BaseXmlModel, tag="Length", **ns_args):
    value: float
    unit: str | None = attr(name="Unit", default=None)

class Thickness(BaseXmlModel, tag="Thickness", **ns_args):
    value: float
    unit: str | None = attr(name="Unit", default=None)

class Gloss(BaseXmlModel, tag="Gloss", **ns_args):
    value: float
    method: str | None = attr(name="Method", default=None)

class Opacity(BaseXmlModel, tag="Opacity", **ns_args):
    value: float
    method: str | None = attr(name="Method", default=None)

class CustomAttributeString(BaseXmlModel, tag="CustomAttributeString", **ns_args):
    label: str = attr(name="Label", default=None)
    method: str = attr(name="Method", default=None)


class CustomAttributeValue(BaseXmlModel, tag="CustomAttributeValue", **ns_args):
    label: str = attr(name="Label", default=None)
    method: str = attr(name="Method", default=None)

class Image(BaseXmlModel, tag="Image", **ns_args):
    content: str



class PhysicalAttributes(BaseXmlModel, tag="PhysicalAttributes", **ns_args):
    targetType: TargetType | None = element(default=None)
    finishType: FinishType | None = element(None)
    substrateType: SubstrateType | None = element(default=None)
    quantity: Quantity | None = element(default=None)
    height: Height | None = element(default=None)
    width:  Width | None = element(default=None)
    length:  Length | None = element(default=None)
    thickness: Thickness | None = element(default=None)
    gloss: Gloss | None = element(default=None)
    opacity: Opacity | None = element(default=None)
    customAttributeString: CustomAttributeString | None = element(default=None    )
    customAttributeValue: CustomAttributeValue = element( default=None    )
    image: Image | None = element(default=None)


class Object(BaseXmlModel, tag="Object", **ns_args):
    object_type: str = attr(name="ObjectType")
    name : str  = attr(name="Name")
    id : str  = attr(name="Id")
    guid : str | None = attr(name="GUID", default=None)

    creation_date : dt.date  = element(tag="CreationDate")
    comment: str | None = element(tag="Comment", default=None)
    color_values : ColorValues | None = element(default=None)
    color_difference_values : ColorDifferenceValues | None = element(default=None)
    tag_collection: TagCollection | None = element(default=[])
    physical_attributes: PhysicalAttributes | None = element(default=None)

class ObjectCollection(BaseXmlModel, tag="ObjectCollection", **ns_args):
    objects: list[Object] = element(default=[])


class TristimulusSpec(BaseXmlModel):
    illuminant: str | None = element(tag="cc:Illuminant")
    custom_illuminant: str | None = element(tag="cc:CustomIlluminant")
    observer: str | None = element(tag="cc:Observer")
    method: str | None = element(tag="cc:Method")

class MeasurementSpec(BaseXmlModel):
    measurement_type: str = element(name="MeasurementType")
    geometry_choice : str = element(name="GeometryChoice")
    wavelength_range : str | None = element(name="WavelengthRange")
    luminance_units_type : str | None = element(name="LuminanceUnitsType")
    calibration_standard: str | None = element(name="CalibrationStandard")
    device: str | None = element(name="Device")


class PhysicalAttributes(BaseXmlModel):
    target_type: str | None = element(name="TargetType")
    finish_type : str | None = element(name="FinishType")
    substrate_type: str | None = element(name="SubstrateType")
    quantity: str | None = element(name="Quantity")
    width: str | None = element(name="Width")
    length: str | None = element(name="Length")
    height: str | None = element(name="Height")
    thickness: str | None = element(name="Thickness")
    gloss: str | None = element(name="Gloss")
    opacity: str | None = element(name="Opacity")
    custom_attribute_string : str | None = element(name="CustomAttributeString")
    custom_attribute_value: str | None = element(name="CustomAttributeValue")
    image: str | None = element(name="Image")

class ColorSpecification(BaseXmlModel):
    id: int | None = attr(name="Id")

    tristimulus_spec: TristimulusSpec | None = element(name="TristimulusSpec")
    measurement_spec: MeasurementSpec | None = element(name="MeasurementSpec")
    physical_attributes: PhysicalAttributes | None = element(name="PhysicalAttributes")

class ColorSpecificationCollection(BaseXmlModel):
    objects: list[ColorSpecification] = element(tag="cc:ColorSpecification", default=[])


class ProfileDirection(Enum):
    input = "Input"
    output = "Output"
    both = "Both"


class ProfileChoice(BaseXmlModel):
    profile_file: str | None = attr(name="ProfileFile")
    profile_uri: str | None = attr(name="ProfileUri")

class ProfileParameter(BaseXmlModel):
    name: str = attr(name="Name")
    value_choice: str = attr(name="ValueChoice")

class Profile(BaseXmlModel):
    id: int = attr(name="Id")
    direction: ProfileDirection = element(name="Direction")

    profile_choice: ProfileChoice | None = element(name="ProfileChoice")
    parameters: list[ProfileParameter] | None = element(name="Parameters", default=[])
    created: str | None = element(name="Created")


class ProfileCollection(BaseXmlModel):
    profiles: list[Profile] = element(tag="cc:Profile", default=[])


class Resources(BaseXmlModel, tag="Resources", **ns_args):
    object_collection: ObjectCollection | None = element(default=None)
    color_specification_collection: ColorSpecificationCollection | None = element(tag="ColorSpecificationCollection", default=None)
    profile_collection: ProfileCollection | None = element(tag="ProfileCollection", default=None)

class CxF(BaseXmlModel, **ns_args):
    file_information: FileInformation | None = element(default=None)
    resources: Resources | None = element(default=None)
    # custom_resources: CustomResources | None


if __name__ == "__main__":
    with open("./tests/resources/sample.cxf", "rb") as in_file:
        input_string = in_file.read()
        cxf = CxF.from_xml(input_string)
        pprint.pprint(cxf)

