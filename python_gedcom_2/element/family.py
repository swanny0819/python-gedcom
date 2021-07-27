"""GEDCOM element consisting of tag `gedcom.tags.GEDCOM_TAG_FAMILY`"""

from python_gedcom_2.element.element import Element
import python_gedcom_2.tags


class NotAnActualFamilyError(Exception):
    pass


class FamilyElement(Element):

    def get_tag(self):
        return python_gedcom_2.tags.GEDCOM_TAG_FAMILY

    def has_children(self):
        """Returns whether or not there is at least one child in this family.
        :rtype: boolean
        """
        return self._is_tag_present(python_gedcom_2.tags.GEDCOM_TAG_CHILD)
