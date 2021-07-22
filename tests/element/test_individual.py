import unittest

from gedcom.parser import Parser

from gedcom.element.individual import IndividualElement


class TestIndividualElement(unittest.TestCase):

    def test_is_deceased__a_person_without_a_death_element_should_not_be_deceased(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 SEX M
                1 BIRT
                    2 DATE 1 JAN 1900
                1 NAME Second /Surname/
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertFalse(individual.is_deceased())

    def test_is_deceased__a_person_with_a_death_element_should_be_deceased(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 SEX M
                1 DEAT
                    2 DATE 1 JAN 1900
                1 NAME Second /Surname/
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertTrue(individual.is_deceased())

    # --------------------- START OF is_child TESTING -----------------------

    def test_is_child__a_person_not_in_a_family_is_not_a_child(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertFalse(individual.is_child())

    def test_is_child__a_person_in_a_family_but_only_as_a_parent_is_not_a_child(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 FAMS @F1@
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertFalse(individual.is_child())

    def test_is_child__a_person_in_a_family_and_as_a_child_is_a_child(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 FAMC @F1@
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertTrue(individual.is_child())

    # --------------------- START OF is_private TESTING -----------------------

    def test_is_private__a_person_not_marked_private_is_not_private(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertFalse(individual.is_private())

    def test_is_child__a_person_with_a_private_tag_but_not_marked_yes_is_not_private(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 PRIV N
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertFalse(individual.is_private())

    def test_is_child__a_person_with_a_private_tag_and_marked_yes_is_private(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 PRIV Y
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertTrue(individual.is_private())

    # --------------------- START OF get_name TESTING -----------------------

    def test_get_name__should_return_full_name_of_a_person_with_a_name_tag_that_has_a_value(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(('First', 'Last'), individual.get_name())

    def test_get_name__should_return_full_name_of_a_person_with_a_name_tag_that_has_sub_elements_with_values(self):
        use_case = """
            0 @I1@ INDI
                1 NAME
                    2 GIVN First
                    2 SURN Last
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(('First', 'Last'), individual.get_name())

    def test_get_name__should_return_full_name_of_a_person_with_a_name_tag_that_only_has_given_name_sub_element(self):
        use_case = """
            0 @I1@ INDI
                1 NAME
                    2 GIVN First
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(('First', ''), individual.get_name())

    def test_get_name__should_return_full_name_of_a_person_with_a_name_tag_that_only_has_surname_sub_element(self):
        use_case = """
            0 @I1@ INDI
                1 NAME
                    2 SURN Last
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(('', 'Last'), individual.get_name())

    def test_get_name__should_return_given_name_of_a_person_with_a_name_tag_that_only_has_a_given_name(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(('First', ''), individual.get_name())

    def test_get_name__should_return_surname_name_of_a_person_with_a_name_tag_that_only_has_a_surname(self):
        use_case = """
            0 @I1@ INDI
                1 NAME /Last/
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(('', 'Last'), individual.get_name())

    def test_get_name__should_return_empty_strings_for_a_person_without_a_name_tag(self):
        use_case = """
            0 @I1@ INDI
                1 BIRT
                    2 DATE Jan 1 1900
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(('', ''), individual.get_name())

    # --------------------- START OF surname_match TESTING -----------------------

    def test_surname_match__should_match_exactly_a_surname(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertTrue(individual.surname_match('Last'))

    def test_surname_match__should_match_a_surname_while_ignoring_case(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertTrue(individual.surname_match('LAST'))

    def test_surname_match__should_not_match_a_surname_if_different(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertFalse(individual.surname_match('not a match'))

    # --------------------- START OF given_name_match TESTING -----------------------

    def test_given_name_match__should_match_exactly_a_given_name(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertTrue(individual.given_name_match('First'))

    def test_given_name_match__should_match_a_given_name_while_ignoring_case(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertTrue(individual.given_name_match('FIRST'))

    def test_given_name_match__should_not_match_a_given_name_if_different(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertFalse(individual.given_name_match('not a match'))

    # --------------------- START OF get_gender TESTING -----------------------

    def test_get_gender__should_get_the_persons_gender_if_present(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 SEX M
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual("M", individual.get_gender())

    def test_get_gender__should_return_an_empty_string_if_gender_is_not_present(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual("", individual.get_gender())

    # --------------------- START OF get_birth_data TESTING -----------------------

    # TODO: Test get_birth_data

    # --------------------- START OF get_birth_year TESTING -----------------------

    def test_get_birth_year__should_remove_about_string_from_a_year(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 BIRT
                    2 DATE ABT 1924
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(1924, individual.get_birth_year())

    def test_get_birth_year__should_remove_after_string_from_a_year(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 BIRT
                    2 DATE AFT 1924
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(1924, individual.get_birth_year())

    def test_get_birth_year__should_remove_before_string_from_a_year(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 BIRT
                    2 DATE AFT 1924
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(1924, individual.get_birth_year())

    def test_get_birth_year__should_handle_case_where_there_is_no_year(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 BIRT
                    2 DATE JUN
                    2 PLAC Chicago
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(-1, individual.get_birth_year())

    def test_get_birth_year__should_return_birth_year_not_found_value_if_no_date_tag_exists(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(-1, individual.get_birth_year())

    # --------------------- START OF get_death_data TESTING -----------------------

    # TODO: Test get_death_data
    
    # --------------------- START OF get_death_year TESTING -----------------------

    def test_get_death_year__should_remove_about_string_from_a_year(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 DEAT
                    2 DATE ABT 1924
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(1924, individual.get_death_year())

    def test_get_death_year__should_remove_after_string_from_a_year(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 DEAT
                    2 DATE AFT 1924
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(1924, individual.get_death_year())

    def test_get_death_year__should_remove_before_string_from_a_year(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 DEAT
                    2 DATE AFT 1924
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(1924, individual.get_death_year())

    def test_get_death_year__should_handle_case_where_there_is_no_year(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 DEAT
                    2 DATE JUN
                    2 PLAC Chicago
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(-1, individual.get_death_year())

    def test_get_death_year__should_return_death_year_not_found_value_if_no_date_tag_exists(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(-1, individual.get_death_year())

    # TODO: Test get_burial_data

    # TODO: Test get_census_data

    # TODO: Test get_last_change_date
    # TODO: Test get_occupation
    # TODO: Test birth_year_match
    # TODO: Test birth_range_match
    # TODO: Test death_year_match
    # TODO: Test death_range_match
    # TODO: Test criteria_match

    # --------------------- START OF get_all_names TESTING -----------------------

    def test_get_all_names__should_be_able_to_match_multiple_names_but_not_non_names(self):
        element = IndividualElement(level=0, pointer="@I5@", tag="INDI", value="")
        element.new_child_element(tag="NAME", value="First /Last/")
        element.new_child_element(tag="SEX", value="M")
        birth = element.new_child_element(tag="BIRT", value="")
        birth.new_child_element(tag="DATE", value="1 JAN 1900")
        element.new_child_element(tag="NAME", value="Second /Surname/")

        all_names = element.get_all_names()
        self.assertEqual(2, len(all_names))
        self.assertEqual('First /Last/', all_names[0])
        self.assertEqual('Second /Surname/', all_names[1])

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
