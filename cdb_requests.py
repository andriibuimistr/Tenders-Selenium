# -*- coding: utf-8 -*-
from tenders.tender_data_for_requests import tender_headers_request, tender_host_selector, json_activate_tender, json_finish_first_stage, json_finish_pq
from flask import abort
import json
import requests
from requests.exceptions import ConnectionError, HTTPError
import time


# Send request to cdb
def request_to_cdb(headers, host, endpoint, method, json_request, request_name, entity=''):
    attempts = 0
    for x in range(5):
        attempts += 1
        try:
            s = requests.Session()
            s.request("HEAD", "{}".format(host))
            r = requests.Request(method, "{}{}".format(host, endpoint),
                                 data=json.dumps(json_request),
                                 headers=headers,
                                 cookies=requests.utils.dict_from_cookiejar(s.cookies))
            prepped = s.prepare_request(r)
            resp = s.send(prepped)
            resp.raise_for_status()
            if resp.status_code in [200, 201, 202]:
                # print("{}: Success".format(request_name))
                # print("       status code:  {}".format(resp.status_code))
                # save_log(resp.status_code, resp.content, resp.headers, host, endpoint, method, request_name, entity)
                return resp
        except HTTPError as error:
            print("{}: Error".format(request_name))
            print("       status code:  {}".format(resp.status_code))
            print("       response content:  {}".format(resp.content))
            print("       headers:           {}".format(resp.headers))
            # save_log(error.response.status_code, resp.content, resp.headers, host, endpoint, method, request_name, entity)
            time.sleep(1)
            if attempts >= 5:
                abort(error.response.status_code, resp.content)
        except ConnectionError as e:
            print('Connection Exception')
            if attempts < 5:
                time.sleep(1)
                continue
            else:
                # save_log(503, str(e), 'No header', host, endpoint, method, request_name, entity)
                abort(503, '{} error: {}'.format(request_name, e))
        except requests.exceptions.MissingSchema as e:
            print('MissingSchema Exception')
            # save_log(500, str(e), 'No header', host, endpoint, method, request_name, entity)
            abort(500, '{} error: {}'.format(request_name, e))
        except Exception as e:
            print('General Exception')
            # save_log(500, str(e), 'No header', host, endpoint, method, request_name, entity)
            abort(500, '{} error: {}'.format(request_name, e))


class TenderRequests:

    def __init__(self, cdb):
        self.cdb = cdb
        self.host = tender_host_selector(cdb)[0]
        self.host_public = tender_host_selector(cdb)[1]
        self.entity = 'tenders'

    # def publish_tender(self, json_tender):
    #     return request_to_cdb(tender_headers_request(self.cdb, json_tender), self.host, '', 'POST', json_tender, 'Publish tender', self.entity)
    #
    # def activate_tender(self, tender_id_long, token, procurement_method):
    #     json_tender_activation = json_activate_tender(procurement_method)
    #     return request_to_cdb(tender_headers_request(self.cdb, json_tender_activation), self.host, '/{}?acc_token={}'.format(tender_id_long, token), 'PATCH', json_tender_activation, 'Activate tender', self.entity)

    def get_tender_info(self, tender_id_long):
        return request_to_cdb(None, self.host_public, '/{}'.format(tender_id_long), 'GET', None, 'Get tender info', self.entity)

    # def finish_first_stage(self, tender_id_long, token):
    #     return request_to_cdb(tender_headers_request(self.cdb, json_finish_first_stage), self.host, '/{}?acc_token={}'.format(tender_id_long, token), 'PATCH', json_finish_first_stage,
    #                           'Finish first stage', self.entity)
    #
    # def patch_second_stage(self, tender_id_long, token, json_patch_2nd_stage):
    #     return request_to_cdb(tender_headers_request(self.cdb, json_patch_2nd_stage), self.host, '/{}?acc_token={}'.format(tender_id_long, token), 'PATCH',  json_patch_2nd_stage,
    #                           'Patch 2nd stage', self.entity)
    #
    # def activate_2nd_stage(self, tender_id_long, token, procurement_method):
    #     json_tender_activation = json_activate_tender(procurement_method)
    #     return request_to_cdb(tender_headers_request(self.cdb, json_tender_activation), self.host, '/{}?acc_token={}'.format(tender_id_long, token), 'PATCH', json_tender_activation,
    #                           'Activate 2nd stage', self.entity)
    #
    # def get_2nd_stage_info(self, tender_id_long, token):
    #     return request_to_cdb(tender_headers_request(self.cdb, None), self.host, '/{}/credentials?acc_token={}'.format(tender_id_long, token), 'PATCH', None, 'Get 2nd stage info', self.entity)
    #
    # def approve_prequalification(self, tender_id_long, qualification_id, token, json_pq):
    #     return request_to_cdb(tender_headers_request(self.cdb, json_pq), self.host, '/{}/qualifications/{}?acc_token={}'.format(tender_id_long, qualification_id, token), 'PATCH', json_pq,
    #                           'Approve prequalification', self.entity)
    #
    # def finish_prequalification(self, tender_id_long, token):
    #     return request_to_cdb(tender_headers_request(self.cdb, json_finish_pq), self.host, '/{}?acc_token={}'.format(tender_id_long, token), 'PATCH', json_finish_pq,
    #                           'Finish prequalification', self.entity)
    #
    # def activate_award_contract(self, tender_id_long, entity, entity_id, token, activation_json, count):
    #     request_to_cdb(tender_headers_request(self.cdb, activation_json), self.host, '/{}/{}/{}?acc_token={}'.format(tender_id_long, entity, entity_id, token), 'PATCH', activation_json,
    #                    'Activate {} {}'.format(entity, count), self.entity)
    #
    # def add_supplier_limited(self, tender_id_long, token, add_supplier_json, supplier_number):
    #     return request_to_cdb(tender_headers_request(self.cdb, add_supplier_json), self.host, '/{}/awards?acc_token={}'.format(tender_id_long, token), 'POST', add_supplier_json,
    #                           'Add supplier {}'.format(supplier_number), self.entity)
    #
    # def make_tender_bid(self, tender_id_long, bid_json, bid_number):
    #     return request_to_cdb(tender_headers_request(self.cdb, bid_json), self.host, '/{}/bids'.format(tender_id_long), 'POST', bid_json, 'Publish bid {}'.format(bid_number), self.entity)
    #
    # def activate_tender_bid(self, tender_id_long, bid_id, bid_token, activate_bid_json, bid_number):
    #     return request_to_cdb(tender_headers_request(self.cdb, activate_bid_json), self.host, '/{}/bids/{}?acc_token={}'.format(tender_id_long, bid_id, bid_token), 'PATCH', activate_bid_json,
    #                           'Activate bid {}'.format(bid_number), self.entity)
    #
    # def get_list_of_tenders(self):
    #     return request_to_cdb(tender_headers_request(self.cdb, None), self.host_public, '', 'GET', None, 'Get list of tenders', self.entity)
    #
    # def get_bid_info(self, tender_id_long, bid_id, bid_token):
    #     return request_to_cdb(tender_headers_request(self.cdb, None), self.host, '/{}/bids/{}?acc_token={}'.format(tender_id_long, bid_id, bid_token), 'GET', None, 'Get bid info', self.entity)