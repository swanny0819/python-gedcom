import unittest

from gedcom.element.individual import IndividualElement


class TestIndividualElement(unittest.TestCase):
    def test_get_all_names__should_be_able_to_match_multiple_names_but_not_non_names(self):
        element = IndividualElement(level=0, pointer="@I5@", tag="INDI", value="")
        element.new_child_element(tag="NAME", value="First /Last/")
        element.new_child_element(tag="SEX", value="M")
        birth = element.new_child_element(tag="BIRT", value="")
        birth.new_child_element(tag="DATE", value="1 JAN 1900")
        element.new_child_element(tag="NAME", value="Second /Surname/")

        all_names = element.get_all_names()
        self.assertEqual(2, len(all_names))
        self.assertEqual('First /Last/', all_names[0])
        self.assertEqual('Second /Surname/', all_names[1])
