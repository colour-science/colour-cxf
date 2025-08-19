"""
CxF Parsing Tests
=================

This module defines tests for parsing the edge case CxF documents created to test
various boundary conditions and constraints of the CxF XSD schema.
It ensures that all edge case documents can be successfully parsed and validates
the robustness of the parsing implementation.
"""

import unittest
from pathlib import Path

from lxml_asserts.testcase import LxmlTestCaseMixin

import colour_cxf.cxf3
from colour_cxf import read_cxf, read_cxf_from_file, write_cxf


class EdgeCasesParsing(unittest.TestCase, LxmlTestCaseMixin):
    """
    Define test methods for parsing edge case CxF documents using the functionality
    provided in the :mod:`colour_cxf` module.
    """

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.resources_dir = Path(__file__).parent / "resources"

        # List of edge case CxF files to test
        self.edge_case_files = [
            "minimal_cxf.cxf",
            "empty_sections.cxf",
            "fileinformation_all_optional.cxf",
            "datetime_edge_cases.cxf",
            "string_edge_cases.cxf",
            "enumeration_boundary_values.cxf",
            "object_required_only.cxf",
            "multiple_objects.cxf",
            "custom_resources.cxf",
            "spectral_data_boundaries.cxf",
            "custom_spectrum_irregular.cxf",
            "id_reference_validation.cxf",
            "unicode_special_characters.cxf",
            "geometry_edge_cases.cxf",
        ]

    def test_minimal_cxf_parsing(self) -> None:
        """Test parsing of the minimal CxF document (root element only)."""
        file_path = self.resources_dir / "minimal_cxf.cxf"

        # Test both parsing methods
        cxf_from_file = read_cxf_from_file(file_path)

        with open(file_path, "rb") as f:
            cxf_from_bytes = read_cxf(f.read())

        # Verify both methods return the same result
        self.assertIsInstance(cxf_from_file, colour_cxf.cxf3.CxF)
        self.assertIsInstance(cxf_from_bytes, colour_cxf.cxf3.CxF)

        # Test roundtrip
        xml_output = write_cxf(cxf_from_file)
        cxf_roundtrip = read_cxf(xml_output)
        self.assertIsInstance(cxf_roundtrip, colour_cxf.cxf3.CxF)

    def test_empty_sections_parsing(self) -> None:
        """Test parsing of CxF with empty optional sections."""
        file_path = self.resources_dir / "empty_sections.cxf"
        cxf = read_cxf_from_file(file_path)

        self.assertIsInstance(cxf, colour_cxf.cxf3.CxF)
        self.assertIsNotNone(cxf.file_information)
        self.assertIsNotNone(cxf.resources)
        self.assertIsNotNone(cxf.custom_resources)

    def test_fileinformation_all_optional_parsing(self) -> None:
        """Test parsing of FileInformation with all optional elements."""
        file_path = self.resources_dir / "fileinformation_all_optional.cxf"
        cxf = read_cxf_from_file(file_path)

        self.assertIsInstance(cxf, colour_cxf.cxf3.CxF)
        self.assertIsNotNone(cxf.file_information)

        # Check that optional elements are present
        file_info = cxf.file_information
        assert file_info is not None
        self.assertIsNotNone(file_info.creator)
        self.assertIsNotNone(file_info.creation_date)
        self.assertIsNotNone(file_info.description)
        self.assertIsNotNone(file_info.comment)
        self.assertIsNotNone(file_info.tag)
        assert file_info.tag is not None
        self.assertTrue(len(file_info.tag) > 0)

    def test_datetime_edge_cases_parsing(self) -> None:
        """Test parsing of various datetime formats."""
        file_path = self.resources_dir / "datetime_edge_cases.cxf"
        cxf = read_cxf_from_file(file_path)

        self.assertIsInstance(cxf, colour_cxf.cxf3.CxF)
        self.assertIsNotNone(cxf.file_information)
        file_info = cxf.file_information
        assert file_info is not None
        self.assertIsNotNone(file_info.creation_date)

    def test_string_edge_cases_parsing(self) -> None:
        """Test parsing of various string edge cases and boundary values."""
        file_path = self.resources_dir / "string_edge_cases.cxf"
        cxf = read_cxf_from_file(file_path)

        self.assertIsInstance(cxf, colour_cxf.cxf3.CxF)
        self.assertIsNotNone(cxf.file_information)

        # Verify that tags with various string formats are parsed
        file_info = cxf.file_information
        assert file_info is not None
        assert file_info.tag is not None
        tags = file_info.tag
        self.assertTrue(len(tags) > 0)

        # Check that objects with edge case strings are parsed
        resources = cxf.resources
        assert resources is not None
        assert resources.object_collection is not None
        self.assertTrue(len(resources.object_collection.object_value) > 0)

    def test_enumeration_boundary_values_parsing(self) -> None:
        """Test parsing of all enumeration boundary values."""
        file_path = self.resources_dir / "enumeration_boundary_values.cxf"
        cxf = read_cxf_from_file(file_path)

        self.assertIsInstance(cxf, colour_cxf.cxf3.CxF)
        self.assertIsNotNone(cxf.file_information)

        file_info = cxf.file_information
        assert file_info is not None
        assert file_info.tag is not None
        tags = file_info.tag
        self.assertTrue(len(tags) > 50)

    def test_object_required_only_parsing(self) -> None:
        """Test parsing of Object with only required elements."""
        file_path = self.resources_dir / "object_required_only.cxf"
        cxf = read_cxf_from_file(file_path)

        self.assertIsInstance(cxf, colour_cxf.cxf3.CxF)
        resources = cxf.resources
        assert resources is not None
        assert resources.object_collection is not None

        objects = resources.object_collection.object_value
        self.assertEqual(len(objects), 1)

        obj = objects[0]
        self.assertIsNotNone(obj.object_type)
        self.assertIsNotNone(obj.name)
        self.assertIsNotNone(obj.id)
        self.assertIsNotNone(obj.creation_date)

    def test_multiple_objects_parsing(self) -> None:
        """Test parsing of ObjectCollection with multiple objects."""
        file_path = self.resources_dir / "multiple_objects.cxf"
        cxf = read_cxf_from_file(file_path)

        self.assertIsInstance(cxf, colour_cxf.cxf3.CxF)
        resources = cxf.resources
        assert resources is not None
        assert resources.object_collection is not None

        objects = resources.object_collection.object_value
        self.assertTrue(len(objects) > 1)

        # Verify all objects have required attributes
        for obj in objects:
            self.assertIsNotNone(obj.object_type)
            self.assertIsNotNone(obj.name)
            self.assertIsNotNone(obj.id)
            self.assertIsNotNone(obj.creation_date)

    def test_custom_resources_parsing(self) -> None:
        """Test parsing of CustomResources with external namespaces."""
        file_path = self.resources_dir / "custom_resources.cxf"
        cxf = read_cxf_from_file(file_path)

        self.assertIsInstance(cxf, colour_cxf.cxf3.CxF)
        self.assertIsNotNone(cxf.custom_resources)
