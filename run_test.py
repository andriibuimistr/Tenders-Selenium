# -*- coding: utf-8 -*-
import actions
import pytest

import helper
from config import driver
from create_tender import create_tender
import msg
import view_from_page


@pytest.mark.usefixtures("pmt")
class TestTendersTest(object):

    @classmethod
    def setup_class(cls):
        cls.driver = driver
        cls.login = actions.login('formyqatesting@gmail.com', 'andriy85')

    def test1_Create_tender(self):
        global json_cdb
        json_cdb = create_tender(self.pmt)

    def test2_Add_document_tender(self):
        with pytest.allure.step('Open tender edit page'):
            actions.open_tender_edit_page(json_cdb['data']['tenderID'])
        with pytest.allure.step('Upload documents'):
            global docs_data
            docs_data = actions.add_documents(json_cdb['data']['tenderID'])

    def test3_Compare_document_content(self):
        helper.compare_document_content(docs_data, json_cdb['data']['id'])


    def test7_Add_supplier(self):
        actions.add_participant_info_limited(self.pmt)

    @staticmethod
    def test8_Qualify_winner_limited():
        actions.qualify_winner_limited()

    def test9_Find_tender_by_identifier(self):
        actions.find_tender_by_id(json_cdb['data']['tenderID'])

    @staticmethod
    def test10_Compare_tender_id():
        assert json_cdb['data']['tenderID'] == view_from_page.get_tender_uid()

    def test11_Compare_tender_title(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['title'] == json_cdb['data']['title'].split('] ')[-1]
        with pytest.allure.step('Check data on tender page'):
            assert self.pmt['data']['title'] == view_from_page.get_tender_title()

    def test12_Compare_tender_description(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['description'] == json_cdb['data']['description']
        with pytest.allure.step('Check data on tender page'):
            assert self.pmt['data']['description'] == view_from_page.get_tender_description()

    def test13_compare_tender_value_amount(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['value']['amount'] == json_cdb['data']['value']['amount']
        with pytest.allure.step('Check data on tender page'):
            assert self.pmt['data']['value']['amount'] == view_from_page.get_tender_value_amount()

    def test14_Compare_tender_currency(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['value']['currency'] == json_cdb['data']['value']['currency']
        with pytest.allure.step('Check data on tender page'):
            assert self.pmt['data']['value']['currency'] == view_from_page.get_tender_currency()

    def test15_compare_value_tax_included(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['value']['valueAddedTaxIncluded'] == json_cdb['data']['value']['valueAddedTaxIncluded']
        with pytest.allure.step('Check data on tender page'):
            assert self.pmt['data']['value']['valueAddedTaxIncluded'] == view_from_page.get_value_added_tax_included()

    def test16_Compare_owner_country(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['procuringEntity']['address']['countryName'] == json_cdb['data']['procuringEntity']['address']['countryName']
        with pytest.allure.step('Check data on tender page'):
            assert self.pmt['data']['procuringEntity']['address']['countryName'] == view_from_page.get_owner_country()

    def test17_Compare_owner_locality(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['procuringEntity']['address']['locality'] == json_cdb['data']['procuringEntity']['address']['locality']
        with pytest.allure.step('Check data on tender page'):
            assert self.pmt['data']['procuringEntity']['address']['locality'] == view_from_page.get_owner_locality()

    def test18_Compare_owner_postal_code(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['procuringEntity']['address']['postalCode'] == json_cdb['data']['procuringEntity']['address']['postalCode']
        with pytest.allure.step('Check data on tender page'):
            assert self.pmt['data']['procuringEntity']['address']['postalCode'] == view_from_page.get_owner_postal_code()

    def test19_Compare_owner_region(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['procuringEntity']['address']['region'] == json_cdb['data']['procuringEntity']['address']['region']
        with pytest.allure.step('Check data on tender page'):
            assert self.pmt['data']['procuringEntity']['address']['region'] == view_from_page.get_owner_region()

    def test20_Compare_owner_street(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['procuringEntity']['address']['streetAddress'] == json_cdb['data']['procuringEntity']['address']['streetAddress']
        with pytest.allure.step('Check data on tender page'):
            assert self.pmt['data']['procuringEntity']['address']['streetAddress'] == view_from_page.get_owner_street()


    @staticmethod
    def test98_Add_contract_limited():
        actions.add_contract()

    @staticmethod
    def test99_Sign_contract_limited():
        actions.sign_contract()


    @classmethod
    def teardown_class(cls):
        cls.driver = driver.quit()
