import pprint
import unittest

from colour_cxf import *
from lxml_asserts.testcase import LxmlTestCaseMixin

class MyTestCase(unittest.TestCase, LxmlTestCaseMixin):
    def test_something(self):
        with open("./resources/sample.cxf", "rb") as in_file:
            import lxml.etree

            input_string = in_file.read()
            tree_input = lxml.etree.fromstring(input_string)
            cxf = read_cxf(input_string)
            tree_roundtrip = lxml.etree.fromstring(write_cxf(cxf))

            self.assertXmlEqual(tree_input, tree_roundtrip, check_tags_order=True)

if __name__ == "__main__":
    unittest.main()
