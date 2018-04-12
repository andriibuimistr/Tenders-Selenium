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


def get_owner_country():
    return driver.find_element_by_xpath('//td[@class="nameField"][contains(text(), "Юридична адреса")]/following-sibling::td[1]').text.split(',')[1].strip()


def get_owner_locality():
    return driver.find_element_by_xpath('//td[@class="nameField"][contains(text(), "Юридична адреса")]/following-sibling::td[1]').text.split(',')[3].strip()


def get_owner_postal_code():
    return driver.find_element_by_xpath('//td[@class="nameField"][contains(text(), "Юридична адреса")]/following-sibling::td[1]').text.split(',')[0].strip()


def get_owner_region():
    return driver.find_element_by_xpath('//td[@class="nameField"][contains(text(), "Юридична адреса")]/following-sibling::td[1]').text.split(',')[2].strip()


def get_owner_street():
    return driver.find_element_by_xpath('//td[@class="nameField"][contains(text(), "Юридична адреса")]/following-sibling::td[1]').text.split(',')[4].strip()


def get_owner_contact_name():
    return driver.find_element_by_xpath('//td[contains(text(), "Особа, відповідальна за процедуру")]/following-sibling::td').text


def get_owner_phone_number():
    return driver.find_element_by_xpath('//td[contains(text(), "Телефон")]/following-sibling::td').text


def get_owner_site():
    return driver.find_element_by_xpath('//td[contains(text(), "Веб сайт")]/following-sibling::td').text


def get_owner_company_name():
    return driver.find_element_by_xpath('//td[contains(text(), "Найменування замовника")]/following-sibling::td/a/span').text


def get_owner_identifier():
    return driver.find_element_by_xpath('//td[@class="js-identifierRatingValue"]').text


def get_item_description(item_text):
    return driver.find_element_by_xpath('//div[@class="itemDescr"][contains(text(), "{}")]'.format(item_text)).text

def get_classification_scheme():
    pass

def get_classification_identifier():
    pass

def get_classification_name():
    pass

def get_item_quantity():
    pass

def get_unit_name():
    pass

def get_delivery_date():
    pass

def get_delivery_country():
    pass

def get_delivery_postal_code():
    pass

def get_delivery_region():
    pass

def get_delivery_locality():
    pass

def get_delivery_street():
    pass

def get_document_name():
    pass

def get_document_type():
    pass

def get_document_content():
    pass
