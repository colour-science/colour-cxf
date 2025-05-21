"""
CxF Roundtrip Tests
===================

This module defines tests for the roundtrip functionality of parsing and writing CxF
documents. It ensures that a CxF document can be read, converted to a Python object,
and then written back to XML without any loss of information.
"""

import unittest

from lxml_asserts.testcase import LxmlTestCaseMixin

from colour_cxf import read_cxf, write_cxf


class ParsingWriting(unittest.TestCase, LxmlTestCaseMixin):
    """
    Define tests methods for parsing/writing *CxF* documents using the functionality
    provided in the :mod: `colour_cxf` module.
    """

    def test_parsing_writing_roundtrip(self) -> None:
        """
        Test parsing/writing of the sample file `sample.cxf`.
        """
        with open("colour_cxf/tests/resources/sample.cxf", "rb") as in_file:
            import lxml.etree

            input_string = in_file.read()
            tree_input = lxml.etree.fromstring(input_string)
            cxf = read_cxf(input_string)
            tree_roundtrip = lxml.etree.fromstring(write_cxf(cxf))

            self.assertXmlEqual(tree_input, tree_roundtrip, check_tags_order=True)