import unittest

from python_gedcom_2 import tags
from python_gedcom_2.element.adoption import AdoptionElement
from python_gedcom_2.element.adult_christening import AdultChristeningElement
from python_gedcom_2.element.annulment import AnnulmentElement
from python_gedcom_2.element.baptism import BaptismElement
from python_gedcom_2.element.bar_mitzvah import BarMitzvahElement
from python_gedcom_2.element.bas_mitzvah import BasMitzvahElement
from python_gedcom_2.element.birth import BirthElement
from python_gedcom_2.element.blessing import BlessingElement
from python_gedcom_2.element.burial import BurialElement
from python_gedcom_2.element.caste import CasteElement
from python_gedcom_2.element.census import CensusElement
from python_gedcom_2.element.children_count import ChildrenCountElement
from python_gedcom_2.element.christening import ChristeningElement
from python_gedcom_2.element.confirmation import ConfirmationElement
from python_gedcom_2.element.cremation import CremationElement
from python_gedcom_2.element.date import DateElement
from python_gedcom_2.element.death import DeathElement
from python_gedcom_2.element.divorce import DivorceElement
from python_gedcom_2.element.divorce_filed import DivorceFiledElement
from python_gedcom_2.element.education import EducationElement
from python_gedcom_2.element.emigration import EmigrationElement
from python_gedcom_2.element.engagement import EngagementElement
from python_gedcom_2.element.event import EventElement
from python_gedcom_2.element.family import FamilyElement
from python_gedcom_2.element.file import FileElement
from python_gedcom_2.element.first_communion import FirstCommunionElement
from python_gedcom_2.element.graduation import GraduationElement
from python_gedcom_2.element.identification_number import IdentificationNumberElement
from python_gedcom_2.element.immigration import ImmigrationElement
from python_gedcom_2.element.individual import IndividualElement
from python_gedcom_2.element.marriage import MarriageElement
from python_gedcom_2.element.marriage_bann import MarriageBannElement
from python_gedcom_2.element.marriage_contract import MarriageContractElement
from python_gedcom_2.element.marriage_count import MarriageCountElement
from python_gedcom_2.element.marriage_license import MarriageLicenseElement
from python_gedcom_2.element.marriage_settlement import MarriageSettlementElement
from python_gedcom_2.element.nationality import NationalityElement
from python_gedcom_2.element.naturalization import NaturalizationElement
from python_gedcom_2.element.object import ObjectElement
from python_gedcom_2.element.occupation import OccupationElement
from python_gedcom_2.element.ordination import OrdinationElement
from python_gedcom_2.element.physical_description import PhysicalDescriptionElement
from python_gedcom_2.element.probate import ProbateElement
from python_gedcom_2.element.property import PropertyElement
from python_gedcom_2.element.religion import ReligionElement
from python_gedcom_2.element.residence import ResidenceElement
from python_gedcom_2.element.retirement import RetirementElement
from python_gedcom_2.element.social_security_number import SocialSecurityNumberElement
from python_gedcom_2.element.title import TitleElement
from python_gedcom_2.element.will import WillElement
from python_gedcom_2.element_creator import ElementCreator


class TestElementCreator(unittest.TestCase):
    def test_create_element__can_create_an_adoption_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_ADOPTION, "", "\n")
        self.assertTrue(isinstance(element, AdoptionElement), element)

    def test_create_element__can_create_an_adult_christening_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_ADULT_CHRISTENING, "", "\n")
        self.assertTrue(isinstance(element, AdultChristeningElement), element)

    def test_create_element__can_create_an_annulment_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_ANNULMENT, "", "\n")
        self.assertTrue(isinstance(element, AnnulmentElement), element)

    def test_create_element__can_create_a_baptism_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_BAPTISM, "", "\n")
        self.assertTrue(isinstance(element, BaptismElement), element)

    def test_create_element__can_create_a_bar_mitzvah_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_BAR_MITZVAH, "", "\n")
        self.assertTrue(isinstance(element, BarMitzvahElement), element)

    def test_create_element__can_create_a_bas_mitzvah_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_BAS_MITZVAH, "", "\n")
        self.assertTrue(isinstance(element, BasMitzvahElement), element)

    def test_create_element__can_create_a_birth_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_BIRTH, "", "\n")
        self.assertTrue(isinstance(element, BirthElement), element)

    def test_create_element__can_create_a_blessing_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_BLESSING, "", "\n")
        self.assertTrue(isinstance(element, BlessingElement), element)

    def test_create_element__can_create_a_burial_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_BURIAL, "", "\n")
        self.assertTrue(isinstance(element, BurialElement), element)

    def test_create_element__can_create_a_caste_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_CASTE, "", "\n")
        self.assertTrue(isinstance(element, CasteElement), element)

    def test_create_element__can_create_a_census_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_CENSUS, "", "\n")
        self.assertTrue(isinstance(element, CensusElement), element)

    def test_create_element__can_create_a_children_count_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_CHILDREN_COUNT, "", "\n")
        self.assertTrue(isinstance(element, ChildrenCountElement), element)

    def test_create_element__can_create_a_christening_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_CHRISTENING, "", "\n")
        self.assertTrue(isinstance(element, ChristeningElement), element)

    def test_create_element__can_create_a_confirmation_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_CONFIRMATION, "", "\n")
        self.assertTrue(isinstance(element, ConfirmationElement), element)

    def test_create_element__can_create_a_cremation_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_CREMATION, "", "\n")
        self.assertTrue(isinstance(element, CremationElement), element)

    def test_create_element__can_create_a_date_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_DATE, "", "\n")
        self.assertTrue(isinstance(element, DateElement), element)

    def test_create_element__can_create_a_death_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_DEATH, "", "\n")
        self.assertTrue(isinstance(element, DeathElement), element)

    def test_create_element__can_create_a_divorce_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_DIVORCE, "", "\n")
        self.assertTrue(isinstance(element, DivorceElement), element)

    def test_create_element__can_create_a_divorce_filed_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_DIVORCE_FILED, "", "\n")
        self.assertTrue(isinstance(element, DivorceFiledElement), element)

    def test_create_element__can_create_an_education_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_EDUCATION, "", "\n")
        self.assertTrue(isinstance(element, EducationElement), element)

    def test_create_element__can_create_an_emigration_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_EMIGRATION, "", "\n")
        self.assertTrue(isinstance(element, EmigrationElement), element)

    def test_create_element__can_create_an_engagement_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_ENGAGEMENT, "", "\n")
        self.assertTrue(isinstance(element, EngagementElement), element)

    def test_create_element__can_create_an_event_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_EVENT, "", "\n")
        self.assertTrue(isinstance(element, EventElement), element)

    def test_create_element__can_create_a_family_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_FAMILY, "", "\n")
        self.assertTrue(isinstance(element, FamilyElement), element)

    def test_create_element__can_create_a_file_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_FILE, "", "\n")
        self.assertTrue(isinstance(element, FileElement), element)

    def test_create_element__can_create_a_first_communion_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_FIRST_COMMUNION, "", "\n")
        self.assertTrue(isinstance(element, FirstCommunionElement), element)

    def test_create_element__can_create_a_graduation_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_GRADUATION, "", "\n")
        self.assertTrue(isinstance(element, GraduationElement), element)

    def test_create_element__can_create_a_identification_number_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_IDENTIFICATION_NUMBER, "", "\n")
        self.assertTrue(isinstance(element, IdentificationNumberElement), element)

    def test_create_element__can_create_a_immigration_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_IMMIGRATION, "", "\n")
        self.assertTrue(isinstance(element, ImmigrationElement), element)

    def test_create_element__can_create_a_individual_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_INDIVIDUAL, "", "\n")
        self.assertTrue(isinstance(element, IndividualElement), element)

    def test_create_element__can_create_a_marriage_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_MARRIAGE, "", "\n")
        self.assertTrue(isinstance(element, MarriageElement), element)

    def test_create_element__can_create_a_marriage_bann_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_MARRIAGE_BANN, "", "\n")
        self.assertTrue(isinstance(element, MarriageBannElement), element)

    def test_create_element__can_create_a_marriage_contract_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_MARRIAGE_CONTRACT, "", "\n")
        self.assertTrue(isinstance(element, MarriageContractElement), element)

    def test_create_element__can_create_a_marriage_count_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_MARRIAGE_COUNT, "", "\n")
        self.assertTrue(isinstance(element, MarriageCountElement), element)

    def test_create_element__can_create_a_marriage_license_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_MARRIAGE_LICENSE, "", "\n")
        self.assertTrue(isinstance(element, MarriageLicenseElement), element)

    def test_create_element__can_create_a_marriage_settlement_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_MARRIAGE_SETTLEMENT, "", "\n")
        self.assertTrue(isinstance(element, MarriageSettlementElement), element)

    def test_create_element__can_create_a_nationality_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_NATIONALITY, "", "\n")
        self.assertTrue(isinstance(element, NationalityElement), element)

    def test_create_element__can_create_a_naturalization_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_NATURALIZATION, "", "\n")
        self.assertTrue(isinstance(element, NaturalizationElement), element)

    def test_create_element__can_create_a_object_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_OBJECT, "", "\n")
        self.assertTrue(isinstance(element, ObjectElement), element)

    def test_create_element__can_create_an_occupation_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_OCCUPATION, "", "\n")
        self.assertTrue(isinstance(element, OccupationElement), element)

    def test_create_element__can_create_an_ordination_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_ORDINATION, "", "\n")
        self.assertTrue(isinstance(element, OrdinationElement), element)

    def test_create_element__can_create_a_physical_description_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_PHYSICAL_DESCRIPTION, "", "\n")
        self.assertTrue(isinstance(element, PhysicalDescriptionElement), element)

    def test_create_element__can_create_a_probate_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_PROBATE, "", "\n")
        self.assertTrue(isinstance(element, ProbateElement), element)

    def test_create_element__can_create_a_property_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_PROPERTY, "", "\n")
        self.assertTrue(isinstance(element, PropertyElement), element)

    def test_create_element__can_create_a_religion_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_RELIGION, "", "\n")
        self.assertTrue(isinstance(element, ReligionElement), element)

    def test_create_element__can_create_a_residence_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_RESIDENCE, "", "\n")
        self.assertTrue(isinstance(element, ResidenceElement), element)

    def test_create_element__can_create_a_retirement_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_RETIREMENT, "", "\n")
        self.assertTrue(isinstance(element, RetirementElement), element)

    def test_create_element__can_create_a_social_security_number_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_SOCIAL_SECURITY_NUMBER, "", "\n")
        self.assertTrue(isinstance(element, SocialSecurityNumberElement), element)

    def test_create_element__can_create_a_title_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_TITLE, "", "\n")
        self.assertTrue(isinstance(element, TitleElement), element)

    def test_create_element__can_create_a_will_element(self):
        element = ElementCreator.create_element(0, "", tags.GEDCOM_TAG_WILL, "", "\n")
        self.assertTrue(isinstance(element, WillElement), element)
