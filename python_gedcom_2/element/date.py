"""GEDCOM element consisting of tag `gedcom.tags.GEDCOM_TAG_DATE`"""

from python_gedcom_2.element.element import Element


RETURN_FIRST_DATE = "first"
RETURN_SECOND_DATE = "second"


class DateElement(Element):
    @staticmethod
    def __is_a_from_to_statement(date_value):
        return date_value.startswith("FROM ") and " TO " in date_value

    @staticmethod
    def __is_a_between_and_statement(date_value):
        return date_value.startswith("BET ") and " AND " in date_value

    @classmethod
    def __contains_multiple_dates(cls, date_value):
        """
        Checks to see if the date string provided follows any of the known patterns for date ranges.
        :type date_value: string
        :rtype: boolean
        """
        if cls.__is_a_between_and_statement(date_value):
            return True
        elif cls.__is_a_from_to_statement(date_value):
            return True
        else:
            return False

    @classmethod
    def __split_date_range(cls, date_value):
        """
        Gets the date info out of the provided range.
        Ex: Turns "BET 1920 AND 1985" into ["1920", "1985"]
        NOTE: We assume what we're being passed in here has already had leading and trailing white space trimmed.
        If it hasn't, you may not get just dates.
        :type date_value: string
        :rtype: list of string
        """
        if cls.__is_a_between_and_statement(date_value):
            date_value = date_value[4:]
            return date_value.split(" AND ")
        elif cls.__is_a_from_to_statement(date_value):
            date_value = date_value[5:]
            return date_value.split(" TO ")

    def get_year(self, which_date_to_return_in_a_range=RETURN_SECOND_DATE):
        """
        Tries to identify the year associated with this date. If it can't, returns -1. In the event
        NOTE: By default, this will return the later year in a date range (ex: 1932 for "BET 1922 AND 1932").
        Since this was the behavior of the code that uses this method before it was refactored into
        a separate DateElement class, I'm keeping that implementation for backwards compatibility.
        :type which_date_to_return_in_a_range: string
        :rtype: int
        """
        date_value = self.get_value().strip()

        if self.__contains_multiple_dates(date_value):
            first_date, second_date = self.__split_date_range(date_value)
            print(first_date, second_date)
            if which_date_to_return_in_a_range == RETURN_FIRST_DATE:
                date_value = first_date
            else:
                date_value = second_date

        date_parts = date_value.split()
        if len(date_parts) == 0:
            date = ""
        else:
            date = date_parts[len(date_parts) - 1]

        if date == "":
            return -1
        try:
            return int(date)
        except ValueError:
            return -1
