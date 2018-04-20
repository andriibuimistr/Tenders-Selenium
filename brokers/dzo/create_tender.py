# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import Select
from initial_data.tender_additional_data import select_procedure
from initial_data.tender_additional_data import limited_procurement, kiev_now, negotiation_procurement
from config import driver
import json
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from helper import *
from selenium_helper import *


def fill_item_data(item_data, item, procurement_type, lot=0):
    try:
        # item title
        driver.find_element_by_name('data[items][{}][description]'.format(item)).send_keys(item_data['description'])
    except:
        driver.find_element_by_xpath('//span[@class="lotIndex"][contains(text(), "{}")]/preceding-sibling::span[contains(text(), "Склад лоту")]/../following-sibling::a'.format(lot + 1)).click()
        driver.find_element_by_name('data[items][{}][description]'.format(item)).send_keys(item_data['description'])
    # quantity
    driver.find_element_by_name('data[items][{}][quantity]'.format(item)).send_keys(item_data['quantity'])

    # unit id
    Select(driver.find_element_by_name('data[items][{}][unit_id]'.format(item))).select_by_visible_text(item_data['unit']['name'])

    # if procurement_type in limited_procurement:
    #     # amount of item
    #     driver.find_element_by_name('data[items][{}][unit][value][amount]'.format(item)).send_keys(item_data['unit']['value']['amount'])

    # select classification
    select_main_classification = driver.find_element_by_xpath('//input[@name="data[items][{}][cpv_id]"]/preceding-sibling::a[contains(text(), "Визначити за довідником")]'.format(item))

    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_name('data[items][{}][description]'.format(item)))
    select_main_classification.click()  # open classification window
    # time.sleep(5)

    driver.switch_to.frame(driver.find_element_by_xpath('//div[@id="modal"]/div/div/iframe'))
    # time.sleep(5)
    wait_for_element_clickable_xpath('//input[@id="search"]')
    driver.find_element_by_xpath('//input[@id="search"]').send_keys(item_data['classification']['id'])
    # time.sleep(2)
    # wait_for_element_clickable_xpath('//a[contains(@id, "{}")]/..'.format(item_data['classification']['id'].replace('-', '_')))
    # driver.find_element_by_xpath('//a[contains(@id, "{}")]/..'.format(item_data['classification']['id'].replace('-', '_'))).click()  # select classification
    click_by_xpath('//a[contains(@id, "{}")]'.format(item_data['classification']['id'].replace('-', '_')))
    # driver.find_element_by_xpath('//div[@class="buttons"]/a').click()  # press select button
    click_by_xpath('//div[@class="buttons"]/a')
    wait_for_element_not_visible_xpath('//div[@class="buttons"]/a')
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


def fill_lot_data(lot_data, lot):
    driver.find_element_by_name('data[lots][{}][title]'.format(lot)).send_keys(lot_data['title'])
    driver.find_element_by_name('data[lots][{}][description]'.format(lot)).send_keys(lot_data['description'])
    driver.find_element_by_name('data[lots][{}][value][amount]'.format(lot)).send_keys(lot_data['value']['amount'])
    driver.find_element_by_name('data[lots][{}][minimalStep][amount]'.format(lot)).send_keys(lot_data['minimalStep']['amount'])
    if 'guarantee' in lot_data:
        driver.find_element_by_xpath(
            '//input[@name="data[lots][{}][title]"]/ancestor::div[contains(@class, "accordionContent")]/descendant::span[contains(text(), "Електронна гарантія")][{}]'.format(lot, lot + 1)).click()
        driver.find_element_by_name('data[lots][{}][guarantee][amount]'.format(lot)).send_keys(lot_data['guarantee']['amount'])


def add_tender_features(feature_data, feature_number):
    driver.find_element_by_name('data[features][{}][title]'.format(feature_number)).send_keys(feature_data['title'])
    driver.find_element_by_name('data[features][{}][description]'.format(feature_number)).send_keys(feature_data['description'])
    for option in range(len(feature_data['enum'])):
        if option > 0:
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_name('data[features][{}][title]'.format(feature_number)))
            driver.find_element_by_xpath('//h3[contains(text(), "Загальні нецінові критерії")]/../descendant::a[contains(text(), "Додати опцію")]').click()
        driver.find_element_by_name('data[features][{}][enum][{}][title]'.format(feature_number, option)).send_keys(feature_data['enum'][option]['title'])
        driver.find_element_by_name('data[features][{}][enum][{}][value]'.format(feature_number, option)).send_keys(str(int(float(feature_data['enum'][option]['value']) * 100)))


def add_lot_features(feature_data, feature_number, lot):
    driver.find_element_by_name('data[features][{}][title]'.format(feature_number)).send_keys(feature_data['title'])
    driver.find_element_by_name('data[features][{}][description]'.format(feature_number)).send_keys(feature_data['description'])
    Select(driver.find_element_by_name('data[features][{}][featureOf]'.format(feature_number))).select_by_value('lot')
    for option in range(len(feature_data['enum'])):
        if option > 0:
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_name('data[features][{}][title]'.format(feature_number)))
            driver.find_element_by_xpath(
                '//span[@class="lotIndex"][contains(text(), "{}")]/preceding-sibling::span[contains(text(), "Нецінові критерії до лоту")]/../following-sibling::div/descendant::a[contains(text(), "Додати опцію")]'.format(lot + 1)).click()
        driver.find_element_by_name('data[features][{}][enum][{}][title]'.format(feature_number, option)).send_keys(feature_data['enum'][option]['title'])
        driver.find_element_by_name('data[features][{}][enum][{}][value]'.format(feature_number, option)).send_keys(str(int(float(feature_data['enum'][option]['value'])*100)))


def create_tender(tender_data):
    data = tender_data['data']
    procurement_type = data['procurementMethodType']
    user_menu = driver.find_element_by_xpath('//div[contains(text(), "Мій ДЗО")]')
    hover = ActionChains(driver).move_to_element(user_menu)
    hover.perform()
    wait_for_element_clickable_xpath('//a[contains(text(), "Мої закупівлі")]')
    driver.find_element_by_xpath('//a[contains(text(), "Мої закупівлі")]').click()  # open procurements page
    driver.find_element_by_xpath('//div[1][@class="newTender multiButtons"]/a').click()  # click "create tender" button

    # select procedure
    Select(driver.find_element_by_name('tender_method')).select_by_visible_text(select_procedure(data['procurementMethodType']))
    wait_for_element_clickable_xpath('//*[@class="jContent"]/div[2]/a[1]')
    driver.find_element_by_xpath('//*[@class="jContent"]/div[2]/a[1]').click()  # close modal window
    wait_for_element_not_visible_xpath('//*[@class="jContent"]/div[2]/a[1]')
    # time.sleep(2)

    if procurement_type in negotiation_procurement:
        wait_for_element_clickable_xpath('//input[@value="additionalConstruction"]/following-sibling::span')
        driver.find_element_by_xpath('//input[@value="additionalConstruction"]/following-sibling::span').click()
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_name('data[description]'))
        driver.find_element_by_name('data[causeDescription]').send_keys(data['causeDescription'])

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
    driver.find_element_by_name('data[title]').send_keys(data['title'])

    # tender description
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_name('data[description]'))
    driver.find_element_by_name('data[description]').send_keys(data['description'])

    # open items section
    if number_of_lots == 0:
        section_number = 1
    else:
        section_number = 2
    wait_for_element_clickable_xpath('(//h3[contains(text(), "Специфікація закупівлі")])[{}]/following::a[contains(@class, "accordionOpen")][1]'.format(section_number))
    items_section = driver.find_element_by_xpath('(//h3[contains(text(), "Специфікація закупівлі")])[{}]/following::a[contains(@class, "accordionOpen")][1]'.format(section_number))  # items section path
    driver.execute_script("arguments[0].scrollIntoView();", items_section)  # scroll to items section
    items_section.click()

    items = -1
    feature_number = -1
    if number_of_lots != 0:
        for lot in range(len(data['lots'])):
            if lot > 0:
                driver.find_element_by_xpath('//a[contains(@class, "addMultiLot")]').click()
            lot_data = data['lots'][lot]
            fill_lot_data(lot_data, lot)
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
                fill_item_data(item_data[lot_item], items, procurement_type, lot)
            if number_of_features != 0:
                features_data = []
                for feature in range(len(data['features'])):
                    if data['features'][feature]['featureOf'] == 'lot' and data['features'][feature]['relatedItem'] == data['lots'][lot]['id']:
                        features_data.append(data['features'][feature])
                driver.find_element_by_xpath('//span[@class="lotIndex"][contains(text(), "{}")]/preceding-sibling::span[contains(text(), "Нецінові критерії до лоту")]/../following-sibling::a'.format(lot + 1)).click()
                for feature in range(len(features_data)):
                    feature_number += 1
                    driver.find_element_by_xpath(
                        '//span[@class="lotIndex"][contains(text(), "{}")]/preceding-sibling::span[contains(text(), "Нецінові критерії до лоту")]/../../descendant::a[contains(text(), "Додати критерій")]'.format(lot + 1)).click()
                    add_lot_features(features_data[feature], feature_number, lot)
    else:
        for item in range(len(data['items'])):
            item_data = data['items'][item]
            if item > 0:
                driver.find_element_by_xpath(
                    '//input[@name="data[items][{}][description]"]/ancestor::div[contains(@class, "listItems")]/following-sibling::table[@class="addNewItem"]/descendant::a[contains(@class, "addMultiItem")]'.format(item - 1)).click()
            fill_item_data(item_data, item, procurement_type)

    if number_of_features != 0:
        features_tender = []
        for feature in range(len(data['features'])):
            if data['features'][feature]['featureOf'] == 'tenderer':
                features_tender.append(data['features'][feature])
        if len(features_tender) > 0:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.find_element_by_xpath('//h3[contains(text(), "Загальні нецінові критерії")]/following-sibling::a[contains(@class, "accordionOpen")]').click()
            for tender_feature in range(len(features_tender)):
                feature_number += 1
                if tender_feature > 0:
                    driver.find_element_by_xpath('//h3[contains(text(), "Загальні нецінові критерії")]/../descendant::a[contains(text(), "Додати критерій")]').click()
                add_tender_features(features_tender[tender_feature], feature_number)

    if procurement_type == 'belowThreshold':
        enquiry_period_field = driver.find_element_by_name('data[enquiryPeriod][endDate]')
        driver.execute_script("arguments[0].scrollIntoView();", enquiry_period_field)
        enquiry_period_field.click()
        driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", enquiry_period_field)
        enquiry_period_field.send_keys(datetime.strftime(datetime.strptime(data['enquiryPeriod']['endDate'], "%Y-%m-%dT%H:%M:%S{}".format(kiev_now)), '%d/%m/%Y'))
    if procurement_type not in limited_procurement:
        tender_period_end_date_field = driver.find_element_by_name('data[tenderPeriod][endDate]')
        driver.execute_script("arguments[0].scrollIntoView();", tender_period_end_date_field)
        tender_period_end_date_field.click()
        driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", tender_period_end_date_field)
        tender_period_end_date_field.send_keys(datetime.strftime(datetime.strptime(data['tenderPeriod']['endDate'], "%Y-%m-%dT%H:%M:%S{}".format(kiev_now)), '%d/%m/%Y'))

    driver.find_element_by_xpath('//button[@value="publicate"]').click()
    if driver.find_element_by_xpath('//button[@class="js-notClean_ignore_plan"]'):
        driver.find_element_by_xpath('//button[@class="js-notClean_ignore_plan"]').click()


