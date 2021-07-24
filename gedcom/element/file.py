"""GEDCOM element consisting of tag `gedcom.tags.GEDCOM_TAG_FILE`"""

from gedcom.element.element import Element


class NotAnActualFileError(Exception):
    pass


class FileElement(Element):
    pass
