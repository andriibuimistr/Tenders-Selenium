# -*- coding: utf-8 -*-
from config import driver
import allure
from core.document_generator import *
from core import service, msg
from core.api_helper import *
from core.selenium_helper import refresh_page

DATA = {'contracts': dict()}


def item_id_page(generated_json, item):
    return generated_json['data']['items'][item]['description'].split(' ')[3]


def item_generated_description(generated_json, item):
    return generated_json['data']['items'][item]['description']


def assert_item_field(generated_data, actual_data, field_name, number):
    with pytest.allure.step('Compare {} of item {}'.format(field_name, number)):
        allure.attach('Generated {}'.format(field_name), str(generated_data))
        allure.attach('Actual {}'.format(field_name.capitalize()), str(actual_data))
        assert generated_data == actual_data


class CDBActions:

    def __init__(self, generated_json, data, broker):
        self.generated_json = generated_json
        self.data = data
        self.broker_config = __import__("brokers.{}.config".format(broker), fromlist=[""])
        self.cdb = self.broker_config.cdb
        self.items_cdb = TenderRequests(self.cdb).get_tender_info(data['json_cdb']['data']['id']).json()['data']['items']
        self.generated_items = generated_json['data']['items']

    # DOCUMENTS
    def compare_document_content_cdb(self, entity):
        docs_cdb = TenderRequests(self.cdb).get_tender_info(self.data['json_cdb']['data']['id']).json()['data']['documents']
        docs_data = self.data['docs_data']
        if entity == 'contract':
            docs_cdb = TenderRequests(self.cdb).get_contract_info(self.data['contracts']['id_long']).json()['data']['documents']
            docs_data = self.data['contract_docs_data']
        number = 0
        for doc in range(len(docs_data)):
            number += 1
            for cdb_doc in range(len(docs_cdb)):
                if docs_cdb[cdb_doc]['title'].split('.')[0] == docs_data[doc]['document_name']:
                    with pytest.allure.step('Compare content of document {}'.format(number)):
                        cdb_content = download_and_open_file(docs_cdb[cdb_doc]['url'])
                        allure.attach('Generated content', docs_data[doc]['content'])
                        allure.attach('Content of file in cdb', cdb_content)
                        assert docs_data[doc]['content'] == cdb_content

    def compare_document_type_cdb(self, entity):
        docs_cdb = TenderRequests(self.cdb).get_tender_info(self.data['json_cdb']['data']['id']).json()['data']['documents']
        docs_data = self.data['docs_data']
        if entity == 'contract':
            docs_cdb = TenderRequests(self.cdb).get_contract_info(self.data['contracts']['id_long']).json()['data']['documents']
            docs_data = self.data['contract_docs_data']
        number = 0
        for doc in range(len(docs_data)):
            number += 1
            for cdb_doc in range(len(docs_cdb)):
                if docs_cdb[cdb_doc]['title'].split('.')[0] == docs_data[doc]['document_name']:
                    with pytest.allure.step('Compare type of document {}'.format(number)):
                        cdb_type = docs_cdb[cdb_doc]['documentType']
                        allure.attach('Generated type', docs_data[doc]['type'])
                        allure.attach('Type of file in cdb', cdb_type)
                        assert docs_data[doc]['type'] == cdb_type

    # ITEMS
    def compare_item_description_cdb(self):
        number = 0
        for item in range(len(self.generated_items)):
            generated_description = item_generated_description(self.generated_json, item)
            number += 1
            for cdb_item in range(len(self.items_cdb)):
                item_in_cdb_description = self.items_cdb[cdb_item]['description']
                if item_in_cdb_description.split(' ')[3] in generated_description:
                    assert_item_field(generated_description, item_in_cdb_description, 'description', number)

    def compare_item_class_id_cdb(self):
        number = 0
        for item in range(len(self.generated_items)):
            generated_description = item_generated_description(self.generated_json, item)
            number += 1
            for cdb_item in range(len(self.items_cdb)):
                item_in_cdb_description = self.items_cdb[cdb_item]['description']
                if item_in_cdb_description.split(' ')[3] in generated_description:
                    generated_class_id = self.generated_json['data']['items'][item]['classification']['id']
                    cdb_class_id = self.items_cdb[cdb_item]['classification']['id']
                    assert_item_field(generated_class_id, cdb_class_id, 'classification_id', number)

    def compare_item_class_name_cdb(self):
        number = 0
        for item in range(len(self.generated_items)):
            generated_description = item_generated_description(self.generated_json, item)
            number += 1
            for cdb_item in range(len(self.items_cdb)):
                item_in_cdb_description = self.items_cdb[cdb_item]['description']
                if item_in_cdb_description.split(' ')[3] in generated_description:
                    generated_class_name = self.generated_json['data']['items'][item]['classification']['description']
                    cdb_class_name = self.items_cdb[cdb_item]['classification']['description']
                    assert_item_field(generated_class_name, cdb_class_name, 'classification_name', number)

    def compare_item_quantity_cdb(self):
        number = 0
        for item in range(len(self.generated_items)):
            generated_description = item_generated_description(self.generated_json, item)
            number += 1
            for cdb_item in range(len(self.items_cdb)):
                item_in_cdb_description = self.items_cdb[cdb_item]['description']
                if item_in_cdb_description.split(' ')[3] in generated_description:
                    generated_item_quantity = self.generated_json['data']['items'][item]['quantity']
                    cdb_item_quantity = self.items_cdb[cdb_item]['quantity']
                    assert_item_field(generated_item_quantity, cdb_item_quantity, 'quantity', number)

    def compare_unit_name_cdb(self):
        number = 0
        for item in range(len(self.generated_items)):
            generated_description = item_generated_description(self.generated_json, item)
            number += 1
            for cdb_item in range(len(self.items_cdb)):
                item_in_cdb_description = self.items_cdb[cdb_item]['description']
                if item_in_cdb_description.split(' ')[3] in generated_description:
                    generated_unit_name = self.generated_json['data']['items'][item]['unit']['name']
                    cdb_unit_name = self.items_cdb[cdb_item]['unit']['name']
                    assert_item_field(generated_unit_name, cdb_unit_name, 'unit_name', number)

    def compare_unit_code_cdb(self):
        number = 0
        for item in range(len(self.generated_items)):
            generated_description = item_generated_description(self.generated_json, item)
            number += 1
            for cdb_item in range(len(self.items_cdb)):
                item_in_cdb_description = self.items_cdb[cdb_item]['description']
                if item_in_cdb_description.split(' ')[3] in generated_description:
                    generated_unit_code = self.generated_json['data']['items'][item]['unit']['code']
                    cdb_unit_code = self.items_cdb[cdb_item]['unit']['code']
                    assert_item_field(generated_unit_code, cdb_unit_code, 'unit_code', number)


class BrokerBasedActions:

    def __init__(self, broker):
        self.broker_config = __import__("brokers.{}.config".format(broker), fromlist=[""])
        self.broker_actions_file = __import__("brokers.{}.actions".format(broker), fromlist=[""])
        self.broker_create_tender_file = __import__("brokers.{}.create_tender".format(broker), fromlist=[""])
        self.broker_view_from_page_file = __import__("brokers.{}.view_from_page".format(broker), fromlist=[""])

    def create_tender(self, pmt, role):
        with pytest.allure.step('Run function for create tender'):
            tender = dict()
            if role == 'owner':
                self.broker_create_tender_file.create_tender(pmt)
            else:
                tender = create_tender(pmt, self.broker_config.cdb)
        with pytest.allure.step('Get ID from tender page'):
            if role == 'owner':
                tender_id = self.broker_view_from_page_file.get_tender_id()  # Get tender_id_long from tender view page
                assert len(tender_id) != 0
                response = TenderRequests(self.broker_config.cdb).get_tender_info(tender_id).json()  # Get tender json from CDB
            else:
                tender_id = tender['data']['id']
                response = tender  # Json with access token if tender was created with api request
            allure.attach('Tender ID: ', tender_id)
        return response

    def go_main_page(self):
        driver.get(self.broker_config.host)

    def login(self, role):
        if role != 'viewer':
            self.go_main_page()
            self.broker_actions_file.login('owner')

    def add_participant_info_limited(self, pmt):
        self.broker_actions_file.add_participant_info_limited(pmt)

    def qualify_winner_limited(self, data):
        self.broker_actions_file.qualify_winner_limited(data['data'])

    def find_tender_by_id(self, data):
        with pytest.allure.step('Find tender by id'):
            self.broker_actions_file.find_tender_by_id(data['json_cdb']['data']['tenderID'])

    def find_contract_by_id(self, data):
        with pytest.allure.step('Find contract by id'):
            self.broker_actions_file.find_contract_by_id(data['contracts']['id_short'])

    def open_tender_edit_page(self):
        with pytest.allure.step('Open tender edit page'):
            self.broker_actions_file.open_tender_edit_page()

    def add_documents_tender(self, role, json_data):
        with pytest.allure.step('Upload documents'):
            with pytest.allure.step('Add documents to tender'):
                if role == 'owner':
                    files = generate_files()
                    self.open_tender_edit_page()
                    self.broker_actions_file.add_documents_tender(files)
                else:
                    files = add_documents_to_tender(json_data['json_cdb']['data']['id'], json_data['json_cdb']['access']['token'], 0, self.broker_config.cdb)
            delete_documents(files)
            return files

    def compare_item_description_on_page(self, generated_json):
        number = 0
        for item in range(len(generated_json['data']['items'])):
            generated_description_identifier = item_id_page(generated_json, item)
            number += 1
            generated_description = generated_json['data']['items'][item]['description']
            item_description_page = self.broker_view_from_page_file.get_item_description(generated_description_identifier)
            assert_item_field(generated_description, item_description_page, 'description', number)

    def compare_item_class_id_page(self, generated_json):
        number = 0
        for item in range(len(generated_json['data']['items'])):
            generated_description_identifier = item_id_page(generated_json, item)
            number += 1
            generated_classification_identifier = generated_json['data']['items'][item]['classification']['id']
            classification_identifier_page = self.broker_view_from_page_file.get_classification_identifier(generated_description_identifier)
            assert_item_field(generated_classification_identifier, classification_identifier_page, 'classification_id', number)

    def compare_item_class_name_page(self, generated_json):
        number = 0
        for item in range(len(generated_json['data']['items'])):
            generated_description_identifier = item_id_page(generated_json, item)
            number += 1
            generated_classification_name = generated_json['data']['items'][item]['classification']['description']
            classification_name_page = self.broker_view_from_page_file.get_classification_name(generated_description_identifier)
            assert_item_field(generated_classification_name, classification_name_page, 'classification_name', number)

    def compare_item_quantity(self, generated_json):
        number = 0
        for item in range(len(generated_json['data']['items'])):
            generated_description_identifier = item_id_page(generated_json, item)
            number += 1
            generated_quantity = generated_json['data']['items'][item]['quantity']
            quantity_page = self.broker_view_from_page_file.get_item_quantity(generated_description_identifier)
            assert_item_field(generated_quantity, quantity_page, 'quantity', number)

    def compare_unit_name(self, generated_json):
        number = 0
        for item in range(len(generated_json['data']['items'])):
            generated_description_identifier = item_id_page(generated_json, item)
            number += 1
            generated_unit_name = generated_json['data']['items'][item]['unit']['name']
            unit_name_page = self.broker_view_from_page_file.get_unit_name(generated_description_identifier)
            assert_item_field(generated_unit_name, unit_name_page, 'unit_name', number)

    def compare_item_delivery_start_date(self, generated_json):
        number = 0
        for item in range(len(generated_json['data']['items'])):
            generated_description_identifier = item_id_page(generated_json, item)
            number += 1
            generated_delivery_start_date = generated_json['data']['items'][item]['deliveryDate']['startDate'][:10]
            start_date_page = self.broker_view_from_page_file.get_delivery_start_date(generated_description_identifier)
            assert_item_field(generated_delivery_start_date, start_date_page, 'delivery_start_date', number)

    def compare_item_delivery_end_date(self, generated_json):
        number = 0
        for item in range(len(generated_json['data']['items'])):
            generated_description_identifier = item_id_page(generated_json, item)
            number += 1
            generated_delivery_end_date = generated_json['data']['items'][item]['deliveryDate']['endDate'][:10]
            end_date_page = self.broker_view_from_page_file.get_delivery_end_date(generated_description_identifier)
            assert_item_field(generated_delivery_end_date, end_date_page, 'delivery_end_date', number)

    def compare_item_delivery_country(self, generated_json):
        number = 0
        for item in range(len(generated_json['data']['items'])):
            generated_description_identifier = item_id_page(generated_json, item)
            number += 1
            generated_delivery_country = generated_json['data']['items'][item]['deliveryAddress']['countryName']
            country_page = self.broker_view_from_page_file.get_delivery_country(generated_description_identifier)
            assert_item_field(generated_delivery_country, country_page, 'delivery_country', number)

    def compare_item_delivery_postal_code(self, generated_json):
        number = 0
        for item in range(len(generated_json['data']['items'])):
            generated_description_identifier = item_id_page(generated_json, item)
            number += 1
            generated_delivery_postal_code = generated_json['data']['items'][item]['deliveryAddress']['postalCode']
            postal_code_page = self.broker_view_from_page_file.get_delivery_postal_code(generated_description_identifier)
            assert_item_field(generated_delivery_postal_code, postal_code_page, 'delivery_postal_code', number)

    def compare_item_delivery_region(self, generated_json):
        number = 0
        for item in range(len(generated_json['data']['items'])):
            generated_description_identifier = item_id_page(generated_json, item)
            number += 1
            generated_delivery_region = generated_json['data']['items'][item]['deliveryAddress']['region']
            region_page = self.broker_view_from_page_file.get_delivery_region(generated_description_identifier)
            assert_item_field(generated_delivery_region, region_page, 'delivery_region', number)

    def compare_item_delivery_locality(self, generated_json):
        number = 0
        for item in range(len(generated_json['data']['items'])):
            generated_description_identifier = item_id_page(generated_json, item)
            number += 1
            generated_delivery_locality = generated_json['data']['items'][item]['deliveryAddress']['locality']
            locality_page = self.broker_view_from_page_file.get_delivery_locality(generated_description_identifier)
            assert_item_field(generated_delivery_locality, locality_page, 'delivery_locality', number)

    def compare_item_delivery_street(self, generated_json):
        number = 0
        for item in range(len(generated_json['data']['items'])):
            generated_description_identifier = item_id_page(generated_json, item)
            number += 1
            generated_delivery_street = generated_json['data']['items'][item]['deliveryAddress']['streetAddress']
            street_page = self.broker_view_from_page_file.get_delivery_street(generated_description_identifier)
            assert_item_field(generated_delivery_street, street_page, 'delivery_street', number)

    def compare_document_content_page(self, data, entity):
        docs_data = data['docs_data']
        if entity == 'contract':
            docs_data = data['contract_docs_data']
        number = 0
        for doc in range(len(docs_data)):
            number += 1
            doc_title = docs_data[doc]['document_name']
            with pytest.allure.step('Compare content of document {}'.format(number)):
                file_content = download_and_open_file(self.broker_view_from_page_file.get_tender_document_link(doc_title))  # get content of file from tender view page
                allure.attach('Generated content', docs_data[doc]['content'])
                allure.attach('Content of file on view page', file_content)
                assert docs_data[doc]['content'] == file_content

    def compare_document_type_page(self, data, entity):
        docs_data = data['docs_data']
        if entity == 'contract':
            docs_data = data['contract_docs_data']
        number = 0
        for doc in range(len(docs_data)):
            number += 1
            doc_title = docs_data[doc]['document_name']
            with pytest.allure.step('Compare type of document {}'.format(number)):
                if entity == 'contract':
                    document_type = self.broker_view_from_page_file.get_contract_document_type(doc_title)
                else:
                    document_type = self.broker_view_from_page_file.get_tender_document_type(doc_title)
                allure.attach('Generated type', docs_data[doc]['type'])
                allure.attach('Type of file on view page', document_type)
                assert docs_data[doc]['type'] == document_type

    def add_contract(self, data):
        contract_data = service.ContractData
        self.broker_actions_file.add_contract(data['data'], contract_data)
        return contract_data

    def sign_contract(self):
        self.broker_actions_file.sign_contract()

    def get_info_from_contract_tender(self):
        self.broker_actions_file.get_info_from_contract_tender()

    def wait_for_contract_generation(self):
        return self.broker_actions_file.wait_for_contract_to_be_generated()

    def open_contract_edit_page(self):
        with pytest.allure.step('Open contract edit page'):
            self.broker_actions_file.open_contract_edit_page()

    def add_documents_contract(self, role, json_data):
        with pytest.allure.step('Upload documents'):
            with pytest.allure.step('Add documents to contract'):
                if role == 'owner':
                    document_data = generate_files('contract')
                    self.open_contract_edit_page()
                    self.broker_actions_file.add_documents_contract(document_data)
                else:
                    pass  # ############################################################################
            delete_documents(document_data)
            return document_data


class BrokerBasedViews:

    def __init__(self, broker, generated_json, data):
        self.broker_config = __import__("brokers.{}.config".format(broker), fromlist=[""])
        self.broker_view_from_page_file = __import__("brokers.{}.view_from_page".format(broker), fromlist=[""])
        self.generated_json = generated_json
        self.data = data
        self.broker = broker

    def compare_tender_uid(self):
        assert self.data['json_cdb']['data']['tenderID'] == self.broker_view_from_page_file.get_tender_uid()

    def compare_tender_title(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.generated_json['data']['title'] == self.data['json_cdb']['data']['title'].split('] ')[-1]
        with pytest.allure.step(msg.compare_site):
            assert self.generated_json['data']['title'] == self.broker_view_from_page_file.get_tender_title()

    def compare_tender_description(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.generated_json['data']['description'] == self.data['json_cdb']['data']['description']
        with pytest.allure.step(msg.compare_site):
            assert self.generated_json['data']['description'] == self.broker_view_from_page_file.get_tender_description()

    def compare_tender_value_amount(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.generated_json['data']['value']['amount'] == self.data['json_cdb']['data']['value']['amount']
        with pytest.allure.step(msg.compare_site):
            assert self.generated_json['data']['value']['amount'] == self.broker_view_from_page_file.get_tender_value_amount()
        return

    def compare_tender_currency(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.generated_json['data']['value']['currency'] == self.data['json_cdb']['data']['value']['currency']
        with pytest.allure.step(msg.compare_site):
            assert self.generated_json['data']['value']['currency'] == self.broker_view_from_page_file.get_tender_currency()

    def compare_tender_value_tax_included(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.generated_json['data']['value']['valueAddedTaxIncluded'] == self.data['json_cdb']['data']['value']['valueAddedTaxIncluded']
        with pytest.allure.step(msg.compare_site):
            assert self.generated_json['data']['value']['valueAddedTaxIncluded'] == self.broker_view_from_page_file.get_value_added_tax_included()

    # PROCURING ENTITY
    def compare_owner_country(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.generated_json['data']['procuringEntity']['address']['countryName'] == self.data['json_cdb']['data']['procuringEntity']['address']['countryName']
        with pytest.allure.step(msg.compare_site):
            assert self.generated_json['data']['procuringEntity']['address']['countryName'] == self.broker_view_from_page_file.get_owner_country()

    def compare_owner_locality(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.generated_json['data']['procuringEntity']['address']['locality'] == self.data['json_cdb']['data']['procuringEntity']['address']['locality']
        with pytest.allure.step(msg.compare_site):
            assert self.generated_json['data']['procuringEntity']['address']['locality'] == self.broker_view_from_page_file.get_owner_locality()

    def compare_owner_postal_code(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.generated_json['data']['procuringEntity']['address']['postalCode'] == self.data['json_cdb']['data']['procuringEntity']['address']['postalCode']
        with pytest.allure.step(msg.compare_site):
            assert self.generated_json['data']['procuringEntity']['address']['postalCode'] == self.broker_view_from_page_file.get_owner_postal_code()

    def compare_owner_region(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.generated_json['data']['procuringEntity']['address']['region'] == self.data['json_cdb']['data']['procuringEntity']['address']['region']
        with pytest.allure.step(msg.compare_site):
            assert self.generated_json['data']['procuringEntity']['address']['region'] == self.broker_view_from_page_file.get_owner_region()

    def compare_owner_street(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.generated_json['data']['procuringEntity']['address']['streetAddress'] == self.data['json_cdb']['data']['procuringEntity']['address']['streetAddress']
        with pytest.allure.step(msg.compare_site):
            assert self.generated_json['data']['procuringEntity']['address']['streetAddress'] == self.broker_view_from_page_file.get_owner_street()

    def compare_owner_contact_name(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.generated_json['data']['procuringEntity']['contactPoint']['name'] == self.data['json_cdb']['data']['procuringEntity']['contactPoint']['name']
        with pytest.allure.step(msg.compare_site):
            assert self.generated_json['data']['procuringEntity']['contactPoint']['name'] == self.broker_view_from_page_file.get_owner_contact_name()

    def compare_owner_phone_number(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.generated_json['data']['procuringEntity']['contactPoint']['telephone'] == self.data['json_cdb']['data']['procuringEntity']['contactPoint']['telephone']
        with pytest.allure.step(msg.compare_site):
            assert self.generated_json['data']['procuringEntity']['contactPoint']['telephone'] == self.broker_view_from_page_file.get_owner_phone_number()

    def compare_owner_site(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.generated_json['data']['procuringEntity']['contactPoint']['url'] == self.data['json_cdb']['data']['procuringEntity']['contactPoint']['url']
        with pytest.allure.step(msg.compare_site):
            assert self.generated_json['data']['procuringEntity']['contactPoint']['url'] == self.broker_view_from_page_file.get_owner_site()

    def compare_owner_company_name(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.generated_json['data']['procuringEntity']['name'] == self.data['json_cdb']['data']['procuringEntity']['name']
        with pytest.allure.step(msg.compare_site):
            assert self.generated_json['data']['procuringEntity']['name'] == self.broker_view_from_page_file.get_owner_company_name()

    def compare_owner_identifier(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.generated_json['data']['procuringEntity']['identifier']['id'] == self.data['json_cdb']['data']['procuringEntity']['identifier']['id']
        with pytest.allure.step(msg.compare_site):
            assert self.generated_json['data']['procuringEntity']['identifier']['id'] == self.broker_view_from_page_file.get_owner_identifier()

    # ITEMS
    def compare_item_description(self):
        with pytest.allure.step(msg.compare_cdb):
            CDBActions(self.generated_json, self.data, self.broker).compare_item_description_cdb()
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_description_on_page(self.generated_json)

    def compare_item_classification_identifier(self):
        with pytest.allure.step(msg.compare_cdb):
            CDBActions(self.generated_json, self.data, self.broker).compare_item_class_id_cdb()
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_class_id_page(self.generated_json)

    def compare_item_classification_name(self):
        with pytest.allure.step(msg.compare_cdb):
            CDBActions(self.generated_json, self.data, self.broker).compare_item_class_name_cdb()
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_class_name_page(self.generated_json)

    def compare_item_quantity(self):
        with pytest.allure.step(msg.compare_cdb):
            CDBActions(self.generated_json, self.data, self.broker).compare_item_quantity_cdb()
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_quantity(self.generated_json)

    def compare_unit_name(self):
        with pytest.allure.step(msg.compare_cdb):
            CDBActions(self.generated_json, self.data, self.broker).compare_unit_name_cdb()
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_unit_name(self.generated_json)

    def compare_unit_code(self):
        with pytest.allure.step(msg.compare_cdb):
            CDBActions(self.generated_json, self.data, self.broker).compare_unit_code_cdb()

    def compare_item_delivery_start_date(self):
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_delivery_start_date(self.generated_json)

    def compare_item_delivery_end_date(self):
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_delivery_end_date(self.generated_json)

    def compare_item_delivery_country(self):
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_delivery_country(self.generated_json)

    def compare_item_delivery_postal_code(self):
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_delivery_postal_code(self.generated_json)

    def compare_item_delivery_region(self):
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_delivery_region(self.generated_json)

    def compare_item_delivery_locality(self):
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_delivery_locality(self.generated_json)

    def compare_item_delivery_street(self):
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_item_delivery_street(self.generated_json)

    # QUALIFICATION
    def wait_for_complaint_period_end_date(self):
        with pytest.allure.step("Wait for qualification complaint period end date"):
            period = self.broker_view_from_page_file.get_qualification_complaint_period_end_date()
            waiting_time = service.count_waiting_time(period[0], period[1], self.broker_config.cdb)
            if waiting_time > 0:
                time.sleep(waiting_time + 60)

    # DOCUMENTS
    def compare_document_content(self, entity=None):
        # time.sleep(240)
        with pytest.allure.step(msg.compare_cdb):
            CDBActions(self.generated_json, self.data, self.broker).compare_document_content_cdb(entity)
        with pytest.allure.step(msg.compare_site):
            refresh_page()
            BrokerBasedActions(self.broker).compare_document_content_page(self.data, entity)

    def compare_document_type(self, entity=None):
        with pytest.allure.step(msg.compare_cdb):
            CDBActions(self.generated_json, self.data, self.broker).compare_document_type_cdb(entity)
        with pytest.allure.step(msg.compare_site):
            BrokerBasedActions(self.broker).compare_document_type_page(self.data, entity)


class BrokerBasedViewsContracts:

    def __init__(self, broker, data):
        self.broker_config = __import__("brokers.{}.config".format(broker), fromlist=[""])
        self.broker_view_from_page_file = __import__("brokers.{}.view_from_page".format(broker), fromlist=[""])
        self.contract_generated_data = data['contract_data']
        self.data = data
        self.broker = broker
        self.new_cdb_json = TenderRequests(self.broker_config.cdb).get_tender_info(self.data['json_cdb']['data']['id']).json()

    @staticmethod
    def compare_contract_values(generated_value, actual_value):
        allure.attach('Generated: ', str(generated_value))
        allure.attach('Actual: ', str(actual_value))
        assert str(generated_value) == str(actual_value)

    # CONTRACTS TENDER
    def compare_contract_number_tender(self):
        BrokerBasedActions(self.broker).find_tender_by_id(self.data)
        BrokerBasedActions(self.broker).get_info_from_contract_tender()
        with pytest.allure.step(msg.compare_cdb):
            self.compare_contract_values(self.contract_generated_data.contract_number, self.new_cdb_json['data']['contracts'][0]['contractNumber'])
        with pytest.allure.step(msg.compare_site):
            self.compare_contract_values(self.contract_generated_data.contract_number, self.broker_view_from_page_file.get_contract_number_tender())

    def compare_contract_date_signed_tender(self):
        with pytest.allure.step(msg.compare_cdb):
            self.compare_contract_values(str(self.contract_generated_data.date_signed)[:10], self.new_cdb_json['data']['contracts'][0]['dateSigned'][:10])
        with pytest.allure.step(msg.compare_site):
            self.compare_contract_values(str(self.contract_generated_data.date_signed)[:10], self.broker_view_from_page_file.get_contract_date_signed_tender())

    def compare_contract_start_date_tender(self):
        with pytest.allure.step(msg.compare_cdb):
            self.compare_contract_values(str(self.contract_generated_data.contract_start_date)[:10], self.new_cdb_json['data']['contracts'][0]['period']['startDate'][:10])
        with pytest.allure.step(msg.compare_site):
            self.compare_contract_values(str(self.contract_generated_data.contract_start_date)[:10], self.broker_view_from_page_file.get_contract_start_date_tender())

    def compare_contract_end_date_tender(self):
        with pytest.allure.step(msg.compare_cdb):
            self.compare_contract_values(str(self.contract_generated_data.contract_end_date)[:10], self.new_cdb_json['data']['contracts'][0]['period']['endDate'][:10])
        with pytest.allure.step(msg.compare_site):
            self.compare_contract_values(str(self.contract_generated_data.contract_end_date)[:10], self.broker_view_from_page_file.get_contract_end_date_tender())


