import unittest

from gedcom.element.object import ObjectElement
from gedcom.element.individual import IndividualElement, NotAnActualIndividualError
from gedcom.element.root import RootElement
from gedcom.parser import Parser, GedcomFormatViolationError


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
        for element in parser.get_root_child_elements():
            if isinstance(element, IndividualElement):
                individuals_in_root_child_elements += 1
        self.assertEqual(20, individuals_in_root_child_elements)

        individuals_in_element_list = 0
        for element in parser.get_element_list():
            if isinstance(element, IndividualElement):
                individuals_in_element_list += 1
        self.assertEqual(20, individuals_in_element_list)

    def test_parse__should_raise_an_exception_when_on_strict_mode_and_the_line_does_not_start_with_a_number(self):
        mismatched_levels_use_case = """
            @I5@ INDI
                1 NAME First /Last/
            """
        gedcom_parser = Parser()
        self.assertRaises(GedcomFormatViolationError, gedcom_parser.parse, self._convert_gedcom_string_into_parsable_content(mismatched_levels_use_case))

    def test_parse__first_quirk_check(self):
        line_without_a_crlf_use_case = """
            0 @I5@ INDI"""
        val = [(a.strip()).encode('utf-8-sig') for a in line_without_a_crlf_use_case.strip().splitlines()]

        gedcom_parser = Parser()
        gedcom_parser.parse(val, strict=False)
        # TODO: Assess here

    def test_parse__second_quirk_check(self):
        line_with_a_carriage_return_but_not_a_continuation_tag_use_case = """
            0 @I5@ INDI
                1 NOTE This is a note field
                that is continued on the next line.
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(line_with_a_carriage_return_but_not_a_continuation_tag_use_case), strict=False)
        indiv_element = gedcom_parser.get_root_child_elements()[0]
        self.assertTrue(isinstance(indiv_element, IndividualElement))
        self.assertEqual('INDI', indiv_element.get_tag())
        self.assertEqual('@I5@', indiv_element.get_pointer())
        indiv_children = indiv_element.get_child_elements()
        self.assertEqual(1, len(indiv_children))
        self.assertEqual('NOTE', indiv_children[0].get_tag())
        note_children = indiv_children[0].get_child_elements()
        self.assertEqual(1, len(note_children))
        self.assertEqual('CONC', note_children[0].get_tag())

    def test_parse__second_quirk_check_but_previous_tag_was_a_continuation(self):
        line_with_a_carriage_return_but_not_a_continuation_tag_use_case = """
            0 @I5@ INDI
                1 NOTE This is a note field
                    2 CONT that is continued 
                    on the next line.
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(line_with_a_carriage_return_but_not_a_continuation_tag_use_case), strict=False)
        indiv_element = gedcom_parser.get_root_child_elements()[0]
        self.assertTrue(isinstance(indiv_element, IndividualElement))
        self.assertEqual('INDI', indiv_element.get_tag())
        self.assertEqual('@I5@', indiv_element.get_pointer())
        indiv_children = indiv_element.get_child_elements()
        self.assertEqual(1, len(indiv_children))
        self.assertEqual('NOTE', indiv_children[0].get_tag())
        note_children = indiv_children[0].get_child_elements()
        self.assertEqual(2, len(note_children))
        self.assertEqual('CONT', note_children[0].get_tag())
        self.assertEqual('that is continued', note_children[0].get_value())
        self.assertEqual('CONT', note_children[1].get_tag())
        self.assertEqual('on the next line.', note_children[1].get_value())

    def test_parse__should_raise_an_exception_when_a_line_jumps_one_or_more_levels(self):
        mismatched_levels_use_case = """
            0 @I5@ INDI
                    2 NAME First /Last/
            """
        gedcom_parser = Parser()
        self.assertRaises(GedcomFormatViolationError, gedcom_parser.parse, self._convert_gedcom_string_into_parsable_content(mismatched_levels_use_case))

    def test_parse__should_be_able_to_parse_single_individual_from_a_string(self):
        single_individual_use_case = """
            0 @I5@ INDI
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
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(single_individual_use_case))
        element_1 = gedcom_parser.get_root_child_elements()[0]
        self.assertTrue(isinstance(element_1, IndividualElement))
        self.assertEqual('INDI', element_1.get_tag())
        self.assertEqual('@I5@', element_1.get_pointer())
        element_1_children = element_1.get_child_elements()
        self.assertEqual(3, len(element_1_children))
        self.assertEqual('NAME', element_1_children[0].get_tag())
        self.assertEqual('SEX', element_1_children[1].get_tag())
        self.assertEqual('BIRT', element_1_children[2].get_tag())

    def test_parse__should_be_able_to_parse_single_family_from_a_string(self):
        single_family_use_case = """
            0 @F28@ FAM
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
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(single_family_use_case))
        element_2 = gedcom_parser.get_root_child_elements()[0]
        self.assertEqual('FAM', element_2.get_tag())
        self.assertEqual('@F28@', element_2.get_pointer())
        element_2_children = element_2.get_child_elements()
        self.assertEqual(5, len(element_2_children))
        self.assertEqual('HUSB', element_2_children[0].get_tag())
        self.assertEqual('WIFE', element_2_children[1].get_tag())
        self.assertEqual('CHIL', element_2_children[2].get_tag())
        self.assertEqual('@I84@', element_2_children[3].get_value())

    def test_parse__should_be_able_to_parse_a_single_object_from_a_string(self):
        single_object_use_case = """
            0 @M232@ OBJE 
                1 FORM jpg
                1 FILE ~/Documents/Documents/Genealogy/Roger/ReunionPictures/photos/people/RogerOval.JPG
                1 TITL Roger Moffat
                1 NOTE Taken at the time of Kurt and Ann Christensen's wedding - 2 March 1996.
                1 _TYPE PHOTO
                1 _PRIM Y
                1 _SIZE 147.000000 193.000000
            """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(single_object_use_case))
        element_1 = gedcom_parser.get_root_child_elements()[0]
        self.assertTrue(isinstance(element_1, ObjectElement))
        self.assertEqual('OBJE', element_1.get_tag())
        self.assertEqual('@M232@', element_1.get_pointer())
        element_1_children = element_1.get_child_elements()
        self.assertEqual(7, len(element_1_children))
        self.assertEqual('FORM', element_1_children[0].get_tag())

    def test_get_marriages__should_raise_exception_if_not_passed_an_individual(self):
        single_individual_use_case = """
            0 @I5@ INDI
                1 NAME First /Last/
            """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(single_individual_use_case))
        self.assertRaises(NotAnActualIndividualError, gedcom_parser.get_marriages, "@I5@")

    def test_get_marriages__should_only_find_marriages_of_provided_individual(self):
        use_case = """
            0 @I5@ INDI
                1 NAME First /Last/
                1 FAMS @F3@
                1 FAMS @F2@
                1 FAMS @F4@
            0 @F1@ FAM
                1 HUSB @I80@
                1 WIFE @I81@
                1 MARR
            0 @F2@ FAM
                1 HUSB @I5@
                1 WIFE @I81@
                1 MARR
                    2 DATE 1901
            0 @F3@ FAM
                1 HUSB @I5@
                1 WIFE @I87@
                1 MARR
                    2 PLAC ILLINOIS
            0 @F4@ FAM
                1 HUSB @I5@
                1 WIFE @I87@
                1 MARR
            """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I5@")
        marriages = gedcom_parser.get_marriages(individual)
        self.assertEqual(3, len(marriages))
        self.assertEqual([('', 'ILLINOIS'), ('1901', ''), ('', '')], marriages)

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
