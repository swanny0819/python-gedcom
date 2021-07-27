"""GEDCOM element consisting of tag `gedcom.tags.GEDCOM_TAG_OBJECT`"""

from python_gedcom_2.element.element import Element
import python_gedcom_2.tags


class NotAnActualObjectError(Exception):
    pass


class ObjectElement(Element):

    def is_object(self):
        """Checks if this element is an actual object
        :rtype: bool
        """
        return self.get_tag() == python_gedcom_2.tags.GEDCOM_TAG_OBJECT
