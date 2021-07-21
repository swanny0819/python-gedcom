"""GEDCOM element consisting of tag `gedcom.tags.GEDCOM_TAG_FAMILY`"""

from gedcom.element.element import Element
import gedcom.tags


class NotAnActualFamilyError(Exception):
    pass


class FamilyElement(Element):

    def get_tag(self):
        return gedcom.tags.GEDCOM_TAG_FAMILY
