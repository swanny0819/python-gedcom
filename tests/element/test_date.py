import unittest

import python_gedcom_2.tags

from python_gedcom_2.element.date import DateElement, RETURN_FIRST_DATE


class TestDateElement(unittest.TestCase):

    # --------------------- START OF get_year TESTING of DATE_APPROXIMATED formats (pg 39 of the GEDCOM 5.5 spec) -----------------------

    def test_get_year__should_remove_about_string_from_a_year(self):
        date_element = DateElement(level=2, pointer="", tag=python_gedcom_2.tags.GEDCOM_TAG_DATE, value="ABT 1924")
        self.assertEqual(1924, date_element.get_year())

    def test_get_year__should_remove_calculated_string_from_a_year(self):
        date_element = DateElement(level=2, pointer="", tag=python_gedcom_2.tags.GEDCOM_TAG_DATE, value="CAL 1924")
        self.assertEqual(1924, date_element.get_year())

    def test_get_year__should_remove_estimated_string_from_a_year(self):
        date_element = DateElement(level=2, pointer="", tag=python_gedcom_2.tags.GEDCOM_TAG_DATE, value="EST 1924")
        self.assertEqual(1924, date_element.get_year())

    # --------------------- START OF get_year TESTING of DATE_EXACT formats (pg 40 of the GEDCOM 5.5 spec) -----------------------

    def test_get_year__should_remove_month_string_from_a_year(self):
        date_element = DateElement(level=2, pointer="", tag=python_gedcom_2.tags.GEDCOM_TAG_DATE, value="JUN 1924")
        self.assertEqual(1924, date_element.get_year())

    def test_get_year__should_remove_day_and_month_string_from_a_year(self):
        date_element = DateElement(level=2, pointer="", tag=python_gedcom_2.tags.GEDCOM_TAG_DATE, value="5 JUN 1924")
        self.assertEqual(1924, date_element.get_year())

    # --------------------- START OF get_year TESTING of DATE_PERIOD formats (pg 41 of the GEDCOM 5.5 spec) -----------------------

    def test_get_year__should_remove_everything_but_last_year_when_provided_date_period(self):
        date_element = DateElement(level=2, pointer="", tag=python_gedcom_2.tags.GEDCOM_TAG_DATE, value="FROM 5 JUN 1924 TO 1 JAN 1985")
        self.assertEqual(1985, date_element.get_year())

    # --------------------- START OF get_year TESTING of DATE_RANGE formats (pg 41-42 of the GEDCOM 5.5 spec) -----------------------

    def test_get__year__should_remove_after_string_from_a_year(self):
        date_element = DateElement(level=2, pointer="", tag=python_gedcom_2.tags.GEDCOM_TAG_DATE, value="AFT 1985")
        self.assertEqual(1985, date_element.get_year())

    def test_get__year__should_remove_before_string_from_a_year(self):
        date_element = DateElement(level=2, pointer="", tag=python_gedcom_2.tags.GEDCOM_TAG_DATE, value="BEF 1985")
        self.assertEqual(1985, date_element.get_year())

    def test_get_year__should_remove_everything_but_last_year_when_provided_between_string(self):
        date_element = DateElement(level=2, pointer="", tag=python_gedcom_2.tags.GEDCOM_TAG_DATE, value="BET 1920 AND 1985")
        self.assertEqual(1985, date_element.get_year())

    def test_get_year__should_remove_everything_but_first_year_when_provided_between_string_and_we_specify_first_year(self):
        date_element = DateElement(level=2, pointer="", tag=python_gedcom_2.tags.GEDCOM_TAG_DATE, value="BET 1920 AND 1985")
        self.assertEqual(1920, date_element.get_year(RETURN_FIRST_DATE))

    def test_get_year__should_remove_everything_but_first_year_when_provided_from_string_and_we_specify_first_year(self):
        date_element = DateElement(level=2, pointer="", tag=python_gedcom_2.tags.GEDCOM_TAG_DATE, value="FROM 1920 TO 1985")
        self.assertEqual(1920, date_element.get_year(RETURN_FIRST_DATE))

    def test_get_year__should_handle_case_where_there_is_no_year(self):
        date_element = DateElement(level=2, pointer="", tag=python_gedcom_2.tags.GEDCOM_TAG_DATE, value="")
        self.assertEqual(-1, date_element.get_year())

    def test_get_year__should_handle_case_where_there_is_no_year_but_there_is_white_space(self):
        date_element = DateElement(level=2, pointer="", tag=python_gedcom_2.tags.GEDCOM_TAG_DATE, value="  ")
        self.assertEqual(-1, date_element.get_year())

    def test_get_year__should_handle_case_where_year_cannot_be_parsed(self):
        date_element = DateElement(level=2, pointer="", tag=python_gedcom_2.tags.GEDCOM_TAG_DATE, value="banana")
        self.assertEqual(-1, date_element.get_year())
