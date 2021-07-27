import unittest

from python_gedcom_2.parser import Parser


class TestFamilyElement(unittest.TestCase):

    def test_has_children__a_family_without_children_has_no_children(self):
        use_case = """
            0 @F1@ FAM
                1 HUSB @I5@
                1 WIFE @I6@
        """
        family = self._parse_use_case_and_get_individual_element(use_case, "@F1@")
        self.assertFalse(family.has_children())

    def test_has_children__a_family_with_at_least_one_child_has_children(self):
        use_case = """
            0 @F1@ FAM
                1 HUSB @I5@
                1 WIFE @I6@
                1 CHIL @I3@
        """
        family = self._parse_use_case_and_get_individual_element(use_case, "@F1@")
        self.assertTrue(family.has_children())

    # ------------------------------ START OF HELPER METHODS -----------------------

    @staticmethod
    def _convert_gedcom_string_into_parsable_content(gedcom_file_contents_test_string):
        # Ignores whitespace "lines" at the start and end of the string - allows prettier presentation in the tests.
        # Ignores leading and trailing whitespace on each line - allows for indentation of lines to show clearer test strings.
        return [(a.strip() + '\n').encode('utf-8-sig') for a in gedcom_file_contents_test_string.strip().splitlines()]

    @staticmethod
    def _get_element_by_pointer(root_child_elements, pointer):
        for element in root_child_elements:
            if element.get_pointer() == pointer:
                return element

    @classmethod
    def _parse_use_case_and_get_individual_element(cls, use_case, pointer):
        gedcom_parser = Parser()
        gedcom_parser.parse(cls._convert_gedcom_string_into_parsable_content(use_case))
        return cls._get_element_by_pointer(gedcom_parser.get_root_child_elements(), pointer)
