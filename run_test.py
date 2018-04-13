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
        global json_cdb
        json_cdb = BrokerBasedActions(self.broker).create_tender(self.pmt)

    def test2_add_document_tender(self):
        BrokerBasedActions(self.broker).open_tender_edit_page(json_cdb['data']['tenderID'])
        global docs_data
        docs_data = BrokerBasedActions(self.broker).add_documents(json_cdb['data']['tenderID'])

    @staticmethod
    def test3_compare_document_content():
        compare_document_content(docs_data, json_cdb['data']['id'])

    @staticmethod
    def test4_compare_document_type():
        compare_document_type(docs_data, json_cdb['data']['id'])

    def test7_add_supplier(self):
        BrokerBasedActions(self.broker).add_participant_info_limited(self.pmt)

    def test8_qualify_winner_limited(self):
        BrokerBasedActions(self.broker).qualify_winner_limited()

    def test9_find_tender_by_identifier(self):
        BrokerBasedActions(self.broker).find_tender_by_id(json_cdb['data']['tenderID'])

    def test10_compare_tender_id(self):
        assert json_cdb['data']['tenderID'] == BrokerBasedViews(self.broker).get_tender_uid()

    def test11_compare_tender_title(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['title'] == json_cdb['data']['title'].split('] ')[-1]
        with pytest.allure.step(msg.compare_site):
            assert self.pmt['data']['title'] == BrokerBasedViews(self.broker).get_tender_title()

    def test12_compare_tender_description(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['description'] == json_cdb['data']['description']
        with pytest.allure.step(msg.compare_site):
            assert self.pmt['data']['description'] == BrokerBasedViews(self.broker).get_tender_description()

    def test13_compare_tender_value_amount(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['value']['amount'] == json_cdb['data']['value']['amount']
        with pytest.allure.step(msg.compare_site):
            assert self.pmt['data']['value']['amount'] == BrokerBasedViews(self.broker).get_tender_value_amount()

    def test14_compare_tender_currency(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['value']['currency'] == json_cdb['data']['value']['currency']
        with pytest.allure.step(msg.compare_site):
            assert self.pmt['data']['value']['currency'] == BrokerBasedViews(self.broker).get_tender_currency()

    def test15_compare_value_tax_included(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['value']['valueAddedTaxIncluded'] == json_cdb['data']['value']['valueAddedTaxIncluded']
        with pytest.allure.step(msg.compare_site):
            assert self.pmt['data']['value']['valueAddedTaxIncluded'] == BrokerBasedViews(self.broker).get_value_added_tax_included()

    def test16_compare_owner_country(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['procuringEntity']['address']['countryName'] == json_cdb['data']['procuringEntity']['address']['countryName']
        with pytest.allure.step(msg.compare_site):
            assert self.pmt['data']['procuringEntity']['address']['countryName'] == BrokerBasedViews(self.broker).get_owner_country()

    def test17_compare_owner_locality(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['procuringEntity']['address']['locality'] == json_cdb['data']['procuringEntity']['address']['locality']
        with pytest.allure.step(msg.compare_site):
            assert self.pmt['data']['procuringEntity']['address']['locality'] == BrokerBasedViews(self.broker).get_owner_locality()

    def test18_compare_owner_postal_code(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['procuringEntity']['address']['postalCode'] == json_cdb['data']['procuringEntity']['address']['postalCode']
        with pytest.allure.step(msg.compare_site):
            assert self.pmt['data']['procuringEntity']['address']['postalCode'] == BrokerBasedViews(self.broker).get_owner_postal_code()

    def test19_compare_owner_region(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['procuringEntity']['address']['region'] == json_cdb['data']['procuringEntity']['address']['region']
        with pytest.allure.step(msg.compare_site):
            assert self.pmt['data']['procuringEntity']['address']['region'] == BrokerBasedViews(self.broker).get_owner_region()

    def test20_compare_owner_street(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['procuringEntity']['address']['streetAddress'] == json_cdb['data']['procuringEntity']['address']['streetAddress']
        with pytest.allure.step(msg.compare_site):
            assert self.pmt['data']['procuringEntity']['address']['streetAddress'] == BrokerBasedViews(self.broker).get_owner_street()

    def test21_compare_owner_contact_name(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['procuringEntity']['contactPoint']['name'] == json_cdb['data']['procuringEntity']['contactPoint']['name']
        with pytest.allure.step(msg.compare_site):
            assert self.pmt['data']['procuringEntity']['contactPoint']['name'] == BrokerBasedViews(self.broker).get_owner_contact_name()

    def test22_compare_owner_phone_number(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['procuringEntity']['contactPoint']['telephone'] == json_cdb['data']['procuringEntity']['contactPoint']['telephone']
        with pytest.allure.step(msg.compare_site):
            assert self.pmt['data']['procuringEntity']['contactPoint']['telephone'] == BrokerBasedViews(self.broker).get_owner_phone_number()

    def test23_compare_owner_site(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['procuringEntity']['contactPoint']['url'] == json_cdb['data']['procuringEntity']['contactPoint']['url']
        with pytest.allure.step(msg.compare_site):
            assert self.pmt['data']['procuringEntity']['contactPoint']['url'] == BrokerBasedViews(self.broker).get_owner_site()

    def test24_compare_owner_company_name(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['procuringEntity']['name'] == json_cdb['data']['procuringEntity']['name']
        with pytest.allure.step(msg.compare_site):
            assert self.pmt['data']['procuringEntity']['name'] == BrokerBasedViews(self.broker).get_owner_company_name()

    def test25_compare_owner_identifier(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['procuringEntity']['identifier']['id'] == json_cdb['data']['procuringEntity']['identifier']['id']
        with pytest.allure.step(msg.compare_site):
            assert self.pmt['data']['procuringEntity']['identifier']['id'] == BrokerBasedViews(self.broker).get_owner_identifier()

    def test26_compare_item_description(self):
        with pytest.allure.step(msg.compare_cdb):
            compare_item_description_cdb(self.pmt, json_cdb['data']['id'])
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_description_on_page(self.pmt)

    def test27_compare_item_classification_identifier(self):
        with pytest.allure.step(msg.compare_cdb):
            compare_item_class_id_cdb(self.pmt, json_cdb['data']['id'])
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_class_id_page(self.pmt)

    def test28_compare_item_classification_name(self):
        with pytest.allure.step(msg.compare_cdb):
            compare_item_class_name_cdb(self.pmt, json_cdb['data']['id'])
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_class_name_page(self.pmt)

    def test29_compare_item_quantity(self):
        with pytest.allure.step(msg.compare_cdb):
            compare_item_quantity_cdb(self.pmt, json_cdb['data']['id'])
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_quantity(self.pmt)

    def test98_add_contract_limited(self):
        BrokerBasedActions(self.broker).add_contract()

    def test99_sign_contract_limited(self):
        BrokerBasedActions(self.broker).sign_contract()

    @classmethod
    def teardown_class(cls):
        cls.driver = driver.quit()
