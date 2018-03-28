# from run_test import driver
import os
import time
from conftest import host, driver
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
from initial_data.tender_additional_data import key_path, key_password, document_path


def save_into_file(data):
    path = os.path.join(os.getcwd(), 'id.txt')
    f = open(path, "w+")
    f.write(data)
    f.close()


def read_from_file():
    path = os.path.join(os.getcwd(), 'id.txt')
    f = open(path, "r")
    data = f.read()
    f.close()
    return data


def login(user_email, user_pass):
    driver.find_element_by_xpath('//a[contains(text(), "Вхід")]').click()  # click link to login page

    driver.find_element_by_name('email').clear()
    driver.find_element_by_name('email').send_keys(user_email)  # enter email

    try:
        psw = driver.find_element_by_name('psw')
        psw.send_keys(user_pass)
    except Exception as e:
        password_block = driver.find_element_by_xpath('//*[@class="line userAllow userAllow1"]')
        psw = driver.find_element_by_name('psw')
        driver.execute_script("arguments[0].style.display = 'table-row';", password_block)
        psw.send_keys(user_pass)
        password_login_button = driver.find_element_by_xpath('//*[@class="buttons userAllow userAllow1"]')
        driver.execute_script("arguments[0].style.display = 'block';", password_login_button)
        print("Password field was not visible {}".format(e))
    driver.find_element_by_xpath('//div[@class="clear double"]/div[1]/div/button').click()  # click login button


def find_tender_by_id():
    uid = read_from_file()
    driver.get(host)
    Select(driver.find_element_by_name('filter[object]')).select_by_value('tenderID')
    driver.find_element_by_name('filter[search]').send_keys(uid)
    driver.find_element_by_xpath('(//button[contains(text(), "Пошук")])[1]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//a[contains(@class, "tenderLink")]').click()
    time.sleep(1)
    return driver.find_element_by_xpath('//a[@title="Оголошення на порталі Уповноваженого органу"]/span').text


def add_participant_info_limited(data):
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
    offer_amount = data['data']['value']['amount']
    driver.find_element_by_name('data[value][amount]').send_keys(str("%.2f" % offer_amount))

    # tax included as in tender
    tax_included = data['data']['value']['valueAddedTaxIncluded']
    if tax_included is True:
        tax_included = '1'
    else:
        tax_included = '0'
    Select(driver.find_element_by_name('data[value][valueAddedTaxIncluded]')).select_by_value(str(tax_included))

    # currency as in tender
    tender_currency = data['data']['value']['currency']
    Select(driver.find_element_by_name('data[value][currency]')).select_by_value(tender_currency)

    # save information
    driver.find_element_by_xpath('//tr[@class="line submitButton"]/td[2]/button').click()

    # close modal window
    time.sleep(2)
    driver.find_element_by_xpath('//div[@class="info"]/a').click()


# sign award with EDS
def qualify_winner_limited():
    time.sleep(2)
    winner_button = driver.find_element_by_xpath('//div[@class="btn2 awardActionItem"]/a')
    driver.execute_script("arguments[0].scrollIntoView();", winner_button)  # scroll to click winner
    winner_button.click()
    time.sleep(2)

    # open EDS window
    eds_button = driver.find_element_by_xpath('//div[@class="sign"]/a')
    driver.execute_script("arguments[0].scrollIntoView();", eds_button)
    eds_button.click()

    main_window = driver.current_window_handle  # set tender window

    # sign page
    driver.switch_to.window(driver.window_handles[-1])  # swith to eds tab
    driver.find_element_by_class_name('js-oldPageLink').click()  # open old eds page
    Select(driver.find_element_by_id('CAsServersSelect')).select_by_index(17)  # select eds entity
    driver.find_element_by_id('PKeyFileInput').send_keys(key_path)  # add sign file
    driver.find_element_by_id('PKeyPassword').send_keys(key_password)  # type password
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
def add_contract():
    # check "add contract" button
    count = 0
    for x in range(5):
        count += 1
        try:
            driver.refresh()
            add_contract_button = driver.find_element_by_xpath('//a[@class="reverse grey setDone"]')
            driver.execute_script("arguments[0].scrollIntoView();", add_contract_button)
            add_contract_button.click()
            if add_contract_button:
                print('Contract button was found on the page')
                break
            else:
                continue
        except Exception as e:
            print('Attempt ' + str(count) + ' - Contract button was not found on the page!')
            if count == 5:
                print(e)
                raise TimeoutError

    driver.find_element_by_xpath('//div[@class="inp l relative"]/input[2]').send_keys(document_path)
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
def sign_contract():
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
                print('Sign contract button was found on the page!')
                break
            else:
                continue
        except Exception as e:
            print('Attempt ' + str(count) + ' - Sign contract button was not found on the page:(')
            if count == 5:
                print(e)
                raise TimeoutError

    # sign page
    driver.switch_to.window(driver.window_handles[-1])  # swith to eds tab
    driver.find_element_by_class_name('js-oldPageLink').click()  # open old eds page
    Select(driver.find_element_by_id('CAsServersSelect')).select_by_visible_text('Тестовий ЦСК АТ "ІІТ"')  # select eds entity
    # driver.execute_script('var elem = document.getElementById("PKeyFileInput"); elem.style.visibility="visible"')
    # eds_file_path = os.getcwd()  # get current directory path

    driver.find_element_by_id('PKeyFileInput').send_keys(key_path)  # add sign file
    driver.find_element_by_id('PKeyPassword').send_keys(key_password)  # type password
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
