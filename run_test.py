# -*- coding: utf-8 -*-
import actions
# import tender
import pytest
import unittest
from conftest import driver
from create_tender import create_tender


@pytest.mark.usefixtures("pmt")
class TendersTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = driver
        cls.login = actions.login('formyqatesting@gmail.com', 'andriy85')

    # def test0_Login(self):
    #     self.login = actions.login('formyqatesting@gmail.com', 'andriy85')

    def test1_Create_tender(self):
        create_tender(self.pmt)

    def test2_Add_supplier(self):
        actions.add_participant_info_limited(self.pmt)

    @staticmethod
    def test3_Qualify_winner_limited():
        actions.qualify_winner_limited()

    @staticmethod
    def test4_Add_contract_limited():
        actions.add_contract()

    @staticmethod
    def test5_Sign_contract_limited():
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
    #
    # def test6_Add_participant_info(self):  # add info about participant
    #     tender.add_participant_info_limited_reporting_simple()
    #
    # def test7_Qualify_winner_limited_reporting_simple(self):  # sign with EDS
    #     tender.qualify_winner_limited_reporting_simple()
    #
    # def test8_Add_contract_limited_reporting_simple(self):  # add contract
    #     tender.add_contract_limited_reporting_simple()
    #
    # def test9_Sign_contract_limited_reporting_simple(self):  # add contract
    #     tender.sign_contract_limited_reporting_simple()

    @classmethod
    def tearDownClass(cls):
        cls.driver = driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)
