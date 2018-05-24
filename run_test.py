# -*- coding: utf-8 -*-
from helper import *
from config import driver


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
        DATA['docs_data'] = BrokerBasedActions(self.broker).add_documents_tender()

    def test3_compare_document_content(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_document_content()

    def test4_compare_document_type(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_document_type()

    def test7_add_supplier(self):
        BrokerBasedActions(self.broker).add_participant_info_limited(self.pmt)

    def test8_qualify_winner_limited(self):
        BrokerBasedActions(self.broker).qualify_winner_limited(self.pmt)

    def test9_find_tender_by_identifier(self):
        BrokerBasedActions(self.broker).find_tender_by_id(DATA)

    def test10_compare_tender_id(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_tender_uid()

    def test11_compare_tender_title(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_tender_title()

    def test12_compare_tender_description(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_tender_description()

    def test13_compare_tender_value_amount(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_tender_value_amount()

    def test14_compare_tender_currency(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_tender_currency()

    def test15_compare_tender_value_tax_included(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_tender_value_tax_included()

    def test16_compare_owner_country(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_owner_country()

    def test17_compare_owner_locality(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_owner_locality()

    def test18_compare_owner_postal_code(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_owner_postal_code()

    def test19_compare_owner_region(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_owner_region()

    def test20_compare_owner_street(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_owner_street()

    def test21_compare_owner_contact_name(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_owner_contact_name()

    def test22_compare_owner_phone_number(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_owner_phone_number()

    def test23_compare_owner_site(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_owner_site()

    def test24_compare_owner_company_name(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_owner_company_name()

    def test25_compare_owner_identifier(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_owner_identifier()

    def test26_compare_item_description(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_item_description()

    def test27_compare_item_classification_identifier(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_item_classification_identifier()

    def test28_compare_item_classification_name(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_item_classification_name()

    def test29_compare_item_quantity(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_item_quantity()

    def test30_compare_unit_name(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_unit_name()

    def test31_compare_unit_code(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_unit_code()

    def test32_compare_item_delivery_start_date(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_item_delivery_start_date()

    def test33_compare_item_delivery_end_date(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_item_delivery_end_date()

    def test34_compare_item_delivery_country(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_item_delivery_country()

    def test35_compare_item_delivery_postal_code(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_item_delivery_postal_code()

    def test36_compare_item_delivery_region(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_item_delivery_region()

    def test37_compare_item_delivery_locality(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_item_delivery_locality()

    def test38_compare_item_delivery_street(self):
        BrokerBasedViews(self.broker, self.pmt, DATA).compare_item_delivery_street()

    def test39_wait_for_complaint_period_end_date(self):
        if DATA['json_cdb']['data']['procurementMethodType'] != 'reporting':
            BrokerBasedViews(self.broker, self.pmt, DATA).wait_for_complaint_period_end_date()

    def test98_add_contract_limited(self):
        BrokerBasedActions(self.broker).add_contract(self.pmt)

    def test99_sign_contract_limited(self):
        BrokerBasedActions(self.broker).sign_contract()

    @classmethod
    def teardown_class(cls):
        cls.driver = driver.quit()
