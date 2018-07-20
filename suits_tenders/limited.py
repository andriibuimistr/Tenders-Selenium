# -*- coding: utf-8 -*-
from core.helper import *
from config import driver


@pytest.mark.usefixtures("broker")
@pytest.mark.usefixtures("pmt")
@pytest.mark.usefixtures("role")
class TestTendersTest(object):

    @classmethod
    def setup_class(cls):
        cls.driver = driver

    def test0_setup(self):
        DATA['initial_json'] = BrokerBasedActions(self.broker, self.role).create_initial_json(self.pmt)
        BrokerBasedActions(self.broker, self.role).login()

    def test1_create_tender(self):
        DATA['json_cdb'] = BrokerBasedActions(self.broker, self.role).create_tender(DATA['initial_json'])

    def test2_add_documents_tender(self):
        DATA['docs_data'] = BrokerBasedActions(self.broker, self.role).add_documents_tender(DATA)

    def test3_add_supplier(self):
        BrokerBasedActions(self.broker, self.role).add_participant_info_limited(DATA['initial_json'], DATA)

    def test4_qualify_winner_limited(self):
        BrokerBasedActions(self.broker, self.role).qualify_winner_limited(DATA)

    def test5_find_tender_by_identifier(self):
        BrokerBasedActions(self.broker, self.role).find_tender_by_id(DATA)

    def test6_compare_tender_document_content(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_document_content()

    def test7_compare_tender_document_type(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_document_type()

    def test10_compare_tender_id(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_tender_uid()

    def test11_compare_tender_title(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_tender_title()

    def test12_compare_tender_description(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_tender_description()

    def test13_compare_tender_value_amount(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_tender_value_amount()

    def test14_compare_tender_currency(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_tender_currency()

    def test15_compare_tender_value_tax_included(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_tender_value_tax_included()

    def test16_compare_owner_country(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_owner_country()

    def test17_compare_owner_locality(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_owner_locality()

    def test18_compare_owner_postal_code(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_owner_postal_code()

    def test19_compare_owner_region(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_owner_region()

    def test20_compare_owner_street(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_owner_street()

    def test21_compare_owner_contact_name(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_owner_contact_name()

    def test22_compare_owner_phone_number(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_owner_phone_number()

    def test23_compare_owner_site(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_owner_site()

    def test24_compare_owner_company_name(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_owner_company_name()

    def test25_compare_owner_identifier(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_owner_identifier()

    def test26_compare_item_description(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_item_description()

    def test27_compare_item_classification_identifier(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_item_classification_identifier()

    def test28_compare_item_classification_name(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_item_classification_name()

    def test29_compare_item_quantity(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_item_quantity()

    def test30_compare_unit_name(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_unit_name()

    def test31_compare_unit_code(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_unit_code()

    def test32_compare_item_delivery_start_date(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_item_delivery_start_date()

    def test33_compare_item_delivery_end_date(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_item_delivery_end_date()

    def test34_compare_item_delivery_country(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_item_delivery_country()

    def test35_compare_item_delivery_postal_code(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_item_delivery_postal_code()

    def test36_compare_item_delivery_region(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_item_delivery_region()

    def test37_compare_item_delivery_locality(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_item_delivery_locality()

    def test38_compare_item_delivery_street(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_item_delivery_street()

    def test39_wait_for_complaint_period_end_date(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).wait_for_complaint_period_end_date(self.role)

    def test98_add_contract_limited(self):
        DATA['contract_data'] = BrokerBasedActions(self.broker, self.role).add_contract(DATA)

    def test99_sign_contract_limited(self):
        BrokerBasedActions(self.broker, self.role).sign_contract(self.role)

    def test100_compare_contract_number_tender(self):
        BrokerBasedViewsContracts(self.broker, self.role, DATA).compare_contract_number_tender()

    def test101_compare_contract_contract_date_signed_tender(self):
        BrokerBasedViewsContracts(self.broker, self.role, DATA).compare_contract_date_signed_tender()

    def test102_compare_contract_start_date_tender(self):
        BrokerBasedViewsContracts(self.broker, self.role, DATA).compare_contract_start_date_tender()

    def test103_compare_contract_end_date_tender(self):
        BrokerBasedViewsContracts(self.broker, self.role, DATA).compare_contract_end_date_tender()

    def test104_wait_for_contract_to_be_generated(self):
        contract_id = BrokerBasedActions(self.broker, self.role).wait_for_contract_generation(DATA)
        DATA['contracts']['id_short'] = contract_id[0]
        DATA['contracts']['id_long'] = contract_id[1]

    def test105_find_contract_by_id(self):
        BrokerBasedActions(self.broker, self.role).find_contract_by_id(DATA)

    def test106_add_documents_contract(self):
        DATA['contract_docs_data'] = BrokerBasedActions(self.broker, self.role).add_documents_contract()

    def test107_compare_contract_document_content(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_document_content('contract')

    def test108_compare_contract_document_type(self):
        BrokerBasedViews(self.broker, self.role, DATA['initial_json'], DATA).compare_document_type('contract')

    @classmethod
    def teardown_class(cls):
        cls.driver = driver.quit()
