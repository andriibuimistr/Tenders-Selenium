# -*- coding: utf-8 -*-
from config import driver
import time
import allure
import pytest
from cdb_requests import TenderRequests
from initial_data.document_generator import download_and_open_file, generate_files, delete_documents

DATA = dict()


def item_id_page(generated_json, item):
    return generated_json['data']['items'][item]['description'].split(' ')[3]


def item_generated_description(generated_json, item):
    return generated_json['data']['items'][item]['description']


def assert_item_field(generated_data, actual_data, field_name, number):
    with pytest.allure.step('Compare {} of item {}'.format(field_name, number)):
        allure.attach('Generated {}'.format(field_name), str(generated_data))
        allure.attach('Actual {}'.format(field_name.capitalize()), str(actual_data))
        assert generated_data == actual_data


def compare_document_content(docs_data, tender_id):
    time.sleep(240)
    docs_cdb = TenderRequests('2.4').get_tender_info(tender_id).json()['data']['documents']
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


def compare_document_type(docs_data, tender_id):
    docs_cdb = TenderRequests('2.4').get_tender_info(tender_id).json()['data']['documents']
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


def compare_item_description_cdb(generated_json, tender_id):
    items_cdb = TenderRequests('2.4').get_tender_info(tender_id).json()['data']['items']
    number = 0
    for item in range(len(generated_json['data']['items'])):
        generated_description = item_generated_description(generated_json, item)
        number += 1
        for cdb_item in range(len(items_cdb)):
            item_in_cdb_description = items_cdb[cdb_item]['description']
            if item_in_cdb_description.split(' ')[3] in generated_description:
                assert_item_field(generated_description, item_in_cdb_description, 'description', number)


def compare_item_class_id_cdb(generated_json, tender_id):
    items_cdb = TenderRequests('2.4').get_tender_info(tender_id).json()['data']['items']
    number = 0
    for item in range(len(generated_json['data']['items'])):
        generated_description = item_generated_description(generated_json, item)
        number += 1
        for cdb_item in range(len(items_cdb)):
            item_in_cdb_description = items_cdb[cdb_item]['description']
            if item_in_cdb_description.split(' ')[3] in generated_description:
                generated_class_id = generated_json['data']['items'][item]['classification']['id']
                cdb_class_id = items_cdb[cdb_item]['classification']['id']
                assert_item_field(generated_class_id, cdb_class_id, 'classification_id', number)


def compare_item_class_name_cdb(generated_json, tender_id):
    items_cdb = TenderRequests('2.4').get_tender_info(tender_id).json()['data']['items']
    number = 0
    for item in range(len(generated_json['data']['items'])):
        generated_description = item_generated_description(generated_json, item)
        number += 1
        for cdb_item in range(len(items_cdb)):
            item_in_cdb_description = items_cdb[cdb_item]['description']
            if item_in_cdb_description.split(' ')[3] in generated_description:
                generated_class_name = generated_json['data']['items'][item]['classification']['description']
                cdb_class_name = items_cdb[cdb_item]['classification']['description']
                assert_item_field(generated_class_name, cdb_class_name, 'classification_name', number)


def compare_item_quantity_cdb(generated_json, tender_id):
    items_cdb = TenderRequests('2.4').get_tender_info(tender_id).json()['data']['items']
    number = 0
    for item in range(len(generated_json['data']['items'])):
        generated_description = item_generated_description(generated_json, item)
        number += 1
        for cdb_item in range(len(items_cdb)):
            item_in_cdb_description = items_cdb[cdb_item]['description']
            if item_in_cdb_description.split(' ')[3] in generated_description:
                generated_item_quantity = generated_json['data']['items'][item]['quantity']
                cdb_item_quantity = items_cdb[cdb_item]['quantity']
                assert_item_field(generated_item_quantity, cdb_item_quantity, 'quantity', number)


def compare_unit_name_cdb(generated_json, tender_id):
    items_cdb = TenderRequests('2.4').get_tender_info(tender_id).json()['data']['items']
    number = 0
    for item in range(len(generated_json['data']['items'])):
        generated_description = item_generated_description(generated_json, item)
        number += 1
        for cdb_item in range(len(items_cdb)):
            item_in_cdb_description = items_cdb[cdb_item]['description']
            if item_in_cdb_description.split(' ')[3] in generated_description:
                generated_unit_name = generated_json['data']['items'][item]['unit']['name']
                cdb_unit_name = items_cdb[cdb_item]['unit']['name']
                assert_item_field(generated_unit_name, cdb_unit_name, 'unit_name', number)


def compare_unit_code_cdb(generated_json, tender_id):
    items_cdb = TenderRequests('2.4').get_tender_info(tender_id).json()['data']['items']
    number = 0
    for item in range(len(generated_json['data']['items'])):
        generated_description = item_generated_description(generated_json, item)
        number += 1
        for cdb_item in range(len(items_cdb)):
            item_in_cdb_description = items_cdb[cdb_item]['description']
            if item_in_cdb_description.split(' ')[3] in generated_description:
                generated_unit_code = generated_json['data']['items'][item]['unit']['code']
                cdb_unit_code = items_cdb[cdb_item]['unit']['code']
                assert_item_field(generated_unit_code, cdb_unit_code, 'unit_code', number)


class BrokerBasedViews:

    def __init__(self, broker):
        self.broker_view_from_page_file = __import__("brokers.{}.view_from_page".format(broker), fromlist=[""])

    def get_tender_uid(self):
        return self.broker_view_from_page_file.get_tender_uid()

    def get_tender_title(self):
        return self.broker_view_from_page_file.get_tender_title()

    def get_tender_description(self):
        return self.broker_view_from_page_file.get_tender_description()

    def get_tender_value_amount(self):
        return self.broker_view_from_page_file.get_tender_value_amount()

    def get_tender_currency(self):
        return self.broker_view_from_page_file.get_tender_currency()

    def get_value_added_tax_included(self):
        return self.broker_view_from_page_file.get_value_added_tax_included()

    def get_owner_country(self):
        return self.broker_view_from_page_file.get_owner_country()

    def get_owner_locality(self):
        return self.broker_view_from_page_file.get_owner_locality()

    def get_owner_postal_code(self):
        return self.broker_view_from_page_file.get_owner_postal_code()

    def get_owner_region(self):
        return self.broker_view_from_page_file.get_owner_region()

    def get_owner_street(self):
        return self.broker_view_from_page_file.get_owner_street()

    def get_owner_contact_name(self):
        return self.broker_view_from_page_file.get_owner_contact_name()

    def get_owner_phone_number(self):
        return self.broker_view_from_page_file.get_owner_phone_number()

    def get_owner_site(self):
        return self.broker_view_from_page_file.get_owner_site()

    def get_owner_company_name(self):
        return self.broker_view_from_page_file.get_owner_company_name()

    def get_owner_identifier(self):
        return self.broker_view_from_page_file.get_owner_identifier()


# def get_field_by_path(data, keys):
#     return get_field_by_path(data[keys[0]], keys[1:]) \
#         if keys else data


class BrokerBasedActions:

    def __init__(self, broker):
        self.broker_actions_file = __import__("brokers.{}.actions".format(broker), fromlist=[""])
        self.broker_create_tender_file = __import__("brokers.{}.create_tender".format(broker), fromlist=[""])
        self.broker_view_from_page_file = __import__("brokers.{}.view_from_page".format(broker), fromlist=[""])

    def create_tender(self, pmt):
        with pytest.allure.step('Run function for create tender'):
            self.broker_create_tender_file.create_tender(pmt)
        with pytest.allure.step('Get ID from tender page'):
            tender_id = self.broker_view_from_page_file.get_tender_id()
            allure.attach('Tender ID: ', tender_id)
            assert len(tender_id) != 0
        with pytest.allure.step('Get json from CDB'):
            response = TenderRequests('2.4').get_tender_info(tender_id)
            allure.attach('Response code: ', response.status_code)
        return response.json()

    def go_main_page(self):
        driver.get(self.broker_actions_file.host)

    def login(self):
        self.go_main_page()
        self.broker_actions_file.login('formyqatesting@gmail.com', 'andriy85')

    def add_participant_info_limited(self, pmt):
        self.broker_actions_file.add_participant_info_limited(pmt)

    def qualify_winner_limited(self, data):
        self.broker_actions_file.qualify_winner_limited(data['data'])

    def find_tender_by_id(self, tid):
        self.broker_actions_file.find_tender_by_id(tid)

    def open_tender_edit_page(self, tid):
        with pytest.allure.step('Open tender edit page'):
            self.broker_actions_file.open_tender_edit_page(tid)

    def add_documents(self):
        with pytest.allure.step('Upload documents'):
            document_data = generate_files(5)
            with pytest.allure.step('Add documents to tender'):
                self.broker_actions_file.add_documents(document_data)
            delete_documents(document_data)
            return document_data

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

    def add_contract(self):
        self.broker_actions_file.add_contract()

    def sign_contract(self):
        self.broker_actions_file.sign_contract()
