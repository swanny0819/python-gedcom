import unittest

from gedcom.element.individual import IndividualElement
from gedcom.element.root import RootElement
from gedcom.parser import Parser


class TestParser(unittest.TestCase):
    def test_invalidate_cache(self):
        parser = Parser()
        parser.parse_file('../tests/files/Musterstammbaum.ged')

        self.assertEqual(32, len(parser.get_element_dictionary()))
        self.assertEqual(396, len(parser.get_element_list()))

        parser.invalidate_cache()

        self.assertEqual(32, len(parser.get_element_dictionary()))
        self.assertEqual(396, len(parser.get_element_list()))

    def test_get_root_element(self):
        parser = Parser()
        self.assertTrue(isinstance(parser.get_root_element(), RootElement))

    def test_parse_file(self):
        parser = Parser()
        self.assertEqual(0, len(parser.get_root_child_elements()))

        parser.parse_file('../tests/files/Musterstammbaum.ged')

        self.assertEqual(34, len(parser.get_root_child_elements()))

        individuals_in_root_child_elements = 0
        individuals_in_element_list = 0

        for element in parser.get_root_child_elements():
            if isinstance(element, IndividualElement):
                individuals_in_root_child_elements += 1

        for element in parser.get_element_list():
            if isinstance(element, IndividualElement):
                individuals_in_element_list += 1

        self.assertEqual(20, individuals_in_root_child_elements)
        self.assertEqual(20, individuals_in_element_list)

    def test_parse_from_string(self):
        case_1 = """0 @I5@ INDI
1 NAME First /Last/
1 SEX M
1 BIRT
2 DATE 1 JAN 1900
2 PLAC Kirkland, King, Washington, USA
3 MAP
4 LATI N47.680663
4 LONG W122.234319
"""
        gedcom_parser = Parser()
        gedcom_parser.parse([(a + '\n').encode('utf-8-sig') for a in case_1.splitlines()])
        element_1 = gedcom_parser.get_root_child_elements()[0]
        self.assertTrue(isinstance(element_1, IndividualElement))
        self.assertEqual('INDI', element_1.get_tag())
        self.assertEqual('@I5@', element_1.get_pointer())
        element_1_children = element_1.get_child_elements()
        self.assertEqual(3, len(element_1_children))
        self.assertEqual('NAME', element_1_children[0].get_tag())
        self.assertEqual('SEX', element_1_children[1].get_tag())
        self.assertEqual('BIRT', element_1_children[2].get_tag())

        case_2 = """0 @F28@ FAM
1 HUSB @I80@
1 WIFE @I81@
1 CHIL @I9@
2 _FREL Natural
2 _MREL Natural
1 CHIL @I84@
2 _FREL Natural
2 _MREL Natural
1 CHIL @I85@
2 _FREL Natural
2 _MREL Natural
"""
        gedcom_parser.parse([(a + '\n').encode('utf-8-sig') for a in case_2.splitlines()])
        element_2 = gedcom_parser.get_root_child_elements()[0]
        self.assertEqual('FAM', element_2.get_tag())
        self.assertEqual('@F28@', element_2.get_pointer())
        element_2_children = element_2.get_child_elements()
        self.assertEqual(5, len(element_2_children))
        self.assertEqual('HUSB', element_2_children[0].get_tag())
        self.assertEqual('WIFE', element_2_children[1].get_tag())
        self.assertEqual('CHIL', element_2_children[2].get_tag())
        self.assertEqual('@I84@', element_2_children[3].get_value())
