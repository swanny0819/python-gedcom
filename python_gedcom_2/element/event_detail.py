from python_gedcom_2.element.date import DateElement
from python_gedcom_2.element.element import Element


class EventDetail(Element):
    """
    An EventDetail can be one of many kinds of actual Element. This is an abstract class to contain a lot of shared methods.
    (See page 29 of the GEDCOM 5.5 spec for details)
    NOTE: This is different from an event element, which is a legitimate GEDCOM tag and has its own rules.
    """

    def get_year_in_date(self):
        date = -1

        for child in self.get_child_elements():
            if isinstance(child, DateElement):
                date = child.get_year()

        return date
