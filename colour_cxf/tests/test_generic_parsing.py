"""
CxF Generic Parsing Tests
=========================

This module defines generic tests that run over all CxF test documents.
These tests verify basic parsing functionality, roundtrip operations, and
performance across all test files without specific validation logic.
"""

import unittest
from pathlib import Path

from lxml_asserts.testcase import LxmlTestCaseMixin

import colour_cxf.cxf3
from colour_cxf import read_cxf, read_cxf_from_file, write_cxf


class GenericCxfParsing(unittest.TestCase, LxmlTestCaseMixin):
    """
    Define generic test methods that run over all CxF documents using the functionality
    provided in the :mod:`colour_cxf` module.
    """

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.resources_dir = Path(__file__).parent / "resources"

        # Collect all XML files for testing
        self.all_cxf_files = []

        # Sample files
        case_files = [
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
            "sample.cxf",
        ]

        # Combine all files for generic testing
        self.all_cxf_files = case_files

    def test_all_files_parsing_success(self) -> None:
        """Test that all CxF documents can be successfully parsed."""

        for filename in self.all_cxf_files:
            file_path = self.resources_dir / filename
            cxf = read_cxf_from_file(file_path)
            self.assertIsInstance(cxf, colour_cxf.cxf3.CxF)

    def test_all_files_roundtrip(self) -> None:
        """Test that all CxF documents can be parsed and written back."""
        for filename in self.all_cxf_files:
            file_path = self.resources_dir / filename

            with self.subTest(filename=filename):
                # Parse the file
                cxf = read_cxf_from_file(file_path)
                self.assertIsInstance(cxf, colour_cxf.cxf3.CxF)

                # Write it back and parse again
                xml_bytes = write_cxf(cxf)
                cxf_roundtrip = read_cxf(xml_bytes)
                self.assertEqual(cxf, cxf_roundtrip)

    def test_parsing_methods_consistency(self) -> None:
        """Test that read_cxf_from_file and read_cxf produce consistent results."""
        for filename in self.all_cxf_files:
            file_path = self.resources_dir / filename

            with self.subTest(filename=filename):
                # Test both parsing methods
                cxf_from_file = read_cxf_from_file(file_path)

                with open(file_path, "rb") as f:
                    cxf_from_bytes = read_cxf(f.read())

                # Verify both methods return the same data
                self.assertEqual(cxf_from_bytes, cxf_from_file)
