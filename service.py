# -*- coding: utf-8 -*-
from _datetime import datetime
import time
from cdb_requests import TenderRequests


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
