# -*- coding: utf-8 -*-
from _datetime import datetime, timedelta
import time
from api.cdb_requests import TenderRequests
import random
import string


def get_time_difference(api_version):
    lt = int(time.mktime(datetime.utcnow().timetuple()))
    r = TenderRequests(api_version).get_list_of_tenders()
    st = int(time.mktime(datetime.strptime(r.headers['Date'][-24:-4], "%d %b %Y %H:%M:%S").timetuple()))
    return st - lt


def count_waiting_time(time_to_wait, time_template, api_version):
    diff = get_time_difference(api_version)
    wait_to = int(time.mktime(datetime.strptime(time_to_wait, time_template).timetuple()))
    time_now = int(time.mktime(datetime.now().timetuple()))
    return (wait_to - diff) - time_now


class ContractData:

    def __init__(self, api_version):
        self.time_difference = get_time_difference(api_version)

    def date_signed(self):
        return datetime.now() + timedelta(seconds=self.time_difference)

    @staticmethod
    def contract_start_date():
        return datetime.now() + timedelta(days=1)

    @staticmethod
    def contract_end_date():
        return datetime.now() + timedelta(days=30)

    @staticmethod
    def contract_number():
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
