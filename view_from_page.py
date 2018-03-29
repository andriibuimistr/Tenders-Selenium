# -*- coding: utf-8 -*-
from config import driver
import time


def get_tender_id():
    tid = driver.find_element_by_id('tender_id').text
    return tid


def get_tender_uid():
    uid = driver.find_element_by_xpath('//a[@title="Оголошення на порталі Уповноваженого органу"]/span').text
    return uid


def get_tender_title():
    time.sleep(5)
    title = driver.find_element_by_xpath('//h1[@class="t_title"]')
    driver.execute_script("arguments[0].scrollIntoView();", title)
    return title.text.split('] ')[-1]


def get_tender_description():
    return driver.find_element_by_xpath('//h2[@class="tenderDescr"]').text


def get_tender_value_amount():
    amount = driver.find_element_by_xpath('//span[contains(@class, "js-pricedecor")]').text.replace('`', '')
    cents = driver.find_element_by_xpath('//span[contains(@class, "js-pricedecor")]/following-sibling::span[1]').text
    return float('{}.{}'.format(amount, cents))


def get_tender_currency():
    currency = driver.find_element_by_xpath('//span[contains(@class, "js-pricedecor")]/following-sibling::span[2]/span').text
    return {'€': 'EUR',
            '$': 'USD',
            'грн': 'UAH',
            '₽': 'RUB',
            '£': 'GBP'}.get(currency, currency)


def get_value_added_tax_included():
    added_tax = driver.find_element_by_xpath('//span[contains(@class, "taxIncluded")]/span').text
    return {'з ПДВ': True,
            'без ПДВ': False}.get(added_tax, added_tax)
