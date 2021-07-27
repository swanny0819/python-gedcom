import unittest

from python_gedcom_2.element.element import Element

from python_gedcom_2.element.object import ObjectElement

from python_gedcom_2.element.individual import IndividualElement

from python_gedcom_2.element.file import FileElement

from python_gedcom_2.element.family import FamilyElement
from python_gedcom_2.element.root import RootElement


class TestElement(unittest.TestCase):

    # --------------------- START OF get_multi_line_value TESTING -----------------------

    # TODO: test_get_multi_line_value__should_get_single_line_multiline_value
    # TODO: test_get_multi_line_value__should_get_and_combine_multiline_values
    # TODO: test_get_multi_line_value__should_return_original_value_passed_into_set_multi_line_value

    # --------------------- START OF set_multi_line_value TESTING -----------------------

    def test_set_multi_line_value__should_take_single_line_value_and_put_it_in_value_of_this_element(self):
        root_element = RootElement()
        multiline_value = "This is a test value that is on a single line"
        root_element.set_multi_line_value(multiline_value)

        child_elements = root_element.get_child_elements()
        self.assertEqual(0, len(child_elements))
        self.assertEqual(multiline_value, root_element.get_value())

    def test_set_multi_line_value__should_take_multiline_value_and_create(self):
        root_element = RootElement()
        multiline_value = "This is a test value\n" \
                          "and so is this\n" \
                          "and this one too"
        root_element.set_multi_line_value(multiline_value)

        child_elements = root_element.get_child_elements()
        self.assertEqual(2, len(child_elements))
        self.assertEqual("This is a test value", root_element.get_value())

        self.assertEqual("and so is this", child_elements[0].get_value())
        self.assertEqual(0, child_elements[0].get_level())
        self.assertEqual("CONT", child_elements[0].get_tag())
        self.assertEqual("", child_elements[0].get_pointer())

        self.assertEqual("and this one too", child_elements[1].get_value())
        self.assertEqual(0, child_elements[1].get_level())
        self.assertEqual("CONT", child_elements[1].get_tag())
        self.assertEqual("", child_elements[1].get_pointer())

    def test_set_multi_line_value__should_remove_existing_value_and_concatenations_but_not_other_nodes(self):
        root_element = RootElement(value="original value")
        root_element.new_child_element("CONC", value="original concatenation")
        root_element.new_child_element("CONT", value="original continued")
        root_element.new_child_element("BIRT", value="1 JUN 2019")

        multiline_value = "This is a test value that is on a single line"
        root_element.set_multi_line_value(multiline_value)

        child_elements = root_element.get_child_elements()
        self.assertEqual(multiline_value, root_element.get_value())
        self.assertEqual(1, len(child_elements))
        self.assertEqual("1 JUN 2019", child_elements[0].get_value())

    # --------------------- START OF new_child_element TESTING -----------------------

    def test_new_child_element__should_create_a_child_family_element(self):
        root_element = RootElement()
        child_element = root_element.new_child_element("FAM", "@F1@")
        self.assertTrue(isinstance(child_element, FamilyElement), child_element)
        self.assertEqual(0, child_element.get_level())
        self.assertEqual("@F1@", child_element.get_pointer())
        self.assertEqual("", child_element.get_value())

    def test_new_child_element__should_create_a_child_file_element(self):
        root_element = RootElement()
        child_element = root_element.new_child_element("FILE", "@F1@")
        self.assertTrue(isinstance(child_element, FileElement), child_element)
        self.assertEqual(0, child_element.get_level())
        self.assertEqual("@F1@", child_element.get_pointer())
        self.assertEqual("", child_element.get_value())

    def test_new_child_element__should_create_a_child_individual_element(self):
        root_element = RootElement()
        child_element = root_element.new_child_element("INDI", "@I1@")
        self.assertTrue(isinstance(child_element, IndividualElement), child_element)
        self.assertEqual(0, child_element.get_level())
        self.assertEqual("@I1@", child_element.get_pointer())
        self.assertEqual("", child_element.get_value())

    def test_new_child_element__should_create_a_child_object_element(self):
        root_element = RootElement()
        child_element = root_element.new_child_element("OBJE", "@O1@")
        self.assertTrue(isinstance(child_element, ObjectElement), child_element)
        self.assertEqual(0, child_element.get_level())
        self.assertEqual("@O1@", child_element.get_pointer())
        self.assertEqual("", child_element.get_value())

    # --------------------- START OF to_gedcom_string TESTING -----------------------

    def test_to_gedcom_string__should_combine_only_the_mandatory_values_non_recursively_for_an_indi_nodes_values(self):
        element = Element(level=0, pointer="@I1@", tag="INDI", value="")
        self.assertEqual("0 @I1@ INDI\n", element.to_gedcom_string())

    def test_to_gedcom_string__should_combine_only_the_mandatory_values_non_recursively_for_a_date_nodes_values(self):
        element = Element(level=2, pointer="", tag="DATE", value="JUN 1 1990")
        self.assertEqual("2 DATE JUN 1 1990\n", element.to_gedcom_string())

    def test_to_gedcom_string__should_combine_only_the_mandatory_values_recursively_for_an_indi_nodes_values(self):
        element = Element(level=0, pointer="@I1@", tag="INDI", value="")
        element.new_child_element("NAME", value="First /Last/")
        birth_element = element.new_child_element("BIRT")
        birth_element.new_child_element("DATE", value="JUN 2 1876")
        expected_string = \
            "0 @I1@ INDI\n" \
            "1 NAME First /Last/\n" \
            "1 BIRT\n" \
            "2 DATE JUN 2 1876\n"
        self.assertEqual(expected_string, element.to_gedcom_string(recursive=True))

    # TODO: test_to_gedcom_string__should_
    # TODO: test_to_gedcom_string__should_
    # TODO: test_to_gedcom_string__should_
    # TODO: test_to_gedcom_string__should_
