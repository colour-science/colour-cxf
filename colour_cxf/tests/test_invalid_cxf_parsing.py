"""
CxF Invalid Document Parsing Tests
==================================

This module defines tests for parsing invalid CxF documents to ensure
proper error detection and handling of:
- Structurally invalid documents (wrong, missing or invalid tags)
- Documents with invalid values (invalid enums, out-of-range values)
"""

import unittest

from lxml_asserts.testcase import LxmlTestCaseMixin
from xsdata.exceptions import ParserError

from colour_cxf import read_cxf


class InvalidCxfParsing(unittest.TestCase, LxmlTestCaseMixin):
    """
    Test parsing of invalid CxF documents to verify error detection.
    """

    def test_malformed_xml_structure(self) -> None:
        """Test that malformed XML structure is properly detected."""

        # Test unclosed tag
        unclosed_tag_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:Resources>
        <cc:ObjectCollection>
            <cc:Object ObjectType="Target" Name="Test" Id="1">
        </cc:ObjectCollection>
    </cc:Resources>
</cc:CxF>"""

        with self.assertRaises(ParserError):
            read_cxf(unclosed_tag_xml)

    def test_invalid_root_element(self) -> None:
        """Test that invalid root element is detected."""

        invalid_root_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:InvalidRoot xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:Resources>
    </cc:Resources>
</cc:InvalidRoot>"""

        with self.assertRaises(ParserError):
            read_cxf(invalid_root_xml)

    def test_missing_namespace(self) -> None:
        """Test that missing namespace declaration is detected."""

        missing_namespace_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<CxF>
    <Resources>
    </Resources>
</CxF>"""

        with self.assertRaises(ParserError):
            read_cxf(missing_namespace_xml)

    def test_wrong_namespace(self) -> None:
        """Test that wrong namespace is detected."""

        wrong_namespace_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://wrong-namespace.com/CxF3-core">
    <cc:Resources>
    </cc:Resources>
</cc:CxF>"""

        with self.assertRaises(ParserError):
            read_cxf(wrong_namespace_xml)

    def test_invalid_element_structure(self) -> None:
        """Test that invalid element structure is detected."""

        # Resources placed before FileInformation (wrong order according to schema)
        wrong_order_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:Resources>
    </cc:Resources>
    <cc:FileInformation>
        <cc:Creator>Test</cc:Creator>
    </cc:FileInformation>
</cc:CxF>"""

        with self.assertRaises(ParserError):
            read_cxf(wrong_order_xml)

    def test_unknown_elements(self) -> None:
        """Test that unknown elements are detected."""

        unknown_element_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:Resources>
        <cc:UnknownElement>Invalid</cc:UnknownElement>
    </cc:Resources>
</cc:CxF>"""

        with self.assertRaises(ParserError):
            read_cxf(unknown_element_xml)

    def test_missing_required_attributes(self) -> None:
        """Test that missing required attributes are detected."""

        # Object without required Id attribute
        missing_id_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:Resources>
        <cc:ObjectCollection>
            <cc:Object ObjectType="Target" Name="Test">
                <cc:ColorValues>
                </cc:ColorValues>
            </cc:Object>
        </cc:ObjectCollection>
    </cc:Resources>
</cc:CxF>"""

        with self.assertRaises(ParserError):
            read_cxf(missing_id_xml)

    def test_invalid_astm_table_enum(self) -> None:
        """Test that invalid ASTM table enumeration values are detected."""

        invalid_astm_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:Resources>
        <cc:ColorSpecificationCollection>
            <cc:ColorSpecification Id="spec1">
                <cc:TristimulusSpec>
                    <cc:Illuminant>D65</cc:Illuminant>
                    <cc:Observer>10</cc:Observer>
                    <cc:AstmTable>InvalidTable</cc:AstmTable>
                </cc:TristimulusSpec>
            </cc:ColorSpecification>
        </cc:ColorSpecificationCollection>
    </cc:Resources>
</cc:CxF>"""

        with self.assertRaises(ParserError):
            read_cxf(invalid_astm_xml)

    def test_invalid_sphere_type_enum(self) -> None:
        """Test that invalid sphere type enumeration values are detected."""

        invalid_sphere_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:Resources>
        <cc:ObjectCollection>
            <cc:Object ObjectType="Target" Name="Test" Id="1">
                <cc:ColorValues>
                    <cc:ReflectanceSpectrum>
                        <cc:MeasurementSpec>
                            <cc:SphereType>InvalidSphere</cc:SphereType>
                        </cc:MeasurementSpec>
                    </cc:ReflectanceSpectrum>
                </cc:ColorValues>
            </cc:Object>
        </cc:ObjectCollection>
    </cc:Resources>
</cc:CxF>"""

        with self.assertRaises(ParserError):
            read_cxf(invalid_sphere_xml)

    def test_invalid_device_class_enum(self) -> None:
        """Test that invalid device class enumeration values are detected."""

        invalid_device_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:Resources>
        <cc:ObjectCollection>
            <cc:Object ObjectType="Target" Name="Test" Id="1">
                <cc:DeviceColorValues>
                    <cc:ColorCMYK>
                        <cc:C>50.0</cc:C>
                        <cc:M>25.0</cc:M>
                        <cc:Y>75.0</cc:Y>
                        <cc:K>10.0</cc:K>
                        <cc:DeviceClass>InvalidDevice</cc:DeviceClass>
                    </cc:ColorCMYK>
                </cc:DeviceColorValues>
            </cc:Object>
        </cc:ObjectCollection>
    </cc:Resources>
</cc:CxF>"""

        with self.assertRaises(ParserError):
            read_cxf(invalid_device_xml)

    def test_out_of_range_rgb_values(self) -> None:
        """Test that RGB values outside valid range are detected."""

        invalid_rgb_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:Resources>
        <cc:ObjectCollection>
            <cc:Object ObjectType="Target" Name="Test" Id="1">
                <cc:ColorValues>
                    <cc:ColorSRGB>
                        <cc:R>300</cc:R>
                        <cc:G>128</cc:G>
                        <cc:B>-50</cc:B>
                    </cc:ColorSRGB>
                </cc:ColorValues>
            </cc:Object>
        </cc:ObjectCollection>
    </cc:Resources>
</cc:CxF>"""

        with self.assertRaises(ParserError):
            read_cxf(invalid_rgb_xml)

    def test_out_of_range_cmyk_values(self) -> None:
        """Test that CMYK values outside valid range are detected."""

        invalid_cmyk_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:Resources>
        <cc:ObjectCollection>
            <cc:Object ObjectType="Target" Name="Test" Id="1">
                <cc:DeviceColorValues>
                    <cc:ColorCMYK>
                        <cc:C>150.0</cc:C>
                        <cc:M>25.0</cc:M>
                        <cc:Y>75.0</cc:Y>
                        <cc:K>-10.0</cc:K>
                    </cc:ColorCMYK>
                </cc:DeviceColorValues>
            </cc:Object>
        </cc:ObjectCollection>
    </cc:Resources>
</cc:CxF>"""

        with self.assertRaises(ParserError):
            read_cxf(invalid_cmyk_xml)

    def test_invalid_datetime_format(self) -> None:
        """Test that invalid datetime format is detected."""

        invalid_datetime_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:FileInformation>
        <cc:CreationDate>not-a-valid-datetime</cc:CreationDate>
    </cc:FileInformation>
</cc:CxF>"""

        with self.assertRaises(ParserError):
            read_cxf(invalid_datetime_xml)

    def test_duplicate_object_ids(self) -> None:
        """Test that duplicate object IDs are detected."""

        duplicate_id_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:Resources>
        <cc:ObjectCollection>
            <cc:Object ObjectType="Target" Name="Test1" Id="duplicate">
                <cc:ColorValues>
                </cc:ColorValues>
            </cc:Object>
            <cc:Object ObjectType="Target" Name="Test2" Id="duplicate">
                <cc:ColorValues>
                </cc:ColorValues>
            </cc:Object>
        </cc:ObjectCollection>
    </cc:Resources>
</cc:CxF>"""

        with self.assertRaises(ParserError):
            read_cxf(duplicate_id_xml)

    def test_invalid_color_specification_reference(self) -> None:
        """Test that invalid ColorSpecification references are detected."""

        invalid_ref_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:Resources>
        <cc:ObjectCollection>
            <cc:Object ObjectType="Target" Name="Test" Id="1">
                <cc:ColorValues>
                    <cc:ColorCIELab ColorSpecification="NonExistentSpec">
                        <cc:L>50.0</cc:L>
                        <cc:A>10.0</cc:A>
                        <cc:B>-5.0</cc:B>
                    </cc:ColorCIELab>
                </cc:ColorValues>
            </cc:Object>
        </cc:ObjectCollection>
        <cc:ColorSpecificationCollection>
            <cc:ColorSpecification Id="ExistingSpec">
                <cc:TristimulusSpec>
                    <cc:Illuminant>D65</cc:Illuminant>
                    <cc:Observer>2</cc:Observer>
                </cc:TristimulusSpec>
            </cc:ColorSpecification>
        </cc:ColorSpecificationCollection>
    </cc:Resources>
</cc:CxF>"""

        with self.assertRaises(ParserError):
            read_cxf(invalid_ref_xml)

    def test_invalid_spectral_wavelength_range(self) -> None:
        """Test that invalid spectral wavelength ranges are detected."""

        invalid_spectrum_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:Resources>
        <cc:ObjectCollection>
            <cc:Object ObjectType="Target" Name="Test" Id="1">
                <cc:ColorValues>
                    <cc:ReflectanceSpectrum StartWL="-100" EndWL="50000" Increment="10">
                        <cc:Value>0.5 0.6 0.7</cc:Value>
                    </cc:ReflectanceSpectrum>
                </cc:ColorValues>
            </cc:Object>
        </cc:ObjectCollection>
    </cc:Resources>
</cc:CxF>"""

        with self.assertRaises(ParserError):
            read_cxf(invalid_spectrum_xml)

    def test_negative_spectral_increment(self) -> None:
        """Test that negative spectral increment is detected."""

        negative_increment_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:Resources>
        <cc:ObjectCollection>
            <cc:Object ObjectType="Target" Name="Test" Id="1">
                <cc:ColorValues>
                    <cc:ReflectanceSpectrum StartWL="400" EndWL="700" Increment="-10">
                        <cc:Value>0.5 0.6 0.7</cc:Value>
                    </cc:ReflectanceSpectrum>
                </cc:ColorValues>
            </cc:Object>
        </cc:ObjectCollection>
    </cc:Resources>
</cc:CxF>"""

        with self.assertRaises(ParserError):
            read_cxf(negative_increment_xml)

    def test_invalid_xml_encoding(self) -> None:
        """Test that invalid XML encoding is detected."""

        # Invalid characters in XML
        invalid_encoding_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:FileInformation>
        <cc:Creator>\x00InvalidChar</cc:Creator>
    </cc:FileInformation>
</cc:CxF>"""

        with self.assertRaises(ParserError):
            read_cxf(invalid_encoding_xml)

    def test_empty_required_fields(self) -> None:
        """Test that empty required fields are detected."""

        empty_name_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">
    <cc:Resources>
        <cc:ObjectCollection>
            <cc:Object ObjectType="Target" Name="" Id="1">
                <cc:ColorValues>
                </cc:ColorValues>
            </cc:Object>
        </cc:ObjectCollection>
    </cc:Resources>
</cc:CxF>"""

        with self.assertRaises(ParserError):
            read_cxf(empty_name_xml)


if __name__ == "__main__":
    unittest.main()
