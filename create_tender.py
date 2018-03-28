# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import Select
from initial_data.tender_additional_data import select_procedure
from initial_data.tender_additional_data import limited_procurement, kiev_now
from login import driver
from initial_data.tender_additional_data import cdb_host, key_path, key_password, document_path
import time
import requests
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
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
    select_main_classification = driver.find_element_by_xpath('//input[@name="data[items][{}][cpv_id]"]/preceding-sibling::a[contains(text(), "Визначити за довідником")]'.format(item))
    v_position = select_main_classification.location['y']
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_name('data[items][{}][description]'.format(item)))
    select_main_classification.click()  # open classification window
    time.sleep(5)

    driver.switch_to.frame(driver.find_element_by_xpath('//div[@id="modal"]/div/div/iframe'))
    driver.find_element_by_xpath('//input[@id="search"]').send_keys(item_data['classification']['id'])
    time.sleep(2)
    driver.find_element_by_xpath('//a[contains(@id, "{}")]'.format(item_data['classification']['id'][:-4])).click()  # select classification
    driver.find_element_by_xpath('//div[@class="buttons"]/a').click()  # press select button
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
    driver.execute_script("arguments[0].scrollIntoView();", select_main_classification)
    delivery_end_date_path.click()
    driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", delivery_end_date_path)
    delivery_end_date_path.clear()
    delivery_end_date_path.click()
    driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", delivery_end_date_path)
    delivery_end_date_path.send_keys(delivery_date)


def fill_lot_data(lot_data, features_data, lot):
    driver.find_element_by_name('data[lots][{}][title]'.format(lot)).send_keys(lot_data['title'])
    driver.find_element_by_name('data[lots][{}][description]'.format(lot)).send_keys(lot_data['description'])
    driver.find_element_by_name('data[lots][{}][value][amount]'.format(lot)).send_keys(lot_data['value']['amount'])
    driver.find_element_by_name('data[lots][{}][minimalStep][amount]'.format(lot)).send_keys(lot_data['minimalStep']['amount'])
    if 'guarantee' in lot_data:
        driver.find_element_by_xpath('//input[@name="data[lots][{}][title]"]/ancestor::div[contains(@class, "accordionContent")]/descendant::span[contains(text(), "Електронна гарантія")][{}]'.format(lot, lot + 1)).click()
        driver.find_element_by_name('data[lots][{}][guarantee][amount]'.format(lot)).send_keys(lot_data['guarantee']['amount'])


def create_tender(tender_data):
    data = tender_data['data']
    procurement_type = data['procurementMethodType']
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
    if tender_type != 'simple':
        Select(driver.find_element_by_name('tender_type')).select_by_value(tender_type)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@class="jContent"]/div[2]/a[1]').click()  # close modal window
        time.sleep(5)

    select_tax_included = driver.find_element_by_name('data[value][valueAddedTaxIncluded]')
    driver.execute_script("arguments[0].scrollIntoView();", select_tax_included)
    Select(select_tax_included).select_by_value(json.dumps(data['value']['valueAddedTaxIncluded']))
    # select currency
    Select(driver.find_element_by_name('data[value][currency]')).select_by_value(data['value']['currency'])

    if number_of_lots == 0:
        # tender amount
        driver.find_element_by_name('data[value][amount]').send_keys(data['value']['amount'])
        if 'minimalStep' in data:
            driver.find_element_by_name('data[minimalStep][amount]').send_keys(data['minimalStep']['amount'])
        if 'guarantee' in data:
            driver.find_element_by_xpath('(//span[contains(text(), "Електронна гарантія")])[1]').click()
            driver.find_element_by_name('data[guarantee][amount]').send_keys(data['guarantee']['amount'])

    # tender title
    actual_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    driver.find_element_by_name('data[title]').send_keys(data['title'])

    # tender description
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_name('data[description]'))
    driver.find_element_by_name('data[description]').send_keys(data['description'])

    # open items section
    if number_of_lots == 0:
        section_number = 1
    else:
        section_number = 2
    items_section = driver.find_element_by_xpath('(//h3[contains(text(), "Специфікація закупівлі")])[{}]/following::a[contains(@class, "accordionOpen")][1]'.format(section_number))  # items section path
    driver.execute_script("arguments[0].scrollIntoView();", items_section)  # scroll to items section
    items_section.click()

    items = -1
    if number_of_lots != 0:
        for lot in range(len(data['lots'])):
            if lot > 0:
                driver.find_element_by_xpath('//a[contains(@class, "addMultiLot")]').click()
            lot_data = data['lots'][lot]
            if number_of_features != 0:
                features_data = []
                for feature in range(len(data['features'])):
                    if data['features'][feature]['featureOf'] == 'lot' and data['features'][feature]['relatedItem'] == data['lots'][lot]['id']:
                        features_data.append(data['features'][feature])
            else:
                features_data = []
            fill_lot_data(lot_data, features_data, lot)
            item_data = []
            for item in range(len(data['items'])):
                if data['items'][item]['relatedLot'] == data['lots'][lot]['id']:
                    item_data.append(data['items'][item])
            for lot_item in range(len(item_data)):
                items += 1
                if lot_item > 0:
                    driver.find_element_by_xpath(
                        '//input[@name="data[items][{}][description]"]/ancestor::div[contains(@class, "listItems")]/following-sibling::table[@class="addNewItem"]/descendant::a[contains(@class, "addMultiItem")]'.format(
                            items - 1)).click()
                fill_item_data(item_data[lot_item], items, procurement_type)
    else:
        for item in range(len(data['items'])):
            item_data = data['items'][item]
            if item > 0:
                driver.find_element_by_xpath('//input[@name="data[items][{}][description]"]/ancestor::div[contains(@class, "listItems")]/following-sibling::table[@class="addNewItem"]/descendant::a[contains(@class, "addMultiItem")]'.format(item - 1)).click()
            fill_item_data(item_data, item, procurement_type)

    if procurement_type == 'belowThreshold':
        enquiry_period_field = driver.find_element_by_name('data[enquiryPeriod][endDate]')
        driver.execute_script("arguments[0].scrollIntoView();", enquiry_period_field)
        enquiry_period_field.click()
        driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", enquiry_period_field)
        enquiry_period_field.send_keys(datetime.strftime(datetime.strptime(data['enquiryPeriod']['endDate'], "%Y-%m-%dT%H:%M:%S{}".format(kiev_now)), '%d/%m/%Y'))

    tender_period_end_date_field = driver.find_element_by_name('data[tenderPeriod][endDate]')
    driver.execute_script("arguments[0].scrollIntoView();", tender_period_end_date_field)
    tender_period_end_date_field.click()
    driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", tender_period_end_date_field)
    tender_period_end_date_field.send_keys(datetime.strftime(datetime.strptime(data['tenderPeriod']['endDate'], "%Y-%m-%dT%H:%M:%S{}".format(kiev_now)), '%d/%m/%Y'))

    driver.find_element_by_xpath('//button[@value="publicate"]').click()
    if driver.find_element_by_xpath('//button[@class="js-notClean_ignore_plan"]'):
        driver.find_element_by_xpath('//button[@class="js-notClean_ignore_plan"]').click()

