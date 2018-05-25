# -*- coding: utf-8 -*-
from datetime import datetime


def convert_date_with_dots_from__page(date):
    date = datetime.strptime(date, '%d.%m.%Y')
    return datetime.strftime(date, '%Y-%m-%d')
