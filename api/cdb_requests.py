# -*- coding: utf-8 -*-
from tender_initial_data.tender_data_for_requests import *
from flask import abort
import json
import requests
from requests.exceptions import ConnectionError, HTTPError
import time
from pprint import pformat


def save_log(code, body, resp_header, host, endpoint, method, request_name, entity, headers, json_request):
    now = datetime.now()
    path = os.path.join(ROOT_DIR, 'logs', entity, str(now.year), str(now.month), str(now.day), str(now.hour),
                        '{} {} {}.txt'.format(code, datetime.now().strftime("%d-%m-%Y %H-%M-%S"), request_name))
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    f = open(path, "w+")
    try:
        body = json.loads(body)
    except Exception as e:
        print(e)
        body = body
    f.write('{} {}{}\n\n{}\n\n{}\n\n{}\n\n{}'.format(method, host, endpoint, str(headers).replace(',', ',\n'),
                                                     pformat(json_request), str(resp_header).replace(',', ',\n'), pformat(body)))
    f.close()


# Send request to cdb
def request_to_cdb(headers, host, endpoint, method, json_request, request_name, entity, is_json=True, files=None):
    if is_json:
        json_request = json.dumps(json_request)
    attempts = 0
    for x in range(5):
        attempts += 1
        try:
            s = requests.Session()
            if method != 'GET':
                s.request("HEAD", "{}".format(host))
            r = requests.Request(method, "{}{}".format(host, endpoint),
                                 data=json_request,
                                 headers=headers,
                                 files=files)
            prepped = s.prepare_request(r)
            resp = s.send(prepped)
            resp.raise_for_status()
            if resp.status_code in [200, 201, 202]:
                print("{}: Success".format(request_name))
                print("       status code:  {}".format(resp.status_code))
                save_log(resp.status_code, resp.content.decode(), resp.headers, host, endpoint, method, request_name, entity, headers, json_request)
                return resp
        except HTTPError as error:
            print("{}: Error".format(request_name))
            print("       status code:  {}".format(resp.status_code))
            print("       response content:  {}".format(resp.content.decode()))
            print("       headers:           {}".format(resp.headers))
            save_log(error.response.status_code, resp.content.decode(), resp.headers, host, endpoint, method, request_name, entity, headers, json_request)
            time.sleep(1)
            if attempts >= 5:
                abort(error.response.status_code, resp.content.decode())
        except ConnectionError as e:
            print('Connection Exception')
            if attempts < 5:
                time.sleep(1)
                continue
            else:
                save_log(503, str(e), 'No header', host, endpoint, method, request_name, entity, headers, json_request)
                abort(503, '{} error: {}'.format(request_name, e))
        except requests.exceptions.MissingSchema as e:
            print('MissingSchema Exception')
            save_log(500, str(e), 'No header', host, endpoint, method, request_name, entity, headers, json_request)
            abort(500, '{} error: {}'.format(request_name, e))
        except Exception as e:
            print('General Exception')
            save_log(500, str(e), 'No header', host, endpoint, method, request_name, entity, headers, json_request)
            abort(500, '{} error: {}'.format(request_name, e))


class TenderRequests(object):

    def __init__(self, cdb):
        self.cdb = cdb
        self.host = tender_host_selector(cdb)[0]
        self.host_public = tender_host_selector(cdb)[1]
        self.ds_host = tender_ds_host_selector(cdb)
        self.entity = 'tenders'
        self.document = 'tender_documents'
        self.entity_contract = 'contract'
        self.host_contracts = contract_host_selector(cdb)[0]
        self.host_public_contracts = contract_host_selector(cdb)[1]

    def publish_tender(self, json_tender):
        return request_to_cdb(headers=tender_headers_request(json_tender),
                              host=self.host,
                              endpoint='',
                              method='POST',
                              json_request=json_tender,
                              request_name='Publish tender',
                              entity=self.entity)

    def activate_tender(self, tender_id_long, token, procurement_method):
        json_tender_activation = json_activate_tender(procurement_method)
        return request_to_cdb(headers=tender_headers_request(json_tender_activation),
                              host=self.host,
                              endpoint='/{}?acc_token={}'.format(tender_id_long, token),
                              method='PATCH',
                              json_request=json_tender_activation,
                              request_name='Activate tender',
                              entity=self.entity)

    def get_tender_info(self, tender_id_long):
        return request_to_cdb(headers=None,
                              host=self.host_public,
                              endpoint='/{}'.format(tender_id_long),
                              method='GET',
                              json_request=None,
                              request_name='Get tender info',
                              entity=self.entity)

    def finish_first_stage(self, tender_id_long, token):
        return request_to_cdb(headers=tender_headers_request(json_finish_first_stage),
                              host=self.host,
                              endpoint='/{}?acc_token={}'.format(tender_id_long, token),
                              method='PATCH',
                              json_request=json_finish_first_stage,
                              request_name='Finish first stage',
                              entity=self.entity)

    def patch_second_stage(self, tender_id_long, token, json_patch_2nd_stage):
        return request_to_cdb(headers=tender_headers_request(json_patch_2nd_stage),
                              host=self.host,
                              endpoint='/{}?acc_token={}'.format(tender_id_long, token),
                              method='PATCH',
                              json_request=json_patch_2nd_stage,
                              request_name='Patch 2nd stage',
                              entity=self.entity)

    def activate_2nd_stage(self, tender_id_long, token, procurement_method):
        json_tender_activation = json_activate_tender(procurement_method)
        return request_to_cdb(headers=tender_headers_request(json_tender_activation),
                              host=self.host,
                              endpoint='/{}?acc_token={}'.format(tender_id_long, token),
                              method='PATCH',
                              json_request=json_tender_activation,
                              request_name='Activate 2nd stage',
                              entity=self.entity)

    def get_2nd_stage_info(self, tender_id_long, token):
        return request_to_cdb(headers=tender_headers_request(None),
                              host=self.host,
                              endpoint='/{}/credentials?acc_token={}'.format(tender_id_long, token),
                              method='PATCH',
                              json_request=None,
                              request_name='Get 2nd stage info',
                              entity=self.entity)

    def approve_prequalification(self, tender_id_long, qualification_id, token, json_pq):
        return request_to_cdb(headers=tender_headers_request(json_pq),
                              host=self.host,
                              endpoint='/{}/qualifications/{}?acc_token={}'.format(tender_id_long, qualification_id, token),
                              method='PATCH',
                              json_request=json_pq,
                              request_name='Approve prequalification',
                              entity=self.entity)

    def finish_prequalification(self, tender_id_long, token):
        return request_to_cdb(headers=tender_headers_request(json_finish_pq),
                              host=self.host,
                              endpoint='/{}?acc_token={}'.format(tender_id_long, token),
                              method='PATCH',
                              json_request=json_finish_pq,
                              request_name='Finish prequalification',
                              entity=self.entity)

    def activate_award_contract(self, tender_id_long, entity, entity_id, token, activation_json, count):
        return request_to_cdb(headers=tender_headers_request(activation_json),
                              host=self.host,
                              endpoint='/{}/{}/{}?acc_token={}'.format(tender_id_long, entity, entity_id, token),
                              method='PATCH',
                              json_request=activation_json,
                              request_name='Activate {} {}'.format(entity, count),
                              entity=self.entity)

    def add_supplier_limited(self, tender_id_long, token, add_supplier_json, supplier_number):
        return request_to_cdb(headers=tender_headers_request(add_supplier_json),
                              host=self.host,
                              endpoint='/{}/awards?acc_token={}'.format(tender_id_long, token),
                              method='POST',
                              json_request=add_supplier_json,
                              request_name='Add supplier {}'.format(supplier_number),
                              entity=self.entity)

    def make_tender_bid(self, tender_id_long, bid_json, bid_number):
        return request_to_cdb(headers=tender_headers_request(bid_json),
                              host=self.host,
                              endpoint='/{}/bids'.format(tender_id_long),
                              method='POST',
                              json_request=bid_json,
                              request_name='Publish bid {}'.format(bid_number),
                              entity=self.entity)

    def activate_tender_bid(self, tender_id_long, bid_id, bid_token, activate_bid_json, bid_number):
        return request_to_cdb(headers=tender_headers_request(activate_bid_json),
                              host=self.host,
                              endpoint='/{}/bids/{}?acc_token={}'.format(tender_id_long, bid_id, bid_token),
                              method='PATCH',
                              json_request=activate_bid_json,
                              request_name='Activate bid {}'.format(bid_number),
                              entity=self.entity)

    def get_list_of_tenders(self):
        return request_to_cdb(headers=tender_headers_request(None),
                              host=self.host_public,
                              endpoint='',
                              method='GET',
                              json_request=None,
                              request_name='Get list of tenders',
                              entity=self.entity)

    def get_bid_info(self, tender_id_long, bid_id, bid_token):
        return request_to_cdb(headers=tender_headers_request(None),
                              host=self.host,
                              endpoint='/{}/bids/{}?acc_token={}'.format(tender_id_long, bid_id, bid_token),
                              method='GET',
                              json_request=None,
                              request_name='Get bid info',
                              entity=self.entity)

    def get_contract_info(self, contract_id_long):
        return request_to_cdb(headers=None,
                              host=self.host_public_contracts,
                              endpoint='/{}'.format(contract_id_long),
                              method='GET',
                              json_request=None,
                              request_name='Get contract info',
                              entity=self.entity_contract)

    def get_contract_token(self, contract_id_long, tender_token):
        return request_to_cdb(headers=tender_headers_request(self.cdb),
                              host=self.host_contracts,
                              endpoint='/{}/credentials?acc_token={}'.format(contract_id_long, tender_token),
                              method='PATCH',
                              json_request=None,
                              request_name='Get contract token',
                              entity=self.entity_contract)

    def add_tender_document_to_ds(self, files):
        return request_to_cdb(headers=tender_headers_add_document_ds,
                              host=self.ds_host,
                              endpoint='',
                              method='POST',
                              json_request=None,
                              request_name='Add document to DS (tenders)',
                              entity=self.document,
                              is_json=False,
                              files=files)

    def add_document_from_ds_to_tender(self, tender_id_long, tender_token, json_with_document, message):
        return request_to_cdb(headers=tender_headers_patch_document_ds,
                              host=self.host,
                              endpoint="/{}/documents?acc_token={}".format(tender_id_long, tender_token),
                              method='POST',
                              json_request=json_with_document,
                              request_name=message,
                              entity=self.document)

    def add_document_from_ds_to_tender_bid(self, tender_id_long, bid_id, doc_type_url, bid_token, json_with_document, message):
        return request_to_cdb(headers=tender_headers_patch_document_ds,
                              host=self.host,
                              endpoint="/{}/bids/{}/{}?acc_token={}".format(tender_id_long, bid_id, doc_type_url, bid_token),
                              method='POST',
                              json_request=json_with_document,
                              request_name=message,
                              entity=self.document)

    def add_document_from_ds_to_entity(self, tender_id_long, entity_id, tender_token, json_with_document, message, entity):
        return request_to_cdb(headers=tender_headers_patch_document_ds,
                              host=self.host,
                              endpoint="/{}/{}/{}/documents?acc_token={}".format(tender_id_long, entity, entity_id, tender_token),
                              method='POST',
                              json_request=json_with_document,
                              request_name=message,
                              entity=self.document)
