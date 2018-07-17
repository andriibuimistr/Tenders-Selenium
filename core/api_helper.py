# -*- coding: utf-8 -*-
from api.cdb_requests import *


def create_tender(json_tender, api_version):
    tender = TenderRequests(api_version)
    t_publish = tender.publish_tender(json_tender)
    tender_id_long = t_publish.json()['data']['id']
    tender_token = t_publish.json()['access']['token']
    tender.activate_tender(tender_id_long, tender_token, json_tender['data']['procurementMethodType'])
    return t_publish.json()
