"""GEDCOM element consisting of tag `gedcom.tags.GEDCOM_TAG_FAMILY`"""

from gedcom.element.element import Element
import gedcom.tags


class NotAnActualFamilyError(Exception):
    pass


class FamilyElement(Element):

    def get_tag(self):
        return gedcom.tags.GEDCOM_TAG_FAMILY

    def has_children(self):
        """Returns whether or not there is at least one child in this family.
        :rtype: boolean
        """
        return self._is_tag_present(gedcom.tags.GEDCOM_TAG_CHILD)
