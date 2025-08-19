"""
CxF Sample File Tests
====================

This module defines tests specific to the sample.cxf file.
These tests verify specific properties and content of the sample file
beyond generic parsing functionality.
"""

import unittest

from lxml_asserts.testcase import LxmlTestCaseMixin

import colour_cxf.cxf3
from colour_cxf import read_cxf_from_file


class SampleCxfTests(unittest.TestCase, LxmlTestCaseMixin):
    """
    Define test methods specific to the sample.cxf file using the functionality
    provided in the :mod:`colour_cxf` module.
    """

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.sample_file_path = "colour_cxf/tests/resources/sample.cxf"

    def test_sample_file_structure(self) -> None:
        """Test that the sample.cxf file has expected structure and content."""
        cxf = read_cxf_from_file(self.sample_file_path)

        # Verify basic structure
        self.assertIsInstance(cxf, colour_cxf.cxf3.CxF)
        self.assertIsNotNone(cxf.file_information)
        self.assertIsNotNone(cxf.resources)

        # Check FileInformation content
        file_info = cxf.file_information
        assert file_info is not None
        self.assertEqual(file_info.creator, "X-Rite, Inc.")
        self.assertIsNotNone(file_info.creation_date)
        self.assertIsNotNone(file_info.description)
        assert file_info.description is not None
        self.assertIn("ColorPort Custom Target", file_info.description)

        # Check Resources structure
        resources = cxf.resources
        assert resources is not None
        self.assertIsNotNone(resources.object_collection)
        self.assertIsNotNone(resources.color_specification_collection)

    def test_sample_file_objects(self) -> None:
        """Test that the sample.cxf file contains expected objects."""
        cxf = read_cxf_from_file(self.sample_file_path)

        resources = cxf.resources
        assert resources is not None
        assert resources.object_collection is not None
        objects = resources.object_collection.object_value
        self.assertGreater(len(objects), 0, "Sample file should contain objects")

        # Check first object properties
        first_obj = objects[0]
        self.assertEqual(first_obj.object_type, "Target")
        self.assertEqual(first_obj.name, "1")
        self.assertEqual(first_obj.id, "1")
        self.assertIsNotNone(first_obj.creation_date)

        # Check that objects have color values
        self.assertIsNotNone(first_obj.color_values)

    def test_sample_file_color_specifications(self) -> None:
        """Test that the sample.cxf file contains expected color specifications."""
        cxf = read_cxf_from_file(self.sample_file_path)

        resources = cxf.resources
        assert resources is not None
        assert resources.color_specification_collection is not None
        color_specs = resources.color_specification_collection.color_specification
        self.assertGreater(
            len(color_specs), 0, "Sample file should contain color specifications"
        )

        # Check first color specification
        first_spec = color_specs[0]
        self.assertEqual(first_spec.id, "CS1")
        self.assertIsNotNone(first_spec.tristimulus_spec)
        self.assertIsNotNone(first_spec.measurement_spec)

    def test_sample_file_spectral_data(self) -> None:
        """Test that the sample.cxf file contains spectral data."""
        cxf = read_cxf_from_file(self.sample_file_path)

        # Find an object with spectral data
        resources = cxf.resources
        assert resources is not None
        assert resources.object_collection is not None
        objects = resources.object_collection.object_value
        spectral_found = False

        for obj in objects:
            if obj.color_values:
                from colour_cxf.cxf3.reflectance_spectrum import ReflectanceSpectrum

                for color_value in obj.color_values.choice:
                    if isinstance(color_value, ReflectanceSpectrum):
                        spectral_found = True
                        self.assertIsNotNone(color_value.start_wl)
                        self.assertIsNotNone(color_value.color_specification)
                        break
                if spectral_found:
                    break

        self.assertTrue(spectral_found, "Sample file should contain spectral data")

    def test_sample_file_color_values(self) -> None:
        """Test that the sample.cxf file contains various color values."""
        cxf = read_cxf_from_file(self.sample_file_path)

        resources = cxf.resources
        assert resources is not None
        assert resources.object_collection is not None
        objects = resources.object_collection.object_value

        # Check for CIELab values
        cielab_found = False
        srgb_found = False

        for obj in objects:
            if obj.color_values:
                from colour_cxf.cxf3.color_cielab import ColorCielab
                from colour_cxf.cxf3.color_srgb import ColorSrgb

                for color_value in obj.color_values.choice:
                    if isinstance(color_value, ColorCielab):
                        cielab_found = True
                        self.assertIsNotNone(color_value.l)
                        self.assertIsNotNone(color_value.a)
                        self.assertIsNotNone(color_value.b)

                    if isinstance(color_value, ColorSrgb):
                        srgb_found = True
                        self.assertIsNotNone(color_value.r)
                        self.assertIsNotNone(color_value.g)
                        self.assertIsNotNone(color_value.b)

                if cielab_found and srgb_found:
                    break

        self.assertTrue(cielab_found, "Sample file should contain CIELab color values")
        self.assertTrue(srgb_found, "Sample file should contain sRGB color values")
