import unittest

from python_gedcom_2.parser import Parser

from python_gedcom_2.element.individual import IndividualElement


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

    # --------------------- START OF is_spouse TESTING -----------------------

    def test_is_spouse__a_person_not_in_a_family_is_not_a_spouse(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertFalse(individual.is_spouse())

    def test_is_spouse__a_person_in_a_family_but_only_as_a_child_is_not_a_spouse(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 FAMC @F1@
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertFalse(individual.is_spouse())

    def test_is_spouse__a_person_in_a_family_and_as_a_spouse_is_a_spouse(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 FAMS @F1@
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertTrue(individual.is_spouse())

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

    def test_get_name__should_remove_suffix_of_a_persons_name_when_they_have_one(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/ Jr
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

    def test_get_birth_data__should_return_an_empty_tuple_if_no_such_data_is_present(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 SEX M
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(("", "", []), individual.get_birth_data())

    def test_get_birth_data__should_return_a_single_tuple_when_there_is_just_a_date(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 BIRT
                    2 DATE JUN 1990
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(("JUN 1990", "", []), individual.get_birth_data())

    def test_get_birth_data__should_return_a_single_tuple_when_there_is_just_a_place(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 BIRT
                    2 PLAC Chicago
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(("", "Chicago", []), individual.get_birth_data())

    def test_get_birth_data__should_return_a_single_tuple_when_there_is_just_a_source(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 BIRT
                    2 SOUR @S1@
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(("", "", ["@S1@"]), individual.get_birth_data())

    def test_get_birth_data__should_return_a_single_full_tuple_when_there_is_a_date_place_and_multiple_sources(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 BIRT
                    2 DATE APR 2001
                    2 PLAC New York
                    2 SOUR @S1@
                    2 SOUR @S2@
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(("APR 2001", "New York", ["@S1@", "@S2@"]), individual.get_birth_data())

    def test_get_birth_data__should_return_a_combination_of_fields_in_a_tuple_when_there_are_multiple_partials(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 BIRT
                    2 DATE APR 2001
                1 BIRT
                    2 PLAC New York
                1 BIRT
                    2 SOUR @S1@
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(("APR 2001", "New York", ["@S1@"]), individual.get_birth_data())

    # --------------------- START OF get_death_data TESTING -----------------------

    def test_get_death_data__should_return_an_empty_tuple_if_no_such_data_is_present(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 SEX M
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(("", "", []), individual.get_death_data())

    def test_get_death_data__should_return_a_single_tuple_when_there_is_just_a_date(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 DEAT
                    2 DATE JUN 1990
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(("JUN 1990", "", []), individual.get_death_data())

    def test_get_death_data__should_return_a_single_tuple_when_there_is_just_a_place(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 DEAT
                    2 PLAC Chicago
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(("", "Chicago", []), individual.get_death_data())

    def test_get_death_data__should_return_a_single_tuple_when_there_is_just_a_source(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 DEAT
                    2 SOUR @S1@
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(("", "", ["@S1@"]), individual.get_death_data())

    def test_get_death_data__should_return_a_single_full_tuple_when_there_is_a_date_place_and_multiple_sources(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 DEAT
                    2 DATE APR 2001
                    2 PLAC New York
                    2 SOUR @S1@
                    2 SOUR @S2@
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(("APR 2001", "New York", ["@S1@", "@S2@"]), individual.get_death_data())

    def test_get_death_data__should_return_a_combination_of_fields_in_a_tuple_when_there_are_multiple_partials(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 DEAT
                    2 DATE APR 2001
                1 DEAT
                    2 PLAC New York
                1 DEAT
                    2 SOUR @S1@
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(("APR 2001", "New York", ["@S1@"]), individual.get_death_data())

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

    # --------------------- START OF get_burial_data TESTING -----------------------

    def test_get_burial_data__should_return_an_empty_tuple_if_no_such_data_is_present(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 SEX M
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(("", "", []), individual.get_burial_data())

    def test_get_burial_data__should_return_a_single_tuple_when_there_is_just_a_date(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 BURI
                    2 DATE JUN 1990
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(("JUN 1990", "", []), individual.get_burial_data())

    def test_get_burial_data__should_return_a_single_tuple_when_there_is_just_a_place(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 BURI
                    2 PLAC Chicago
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(("", "Chicago", []), individual.get_burial_data())

    def test_get_burial_data__should_return_a_single_tuple_when_there_is_just_a_source(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 BURI
                    2 SOUR @S1@
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(("", "", ["@S1@"]), individual.get_burial_data())

    def test_get_burial_data__should_return_a_single_full_tuple_when_there_is_a_date_place_and_multiple_sources(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 BURI
                    2 DATE APR 2001
                    2 PLAC New York
                    2 SOUR @S1@
                    2 SOUR @S2@
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(("APR 2001", "New York", ["@S1@", "@S2@"]), individual.get_burial_data())

    def test_get_burial_data__should_return_a_combination_of_fields_in_a_tuple_when_there_are_multiple_partials(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 BURI
                    2 DATE APR 2001
                1 BURI
                    2 PLAC New York
                1 BURI
                    2 SOUR @S1@
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual(("APR 2001", "New York", ["@S1@"]), individual.get_burial_data())

    # --------------------- START OF get_census_data TESTING -----------------------

    def test_get_census_data__should_return_an_empty_list_if_no_such_data_is_present(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 SEX M
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual([], individual.get_census_data())

    def test_get_census_data__should_return_a_list_containing_a_single_tuple_when_there_is_just_a_date(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 CENS
                    2 DATE JUN 1990
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual([("JUN 1990", "", [])], individual.get_census_data())

    def test_get_census_data__should_return_a_list_containing_a_single_tuple_when_there_is_just_a_place(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 CENS
                    2 PLAC Chicago
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual([("", "Chicago", [])], individual.get_census_data())

    def test_get_census_data__should_return_a_list_containing_a_single_tuple_when_there_is_just_a_source(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 CENS
                    2 SOUR @S1@
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual([("", "", ["@S1@"])], individual.get_census_data())

    def test_get_census_data__should_return_a_list_containing_a_single_full_tuple_when_there_is_a_date_place_and_multiple_sources(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 CENS
                    2 DATE APR 2001
                    2 PLAC New York
                    2 SOUR @S1@
                    2 SOUR @S2@
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual([("APR 2001", "New York", ["@S1@", "@S2@"])], individual.get_census_data())

    def test_get_census_data__should_return_separate_tuples_when_there_are_multiple_partials(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 CENS
                    2 DATE APR 2001
                1 CENS
                    2 PLAC New York
                1 CENS
                    2 SOUR @S1@
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual([("APR 2001", "", []), ("", "New York", []), ("", "", ["@S1@"])], individual.get_census_data())

    # --------------------- START OF get_last_change_date TESTING -----------------------

    def test_get_last_change_date__should_return_empty_string_if_there_is_no_last_change_date(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual("", individual.get_last_change_date())

    def test_get_last_change_date__should_return_the_date_if_there_is_a_last_change_date(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 CHAN
                    2 DATE Jun 1990
                    2 SOUR @S1@
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual("Jun 1990", individual.get_last_change_date())

    # --------------------- START OF get_occupation TESTING -----------------------

    def test_get_occupation__should_return_empty_string_if_there_is_no_occupation(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual("", individual.get_occupation())

    def test_get_occupation__should_return_the_occupation_if_there_is_one(self):
        use_case = """
            0 @I1@ INDI
                1 NAME First /Last/
                1 OCCU Plumber
                1 SEX M
        """
        individual = self._parse_use_case_and_get_individual_element(use_case, "@I1@")
        self.assertEqual("Plumber", individual.get_occupation())

    # --------------------- START OF birth_year_match TESTING -----------------------

    _birth_year_match_use_case = """
        0 @I1@ INDI
            1 NAME First /Last/
            1 BIRT
                2 DATE April 1 1990
    """

    def test_birth_year_match__should_return_true_if_the_year_matches(self):
        individual = self._parse_use_case_and_get_individual_element(self._birth_year_match_use_case, "@I1@")
        self.assertTrue(individual.birth_year_match(1990))

    def test_birth_year_match__should_return_false_if_the_year_does_not_match(self):
        individual = self._parse_use_case_and_get_individual_element(self._birth_year_match_use_case, "@I1@")
        self.assertFalse(individual.birth_year_match(1800))

    # --------------------- START OF birth_range_match TESTING -----------------------

    _birth_range_match_use_case = """
        0 @I1@ INDI
            1 NAME First /Last/
            1 BIRT
                2 DATE April 1 1990
    """

    def test_birth_year_match__should_return_false_if_the_year_is_before_the_range(self):
        individual = self._parse_use_case_and_get_individual_element(self._birth_range_match_use_case, "@I1@")
        self.assertFalse(individual.birth_range_match(2000, 2100))

    def test_birth_year_match__should_return_true_if_the_year_is_in_the_range(self):
        individual = self._parse_use_case_and_get_individual_element(self._birth_range_match_use_case, "@I1@")
        self.assertTrue(individual.birth_range_match(1900, 2000))

    def test_birth_year_match__should_return_false_if_the_year_is_after_the_range(self):
        individual = self._parse_use_case_and_get_individual_element(self._birth_range_match_use_case, "@I1@")
        self.assertFalse(individual.birth_range_match(1800, 1900))

    # --------------------- START OF death_year_match TESTING -----------------------

    _death_year_match_use_case = """
        0 @I1@ INDI
            1 NAME First /Last/
            1 DEAT
                2 DATE April 1 1990
    """

    def test_death_year_match__should_return_true_if_the_year_matches(self):
        individual = self._parse_use_case_and_get_individual_element(self._death_year_match_use_case, "@I1@")
        self.assertTrue(individual.death_year_match(1990))

    def test_death_year_match__should_return_false_if_the_year_does_not_match(self):
        individual = self._parse_use_case_and_get_individual_element(self._death_year_match_use_case, "@I1@")
        self.assertFalse(individual.death_year_match(1800))

    # --------------------- START OF death_range_match TESTING -----------------------

    _death_range_match_use_case = """
        0 @I1@ INDI
            1 NAME First /Last/
            1 DEAT
                2 DATE April 1 1990
    """

    def test_death_year_match__should_return_false_if_the_year_is_before_the_range(self):
        individual = self._parse_use_case_and_get_individual_element(self._death_range_match_use_case, "@I1@")
        self.assertFalse(individual.death_range_match(2000, 2100))

    def test_death_year_match__should_return_true_if_the_year_is_in_the_range(self):
        individual = self._parse_use_case_and_get_individual_element(self._death_range_match_use_case, "@I1@")
        self.assertTrue(individual.death_range_match(1900, 2000))

    def test_death_year_match__should_return_false_if_the_year_is_after_the_range(self):
        individual = self._parse_use_case_and_get_individual_element(self._death_range_match_use_case, "@I1@")
        self.assertFalse(individual.death_range_match(1800, 1900))

    # --------------------- START OF criteria_match TESTING -----------------------

    _criteria_match_use_case = """
        0 @I1@ INDI
            1 NAME First /Last/
            1 BIRT
                2 DATE April 1 1990
            1 DEAT
                2 DATE Jun 21 1999
    """

    def test_criteria_match__should_match_on_matching_surname(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertTrue(individual.criteria_match("surname=Last"))

    def test_criteria_match__should_fail_to_match_on_matching_surname(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertFalse(individual.criteria_match("surname=NotAMatch"))

    def test_criteria_match__should_match_on_matching_given_name(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertTrue(individual.criteria_match("name=First"))

    def test_criteria_match__should_fail_to_match_on_matching_given_name(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertFalse(individual.criteria_match("name=NotAMatch"))

    def test_criteria_match__should_match_on_matching_birth_year(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertTrue(individual.criteria_match("birth=1990"))

    def test_criteria_match__should_fail_to_match_on_matching_birth_year(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertFalse(individual.criteria_match("birth=2127"))

    def test_criteria_match__should_fail_to_match_when_the_provided_birth_year_is_not_numeric(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertFalse(individual.criteria_match("birth=not_a_number"))

    def test_criteria_match__should_match_on_matching_birth_range(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertTrue(individual.criteria_match("birth_range=1900-2000"))

    def test_criteria_match__should_fail_to_match_on_non_matching_birth_range(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertFalse(individual.criteria_match("birth_range=2000-2100"))

    def test_criteria_match__should_fail_to_match_when_the_provided_birth_year_range_is_not_numeric(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertFalse(individual.criteria_match("birth_range=1900-not_a_number"))

    def test_criteria_match__should_fail_to_match_when_the_provided_birth_year_range_does_not_have_a_separator(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertFalse(individual.criteria_match("birth_range=not_a_number"))

    def test_criteria_match__should_match_on_matching_death_year(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertTrue(individual.criteria_match("death=1999"))

    def test_criteria_match__should_fail_to_match_on_matching_death_year(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertFalse(individual.criteria_match("death=2127"))

    def test_criteria_match__should_fail_to_match_when_the_provided_death_year_is_not_numeric(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertFalse(individual.criteria_match("death=not_a_number"))

    def test_criteria_match__should_match_on_matching_death_range(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertTrue(individual.criteria_match("death_range=1900-2000"))

    def test_criteria_match__should_fail_to_match_on_non_matching_death_range(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertFalse(individual.criteria_match("death_range=2000-2100"))

    def test_criteria_match__should_fail_to_match_when_the_provided_death_year_range_is_not_numeric(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertFalse(individual.criteria_match("death_range=1900-not_a_number"))

    def test_criteria_match__should_fail_to_match_when_the_provided_death_year_range_does_not_have_a_separator(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertFalse(individual.criteria_match("death_range=not_a_number"))

    def test_criteria_match__should_match_on_multiple_criteria(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertTrue(individual.criteria_match("name=First:surname=Last"))

    def test_criteria_match__should_not_match_when_single_criterion_is_missing_a_separator(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertFalse(individual.criteria_match("nameFirst"))

    def test_criteria_match__should_not_match_when_multiple_criteria_and_one__is_missing_a_separator(self):
        individual = self._parse_use_case_and_get_individual_element(self._criteria_match_use_case, "@I1@")
        self.assertFalse(individual.criteria_match("name=First:surnameLast"))

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
