# -*- coding: utf-8 -*-
from config import driver
import time
import allure
import pytest
from cdb_requests import TenderRequests
from initial_data.document_generator import download_and_open_file, generate_files, delete_documents

DATA = dict()


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
        generated_description = generated_json['data']['items'][item]['description']
        number += 1
        for cdb_item in range(len(items_cdb)):
            item_in_cdb_description = items_cdb[cdb_item]['description']
            if item_in_cdb_description.split(' ')[3] in generated_description:
                with pytest.allure.step('Compare description of item {}'.format(number)):
                    allure.attach('Generated description', generated_description)
                    allure.attach('Description in cdb', item_in_cdb_description)
                    assert generated_description == item_in_cdb_description


def compare_item_class_id_cdb(generated_json, tender_id):
    items_cdb = TenderRequests('2.4').get_tender_info(tender_id).json()['data']['items']
    number = 0
    for item in range(len(generated_json['data']['items'])):
        generated_description = generated_json['data']['items'][item]['description']
        number += 1
        for cdb_item in range(len(items_cdb)):
            item_in_cdb_description = items_cdb[cdb_item]['description']
            if item_in_cdb_description.split(' ')[3] in generated_description:
                generated_class_id = generated_json['data']['items'][item]['classification']['id']
                cdb_class_id = items_cdb[cdb_item]['classification']['id']
                with pytest.allure.step('Compare classification id of item {}'.format(number)):
                    allure.attach('Generated classification id', generated_class_id)
                    allure.attach('Classification id in cdb', cdb_class_id)
                    assert generated_class_id == cdb_class_id


def compare_item_class_name_cdb(generated_json, tender_id):
    items_cdb = TenderRequests('2.4').get_tender_info(tender_id).json()['data']['items']
    number = 0
    for item in range(len(generated_json['data']['items'])):
        generated_description = generated_json['data']['items'][item]['description']
        number += 1
        for cdb_item in range(len(items_cdb)):
            item_in_cdb_description = items_cdb[cdb_item]['description']
            if item_in_cdb_description.split(' ')[3] in generated_description:
                generated_class_name = generated_json['data']['items'][item]['classification']['description']
                cdb_class_name = items_cdb[cdb_item]['classification']['description']
                with pytest.allure.step('Compare classification description of item {}'.format(number)):
                    allure.attach('Generated classification description', generated_class_name)
                    allure.attach('Classification description in cdb', cdb_class_name)
                    assert generated_class_name == cdb_class_name


def compare_item_quantity_cdb(generated_json, tender_id):
    items_cdb = TenderRequests('2.4').get_tender_info(tender_id).json()['data']['items']
    number = 0
    for item in range(len(generated_json['data']['items'])):
        generated_description = generated_json['data']['items'][item]['description']
        number += 1
        for cdb_item in range(len(items_cdb)):
            item_in_cdb_description = items_cdb[cdb_item]['description']
            if item_in_cdb_description.split(' ')[3] in generated_description:
                generated_item_quantity = generated_json['data']['items'][item]['quantity']
                cdb_item_quantity = items_cdb[cdb_item]['quantity']
                with pytest.allure.step('Compare quantity of item {}'.format(number)):
                    allure.attach('Generated quantity', str(generated_item_quantity))
                    allure.attach('Quantity in cdb', str(cdb_item_quantity))
                    assert generated_item_quantity == cdb_item_quantity


def compare_unit_name_cdb(generated_json, tender_id):
    items_cdb = TenderRequests('2.4').get_tender_info(tender_id).json()['data']['items']
    number = 0
    for item in range(len(generated_json['data']['items'])):
        generated_description = generated_json['data']['items'][item]['description']
        number += 1
        for cdb_item in range(len(items_cdb)):
            item_in_cdb_description = items_cdb[cdb_item]['description']
            if item_in_cdb_description.split(' ')[3] in generated_description:
                generated_unit_name = generated_json['data']['items'][item]['unit']['name']
                cdb_unit_name = items_cdb[cdb_item]['unit']['name']
                with pytest.allure.step('Compare unit name of item {}'.format(number)):
                    allure.attach('Generated unit name', generated_unit_name)
                    allure.attach('Unit name in cdb', cdb_unit_name)
                    assert generated_unit_name == cdb_unit_name


def compare_unit_code_cdb(generated_json, tender_id):
    items_cdb = TenderRequests('2.4').get_tender_info(tender_id).json()['data']['items']
    number = 0
    for item in range(len(generated_json['data']['items'])):
        generated_description = generated_json['data']['items'][item]['description']
        number += 1
        for cdb_item in range(len(items_cdb)):
            item_in_cdb_description = items_cdb[cdb_item]['description']
            if item_in_cdb_description.split(' ')[3] in generated_description:
                generated_unit_code = generated_json['data']['items'][item]['unit']['code']
                cdb_unit_code = items_cdb[cdb_item]['unit']['code']
                with pytest.allure.step('Compare unit code of item {}'.format(number)):
                    allure.attach('Generated unit code', generated_unit_code)
                    allure.attach('Unit code in cdb', cdb_unit_code)
                    assert generated_unit_code == cdb_unit_code


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


class BrokerBasedActions:

    def __init__(self, broker):
        self.broker_actions_file = __import__("brokers.{}.actions".format(broker), fromlist=[""])
        self.broker_create_tender_file = __import__("brokers.{}.create_tender".format(broker), fromlist=[""])
        self.broker_view_from_page_file = __import__("brokers.{}.view_from_page".format(broker), fromlist=[""])

    def create_tender(self, pmt):
        self.broker_create_tender_file.create_tender(pmt)
        tender_id = self.broker_view_from_page_file.get_tender_id()
        json_cdb = TenderRequests('2.4').get_tender_info(tender_id).json()
        return json_cdb

    def go_main_page(self):
        driver.get(self.broker_actions_file.host)

    def login(self):
        self.go_main_page()
        self.broker_actions_file.login('formyqatesting@gmail.com', 'andriy85')

    def add_participant_info_limited(self, pmt):
        self.broker_actions_file.add_participant_info_limited(pmt)

    def qualify_winner_limited(self):
        self.broker_actions_file.qualify_winner_limited()

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
            generated_description = generated_json['data']['items'][item]['description']
            number += 1
            item_description_page = self.broker_view_from_page_file.get_item_description(generated_description.split(' ')[3])
            with pytest.allure.step('Compare description of item {}'.format(number)):
                allure.attach('Generated description', generated_description)
                allure.attach('Description on page', item_description_page)
                assert generated_description == item_description_page

    def compare_item_class_id_page(self, generated_json):
        number = 0
        for item in range(len(generated_json['data']['items'])):
            generated_description_identifier = generated_json['data']['items'][item]['description'].split(' ')[3]
            number += 1
            generated_classification_identifier = generated_json['data']['items'][item]['classification']['id']
            classification_identifier_page = self.broker_view_from_page_file.get_classification_identifier(generated_description_identifier)
            with pytest.allure.step('Compare classification id of item {}'.format(number)):
                allure.attach('Generated classification id', generated_classification_identifier)
                allure.attach('Classification id on page', classification_identifier_page)
                assert generated_classification_identifier == classification_identifier_page

    def compare_item_class_name_page(self, generated_json):
        number = 0
        for item in range(len(generated_json['data']['items'])):
            generated_description_identifier = generated_json['data']['items'][item]['description'].split(' ')[3]
            number += 1
            generated_classification_name = generated_json['data']['items'][item]['classification']['description']
            classification_name_page = self.broker_view_from_page_file.get_classification_name(generated_description_identifier)
            with pytest.allure.step('Compare classification id of item {}'.format(number)):
                allure.attach('Generated classification id', generated_classification_name)
                allure.attach('Classification id on page', classification_name_page)
                assert generated_classification_name == classification_name_page

    def compare_item_quantity(self, generated_json):
        number = 0
        for item in range(len(generated_json['data']['items'])):
            generated_description_identifier = generated_json['data']['items'][item]['description'].split(' ')[3]
            number += 1
            generated_quantity = generated_json['data']['items'][item]['quantity']
            quantity_page = self.broker_view_from_page_file.get_item_quantity(generated_description_identifier)
            with pytest.allure.step('Compare quantity of item {}'.format(number)):
                allure.attach('Generated quantity', str(generated_quantity))
                allure.attach('Quantity on page', str(quantity_page))
                assert generated_quantity == quantity_page

    def compare_unit_name(self, generated_json):
        number = 0
        for item in range(len(generated_json['data']['items'])):
            generated_description_identifier = generated_json['data']['items'][item]['description'].split(' ')[3]
            number += 1
            generated_unit_name = generated_json['data']['items'][item]['unit']['name']
            unit_name_page = self.broker_view_from_page_file.get_unit_name(generated_description_identifier)
            with pytest.allure.step('Compare unit name of item {}'.format(number)):
                allure.attach('Generated unit name', generated_unit_name)
                allure.attach('Unit name on page', unit_name_page)
                assert generated_unit_name == unit_name_page

    def add_contract(self):
        self.broker_actions_file.add_contract()

    def sign_contract(self):
        self.broker_actions_file.sign_contract()
