"""
Base GEDCOM element
"""

from sys import version_info

from python_gedcom_2.element_creator import ElementCreator
from python_gedcom_2.helpers import deprecated
import python_gedcom_2.tags


class Element(object):
    """GEDCOM element

    Each line in a GEDCOM file is an element with the format

    `level [pointer] tag [value]`

    where `level` and `tag` are required, and `pointer` and `value` are
    optional.  Elements are arranged hierarchically according to their
    level, and elements with a level of zero are at the top level.
    Elements with a level greater than zero are children of their
    parent.

    A pointer has the format `@pname@`, where `pname` is any sequence of
    characters and numbers. The pointer identifies the object being
    pointed to, so that any pointer included as the value of any
    element points back to the original object.  For example, an
    element may have a `FAMS` tag whose value is `@F1@`, meaning that this
    element points to the family record in which the associated person
    is a spouse. Likewise, an element with a tag of `FAMC` has a value
    that points to a family record in which the associated person is a
    child.

    See a GEDCOM file for examples of tags and their values.

    Tags available to an element are seen here: `gedcom.tags`
    """

    def __init__(self, level, pointer, tag, value, crlf="\n", multi_line=True):
        # basic element info
        self.__level = level
        self.__pointer = pointer
        self.__tag = tag
        self.__value = value
        self.__crlf = crlf

        # structuring
        self.__children = []
        self.__parent = None

        if multi_line:
            self.set_multi_line_value(value)

    def get_level(self):
        """Returns the level of this element from within the GEDCOM file
        :rtype: int
        """
        return self.__level

    def get_pointer(self):
        """Returns the pointer of this element from within the GEDCOM file
        :rtype: str
        """
        return self.__pointer

    def get_tag(self):
        """Returns the tag of this element from within the GEDCOM file
        :rtype: str
        """
        return self.__tag

    def get_value(self):
        """Return the value of this element from within the GEDCOM file
        :rtype: str
        """
        return self.__value

    def set_value(self, value):
        """Sets the value of this element
        :type value: str
        """
        self.__value = value

    def get_multi_line_value(self):
        """Returns the value of this element including concatenations or continuations
        :rtype: str
        """
        result = self.get_value()
        last_crlf = self.__crlf
        for element in self.get_child_elements():
            tag = element.get_tag()
            if tag == python_gedcom_2.tags.GEDCOM_TAG_CONCATENATION:
                result += element.get_value()
                last_crlf = element.__crlf
            elif tag == python_gedcom_2.tags.GEDCOM_TAG_CONTINUED:
                result += last_crlf + element.get_value()
                last_crlf = element.__crlf
        return result

    def __available_characters(self):
        """Get the number of available characters of the elements original string
        :rtype: int
        """
        element_characters = len(self.to_gedcom_string())
        return 0 if element_characters > 255 else 255 - element_characters

    def __line_length(self, line):
        """@TODO Write docs.
        :type line: str
        :rtype: int
        """
        total_characters = len(line)
        available_characters = self.__available_characters()
        if total_characters <= available_characters:
            return total_characters
        spaces = 0
        while spaces < available_characters and line[available_characters - spaces - 1] == ' ':
            spaces += 1
        if spaces == available_characters:
            return available_characters
        return available_characters - spaces

    def __set_bounded_value(self, value):
        """@TODO Write docs.
        :type value: str
        :rtype: int
        """
        line_length = self.__line_length(value)
        self.set_value(value[:line_length])
        return line_length

    def __add_bounded_child(self, tag, value):
        """@TODO Write docs.
        :type tag: str
        :type value: str
        :rtype: int
        """
        child = self.new_child_element(tag)
        return child.__set_bounded_value(value)

    def __add_concatenation(self, string):
        """@TODO Write docs.
        :rtype: str
        """
        index = 0
        size = len(string)
        while index < size:
            index += self.__add_bounded_child(python_gedcom_2.tags.GEDCOM_TAG_CONCATENATION, string[index:])

    def set_multi_line_value(self, value):
        """Sets the value of this element, adding concatenation and continuation lines when necessary
        :type value: str
        """
        self.set_value('')
        self.__children = [child for child in self.get_child_elements() if
                           child.get_tag() not in (python_gedcom_2.tags.GEDCOM_TAG_CONCATENATION, python_gedcom_2.tags.GEDCOM_TAG_CONTINUED)]

        lines = value.splitlines()
        if lines:
            line = lines.pop(0)
            n = self.__set_bounded_value(line)
            self.__add_concatenation(line[n:])

            for line in lines:
                n = self.__add_bounded_child(python_gedcom_2.tags.GEDCOM_TAG_CONTINUED, line)
                self.__add_concatenation(line[n:])

    def get_child_elements(self):
        """Returns the direct child elements of this element
        :rtype: list of Element
        """
        return self.__children

    def new_child_element(self, tag, pointer="", value=""):
        """Creates and returns a new child element of this element

        :type tag: str
        :type pointer: str
        :type value: str
        :rtype: Element
        """
        child_element = ElementCreator.create_element(self.get_level() + 1, pointer, tag, value, self.__crlf)
        self.add_child_element(child_element)
        return child_element

    def add_child_element(self, element):
        """Adds a child element to this element

        :type element: Element
        """
        self.get_child_elements().append(element)
        element.set_parent_element(self)

        return element

    def get_parent_element(self):
        """Returns the parent element of this element
        :rtype: Element
        """
        return self.__parent

    def set_parent_element(self, element):
        """Adds a parent element to this element

        There's usually no need to call this method manually,
        `add_child_element()` calls it automatically.

        :type element: Element
        """
        self.__parent = element

    def _is_tag_present(self, tag):
        for child in self.get_child_elements():
            if child.get_tag() == tag:
                return True
        return False

    @deprecated
    def get_individual(self):
        """Returns this element and all of its sub-elements represented as a GEDCOM string
        ::deprecated:: As of version 1.0.0 use `to_gedcom_string()` method instead
        :rtype: str
        """
        return self.to_gedcom_string(True)

    def to_gedcom_string(self, recursive=False):
        """Formats this element and optionally all of its sub-elements into a GEDCOM string
        :type recursive: bool
        :rtype: str
        """

        result = str(self.get_level())

        if self.get_pointer() != "":
            result += ' ' + self.get_pointer()

        result += ' ' + self.get_tag()

        if self.get_value() != "":
            result += ' ' + self.get_value()

        result += self.__crlf

        if self.get_level() < 0:
            result = ''

        if recursive:
            for child_element in self.get_child_elements():
                result += child_element.to_gedcom_string(True)

        return result

    def __str__(self):
        """:rtype: str"""
        if version_info[0] >= 3:
            return self.to_gedcom_string()

        return self.to_gedcom_string().encode('utf-8-sig')
