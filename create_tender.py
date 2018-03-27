# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import Select
from initial_data.tender_additional_data import select_procedure
from initial_data.tender_additional_data import limited_procurement, kiev_now
from login import driver
from initial_data.tender_additional_data import cdb_host, key_path, key_password, document_path
import time
import requests
import os
import json
from datetime import datetime, timedelta
from selenium.webdriver.common.action_chains import ActionChains


def fill_item_data(item_data, item, procurement_type):
    # item title
    driver.find_element_by_name('data[items][{}][description]'.format(item)).send_keys(item_data['description'])

    # quantity
    driver.find_element_by_name('data[items][{}][quantity]'.format(item)).send_keys(item_data['quantity'])

    # unit id
    Select(driver.find_element_by_name('data[items][{}][unit_id]'.format(item))).select_by_visible_text(item_data['unit']['name'])

    if procurement_type in limited_procurement:
        # amount of item
        driver.find_element_by_name('data[items][{}][unit][value][amount]'.format(item)).send_keys(item_data['value']['amount'])

    # select classification
    driver.find_element_by_xpath('//input[@name="data[items][{}][cpv_id]"]/preceding-sibling::a[contains(text(), "Визначити за довідником")]'.format(item)).click()  # open classification window
    time.sleep(5)

    # switch to iframe (driver.switch_to.frame for Python 3, driver.switch_to_frame for Python2)
    driver.switch_to.frame(driver.find_element_by_xpath('//div[@id="modal"]/div/div/iframe'))
    driver.find_element_by_xpath('//input[@id="search"]').send_keys(item_data['classification']['id'])
    time.sleep(2)
    driver.find_element_by_xpath('//a[contains(@id, "{}")]'.format(item_data['classification']['id'][:-4])).click()  # select classification
    driver.find_element_by_xpath('//div[@class="buttons"]/a').click()  # press select button
    # switch to default window ('driver.switch_to.default_content' for Python 3, 'driver.switch_to_default_content' for Python 2)
    driver.switch_to.default_content()

    # select country
    Select(driver.find_element_by_name('data[items][{}][country_id]'.format(item))).select_by_visible_text(item_data['deliveryAddress']['countryName'])

    # select region
    Select(driver.find_element_by_name('data[items][{}][region_id]'.format(item))).select_by_visible_text(item_data['deliveryAddress']['region'])
    driver.find_element_by_name('data[items][{}][deliveryAddress][locality]'.format(item)).clear()
    driver.find_element_by_name('data[items][{}][deliveryAddress][locality]'.format(item)).send_keys(item_data['deliveryAddress']['locality'])
    driver.find_element_by_name('data[items][{}][deliveryAddress][streetAddress]'.format(item)).clear()
    driver.find_element_by_name('data[items][{}][deliveryAddress][streetAddress]'.format(item)).send_keys(item_data['deliveryAddress']['streetAddress'])
    driver.find_element_by_name('data[items][{}][deliveryAddress][postalCode]'.format(item)).clear()
    driver.find_element_by_name('data[items][{}][deliveryAddress][postalCode]'.format(item)).send_keys(item_data['deliveryAddress']['postalCode'])

    # delivery end date
    delivery_date = datetime.strftime(datetime.strptime(item_data['deliveryDate']['endDate'], "%Y-%m-%dT%H:%M:%S{}".format(kiev_now)), '%d/%m/%Y')
    delivery_end_date_path = driver.find_element_by_name('data[items][{}][deliveryDate][endDate]'.format(item))
    driver.execute_script("arguments[0].scrollIntoView();", delivery_end_date_path)
    delivery_end_date_path.click()
    driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", delivery_end_date_path)
    delivery_end_date_path.clear()
    delivery_end_date_path.click()
    driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", delivery_end_date_path)
    delivery_end_date_path.send_keys(delivery_date)


def create_tender(tender_data):
    data = tender_data['data']
    user_menu = driver.find_element_by_xpath('//div[contains(text(), "Мій ДЗО")]')
    hover = ActionChains(driver).move_to_element(user_menu)
    hover.perform()
    driver.find_element_by_xpath('//a[contains(text(), "Мої закупівлі")]').click()  # open procurements page
    driver.find_element_by_xpath('//div[1][@class="newTender multiButtons"]/a').click()  # click "create tender" button

    # select procedure
    Select(driver.find_element_by_name('tender_method')).select_by_visible_text(select_procedure(data['procurementMethodType']))
    time.sleep(2)
    driver.find_element_by_xpath('//*[@class="jContent"]/div[2]/a[1]').click()  # close modal window
    time.sleep(5)

    number_of_lots = 0
    if 'lots' in data:
        number_of_lots = len(data['lots'])

    number_of_features = 0
    if 'features' in data:
        number_of_features = len(data['features'])

    tender_type = 'simple'
    if number_of_features == 0 and number_of_lots > 0:
        tender_type = 'lots'
    elif number_of_features > 0 and number_of_lots == 0:
        tender_type = 'features'
    elif number_of_features > 0 and number_of_lots > 0:
        tender_type = 'features_lots'

    # Select tender type
    Select(driver.find_element_by_name('tender_type')).select_by_value(tender_type)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@class="jContent"]/div[2]/a[1]').click()  # close modal window
    time.sleep(5)

    select_tax_included = driver.find_element_by_name('data[value][valueAddedTaxIncluded]')
    driver.execute_script("arguments[0].scrollIntoView();", select_tax_included)
    Select(select_tax_included).select_by_value(json.dumps(data['value']['valueAddedTaxIncluded']))

    if number_of_lots == 0:
        # select currency
        Select(driver.find_element_by_name('data[value][currency]')).select_by_value(data['value']['currency'])
        # tender amount
        driver.find_element_by_name('data[value][amount]').send_keys(data['value']['amount'])
        if 'minimalStep' in data:
            driver.find_element_by_name('data[minimalStep][amount]').send_keys(data['minimalStep']['amount'])
        if 'guarantee' in data:
            driver.find_element_by_xpath('(//span[contains(text(), "Електронна гарантія")])[1]').click()
            driver.find_element_by_name('data[guarantee][amount]').send_keys(data['guarantee']['amount'])

    # tender title
    actual_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    driver.find_element_by_name('data[title]').send_keys('Limited Reporting ' + actual_time)

    # tender description
    driver.find_element_by_name('data[description]').send_keys('Limited Reporting Description')

    # open items section
    items_section = driver.find_element_by_xpath('//section[@id="multiItems"]//a[@class="accordionOpen icons icon_view"]')  # items section path
    driver.execute_script("arguments[0].scrollIntoView();", items_section)  # scroll to items section
    items_section.click()

    for item in range(len(data['items'])):
        item_data = data['items'][item]
        procurement_type = data['procurementMethodType']
        if item > 0:
            driver.find_element_by_xpath('//input[@name="data[items][{}][description]"]/ancestor::div[contains(@class, "listItems")]/following-sibling::table[@class="addNewItem"]/descendant::a[contains(@class, "addMultiItem")]'.format(item - 1)).click()
        fill_item_data(item_data, item, procurement_type)


    print(tender_data)
