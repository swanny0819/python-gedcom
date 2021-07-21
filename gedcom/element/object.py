"""GEDCOM element consisting of tag `gedcom.tags.GEDCOM_TAG_OBJECT`"""

from gedcom.element.element import Element
import gedcom.tags


class NotAnActualObjectError(Exception):
    pass


class ObjectElement(Element):

    def is_object(self):
        """Checks if this element is an actual object
        :rtype: bool
        """
        return self.get_tag() == gedcom.tags.GEDCOM_TAG_OBJECT
