# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import Select
from login import driver
import time
import requests
import os
from datetime import datetime, timedelta


cdb_host = 'http://api-sandbox.prozorro.openprocurement.net/api/dev/tenders/'


def create_limited_reporting_simple():
    driver.find_element_by_xpath('//nav[@class="l menu relative clear yetInside1"]/div[1]/a').click()  # open procurements page
    driver.find_element_by_xpath('//div[1][@class="newTender multiButtons"]/a').click()  # click "create tender" button

    # select procedure
    Select(driver.find_element_by_name('tender_method')).select_by_value('limited_reporting')
    time.sleep(2)
    driver.find_element_by_xpath('//*[@class="jContent"]/div[2]/a[1]').click()  # close modal window
    time.sleep(5)

    # select currency
    Select(driver.find_element_by_name('data[value][currency]')).select_by_value('USD')

    # tender amount
    driver.find_element_by_name('data[value][amount]').send_keys('1000')

    # VAT
    select_tax_included = driver.find_element_by_name('data[value][valueAddedTaxIncluded]')
    driver.execute_script("arguments[0].scrollIntoView();", select_tax_included)
    Select(select_tax_included).select_by_value('false')

    # tender title
    actual_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    driver.find_element_by_name('data[title]').send_keys('Limited Reporting ' + actual_time)

    # tender description
    driver.find_element_by_name('data[description]').send_keys('Limited Reporting Description')

    # open items section
    items_section = driver.find_element_by_xpath('//section[@id="multiItems"]//a[@class="accordionOpen icons icon_view"]')  # items section path
    driver.execute_script("arguments[0].scrollIntoView();", items_section)  # scroll to items section
    items_section.click()

    # item title
    driver.find_element_by_name('data[items][0][description]').send_keys('Item 1')

    # quantity
    driver.find_element_by_name('data[items][0][quantity]').send_keys('10')

    # unit id
    Select(driver.find_element_by_name('data[items][0][unit_id]')).select_by_value('927')

    # amount of item
    driver.find_element_by_name('data[items][0][unit][value][amount]').send_keys('2')

    # select classification
    driver.find_element_by_xpath('//div[1][@class="relative inp empty"]/a[1]').click()  # open classification window
    time.sleep(5)

    # switch to iframe (driver.switch_to.frame for Python 3, driver.switch_to_frame for Python2)
    driver.switch_to.frame(driver.find_element_by_xpath('//div[@id="modal"]/div/div/iframe'))
    driver.find_element_by_xpath('//div[@id="frmt"]/ul/li[1]').click()  # select classification
    driver.find_element_by_xpath('//div[@class="buttons"]/a').click()  # press select button
    # switch to default window ('driver.switch_to.default_content' for Python 3, 'driver.switch_to_default_content' for Python 2)
    driver.switch_to.default_content()

    # select country
    Select(driver.find_element_by_name('data[items][0][country_id]')).select_by_value('461')

    # select region
    Select(driver.find_element_by_name('data[items][0][region_id]')).select_by_value('by_docs')

    # delivery end date
    delivery_date = (datetime.now() + timedelta(days=10)).strftime('%d/%m/%Y')
    delivery_end_date_path = driver.find_element_by_name('data[items][0][deliveryDate][endDate]')
    driver.execute_script("arguments[0].scrollIntoView();", delivery_end_date_path)
    delivery_end_date_path.click()
    driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", delivery_end_date_path)
    delivery_end_date_path.send_keys(delivery_date)
    #driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/table/tbody/tr[last()]/td[@data-handler="selectDay"][last()]').click()

    ''' # save draft
    save_draft_button = driver.find_element_by_xpath('//button[@class="saveDraft"]')  # button path
    driver.execute_script("arguments[0].scrollIntoView();", save_draft_button)  # scroll to button
    save_draft_button.click()  # save draft'''

    # publish tender
    publish_button = driver.find_element_by_xpath('//div[@class="clear double"]/div/div/button')
    driver.execute_script("arguments[0].scrollIntoView();", publish_button)
    publish_button.click()

    if driver.find_element_by_xpath('//div[@class="saved"]'):
        driver.find_element_by_xpath('//section[@class="buttons"]/div/button').click()
    else:
        pass


# get tender json from CDB
def get_json_from_cdb():
    # get long tender ID
    tender_id = driver.find_element_by_xpath('//span[@id="tender_id"]').text
    cdb_json = requests.get(cdb_host + tender_id)
    return cdb_json.json()

# get and convert information from tender page
def get_data_limited_reporting_simple(parameter):
    result = None
    if parameter == 'tender_amount': # convert tender amount
        result = driver.find_element_by_xpath('//*[@class="infoBlock relative"]/table/tbody[2]/tr/td[2]/span[1]').text.replace('`', '')
    elif parameter == 'tender_currency':
        currency = driver.find_element_by_xpath('//*[@class="infoBlock relative"]/table/tbody[2]/tr/td[2]/span[2]').text
        if currency == '$':
            result = 'USD'
    elif parameter == 'tender_taxIncluded':
        tax_included = driver.find_element_by_xpath('//*[@class="infoBlock relative"]/table/tbody[2]/tr/td[2]/span[3]/span').text
        if tax_included == u'без ПДВ':
            result = False
        elif tax_included == u'з ПДВ':
            result = True
    return result


def add_participant_info_limited_reporting_simple():
    add_participant_info_button = driver.find_element_by_xpath('//a[@class="button reverse addAward"]')  # path of "add info" button
    driver.execute_script("arguments[0].scrollIntoView();", add_participant_info_button)  # scroll to button
    add_participant_info_button.click()
    time.sleep(2)
    driver.find_element_by_xpath('//div[@class="jBtnWrap"]/a[1]').click()  # click "ok" in modal window
    time.sleep(2)
    driver.find_element_by_name('data[suppliers][0][name]').send_keys('Name of participant\'s organization')  # participant's name
    Select(driver.find_element_by_name('data[suppliers][0][identifier][scheme]')).select_by_value('UA-EDR')  # select country of registration
    driver.find_element_by_name('data[suppliers][0][identifier][id]').send_keys('00000000')  # identifier
    Select(driver.find_element_by_name('data[suppliers][0][address][countryName]')).select_by_value(u'Україна')  # select country
    time.sleep(1)
    Select(driver.find_element_by_name('data[suppliers][0][address][region]')).select_by_value(u'м. Київ')  # select region
    driver.find_element_by_name('data[suppliers][0][address][locality]').send_keys(u'Київ')  # locality
    driver.find_element_by_name('data[suppliers][0][address][streetAddress]').send_keys(u'Адрес')  # address
    driver.find_element_by_name('data[suppliers][0][address][postalCode]').send_keys('00000')  # postal code
    driver.find_element_by_name('data[suppliers][0][contactPoint][name]').send_keys(u'Контактное Лицо')  # contact point
    driver.find_element_by_name('data[suppliers][0][contactPoint][email]').send_keys('i@i.ua')  # email
    driver.find_element_by_name('data[suppliers][0][contactPoint][telephone]').send_keys('+380200000000')  # phone number
    driver.find_element_by_name('data[suppliers][0][contactPoint][faxNumber]').send_keys('+380200000000')  # fax
    driver.find_element_by_name('data[suppliers][0][contactPoint][url]').send_keys('https://www.google.com.ua/?gws_rd=ssl')  # site

    # amount as in tender
    offer_amount = get_json_from_cdb()['data']['value']['amount']
    driver.find_element_by_name('data[value][amount]').send_keys(str("%.2f" % offer_amount))

    # tax included as in tender
    taxIncluded = get_json_from_cdb()['data']['value']['valueAddedTaxIncluded']
    if taxIncluded == True:
        taxIncluded = '1'
    elif taxIncluded == False:
        taxIncluded = '0'
    Select(driver.find_element_by_name('data[value][valueAddedTaxIncluded]')).select_by_value(str(taxIncluded))

    # currency as in tender
    tender_currency = get_json_from_cdb()['data']['value']['currency']
    Select(driver.find_element_by_name('data[value][currency]')).select_by_value(tender_currency)

    # save information
    driver.find_element_by_xpath('//tr[@class="line submitButton"]/td[2]/button').click()

    # close modal window
    time.sleep(2)
    driver.find_element_by_xpath('//div[@class="info"]/a').click()


# sign award with EDS
def qualify_winner_limited_reporting_simple():
    winner_button = driver.find_element_by_xpath('//div[@class="btn2 awardActionItem"]/a')
    driver.execute_script("arguments[0].scrollIntoView();", winner_button)  # scroll to click winner
    winner_button.click()
    time.sleep(2)

    # open EDS window
    eds_button = driver.find_element_by_xpath('//div[@class="sign"]/a')
    driver.execute_script("arguments[0].scrollIntoView();", eds_button)
    eds_button.click()

    main_window = driver.current_window_handle  # set tender window
    # tender_url = driver.current_url  # set tender url

    # sign page
    driver.switch_to.window(driver.window_handles[-1])  # swith to eds tab
    driver.find_element_by_class_name('js-oldPageLink').click()  # open old eds page
    Select(driver.find_element_by_id('CAsServersSelect')).select_by_index(17)  # select eds entity
    # driver.execute_script('var elem = document.getElementById("PKeyFileInput"); elem.style.visibility="visible"')
    eds_file_path = os.getcwd()  # get current directory path
    driver.find_element_by_id('PKeyFileInput').send_keys('{}\Key-6.dat'.format(eds_file_path))  # add sign file
    driver.find_element_by_id('PKeyPassword').send_keys('12345677')  # type password
    driver.find_element_by_id('PKeyReadButton').click()  # click read key button

    if driver.find_element_by_id(
            'PKStatusInfo').text == u'Ключ успішно завантажено':  # check successful read key message
        time.sleep(2)
        driver.find_element_by_id('SignDataButton').click()  # click sign button
        time.sleep(2)
        if driver.find_element_by_id('PKStatusInfo').text == u'Підпис успішно накладено та передано у ЦБД':
            time.sleep(2)
            driver.close()  # close sign page tab
            driver.switch_to_window(main_window)  # switch to tender window


# add contract for limited reporting procedure
def add_contract_limited_reporting_simple():
    # check "add contract" button
    count = 0
    for x in range(5):
        count += 1
        try:
            #time.sleep(20)
            driver.refresh()
            add_contract_button = driver.find_element_by_xpath('//a[@class="reverse grey setDone"]')
            driver.execute_script("arguments[0].scrollIntoView();", add_contract_button)
            add_contract_button.click()
            if add_contract_button:
                print 'Contract button was found on the page'
                break
            else:
                continue
        except Exception as e:
            print 'Attempt ' + str(count) + ' - Contract button was not found on the page!'
            if count == 5:
                print e
                raise StandardError

    doc_file_path = os.getcwd()
    driver.find_element_by_xpath('//div[@class="inp l relative"]/input[2]').send_keys('{}\Doc.pdf'.format(doc_file_path))
    driver.find_element_by_xpath('//div[@class="inp langSwitch langSwitch_uk dataFormatHelpInside"]/input').send_keys('Contract')
    Select(driver.find_element_by_name('documentType')).select_by_value('contractSigned')
    driver.find_element_by_xpath('//button[@class="icons icon_upload relative"]').click()
    time.sleep(2)

    driver.find_element_by_name('data[contractNumber]').send_keys('123456')

    # add date of sign
    date_signed_path = driver.find_element_by_name('data[dateSigned]')
    date_signed = datetime.now().strftime('%d/%m/%Y')
    driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", date_signed_path)
    date_signed_path.send_keys(date_signed)

    # contract start date
    time.sleep(1)
    contract_start_date_path = driver.find_element_by_name('data[period][startDate]')
    contract_start_date = (datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')
    driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", contract_start_date_path)
    contract_start_date_path.send_keys(contract_start_date)

    # contract end date
    time.sleep(1)
    contract_end_date_path = driver.find_element_by_name('data[period][endDate]')
    contract_end_date = (datetime.now() + timedelta(days=30)).strftime('%d/%m/%Y')
    driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", contract_end_date_path)
    contract_end_date_path.send_keys(contract_end_date)

    # submit form button
    time.sleep(2)
    driver.find_element_by_xpath('//button[@class="bidAction"]').click()

    # click "ok" in modal window
    time.sleep(2)
    driver.find_element_by_xpath('//div[@class="jBtnWrap"]/a[1]').click()

    time.sleep(2)


# sign contract for limited reporting procedure
def sign_contract_limited_reporting_simple():
    # check "sign contract" button
    main_window = driver.current_window_handle  # set tender window
    count = 0
    for x in range(5):
        count += 1
        try:
            driver.refresh()
            time.sleep(2)
            add_contract_button = driver.find_element_by_xpath('//a[@class="reverse grey setDone"]')
            driver.execute_script("arguments[0].scrollIntoView();", add_contract_button)
            add_contract_button.click()
            time.sleep(2)
            sign_contract_button = driver.find_element_by_xpath('//div[@class="sign"]/a')
            driver.execute_script("arguments[0].scrollIntoView();", sign_contract_button)
            sign_contract_button.click()
            if sign_contract_button:
                print 'Sign contract button was found on the page!'
                break
            else:
                continue
        except Exception as e:
            print 'Attempt ' + str(count) + ' - Sign contract button was not found on the page:('
            if count == 5:
                print e
                raise StandardError

    # sign page
    driver.switch_to.window(driver.window_handles[-1])  # swith to eds tab
    driver.find_element_by_class_name('js-oldPageLink').click()  # open old eds page
    Select(driver.find_element_by_id('CAsServersSelect')).select_by_index(17)  # select eds entity
    # driver.execute_script('var elem = document.getElementById("PKeyFileInput"); elem.style.visibility="visible"')
    eds_file_path = os.getcwd()  # get current directory path
    driver.find_element_by_id('PKeyFileInput').send_keys('{}\Key-6.dat'.format(eds_file_path))  # add sign file
    driver.find_element_by_id('PKeyPassword').send_keys('qwerty')  # type password
    driver.find_element_by_id('PKeyReadButton').click()  # click read key button

    if driver.find_element_by_id('PKStatusInfo').text == u'Ключ успішно завантажено':  # check successful read key message
        time.sleep(2)
        driver.find_element_by_id('SignDataButton').click()  # click sign button
        time.sleep(2)
        if driver.find_element_by_id('PKStatusInfo').text == u'Підпис успішно накладено та передано у ЦБД':
            time.sleep(2)
            driver.close()  # close sign page tab
            driver.switch_to_window(main_window)  # switch to tender window

    # close modal window
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="modal"]/div[2]/a').click()
    time.sleep(2)