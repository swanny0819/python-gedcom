import importlib
import re

import python_gedcom_2
import python_gedcom_2.tags


class ElementCreator:
    @staticmethod
    def _get_file_name_from_class_name(class_name):
        capitalized_words_in_class_name = re.findall('[A-Z][^A-Z]*', class_name)
        capitalized_words_without_element_string_at_end = capitalized_words_in_class_name[:-1]
        return "_".join(capitalized_words_without_element_string_at_end).lower()

    @classmethod
    def create_element(cls, level, pointer, tag, value, linebreak, is_multiline=True):
        from python_gedcom_2.element.element import Element

        tag_element_dict = {
            python_gedcom_2.tags.GEDCOM_TAG_ADOPTION: "AdoptionElement",
            python_gedcom_2.tags.GEDCOM_TAG_ADULT_CHRISTENING: "AdultChristeningElement",
            python_gedcom_2.tags.GEDCOM_TAG_ANNULMENT: "AnnulmentElement",
            python_gedcom_2.tags.GEDCOM_TAG_BAPTISM: "BaptismElement",
            python_gedcom_2.tags.GEDCOM_TAG_BAR_MITZVAH: "BarMitzvahElement",
            python_gedcom_2.tags.GEDCOM_TAG_BAS_MITZVAH: "BasMitzvahElement",
            python_gedcom_2.tags.GEDCOM_TAG_BIRTH: "BirthElement",
            python_gedcom_2.tags.GEDCOM_TAG_BLESSING: "BlessingElement",
            python_gedcom_2.tags.GEDCOM_TAG_BURIAL: "BurialElement",
            python_gedcom_2.tags.GEDCOM_TAG_CASTE: "CasteElement",
            python_gedcom_2.tags.GEDCOM_TAG_CENSUS: "CensusElement",
            python_gedcom_2.tags.GEDCOM_TAG_CHILDREN_COUNT: "ChildrenCountElement",
            python_gedcom_2.tags.GEDCOM_TAG_CHRISTENING: "ChristeningElement",
            python_gedcom_2.tags.GEDCOM_TAG_CONFIRMATION: "ConfirmationElement",
            python_gedcom_2.tags.GEDCOM_TAG_CREMATION: "CremationElement",
            python_gedcom_2.tags.GEDCOM_TAG_DATE: "DateElement",
            python_gedcom_2.tags.GEDCOM_TAG_DEATH: "DeathElement",
            python_gedcom_2.tags.GEDCOM_TAG_DIVORCE: "DivorceElement",
            python_gedcom_2.tags.GEDCOM_TAG_DIVORCE_FILED: "DivorceFiledElement",
            python_gedcom_2.tags.GEDCOM_TAG_EDUCATION: "EducationElement",
            python_gedcom_2.tags.GEDCOM_TAG_EMIGRATION: "EmigrationElement",
            python_gedcom_2.tags.GEDCOM_TAG_ENGAGEMENT: "EngagementElement",
            python_gedcom_2.tags.GEDCOM_TAG_EVENT: "EventElement",
            python_gedcom_2.tags.GEDCOM_TAG_FAMILY: "FamilyElement",
            python_gedcom_2.tags.GEDCOM_TAG_FILE: "FileElement",
            python_gedcom_2.tags.GEDCOM_TAG_FIRST_COMMUNION: "FirstCommunionElement",
            python_gedcom_2.tags.GEDCOM_TAG_GRADUATION: "GraduationElement",
            python_gedcom_2.tags.GEDCOM_TAG_IDENTIFICATION_NUMBER: "IdentificationNumberElement",
            python_gedcom_2.tags.GEDCOM_TAG_IMMIGRATION: "ImmigrationElement",
            python_gedcom_2.tags.GEDCOM_TAG_INDIVIDUAL: "IndividualElement",
            python_gedcom_2.tags.GEDCOM_TAG_MARRIAGE: "MarriageElement",
            python_gedcom_2.tags.GEDCOM_TAG_MARRIAGE_BANN: "MarriageBannElement",
            python_gedcom_2.tags.GEDCOM_TAG_MARRIAGE_CONTRACT: "MarriageContractElement",
            python_gedcom_2.tags.GEDCOM_TAG_MARRIAGE_COUNT: "MarriageCountElement",
            python_gedcom_2.tags.GEDCOM_TAG_MARRIAGE_LICENSE: "MarriageLicenseElement",
            python_gedcom_2.tags.GEDCOM_TAG_MARRIAGE_SETTLEMENT: "MarriageSettlementElement",
            python_gedcom_2.tags.GEDCOM_TAG_NATIONALITY: "NationalityElement",
            python_gedcom_2.tags.GEDCOM_TAG_NATURALIZATION: "NaturalizationElement",
            python_gedcom_2.tags.GEDCOM_TAG_OBJECT: "ObjectElement",
            python_gedcom_2.tags.GEDCOM_TAG_OCCUPATION: "OccupationElement",
            python_gedcom_2.tags.GEDCOM_TAG_ORDINATION: "OrdinationElement",
            python_gedcom_2.tags.GEDCOM_TAG_PHYSICAL_DESCRIPTION: "PhysicalDescriptionElement",
            python_gedcom_2.tags.GEDCOM_TAG_PROBATE: "ProbateElement",
            python_gedcom_2.tags.GEDCOM_TAG_PROPERTY: "PropertyElement",
            python_gedcom_2.tags.GEDCOM_TAG_RELIGION: "ReligionElement",
            python_gedcom_2.tags.GEDCOM_TAG_RESIDENCE: "ResidenceElement",
            python_gedcom_2.tags.GEDCOM_TAG_RETIREMENT: "RetirementElement",
            python_gedcom_2.tags.GEDCOM_TAG_SOC_SEC_NUMBER: "SocialSecurityNumberElement",
            python_gedcom_2.tags.GEDCOM_TAG_TITLE: "TitleElement",
            python_gedcom_2.tags.GEDCOM_TAG_WILL: "WillElement",
        }

        if tag in tag_element_dict:
            class_name_in_string_form = tag_element_dict[tag]
            file_name_without_extension_for_this_class = cls._get_file_name_from_class_name(class_name_in_string_form)
            module = importlib.import_module("python_gedcom_2.element." + file_name_without_extension_for_this_class)
            class_ = getattr(module, class_name_in_string_form)

            element = class_(level, pointer, tag, value, linebreak, is_multiline)
        else:
            element = Element(level, pointer, tag, value, linebreak, is_multiline)

        return element
