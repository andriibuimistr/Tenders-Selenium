# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import Select
from initial_data.tender_additional_data import select_procedure
from login import driver
from initial_data.tender_additional_data import cdb_host, key_path, key_password, document_path
import time
import requests
import os
from datetime import datetime, timedelta
from selenium.webdriver.common.action_chains import ActionChains


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




    print(tender_data)
