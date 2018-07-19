# -*- coding: utf-8 -*-
from api.cdb_requests import *
from random import randint
from datetime import timedelta
from config import fake
import pytest


# ######################################### BIDS ###################################3
def generate_annual_costs_reduction_list():
    annual_costs_reduction_list = []
    cost = 0
    for x in range(21):
        cost += 1000
        if cost > 15000:
            cost = 15000
        annual_costs_reduction_list.append(cost)
    return annual_costs_reduction_list


def generate_bid_values(tender_json, lot_number):
    list_of_lots_id = []
    procurement_method = tender_json['data']['procurementMethodType']
    if 'lots' in tender_json['data']:
        number_of_lots = len(tender_json['data']['lots'])
        list_of_lots_id = []
        for lot in range(number_of_lots):
            list_of_lots_id.append(tender_json['data']['lots'][lot]['id'])
    else:
        number_of_lots = 0

    if procurement_method != 'esco':
        tender_currency = tender_json['data']['value']['currency']
        value_added_tax_included = tender_json['data']['value']['valueAddedTaxIncluded']
        if number_of_lots == 0:
            values_json = {"value": {
                            "amount": randint(100, 999),
                            "currency": tender_currency,
                            "valueAddedTaxIncluded": value_added_tax_included
                     }}
        else:
            values_json = {"lotValues": []}
            for lot in range(number_of_lots):
                lot_id = list_of_lots_id[lot]
                values = {
                            "relatedLot": lot_id,
                            "value": {
                                    "amount": randint(100, 999),
                                    "valueAddedTaxIncluded": value_added_tax_included,
                                    "currency": tender_currency
                            }
                        }
                if procurement_method in limited_procurement:
                    values_json = values
                    values_json['lotID'] = list_of_lots_id[lot_number]
                    del values_json['relatedLot']
                else:
                    values_json['lotValues'].append(values)
    else:
        if number_of_lots == 0:
            values_json = {"value": {
                                  "contractDuration": {
                                    "days": 0,
                                    "years": 15
                                  },
                                  "yearlyPaymentsPercentage": 0.8,
                                  "annualCostsReduction": generate_annual_costs_reduction_list()
                                }}
        else:
            values_json = {"lotValues": []}
            for lot in range(number_of_lots):
                lot_id = list_of_lots_id[lot]
                values = {"relatedLot": lot_id,
                          "value": {
                                  "contractDuration": {
                                    "days": 0,
                                    "years": 15
                                  },
                                  "yearlyPaymentsPercentage": 0.8,
                                  "annualCostsReduction": generate_annual_costs_reduction_list()
                                }}
                values_json['lotValues'].append(values)

    if 'features' in tender_json['data']:
        values_json['parameters'] = []
        for feature in range(len(tender_json['data']['features'])):
            number_of_feature_values = len(tender_json['data']['features'][feature]['enum'])
            values_json['parameters'].append({
                "code": tender_json['data']['features'][feature]['code'],
                "value": tender_json['data']['features'][feature]['enum'][randint(0, number_of_feature_values - 1)]['value']
            })
    return values_json


# generate json for bid
def generate_json_bid(user_idf, tender_json, lot_number=False):
    values = generate_bid_values(tender_json, lot_number)
    bid_json = {
                "data": {
                        "selfEligible": True,
                        "selfQualified": True,
                        "tenderers": [
                          {
                            "contactPoint": {
                              "telephone": "+380 (432) 21-69-30",
                              "name": "Сергій Олексюк",
                              "email": "bidder@r.com"
                            },
                            "identifier": {
                              "scheme": "UA-EDR",
                              "id": user_idf,
                              "uri": "http://www.site.domain"
                            },
                            "name": fake.company(),
                            "address": {
                              "countryName": "Україна",
                              "postalCode": "21100",
                              "region": "м. Вінниця",
                              "streetAddress": "вул. Островського, 33",
                              "locality": "м. Вінниця"
                            }
                          }
                        ],
                        "subcontractingDetails": "ДКП «Книга», Україна, м. Львів, вул. Островського, 33"
                        }
                    }
    procurement_method = tender_json['data']['procurementMethodType']

    if procurement_method in limited_procurement:
        bid_json['data']['suppliers'] = bid_json['data']['tenderers']
        del bid_json['data']['tenderers']

    for key in values:
        bid_json['data'][key] = values[key]
    return bid_json


def add_suppliers_for_limited(number_of_lots, tender_id, tender_token, list_of_id_lots, api_version, tender_json):
    with pytest.allure.step('Add suppliers for limited procedure'):
        tender = TenderRequests(api_version)
        supplier = 0
        if number_of_lots == 0:
            with pytest.allure.step('Add supplier whole procedure'):
                supplier += 1
                limited_supplier_json = generate_json_bid('00037256', tender_json)
                del limited_supplier_json["data"]["selfEligible"], limited_supplier_json["data"]["selfQualified"], limited_supplier_json["data"]["subcontractingDetails"]
                tender.add_supplier_limited(tender_id, tender_token, limited_supplier_json, supplier)
        else:
            with pytest.allure.step('Add supplier for one lot'):
                for lot_id in range(len(list_of_id_lots)):
                    supplier += 1
                    with pytest.allure.step('Add supplier {}'.format(supplier)):
                        limited_supplier_json = generate_json_bid('00037256', tender_json, supplier - 1)
                        del limited_supplier_json["data"]["selfEligible"], limited_supplier_json["data"]["selfQualified"], limited_supplier_json["data"]["subcontractingDetails"]
                        tender.add_supplier_limited(tender_id, tender_token, limited_supplier_json, supplier)


# ########################################   TENDERS   ###################################################

def create_tender(json_tender, api_version):
    tender = TenderRequests(api_version)
    with pytest.allure.step('Publish tender in CDB'):
        t_publish = tender.publish_tender(json_tender)
    tender_id_long = t_publish.json()['data']['id']
    tender_token = t_publish.json()['access']['token']
    with pytest.allure.step('Activate tender'):
        tender.activate_tender(tender_id_long, tender_token, json_tender['data']['procurementMethodType'])
    return t_publish.json()


def run_activate_award(api_version, tender_id_long, tender_token, list_of_awards, procurement_method):
    tender = TenderRequests(api_version)
    award_number = 0
    activate_award_json = activate_award_json_select(procurement_method)
    for award in range(len(list_of_awards)):
        award_number += 1
        award_id = list_of_awards[award]['id']
        # add_document_to_entity(tender_id_long, award_id, tender_token, api_version, 'awards')
        tender.activate_award_contract(tender_id_long, 'awards', award_id, tender_token, activate_award_json, award_number)

# ########################################   CONTRACTS   ###################################################


def activate_contract_json(complaint_end_date, contract_data):
    # contract_end_date = datetime.now() + timedelta(days=120)
    # complaint_end_date = datetime.strptime(complaint_end_date, '%Y-%m-%dT%H:%M:%S.%f{}'.format(kiev_now))
    contract_json = {
                      "data": {
                        "period": {
                          "startDate": contract_data.contract_start_date.strftime("%Y-%m-%dT%H:%M:%S.%f{}".format(kiev_now)),  # datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f{}".format(kiev_now)),
                          "endDate": contract_data.contract_end_date.strftime("%Y-%m-%dT%H:%M:%S.%f{}".format(kiev_now))  # contract_end_date.strftime("%Y-%m-%dT%H:%M:%S.%f{}".format(kiev_now))
                        },
                        "dateSigned": contract_data.date_signed.strftime("%Y-%m-%dT%H:%M:%S.%f{}".format(kiev_now)),  # (complaint_end_date + timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%S.%f{}".format(kiev_now))
                        "status": "active",
                        "contractNumber": contract_data.contract_number
                      }
                    }
    return contract_json


def check_if_contract_exists(tender, tender_id_long):
    with pytest.allure.step('Check if contract was generated'):
        for x in range(10):
            get_t_info = tender.get_tender_info(tender_id_long).json()
            if 'contracts' in get_t_info['data']:
                return get_t_info['data']['contracts']
            else:
                time.sleep(10)


def run_activate_contract(api_version, tender_id_long, tender_token, contract_data):
    tender = TenderRequests(api_version)
    tender_actual_data = tender.get_tender_info(tender_id_long).json()
    list_of_contracts = check_if_contract_exists(tender, tender_id_long)
    if tender_actual_data['data']['procurementMethodType'] in negotiation_procurement:
        complaint_end_date = tender_actual_data['data']['awards'][-1]['complaintPeriod']['endDate']
    else:
        complaint_end_date = datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S.%f{}'.format(kiev_now))
    contract_number = 0
    json_activate_contract = activate_contract_json(complaint_end_date, contract_data)
    for contract in range(len(list_of_contracts)):
        contract_number += 1
        contract_id = list_of_contracts[contract]['id']
        # add_document_to_entity(tender_id_long, contract_id, tender_token, api_version, 'contracts')
        tender.activate_award_contract(tender_id_long, 'contracts', contract_id, tender_token, json_activate_contract, contract_number)
