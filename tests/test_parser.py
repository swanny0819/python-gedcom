import unittest

from python_gedcom_2.element.family import NotAnActualFamilyError

from python_gedcom_2.element.object import ObjectElement
from python_gedcom_2.element.individual import IndividualElement, NotAnActualIndividualError
from python_gedcom_2.element.root import RootElement
from python_gedcom_2.parser import Parser, GedcomFormatViolationError, FAMILY_MEMBERS_TYPE_PARENTS, FAMILY_MEMBERS_TYPE_HUSBAND, FAMILY_MEMBERS_TYPE_WIFE, \
    FAMILY_MEMBERS_TYPE_CHILDREN, PointerNotFoundException


class TestParser(unittest.TestCase):
    def test_invalidate_cache(self):
        parser = Parser()
        parser.parse_file('../tests/files/Musterstammbaum.ged')

        self.assertEqual(32, len(parser.get_element_dictionary()))
        self.assertEqual(396, len(parser.get_element_list()))

        parser.invalidate_cache()

        self.assertEqual(32, len(parser.get_element_dictionary()))
        self.assertEqual(396, len(parser.get_element_list()))

    def test_get_element_by_pointer__should_find_the_indicated_person(self):
        file_lines = """
            0 @I1@ INDI
                1 NAME Patrick /Swanson/
            0 @I2@ INDI
                1 NAME Bob /Dole/
        """
        parser = Parser()
        parser.parse(self._convert_gedcom_string_into_parsable_content(file_lines), strict=False)
        element = parser.get_element_by_pointer("@I2@")
        self.assertIsNotNone(element)
        self.assertTrue(isinstance(element, IndividualElement))
        # noinspection PyUnresolvedReferences
        self.assertEqual(('Bob', 'Dole'), element.get_name())

    def test_get_element_by_pointer__should_raise_an_exception_when_it_cannot_find_the_indicated_person(self):
        file_lines = """
            0 @I1@ INDI
                1 NAME Patrick /Swanson/
            0 @I2@ INDI
                1 NAME Bob /Dole/
        """
        parser = Parser()
        parser.parse(self._convert_gedcom_string_into_parsable_content(file_lines), strict=False)
        self.assertRaises(PointerNotFoundException, parser.get_element_by_pointer, "@I3@")

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

    _marriages_use_case = """
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

    def test_get_marriages__should_only_find_marriages_of_provided_individual(self):
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(self._marriages_use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I5@")
        marriages = gedcom_parser.get_marriages(individual)
        self.assertEqual([('', 'ILLINOIS'), ('1901', ''), ('', '')], marriages)

    def test_get_marriage_years__should_raise_exception_if_not_passed_an_individual_element(self):
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(self._marriages_use_case))
        self.assertRaises(NotAnActualIndividualError, gedcom_parser.get_marriage_years, "@I5@")

    def test_get_marriage_years__should_gracefully_handle_value_errors_in_the_date(self):
        value_error_use_case = """
                0 @I5@ INDI
                    1 NAME First /Last/
                    1 FAMS @F2@
                0 @F2@ FAM
                    1 HUSB @I5@
                    1 WIFE @I81@
                    1 MARR
                        2 DATE This is not a date.
                """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(value_error_use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I5@")
        marriage_years = gedcom_parser.get_marriage_years(individual)
        self.assertEqual([], marriage_years)

    def test_get_marriage_years__should_only_find_marriage_years_of_provided_individual(self):
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(self._marriages_use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I5@")
        marriage_years = gedcom_parser.get_marriage_years(individual)
        self.assertEqual([1901], marriage_years)

    # ------------------- START OF marriage_year_match TESTING ----------------

    def test_marriage_year_match__should_raise_exception_if_not_passed_an_individual_element(self):
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(self._marriages_use_case))
        self.assertRaises(NotAnActualIndividualError, gedcom_parser.marriage_year_match, "@I5@", 1953)

    def test_marriage_year_match__should_be_able_to_match_the_year_if_present(self):
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(self._marriages_use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I5@")
        self.assertTrue(gedcom_parser.marriage_year_match(individual, 1901))

    def test_marriage_year_match__should_not_be_able_to_match_the_year_if_not_present(self):
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(self._marriages_use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I5@")
        self.assertFalse(gedcom_parser.marriage_year_match(individual, 1902))

    # ------------------- START OF marriage_range_match TESTING ----------------

    def test_marriage_range_match__should_raise_exception_if_not_passed_an_individual_element(self):
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(self._marriages_use_case))
        self.assertRaises(NotAnActualIndividualError, gedcom_parser.marriage_range_match, "@I5@", 1953, 1957)

    def test_marriage_range_match__should_be_able_to_match_the_year_if_present_in_the_range(self):
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(self._marriages_use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I5@")
        self.assertTrue(gedcom_parser.marriage_range_match(individual, 1900, 1902))

    def test_marriage_range_match__should_not_be_able_to_match_the_year_if_all_precede_the_range(self):
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(self._marriages_use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I5@")
        self.assertFalse(gedcom_parser.marriage_range_match(individual, 1902, 1999))

    def test_marriage_range_match__should_not_be_able_to_match_the_year_if_all_follow_the_range(self):
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(self._marriages_use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I5@")
        self.assertFalse(gedcom_parser.marriage_range_match(individual, 1801, 1899))

    # ------------------- START OF get_families TESTING ----------------

    def test_get_families__should_raise_exception_if_not_passed_an_individual_element(self):
        simple_use_case = """
                0 @I5@ INDI
                    1 NAME First /Last/
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(simple_use_case))
        self.assertRaises(NotAnActualIndividualError, gedcom_parser.get_families, "@I5@")

    # ------------------- START OF get_ancestors TESTING ----------------

    def test_get_ancestors__should_raise_exception_if_not_passed_an_individual_element(self):
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(""))
        self.assertRaises(NotAnActualIndividualError, gedcom_parser.get_ancestors, "@I5@")

    def test_get_ancestors__should_return_nobody_if_they_have_no_ancestors(self):
        use_case = """
                0 @I5@ INDI
                    1 NAME First /Last/
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I5@")
        ancestors = gedcom_parser.get_ancestors(individual)
        self.assertEqual(0, len(ancestors), ancestors)

    def test_get_ancestors__should_return_the_persons_parents_if_they_have_no_grandparents(self):
        use_case = """
            0 @I1@ INDI
                1 NAME Kid /Last/
                1 FAMC @F1@
            0 @I2@ INDI
                1 NAME Dad /Last/
                1 FAMS @F1@
            0 @I3@ INDI
                1 NAME Mom /Maiden/
                1 FAMS @F1@
            0 @F1@ FAM
                1 HUSB @I2@
                1 WIFE @I3@
                1 CHIL @I1@
                    2 _FREL Natural
                    2 _MREL Natural
                1 MARR
            """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I1@")
        ancestors = gedcom_parser.get_ancestors(individual)
        self.assertEqual(2, len(ancestors), ancestors)
        self.assertEqual("@I2@", ancestors[0].get_pointer())
        self.assertEqual("@I3@", ancestors[1].get_pointer())

    def test_get_ancestors__should_return_the_persons_single_parent_if_they_do_not_have_two(self):
        use_case = """
            0 @I1@ INDI
                1 NAME Kid /Last/
                1 FAMC @F1@
            0 @I2@ INDI
                1 NAME Dad /Last/
                1 FAMS @F1@
            0 @F1@ FAM
                1 HUSB @I2@
                1 CHIL @I1@
                    2 _MREL Natural
                1 MARR
            """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I1@")
        ancestors = gedcom_parser.get_ancestors(individual)
        self.assertEqual(1, len(ancestors), ancestors)
        self.assertEqual("@I2@", ancestors[0].get_pointer())

    def test_get_ancestors__should_return_the_persons_parents_and_available_grandparents_if_they_have_some(self):
        use_case = """
            0 @I1@ INDI
                1 NAME Kid /Last/
                1 FAMC @F1@
            0 @I2@ INDI
                1 NAME Dad /Last/
                1 FAMS @F1@
                1 FAMC @F2@
            0 @I3@ INDI
                1 NAME Mom /Maiden/
                1 FAMS @F1@
            0 @I4@ INDI
                1 NAME Grandpa /Last/
                1 FAMS @F2@
            0 @I5@ INDI
                1 NAME Grandma /Maiden/
                1 FAMS @F2@
            0 @F1@ FAM
                1 HUSB @I2@
                1 WIFE @I3@
                1 CHIL @I1@
                    2 _FREL Natural
                    2 _MREL Natural
                1 MARR
            0 @F2@ FAM
                1 HUSB @I4@
                1 WIFE @I5@
                1 CHIL @I2@
                    2 _FREL Natural
                    2 _MREL Natural
                1 MARR
            """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I1@")
        ancestors = gedcom_parser.get_ancestors(individual)
        self.assertEqual(4, len(ancestors), ancestors)
        self.assertEqual("@I2@", ancestors[0].get_pointer())
        self.assertEqual("@I3@", ancestors[1].get_pointer())
        self.assertEqual("@I4@", ancestors[2].get_pointer())
        self.assertEqual("@I5@", ancestors[3].get_pointer())

    def test_get_ancestors__should_not_return_the_persons_grandparents_if_searching_natural_only_and_the_parent_was_adopted(self):
        use_case = """
            0 @I1@ INDI
                1 NAME Kid /Last/
                1 FAMC @F1@
            0 @I2@ INDI
                1 NAME Dad /Last/
                1 FAMS @F1@
                1 FAMC @F2@
            0 @I3@ INDI
                1 NAME Mom /Maiden/
                1 FAMS @F1@
            0 @I4@ INDI
                1 NAME Grandpa /Last/
                1 FAMS @F2@
            0 @I5@ INDI
                1 NAME Grandma /Maiden/
                1 FAMS @F2@
            0 @F1@ FAM
                1 HUSB @I2@
                1 WIFE @I3@
                1 CHIL @I1@
                    2 _FREL Natural
                    2 _MREL Natural
                1 MARR
            0 @F2@ FAM
                1 HUSB @I4@
                1 WIFE @I5@
                1 CHIL @I2@
                    2 _FREL Adopted
                    2 _MREL Adopted
                1 MARR
            """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I1@")
        ancestors = gedcom_parser.get_ancestors(individual, ancestor_type="NAT")
        self.assertEqual(2, len(ancestors), ancestors)
        self.assertEqual("@I2@", ancestors[0].get_pointer())
        self.assertEqual("@I3@", ancestors[1].get_pointer())

    # ------------------- START OF get_parents TESTING ----------------

    def test_get_parents__should_raise_exception_if_not_passed_an_individual_element(self):
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(""))
        self.assertRaises(NotAnActualIndividualError, gedcom_parser.get_parents, "@I5@")

    def test_get_parents__should_handle_a_person_without_parents(self):
        use_case = """
                0 @I5@ INDI
                    1 NAME First /Last/
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I5@")
        parents = gedcom_parser.get_parents(individual)
        self.assertEqual([], parents)

    def test_get_parents__should_handle_a_person_with_both_natural_parents_when_getting_all(self):
        use_case = """
            0 @I1@ INDI
                1 NAME Kid /Last/
                1 FAMC @F1@
            0 @I2@ INDI
                1 NAME Dad /Last/
                1 FAMS @F1@
            0 @I3@ INDI
                1 NAME Mom /Maiden/
                1 FAMS @F1@
            0 @F1@ FAM
                1 HUSB @I2@
                1 WIFE @I3@
                1 CHIL @I1@
                    2 _FREL Natural
                    2 _MREL Natural
                1 MARR
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I1@")
        parents = gedcom_parser.get_parents(individual)
        self.assertEqual(2, len(parents), parents)
        self.assertEqual("@I2@", parents[0].get_pointer())
        self.assertEqual("@I3@", parents[1].get_pointer())

    def test_get_parents__should_only_return_the_indicated_childs_parents_when_getting_natural_parents_only(self):
        use_case = """
            0 @I1@ INDI
                1 NAME Adopted Kid /Last/
                1 FAMC @F1@
            0 @I4@ INDI
                1 NAME Natural Kid /Last/
                1 FAMC @F1@
            0 @I2@ INDI
                1 NAME Dad /Last/
                1 FAMS @F1@
            0 @I3@ INDI
                1 NAME Mom /Maiden/
                1 FAMS @F1@
            0 @F1@ FAM
                1 HUSB @I2@
                1 WIFE @I3@
                1 CHIL @I1@
                    2 _FREL Adopted
                    2 _MREL Adopted
                1 CHIL @I4@
                    2 _FREL Natural
                    2 _MREL Natural
                1 MARR
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I1@")
        parents = gedcom_parser.get_parents(individual, parent_type="NAT")
        self.assertEqual(0, len(parents), parents)

    def test_get_parents__should_handle_a_person_with_both_adoptive_parents_when_getting_all(self):
        use_case = """
            0 @I1@ INDI
                1 NAME Kid /Last/
                1 FAMC @F1@
            0 @I2@ INDI
                1 NAME Dad /Last/
                1 FAMS @F1@
            0 @I3@ INDI
                1 NAME Mom /Maiden/
                1 FAMS @F1@
            0 @F1@ FAM
                1 HUSB @I2@
                1 WIFE @I3@
                1 CHIL @I540@
                    2 _FREL Adopted
                    2 _MREL Adopted
                1 MARR
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I1@")
        parents = gedcom_parser.get_parents(individual)
        self.assertEqual(2, len(parents), parents)
        self.assertEqual("@I2@", parents[0].get_pointer())
        self.assertEqual("@I3@", parents[1].get_pointer())

    def test_get_parents__should_handle_a_person_with_a_single_natural_female_parent_when_getting_natural_only(self):
        use_case = """
            0 @I1@ INDI
                1 NAME Kid /Last/
                1 FAMC @F1@
            0 @I2@ INDI
                1 NAME Dad /Last/
                1 FAMS @F1@
            0 @I3@ INDI
                1 NAME Mom /Maiden/
                1 FAMS @F1@
            0 @F1@ FAM
                1 HUSB @I2@
                1 WIFE @I3@
                1 CHIL @I1@
                    2 _MREL Natural
                    2 _FREL Adopted
                1 MARR
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I1@")
        parents = gedcom_parser.get_parents(individual, parent_type="NAT")
        self.assertEqual(1, len(parents), parents)
        self.assertEqual("@I3@", parents[0].get_pointer())

    def test_get_parents__should_handle_a_person_with_a_single_natural_male_parent_when_getting_natural_only(self):
        use_case = """
            0 @I1@ INDI
                1 NAME Kid /Last/
                1 FAMC @F1@
            0 @I2@ INDI
                1 NAME Dad /Last/
                1 FAMS @F1@
            0 @I3@ INDI
                1 NAME Mom /Maiden/
                1 FAMS @F1@
            0 @F1@ FAM
                1 HUSB @I2@
                1 WIFE @I3@
                1 CHIL @I1@
                    2 _MREL Adopted
                    2 _FREL Natural
                1 MARR
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I1@")
        parents = gedcom_parser.get_parents(individual, parent_type="NAT")
        self.assertEqual(1, len(parents), parents)
        self.assertEqual("@I2@", parents[0].get_pointer())

    def test_get_parents__should_handle_a_person_with_no_natural_parent_when_getting_natural_only(self):
        use_case = """
            0 @I1@ INDI
                1 NAME Kid /Last/
                1 FAMC @F1@
            0 @I2@ INDI
                1 NAME Dad /Last/
                1 FAMS @F1@
            0 @I3@ INDI
                1 NAME Mom /Maiden/
                1 FAMS @F1@
            0 @F1@ FAM
                1 HUSB @I2@
                1 WIFE @I3@
                1 CHIL @I1@
                    2 _FREL Adopted
                    2 _MREL Adopted
                1 MARR
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I1@")
        parents = gedcom_parser.get_parents(individual, parent_type="NAT")
        self.assertEqual(0, len(parents), parents)

    def test_get_parents__should_handle_a_person_with_parents_in_multiple_families(self):
        use_case = """
            0 @I1@ INDI
                1 NAME Kid /Last/
                1 FAMC @F1@
                1 FAMC @F2@
            0 @I2@ INDI
                1 NAME Dad /Last/
                1 FAMS @F1@
            0 @I3@ INDI
                1 NAME Mom /Maiden/
                1 FAMS @F1@
            0 @I4@ INDI
                1 NAME Dad /Adoptive/
                1 FAMS @F2@
            0 @I5@ INDI
                1 NAME Mom /MaidenAdoptive/
                1 FAMS @F2@
            0 @F1@ FAM
                1 HUSB @I2@
                1 WIFE @I3@
                1 CHIL @1@
                    2 _FREL Natural
                    2 _MREL Natural
                1 MARR
            0 @F2@ FAM
                1 HUSB @I4@
                1 WIFE @I5@
                1 CHIL @I1@
                    2 _FREL Adopted
                    2 _MREL Adopted
                1 MARR
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        individual = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I1@")
        parents = gedcom_parser.get_parents(individual)
        self.assertEqual(4, len(parents), parents)
        self.assertEqual("@I2@", parents[0].get_pointer())
        self.assertEqual("@I3@", parents[1].get_pointer())
        self.assertEqual("@I4@", parents[2].get_pointer())
        self.assertEqual("@I5@", parents[3].get_pointer())
    # ----------------- TESTS FOR get_children --------------------------

    _file_lines_for_get_children_testing = """
        0 @I1@ INDI
            1 NAME Patrick /Swanson/
            1 FAMS @F1@
        0 @I2@ INDI
            1 NAME Ashley /Williams/
            1 FAMS @F1@
        0 @I3@ INDI
            1 NAME First /Swanson/
            1 FAMC @F1@
        0 @I4@ INDI
            1 NAME Second /Swanson/
            1 FAMC @F1@
        0 @I5@ INDI
            1 NAME Third /Swanson/
            1 FAMC @F1@
        0 @I6@ INDI
            1 NAME Fourth /Swanson/
            1 FAMC @F1@
        0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 CHIL @I3@
                2 _FREL Natural
                2 _MREL Natural
            1 CHIL @I4@
                2 _FREL Natural
                2 _MREL Adopted
            1 CHIL @I5@
                2 _FREL Adopted
                2 _MREL Natural
            1 CHIL @I6@
                2 _FREL Adopted
                2 _MREL Adopted
    """

    def test_get_children__should_raise_an_error_when_something_that_is_not_a_person_is_passed_in(self):
        parser = Parser()
        parser.parse(self._convert_gedcom_string_into_parsable_content(self._file_lines_for_get_children_testing))
        parent = parser.get_element_by_pointer("@F1@")
        self.assertRaises(NotAnActualIndividualError, parser.get_children, parent)

    def test_get_children__should_find_all_children_when_looking_for_children_of_all_types(self):
        parser = Parser()
        parser.parse(self._convert_gedcom_string_into_parsable_content(self._file_lines_for_get_children_testing))
        parent = parser.get_element_by_pointer("@I1@")
        # noinspection PyTypeChecker
        children = parser.get_children(parent)
        self.assertEqual(4, len(children))

    def test_get_children__should_find_only_natural_children_when_looking_for_only_natural_children_of_the_husband(self):
        parser = Parser()
        parser.parse(self._convert_gedcom_string_into_parsable_content(self._file_lines_for_get_children_testing))
        parent = parser.get_element_by_pointer("@I1@")
        # noinspection PyTypeChecker
        children = parser.get_children(parent, child_type="NAT")
        self.assertEqual(2, len(children))
        self.assertEqual(('First', 'Swanson'), children[0].get_name())
        self.assertEqual(('Second', 'Swanson'), children[1].get_name())

    def test_get_children__should_find_only_natural_children_when_looking_for_only_natural_children_of_the_wife(self):
        parser = Parser()
        parser.parse(self._convert_gedcom_string_into_parsable_content(self._file_lines_for_get_children_testing))
        parent = parser.get_element_by_pointer("@I2@")
        # noinspection PyTypeChecker
        children = parser.get_children(parent, child_type="NAT")
        self.assertEqual(2, len(children))
        self.assertEqual(('First', 'Swanson'), children[0].get_name())
        self.assertEqual(('Third', 'Swanson'), children[1].get_name())

    def test_get_children__should_gracefully_handle_being_given_an_individual_that_is_not_in_a_family(self):
        file_lines = """
            0 @I1@ INDI
                1 NAME Patrick /Swanson/
        """
        parser = Parser()
        parser.parse(self._convert_gedcom_string_into_parsable_content(file_lines))
        parent = parser.get_element_by_pointer("@I1@")
        # noinspection PyTypeChecker
        children = parser.get_children(parent, child_type="NAT")
        self.assertEqual(0, len(children))

    # ------------------- START OF find_path_to_ancestor TESTING ----------------

    def test_find_path_to_ancestor__should_raise_exception_if_not_passed_an_individual_element_for_the_descendant(self):
        use_case = """
            0 @I1@ INDI
                1 NAME Kid /Last/
            0 @I2@ INDI
                1 NAME Dad /Last/
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        ancestor = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I2@")
        self.assertRaises(NotAnActualIndividualError, gedcom_parser.find_path_to_ancestor, "@I1@", ancestor)

    def test_find_path_to_ancestor__should_raise_exception_if_not_passed_an_individual_element_for_the_ancestor(self):
        use_case = """
            0 @I1@ INDI
                1 NAME Kid /Last/
            0 @I2@ INDI
                1 NAME Dad /Last/
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        descendant = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I1@")
        self.assertRaises(NotAnActualIndividualError, gedcom_parser.find_path_to_ancestor, descendant, "@I2@")

    def test_find_path_to_ancestor__should_create_path_when_ancestor_is_the_descendant(self):
        use_case = """
            0 @I1@ INDI
                1 NAME Kid /Last/
                1 FAMC @F1@
            0 @I2@ INDI
                1 NAME Dad /Last/
                1 FAMS @F1@
            0 @F1@ FAM
                1 HUSB @I2@
                1 CHIL @I1@
                    2 _MREL Natural
                1 MARR
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        descendant = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I1@")
        ancestor = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I1@")
        path = gedcom_parser.find_path_to_ancestor(descendant, ancestor)
        self.assertEqual([descendant], path)

    def test_find_path_to_ancestor__should_create_path_when_ancestor_is_parent_of_descendant(self):
        use_case = """
            0 @I1@ INDI
                1 NAME Kid /Last/
                1 FAMC @F1@
            0 @I2@ INDI
                1 NAME Dad /Last/
                1 FAMS @F1@
            0 @F1@ FAM
                1 HUSB @I2@
                1 CHIL @I1@
                    2 _FREL Natural
                1 MARR
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        descendant = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I1@")
        ancestor = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I2@")
        path = gedcom_parser.find_path_to_ancestor(descendant, ancestor)
        self.assertEqual([descendant.get_pointer(), ancestor.get_pointer()], self._convert_element_list_to_pointer_list(path))

    def test_find_path_to_ancestor__should_create_path_when_ancestor_is_grandparent_of_descendant(self):
        use_case = """
            0 @I1@ INDI
                1 NAME Kid /Last/
                1 FAMC @F1@
            0 @I2@ INDI
                1 NAME Dad /Last/
                1 FAMS @F1@
                1 FAMC @F2@
            0 @I3@ INDI
                1 NAME Grandpa /Last/
                1 FAMS @F2@
            0 @F1@ FAM
                1 HUSB @I2@
                1 CHIL @I1@
                    2 _FREL Natural
                1 MARR
            0 @F2@ FAM
                1 HUSB @I3@
                1 CHIL @I2@
                    2 _FREL Natural
                1 MARR
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        descendant = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I1@")
        ancestor = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I3@")
        path = gedcom_parser.find_path_to_ancestor(descendant, ancestor)

        self.assertEqual(["@I1@", "@I2@", "@I3@"], self._convert_element_list_to_pointer_list(path))

    def test_find_path_to_ancestor__should_create_empty_path_when_ancestor_is_not_actually_an_ancestor(self):
        use_case = """
            0 @I1@ INDI
                1 NAME Kid /Last/
                1 FAMC @F1@
            0 @I2@ INDI
                1 NAME Other /Guy/
            0 @I3@ INDI
                1 NAME Dad /Last/
                1 FAMS @F1@
            0 @F1@ FAM
                1 HUSB @I3@
                1 CHIL @I1@
                    2 _FREL Natural
                1 MARR
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        descendant = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I1@")
        ancestor = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@I2@")
        path = gedcom_parser.find_path_to_ancestor(descendant, ancestor)

        self.assertEqual(None, path)

    # ------------------- START OF get_family_members TESTING ----------------

    def test_get_family_members__should_raise_exception_if_not_passed_a_family_element(self):
        use_case = """
            0 @I1@ INDI
                1 NAME Kid /Last/
                1 FAMC @F1@
            0 @F1@ FAM
                1 CHIL @I1@
                1 MARR
        """
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(use_case))
        self.assertRaises(NotAnActualFamilyError, gedcom_parser.get_family_members, "@I1@")

    _get_family_members_use_case = """
            0 @I1@ INDI
                1 NAME Kid /Last/
                1 FAMC @F1@
            0 @I2@ INDI
                1 NAME Husband /Last/
                1 FAMS @F1@
            0 @I3@ INDI
                1 NAME Wife /Maiden/
                1 FAMS @F1@
            0 @F1@ FAM
                1 HUSB @I2@
                1 WIFE @I3@
                1 CHIL @I1@
                    2 _FREL Natural
                    2 _MREL Natural
                1 MARR
        """

    def test_get_family_members__should_get_all_family_members_if_not_using_a_family_member_type_flag(self):
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(self._get_family_members_use_case))
        family_element = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@F1@")
        family_members = gedcom_parser.get_family_members(family_element)
        self.assertEqual(["@I2@", "@I3@", "@I1@"], self._convert_element_list_to_pointer_list(family_members))

    def test_get_family_members__should_get_the_parents_only_if_searching_using_the_parent_flag(self):
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(self._get_family_members_use_case))
        family_element = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@F1@")
        family_members = gedcom_parser.get_family_members(family_element, members_type=FAMILY_MEMBERS_TYPE_PARENTS)
        self.assertEqual(["@I2@", "@I3@"], self._convert_element_list_to_pointer_list(family_members))

    def test_get_family_members__should_get_the_husband_only_if_searching_using_the_husband_flag(self):
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(self._get_family_members_use_case))
        family_element = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@F1@")
        family_members = gedcom_parser.get_family_members(family_element, members_type=FAMILY_MEMBERS_TYPE_HUSBAND)
        self.assertEqual(["@I2@"], self._convert_element_list_to_pointer_list(family_members))

    def test_get_family_members__should_get_the_wife_only_if_searching_using_the_wife_flag(self):
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(self._get_family_members_use_case))
        family_element = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@F1@")
        family_members = gedcom_parser.get_family_members(family_element, members_type=FAMILY_MEMBERS_TYPE_WIFE)
        self.assertEqual(["@I3@"], self._convert_element_list_to_pointer_list(family_members))

    def test_get_family_members__should_get_the_children_only_if_searching_using_the_children_flag(self):
        gedcom_parser = Parser()
        gedcom_parser.parse(self._convert_gedcom_string_into_parsable_content(self._get_family_members_use_case))
        family_element = self._get_element_by_pointer(gedcom_parser.get_root_child_elements(), "@F1@")
        family_members = gedcom_parser.get_family_members(family_element, members_type=FAMILY_MEMBERS_TYPE_CHILDREN)
        self.assertEqual(["@I1@"], self._convert_element_list_to_pointer_list(family_members))

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

    @staticmethod
    def _convert_element_list_to_pointer_list(element_list):
        return [x.get_pointer() for x in element_list]
