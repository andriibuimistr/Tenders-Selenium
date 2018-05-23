# -*- coding: utf-8 -*-
from helper import *
from config import driver
import msg


@pytest.mark.usefixtures("broker")
@pytest.mark.usefixtures("pmt")
class TestTendersTest(object):

    @classmethod
    def setup_class(cls):
        cls.driver = driver

    def test0_login(self):
        BrokerBasedActions(self.broker).login()

    def test1_create_tender(self):
        DATA['json_cdb'] = BrokerBasedActions(self.broker).create_tender(self.pmt)

    def test2_add_documents_tender(self):
        BrokerBasedActions(self.broker).open_tender_edit_page(DATA)
        DATA['docs_data'] = BrokerBasedActions(self.broker).add_documents()

    # @staticmethod
    # def test3_compare_document_content():
    #     compare_document_content(DATA)
    #
    # @staticmethod
    # def test4_compare_document_type():
    #     compare_document_type(DATA)

    def test7_add_supplier(self):
        BrokerBasedActions(self.broker).add_participant_info_limited(self.pmt)

    def test8_qualify_winner_limited(self):
        BrokerBasedActions(self.broker).qualify_winner_limited(self.pmt)

    def test9_find_tender_by_identifier(self):
        BrokerBasedActions(self.broker).find_tender_by_id(DATA)

    def test10_compare_tender_id(self):
        BrokerBasedViews(self.broker).compare_tender_uid(DATA)

    def test11_compare_tender_title(self):
        BrokerBasedViews(self.broker).compare_tender_title(self.pmt, DATA)

    def test12_compare_tender_description(self):
        BrokerBasedViews(self.broker).compare_tender_description(self.pmt, DATA)

    def test13_compare_tender_value_amount(self):
        BrokerBasedViews(self.broker).compare_tender_value_amount(self.pmt, DATA)

    def test14_compare_tender_currency(self):
        BrokerBasedViews(self.broker).compare_tender_currency(self.pmt, DATA)

    def test15_compare_tender_value_tax_included(self):
        BrokerBasedViews(self.broker).compare_tender_value_tax_included(self.pmt, DATA)

    def test16_compare_owner_country(self):
        BrokerBasedViews(self.broker).compare_owner_country(self.pmt, DATA)

    def test17_compare_owner_locality(self):
        BrokerBasedViews(self.broker).compare_owner_locality(self.pmt, DATA)

    def test18_compare_owner_postal_code(self):
        BrokerBasedViews(self.broker).compare_owner_postal_code(self.pmt, DATA)

    def test19_compare_owner_region(self):
        BrokerBasedViews(self.broker).compare_owner_region(self.pmt, DATA)

    def test20_compare_owner_street(self):
        BrokerBasedViews(self.broker).compare_owner_street(self.pmt, DATA)

    def test21_compare_owner_contact_name(self):
        BrokerBasedViews(self.broker).compare_owner_contact_name(self.pmt, DATA)

    def test22_compare_owner_phone_number(self):
        BrokerBasedViews(self.broker).compare_owner_phone_number(self.pmt, DATA)

    def test23_compare_owner_site(self):
        BrokerBasedViews(self.broker).compare_owner_site(self.pmt, DATA)

    def test24_compare_owner_company_name(self):
        BrokerBasedViews(self.broker).compare_owner_company_name(self.pmt, DATA)

    def test25_compare_owner_identifier(self):
        BrokerBasedViews(self.broker).compare_owner_identifier(self.pmt, DATA)

    def test26_compare_item_description(self):
        with pytest.allure.step(msg.compare_cdb):
            CDBActions(self.pmt, DATA).compare_item_description_cdb()
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_description_on_page(self.pmt)

    def test27_compare_item_classification_identifier(self):
        with pytest.allure.step(msg.compare_cdb):
            CDBActions(self.pmt, DATA).compare_item_class_id_cdb()
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_class_id_page(self.pmt)

    def test28_compare_item_classification_name(self):
        with pytest.allure.step(msg.compare_cdb):
            CDBActions(self.pmt, DATA).compare_item_class_name_cdb()
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_class_name_page(self.pmt)

    def test29_compare_item_quantity(self):
        with pytest.allure.step(msg.compare_cdb):
            CDBActions(self.pmt, DATA).compare_item_quantity_cdb()
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_quantity(self.pmt)

    def test30_compare_unit_name(self):
        with pytest.allure.step(msg.compare_cdb):
            CDBActions(self.pmt, DATA).compare_unit_name_cdb()
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_unit_name(self.pmt)

    def test31_compare_unit_code(self):
        with pytest.allure.step(msg.compare_cdb):
            CDBActions(self.pmt, DATA).compare_unit_code_cdb()

    def test32_compare_item_delivery_start_date(self):
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_delivery_start_date(self.pmt)

    def test33_compare_item_delivery_end_date(self):
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_delivery_end_date(self.pmt)

    def test34_compare_item_delivery_country(self):
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_delivery_country(self.pmt)

    def test35_compare_item_delivery_postal_code(self):
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_delivery_postal_code(self.pmt)

    def test36_compare_item_delivery_region(self):
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_delivery_region(self.pmt)

    def test37_compare_item_delivery_locality(self):
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_delivery_locality(self.pmt)

    def test38_compare_item_delivery_street(self):
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_delivery_street(self.pmt)

    def test98_add_contract_limited(self):
        BrokerBasedActions(self.broker).add_contract()

    def test99_sign_contract_limited(self):
        BrokerBasedActions(self.broker).sign_contract()

    @classmethod
    def teardown_class(cls):
        cls.driver = driver.quit()
