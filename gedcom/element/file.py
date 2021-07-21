"""GEDCOM element consisting of tag `gedcom.tags.GEDCOM_TAG_FILE`"""

from gedcom.element.element import Element
import gedcom.tags


class NotAnActualFileError(Exception):
    pass


class FileElement(Element):

    def get_tag(self):
        return gedcom.tags.GEDCOM_TAG_FILE
