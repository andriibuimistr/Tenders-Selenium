# -*- coding: utf-8 -*-
import actions
import pytest
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

    def test2_Add_supplier(self):
        actions.add_participant_info_limited(self.pmt)

    @staticmethod
    def test3_Qualify_winner_limited():
        actions.qualify_winner_limited()

    def test4_Find_tender_by_identifier(self):
        actions.find_tender_by_id(json_cdb['data']['tenderID'])

    @staticmethod
    def test5_Compare_tender_id():
        assert json_cdb['data']['tenderID'] == view_from_page.get_tender_uid()

    def test6_Compare_tender_title(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['title'] == json_cdb['data']['title'].split('] ')[-1]
        with pytest.allure.step('Check data on tender page'):
            assert self.pmt['data']['title'] == view_from_page.get_tender_title()

    def test7_Compare_tender_description(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['description'] == json_cdb['data']['description']
        with pytest.allure.step('Check data on tender page'):
            assert self.pmt['data']['description'] == view_from_page.get_tender_description()

    def test8_compare_tender_value_amount(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['value']['amount'] == json_cdb['data']['value']['amount']
        with pytest.allure.step('Check data on tender page'):
            assert self.pmt['data']['value']['amount'] == view_from_page.get_tender_value_amount()

    def test9_Compare_tender_currency(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['value']['currency'] == json_cdb['data']['value']['currency']
        with pytest.allure.step('Check data on tender page'):
            assert self.pmt['data']['value']['currency'] == view_from_page.get_tender_currency()

    def test10_compare_value_tax_included(self):
        with pytest.allure.step(msg.compare_cdb):
            assert self.pmt['data']['value']['valueAddedTaxIncluded'] == json_cdb['data']['value']['valueAddedTaxIncluded']
        with pytest.allure.step('Check data on tender page'):
            assert self.pmt['data']['value']['valueAddedTaxIncluded'] == view_from_page.get_value_added_tax_included()


    @staticmethod
    def test98_Add_contract_limited():
        actions.add_contract()

    @staticmethod
    def test99_Sign_contract_limited():
        actions.sign_contract()

    # def test3_Compare_tender_amount(self):
    #     cdb_json = tender.get_json_from_cdb()
    #     self.assertEqual(cdb_json['data']['value']['amount'], float(tender.get_data_limited_reporting_simple('tender_amount')))
    #
    # def test4_Compare_tender_currency(self):
    #     cdb_json = tender.get_json_from_cdb()
    #     self.assertEqual(cdb_json['data']['value']['currency'], tender.get_data_limited_reporting_simple('tender_currency'))
    #
    # def test5_Compare_tender_taxIncluded(self):  # add info about participant
    #     cdb_json = tender.get_json_from_cdb()
    #     self.assertEqual(cdb_json['data']['value']['valueAddedTaxIncluded'], tender.get_data_limited_reporting_simple('tender_taxIncluded'))

    @classmethod
    def teardown_class(cls):
        cls.driver = driver.quit()

#
# if __name__ == "__main__":
#     unittest.main(verbosity=2)
