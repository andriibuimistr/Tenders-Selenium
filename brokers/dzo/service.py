# -*- coding: utf-8 -*-
from datetime import datetime


def convert_delivery_date(date):
    date = datetime.strptime(date, '%d.%m.%Y')
    return datetime.strftime(date, '%Y-%m-%d')
