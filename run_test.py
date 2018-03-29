# -*- coding: utf-8 -*-
import actions
import pytest
import unittest
from config import driver, td, json_cdb
from create_tender import create_tender
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

    def test4_Compare_tender_title(self):
        assert self.pmt['data']['title'] == view_from_page.get_tender_title()

    def test5_Compare_tender_description(self):
        assert self.pmt['data']['description'] == view_from_page.get_tender_description()

    @staticmethod
    def test6_Compare_tender_id():
        assert json_cdb['data']['tenderID'] == view_from_page.get_tender_uid()

    @staticmethod
    def test7_Add_contract_limited():
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
