"""GEDCOM element consisting of tag `gedcom.tags.GEDCOM_TAG_INDIVIDUAL`"""

import re as regex

from python_gedcom_2.element.birth import BirthElement
from python_gedcom_2.element.death import DeathElement
from python_gedcom_2.element.element import Element
from python_gedcom_2.element.event_detail import EventDetail
from python_gedcom_2.helpers import deprecated
import python_gedcom_2.tags


class NotAnActualIndividualError(Exception):
    pass


class IndividualElement(Element):

    def get_tag(self):
        return python_gedcom_2.tags.GEDCOM_TAG_INDIVIDUAL

    def is_deceased(self):
        """Checks if this individual is deceased
        :rtype: bool
        """
        return self._is_tag_present(python_gedcom_2.tags.GEDCOM_TAG_DEATH)

    def is_child(self):
        """Checks if this element is a child of a family
        :rtype: bool
        """
        return self._is_tag_present(python_gedcom_2.tags.GEDCOM_TAG_FAMILY_CHILD)

    def is_spouse(self):
        """Checks if this element is a spouse in a family
        :rtype: bool
        """
        return self._is_tag_present(python_gedcom_2.tags.GEDCOM_TAG_FAMILY_SPOUSE)

    def is_private(self):
        """Checks if this individual is marked private
        :rtype: bool
        """
        for child in self.get_child_elements():
            if child.get_tag() == python_gedcom_2.tags.GEDCOM_TAG_PRIVATE:
                private = child.get_value()
                if private == 'Y':
                    return True

        return False

    def get_name(self):
        """Returns an individual's names as a tuple: (`str` given_name, `str` surname)
        If this person has a suffix (e.g., 'Jr') it gets removed entirely.
        :rtype: tuple
        """
        given_name = ""
        surname = ""

        # Return the first gedcom.tags.GEDCOM_TAG_NAME that is found.
        # Alternatively as soon as we have both the gedcom.tags.GEDCOM_TAG_GIVEN_NAME and _SURNAME return those.
        found_given_name = False
        found_surname_name = False

        for child in self.get_child_elements():
            if child.get_tag() == python_gedcom_2.tags.GEDCOM_TAG_NAME:
                # Some GEDCOM files don't use child tags but instead
                # place the name in the value of the NAME tag.
                if child.get_value() != "":
                    name = child.get_value().split('/')

                    if len(name) > 0:
                        given_name = name[0].strip()
                        if len(name) > 1:
                            surname = name[1].strip()

                    return given_name, surname

                for childOfChild in child.get_child_elements():

                    if childOfChild.get_tag() == python_gedcom_2.tags.GEDCOM_TAG_GIVEN_NAME:
                        given_name = childOfChild.get_value()
                        found_given_name = True

                    if childOfChild.get_tag() == python_gedcom_2.tags.GEDCOM_TAG_SURNAME:
                        surname = childOfChild.get_value()
                        found_surname_name = True

                if found_given_name and found_surname_name:
                    return given_name, surname

        # If we reach here we are probably returning empty strings
        return given_name, surname

    def get_all_names(self):
        return [a.get_value() for a in self.get_child_elements() if a.get_tag() == python_gedcom_2.tags.GEDCOM_TAG_NAME]

    def surname_match(self, surname_to_match):
        """Matches a string with the surname of an individual
        :type surname_to_match: str
        :rtype: bool
        """
        (given_name, surname) = self.get_name()
        return regex.search(surname_to_match, surname, regex.IGNORECASE)

    @deprecated
    def given_match(self, name):
        """Matches a string with the given name of an individual
        ::deprecated:: As of version 1.0.0 use `given_name_match()` method instead
        :type name: str
        :rtype: bool
        """
        return self.given_name_match(name)

    def given_name_match(self, given_name_to_match):
        """Matches a string with the given name of an individual
        :type given_name_to_match: str
        :rtype: bool
        """
        (given_name, surname) = self.get_name()
        return regex.search(given_name_to_match, given_name, regex.IGNORECASE)

    def get_gender(self):
        """Returns the gender of a person in string format
        :rtype: str
        """
        gender = ""

        for child in self.get_child_elements():
            if child.get_tag() == python_gedcom_2.tags.GEDCOM_TAG_SEX:
                gender = child.get_value()

        return gender

    def __get_data_for_date_bearing_tag(self, tag):
        date = ""
        place = ""
        sources = []

        for child in self.get_child_elements():
            if child.get_tag() == tag:
                for childOfChild in child.get_child_elements():

                    if childOfChild.get_tag() == python_gedcom_2.tags.GEDCOM_TAG_DATE:
                        date = childOfChild.get_value()

                    if childOfChild.get_tag() == python_gedcom_2.tags.GEDCOM_TAG_PLACE:
                        place = childOfChild.get_value()

                    if childOfChild.get_tag() == python_gedcom_2.tags.GEDCOM_TAG_SOURCE:
                        sources.append(childOfChild.get_value())

        return date, place, sources

    def get_birth_data(self):
        """Returns the birth data of a person formatted as a tuple: (`str` date, `str` place, `list` sources)
        :rtype: tuple
        """
        return self.__get_data_for_date_bearing_tag(python_gedcom_2.tags.GEDCOM_TAG_BIRTH)

    def get_death_data(self):
        """Returns the death data of a person formatted as a tuple: (`str` date, `str` place, `list` sources)
        :rtype: tuple
        """
        return self.__get_data_for_date_bearing_tag(python_gedcom_2.tags.GEDCOM_TAG_DEATH)

    def __get_year_in_element(self, element_class):
        year = -1
        for child in self.get_child_elements():
            if isinstance(child, EventDetail) and isinstance(child, element_class):
                year = child.get_year_in_date()
        return year

    def get_birth_year(self):
        """Returns the birth year of a person in integer format
        :rtype: int
        """
        return self.__get_year_in_element(BirthElement)

    def get_death_year(self):
        """Returns the death year of a person in integer format
        :rtype: int
        """
        return self.__get_year_in_element(DeathElement)

    @deprecated
    def get_burial(self):
        """Returns the burial data of a person formatted as a tuple: (`str` date, `str´ place, `list` sources)
        ::deprecated:: As of version 1.0.0 use `get_burial_data()` method instead
        :rtype: tuple
        """
        self.get_burial_data()

    def get_burial_data(self):
        """Returns the burial data of a person formatted as a tuple: (`str` date, `str´ place, `list` sources)
        :rtype: tuple
        """
        return self.__get_data_for_date_bearing_tag(python_gedcom_2.tags.GEDCOM_TAG_BURIAL)

    @deprecated
    def get_census(self):
        """Returns a list of censuses of an individual formatted as tuples: (`str` date, `str´ place, `list` sources)
        ::deprecated:: As of version 1.0.0 use `get_census_data()` method instead
        :rtype: list of tuple
        """
        self.get_census_data()

    def get_census_data(self):
        """Returns a list of censuses of an individual formatted as tuples: (`str` date, `str´ place, `list` sources)
        :rtype: list of tuple
        """
        census = []

        for child in self.get_child_elements():
            if child.get_tag() == python_gedcom_2.tags.GEDCOM_TAG_CENSUS:

                date = ''
                place = ''
                sources = []

                for childOfChild in child.get_child_elements():

                    if childOfChild.get_tag() == python_gedcom_2.tags.GEDCOM_TAG_DATE:
                        date = childOfChild.get_value()

                    if childOfChild.get_tag() == python_gedcom_2.tags.GEDCOM_TAG_PLACE:
                        place = childOfChild.get_value()

                    if childOfChild.get_tag() == python_gedcom_2.tags.GEDCOM_TAG_SOURCE:
                        sources.append(childOfChild.get_value())

                census.append((date, place, sources))

        return census

    def get_last_change_date(self):
        """Returns the date of when the person data was last changed formatted as a string
        :rtype: str
        """
        date = ""

        for child in self.get_child_elements():
            if child.get_tag() == python_gedcom_2.tags.GEDCOM_TAG_CHANGE:
                for childOfChild in child.get_child_elements():
                    if childOfChild.get_tag() == python_gedcom_2.tags.GEDCOM_TAG_DATE:
                        date = childOfChild.get_value()

        return date

    def get_occupation(self):
        """Returns the occupation of a person
        :rtype: str
        """
        occupation = ""

        for child in self.get_child_elements():
            if child.get_tag() == python_gedcom_2.tags.GEDCOM_TAG_OCCUPATION:
                occupation = child.get_value()

        return occupation

    def birth_year_match(self, year):
        """Returns `True` if the given year matches the birth year of this person
        :type year: int
        :rtype: bool
        """
        return self.get_birth_year() == year

    def birth_range_match(self, from_year, to_year):
        """Checks if the birth year of a person lies within the given range
        :type from_year: int
        :type to_year: int
        :rtype: bool
        """
        birth_year = self.get_birth_year()

        if from_year <= birth_year <= to_year:
            return True

        return False

    def death_year_match(self, year):
        """Returns `True` if the given year matches the death year of this person
        :type year: int
        :rtype: bool
        """
        return self.get_death_year() == year

    def death_range_match(self, from_year, to_year):
        """Checks if the death year of a person lies within the given range
        :type from_year: int
        :type to_year: int
        :rtype: bool
        """
        death_year = self.get_death_year()

        if from_year <= death_year <= to_year:
            return True

        return False

    def criteria_match(self, criteria):
        """Checks if this individual matches all of the given criteria

        `criteria` is a colon-separated list, where each item in the
        list has the form [name]=[value]. The following criteria are supported:

        surname=[name]
             Match a person with [name] in any part of the `surname`.
        given_name=[given_name]
             Match a person with [given_name] in any part of the given `given_name`.
        birth=[year]
             Match a person whose birth year is a four-digit [year].
        birth_range=[from_year-to_year]
             Match a person whose birth year is in the range of years from
             [from_year] to [to_year], including both [from_year] and [to_year].
        death=[year]
             Match a person whose death year is a four-digit [year].
        death_range=[from_year-to_year]
             Match a person whose death year is in the range of years from
             [from_year] to [to_year], including both [from_year] and [to_year].

        :type criteria: str
        :rtype: bool
        """

        match = True

        # Check if criteria is a valid criteria and can be split by `:` and `=` characters
        if ":" in criteria:
            for criterion in criteria.split(':'):
                if "=" not in criterion:
                    return False
        else:
            if "=" not in criteria:
                return False

        for criterion in criteria.split(':'):
            key, value = criterion.split('=')

            if key == "surname" and not self.surname_match(value):
                match = False
            elif key == "name" and not self.given_name_match(value):
                match = False
            elif key == "birth":

                try:
                    year = int(value)
                    if not self.birth_year_match(year):
                        match = False
                except ValueError:
                    match = False

            elif key == "birth_range":

                try:
                    from_year, to_year = value.split('-')
                    from_year = int(from_year)
                    to_year = int(to_year)
                    if not self.birth_range_match(from_year, to_year):
                        match = False
                except ValueError:
                    match = False

            elif key == "death":

                try:
                    year = int(value)
                    if not self.death_year_match(year):
                        match = False
                except ValueError:
                    match = False

            elif key == "death_range":

                try:
                    from_year, to_year = value.split('-')
                    from_year = int(from_year)
                    to_year = int(to_year)
                    if not self.death_range_match(from_year, to_year):
                        match = False
                except ValueError:
                    match = False

        return match
