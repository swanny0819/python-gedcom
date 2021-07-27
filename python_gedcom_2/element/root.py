"""Virtual GEDCOM root element containing all logical records as children"""

from python_gedcom_2.element.element import Element


class RootElement(Element):
    """Virtual GEDCOM root element containing all logical records as children"""

    def __init__(self, level=-1, pointer="", tag="ROOT", value="", crlf="\n", multi_line=True):
        super(RootElement, self).__init__(level, pointer, tag, value, crlf, multi_line)
