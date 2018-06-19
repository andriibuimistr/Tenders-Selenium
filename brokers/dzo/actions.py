# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import Select
from brokers.dzo.config import *
# from selenium_helper import *
from initial_data.tender_additional_data import key_path, key_password, document_path
from brokers.dzo.view_from_page import *


def login(user):
    click_by_xpath('//a[contains(text(), "Вхід")]')
    driver.find_element_by_name('email').clear()
    send_keys_name('email', credentials[user]['username'])
    password_block = driver.find_element_by_xpath('//*[@class="line userAllow userAllow1"]')
    driver.execute_script("arguments[0].style.display = 'table-row';", password_block)
    send_keys_name('psw', credentials[user]['password'])
    password_login_button = driver.find_element_by_xpath('//*[@class="buttons userAllow userAllow1"]')
    driver.execute_script("arguments[0].style.display = 'block';", password_login_button)
    click_by_xpath('//div[@class="clear double"]/div[1]/div/button')


def find_tender_by_id(uid):
    driver.get(host)
    Select(driver.find_element_by_name('filter[object]')).select_by_value('tenderID')
    wait_for_element_present_name('filter[object]')
    send_keys_name('filter[search]', uid)
    click_by_xpath('(//button[contains(text(), "Пошук")])[1]')
    wait_for_element_clickable_xpath('//span[contains(text(), "{}")]'.format(uid))
    click_by_xpath('//span[contains(text(), "{}")]/ancestor::div[5]/descendant::h2[@class="title"]/a'.format(uid))
    return get_text_xpath('//a[@title="Оголошення на порталі Уповноваженого органу"]/span')


def find_contract_by_id(uid):
    driver.get(host)
    click_by_xpath('//a[@href="/tenders/contracts"]')
    wait_for_element_clickable_name('filter[object]')
    Select(driver.find_element_by_name('filter[object]')).select_by_value('contractID')
    wait_for_element_present_name('filter[object]')
    send_keys_name('filter[search]', uid)
    click_by_xpath('(//button[contains(text(), "Пошук")])[1]')
    wait_for_element_clickable_xpath('//span[contains(text(), "{}")]'.format(uid))
    click_by_xpath('//span[contains(text(), "{}")]/ancestor::div[5]/descendant::h2[@class="title"]/a'.format(uid))
    return get_text_xpath('//a[@title="Оголошення в ЦБД"]/span')


def open_tender_edit_page(uid):
    tender_edit_button = driver.find_element_by_xpath('//a[contains(@class, "save")]')
    scroll_into_view_xpath('//a[contains(@class, "save")]')  # scroll to tender edit button
    tender_edit_button.click()
    wait_for_element_clickable_xpath('//h3[contains(@class, "bigTitle")]')


def open_contract_edit_page():
    scroll_into_view_xpath('//a[contains(@class, "save")]')
    click_by_xpath('//a[contains(@class, "save")]')
    wait_for_element_clickable_xpath('//h3[contains(@class, "bigTitle")]')


def eds_sign(eds_button):
    driver.execute_script("arguments[0].scrollIntoView();", eds_button)
    eds_button.click()

    main_window = driver.current_window_handle  # set tender window

    # sign page
    driver.switch_to.window(driver.window_handles[-1])  # swith to eds tab
    driver.find_element_by_class_name('js-oldPageLink').click()  # open old eds page
    for x in range(5):
        Select(driver.find_element_by_id('CAsServersSelect')).select_by_index(17)  # select eds entity
        add_docs_id('PKeyFileInput', key_path)  # add sign file
        send_keys_id('PKeyPassword', key_password)  # type password
        click_by_id('PKeyReadButton')  # click read key button

        if driver.find_element_by_id('PKStatusInfo').text == u'Ключ успішно завантажено':  # check successful read key message
            time.sleep(2)
            click_by_id('SignDataButton')  # click sign button
            time.sleep(5)
            if driver.find_element_by_id('PKStatusInfo').text == u'Підпис успішно накладено та передано у ЦБД':
                driver.close()  # close sign page tab
                driver.switch_to_window(main_window)  # switch to tender window
                break
            else:
                driver.find_element_by_xpath('//button[@id="PKeyReadButton"][contains(text(), "Зтерти")]').click()


def add_participant_info_limited(data):
    add_participant_info_button = driver.find_element_by_xpath('//a[@class="button reverse addAward"]')  # path of "add info" button
    scroll_into_view_xpath('//a[@class="button reverse addAward"]')  # scroll to button
    add_participant_info_button.click()
    click_and_wait_for_disappear_xpath('//div[@class="jBtnWrap"]/a[1]')
    send_keys_name('data[suppliers][0][name]', 'Name of participant\'s organization')
    Select(driver.find_element_by_name('data[suppliers][0][identifier][scheme]')).select_by_value('UA-EDR')  # select country of registration
    send_keys_name('data[suppliers][0][identifier][id]', '00000000')  # identifier
    Select(driver.find_element_by_name('data[suppliers][0][address][countryName]')).select_by_value(u'Україна')  # select country
    wait_for_element_clickable_name('data[suppliers][0][address][region]')
    Select(driver.find_element_by_name('data[suppliers][0][address][region]')).select_by_value(u'м. Київ')  # select region
    send_keys_name('data[suppliers][0][address][locality]', u'Київ')  # locality
    send_keys_name('data[suppliers][0][address][streetAddress]', u'Адрес')  # address
    send_keys_name('data[suppliers][0][address][postalCode]', '00000')  # postal code
    send_keys_name('data[suppliers][0][contactPoint][name]', u'Контактное Лицо')  # contact point
    send_keys_name('data[suppliers][0][contactPoint][email]', 'i@i.ua')  # email
    send_keys_name('data[suppliers][0][contactPoint][telephone]', '+380200000000')  # phone number
    send_keys_name('data[suppliers][0][contactPoint][faxNumber]', '+380200000000')  # fax
    send_keys_name('data[suppliers][0][contactPoint][url]', 'https://www.google.com.ua/?gws_rd=ssl')  # site

    if check_presence_xpath('//select[@name="data[lotID]"]') is True:
        Select(driver.find_element_by_xpath('//select[@name="data[lotID]"]')).select_by_index(1)

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
    click_by_xpath('//tr[@class="line submitButton"]/td[2]/button')

    # close modal window
    wait_for_element_not_visible_xpath('//body[contains(@class, "blocked")]', 20)
    wait_for_element_clickable_xpath('//div[@class="info"]/a')
    click_by_xpath('//div[@class="info"]/a')


def add_qualification_document():
    add_docs_xpath('//input[contains(@name, "upload")]', document_path)
    send_keys_xpath('//div[@class="inp langSwitch langSwitch_uk dataFormatHelpInside"]/input', 'Qualified')
    Select(driver.find_element_by_name('documentType')).select_by_value('notice')
    click_by_xpath('//button[@class="icons icon_upload relative"]')
    wait_for_element_not_visible_xpath('//body[contains(@class, "blocked")]', 20)
    scroll_into_view_xpath('//button[contains(@class, "bidAction")]')
    click_by_xpath('//input[@name="data[qualified]"]/..')
    click_by_xpath('//button[contains(@class, "bidAction")]')
    wait_for_element_not_visible_xpath('//button[contains(@class, "bidAction")]', 20)


# sign award with EDS
def qualify_winner_limited(data):
    procurement_type = data['procurementMethodType']
    wait_for_element_clickable_xpath('//div[@class="btn2 awardActionItem"]/a')
    winner_button = driver.find_element_by_xpath('//div[@class="btn2 awardActionItem"]/a')
    scroll_into_view_xpath('//div[@class="btn2 awardActionItem"]/a')  # scroll to click winner
    winner_button.click()

    if procurement_type == 'reporting':
        # open EDS window
        wait_for_element_present_xpath('//div[@class="sign"]/a')
        eds_button = driver.find_element_by_xpath('//div[@class="sign"]/a')
        eds_sign(eds_button)
        count = 0
        for x in range(20):
            count += 1
            try:
                refresh_page()
                if check_presence_xpath('//a[@class="reverse grey setDone"]') is True:
                    break
            except Exception as e:
                time.sleep(2)
                if count == 20:
                    print(''.format(e))
                    raise TimeoutError
    else:
        add_qualification_document()
        count = 0
        for x in range(20):
            count += 1
            try:
                refresh_page()
                wait_for_element_clickable_xpath('//a[contains(text(), "Необхідний ЕЦП")]')
                sign_winner_button = driver.find_element_by_xpath('//a[contains(text(), "Необхідний ЕЦП")]')
                scroll_into_view_xpath('//a[contains(text(), "Необхідний ЕЦП")]')
                sign_winner_button.click()
                sign_contract_button = driver.find_element_by_xpath('//div[@class="sign"]/a')
                scroll_into_view_xpath('//div[@class="sign"]/a')
                if sign_contract_button.is_displayed():
                    eds_sign(sign_contract_button)
                    break
                else:
                    time.sleep(10)
                    continue
            except Exception as e:
                if count == 20:
                    print(str(e))
                    raise TimeoutError
        count = 0
        for x in range(20):
            count += 1
            try:
                refresh_page()
                complaint_period_title = wait_for_element_present_xpath('//span[contains(text(), "Триває період прийому оскаржень щодо кваліфікації учасника. Дата завершення:")]')
                if complaint_period_title:
                    break
            except Exception as e:
                time.sleep(10)
                if count == 20:
                    print(str(e))
                    raise TimeoutError

    # close modal window
    wait_for_element_clickable_xpath('//*[@id="modal"]/div[2]/a')


# add contract for limited reporting procedure
def add_contract(data, contract_dates):
    procurement_type = data['procurementMethodType']
    if procurement_type != 'reporting':
        count = 0
        for x in range(20):
            count += 1
            try:
                refresh_page()
                wait_for_element_present_xpath('//a[@class="reverse grey setDone"]')
                break
            except Exception as e:
                if count == 20:
                    print(str(e))
                    raise TimeoutError

    add_contract_button = driver.find_element_by_xpath('//a[@class="reverse grey setDone"]')
    scroll_into_view_xpath('//a[@class="reverse grey setDone"]')
    add_contract_button.click()
    add_docs_xpath('//div[@class="inp l relative"]/input[2]', document_path)
    send_keys_xpath('//div[@class="inp langSwitch langSwitch_uk dataFormatHelpInside"]/input', 'Contract')
    Select(driver.find_element_by_name('documentType')).select_by_value('contractSigned')
    click_by_xpath('//button[@class="icons icon_upload relative"]')
    wait_for_element_not_visible_xpath('//body[contains(@class, "blocked")]', 10)

    click_by_name('data[contractNumber]')
    send_keys_name('data[contractNumber]', contract_dates.contract_number)

    # add date of sign
    date_signed_path = driver.find_element_by_name('data[dateSigned]')
    date_signed = contract_dates.date_signed.strftime('%d/%m/%Y')
    driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", date_signed_path)
    date_signed_path.send_keys(date_signed)

    # contract start date
    wait_for_element_clickable_name('data[period][startDate]')
    contract_start_date_path = driver.find_element_by_name('data[period][startDate]')
    contract_start_date = contract_dates.contract_start_date.strftime('%d/%m/%Y')
    driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", contract_start_date_path)
    contract_start_date_path.send_keys(contract_start_date)

    # contract end date
    wait_for_element_clickable_name('data[period][endDate]')
    contract_end_date_path = driver.find_element_by_name('data[period][endDate]')
    contract_end_date = contract_dates.contract_end_date.strftime('%d/%m/%Y')
    driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", contract_end_date_path)
    contract_end_date_path.send_keys(contract_end_date)

    # submit form button
    click_by_xpath('//button[@class="bidAction"]')

    # click "ok" in modal window
    # wait_for_element_not_visible_xpath('//div[@class="jAlertWrap"]', 10)
    wait_for_element_clickable_xpath('//div[@class="jBtnWrap"]/a[1]')
    click_by_xpath('//div[@class="jBtnWrap"]/a[1]')
    wait_for_element_not_visible_xpath('//div[@class="jBtnWrap"]/a[1]', 10)


# sign contract for limited reporting procedure
def sign_contract():
    count = 0
    for x in range(20):
        count += 1
        try:
            refresh_page()
            wait_for_element_clickable_xpath('//a[@class="reverse grey setDone"]')
            add_contract_button = driver.find_element_by_xpath('//a[@class="reverse grey setDone"]')
            scroll_into_view_xpath('//a[@class="reverse grey setDone"]')
            add_contract_button.click()
            sign_contract_button = driver.find_element_by_xpath('//div[@class="sign"]/a')
            scroll_into_view_xpath('//div[@class="sign"]/a')
            if sign_contract_button.is_displayed():
                eds_sign(sign_contract_button)
                break
            else:
                continue
        except Exception as e:
            time.sleep(10)
            if count == 20:
                print(e)
                raise TimeoutError

    # close modal window
    wait_for_element_clickable_xpath('//*[@id="modal"]/div[2]/a')
    click_by_xpath('//button[@class="icons icon_upload relative"]')


def add_documents_tender(document_data):
    add_documents_tender_section = driver.find_element_by_xpath('//h3[contains(text(), "Тендерна документація")]/following-sibling::a')
    scroll_into_view_xpath('//h3[contains(text(), "Тендерна документація")]/following-sibling::a')
    add_documents_tender_section.click()
    for doc in range(len(document_data)):
        scroll_into_view_xpath('(//input[@ name="upload"])')
        add_docs_xpath('(//input[@ name="upload"])', document_data[doc]['file_path'])
        wait_for_element_clickable_xpath('//input[@class="js-title"][contains(@value, "{}")]'.format(document_data[doc]['document_name']))
        Select(driver.find_element_by_xpath('(//select[@class="js-documentType"])[last()]')).select_by_value(document_data[doc]['type'])
    save_changes_button = driver.find_element_by_xpath('//button[text()="Зберегти"]')
    scroll_into_view_xpath('//button[text()="Зберегти"]')
    save_changes_button.click()
    wait_for_element_clickable_xpath('//h1[@class="t_title"]')


def add_documents_contract(document_data):
    add_documents_tender_section = driver.find_element_by_xpath('//h3[contains(text(), "Документи договору/змін")]/following-sibling::a')
    scroll_into_view_xpath('//h3[contains(text(), "Документи договору/змін")]/following-sibling::a')
    add_documents_tender_section.click()
    for doc in range(len(document_data)):
        scroll_into_view_xpath('(//input[@ name="upload"])')
        add_docs_xpath('(//input[@ name="upload"])', document_data[doc]['file_path'])
        wait_for_element_clickable_xpath('//input[@class="js-title"][contains(@value, "{}")]'.format(document_data[doc]['document_name']))
        Select(driver.find_element_by_xpath('(//select[@class="js-documentType"])[last()]')).select_by_value(document_data[doc]['type'])
    scroll_into_view_xpath('(//input[@name="change[rationaleTypes][]"])[1]/following-sibling::span')
    click_by_xpath('(//input[@name="change[rationaleTypes][]"])[1]/following-sibling::span')
    date_signed = driver.find_element_by_name('change[dateSigned]')
    scroll_into_view_xpath('//input[@name="change[dateSigned]"]')
    date_signed.click()
    driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", date_signed)
    date_signed.send_keys(datetime.strftime(datetime.now(), '%d/%m/%Y'))
    send_keys_name('change[rationale]', 'Reason text')
    save_changes_button = driver.find_element_by_xpath('//button[@value="save"]')
    scroll_into_view_xpath('//button[@value="save"]')
    save_changes_button.click()
    wait_for_element_clickable_xpath('//h1[@class="t_title"]')


def get_info_from_contract_tender():
    refresh_page()
    scroll_into_view_xpath('//a[contains(@href, "/contract/documents")]')
    click_by_xpath('//a[contains(@href, "/contract/documents")]')
    wait_for_element_clickable_xpath('//a[@onclick="modalClose();"]')


def wait_for_contract_to_be_generated():
    count = 0
    for x in range(20):
        count += 1
        refresh_page()
        if check_presence_xpath('//a[contains(text(), "Зміни/виконання договору")]') is True:
            click_by_xpath('//a[contains(text(), "Зміни/виконання договору")]')
            return get_contract_id_short(), get_contract_id_long()
        else:
            time.sleep(60)
            if count == 20:
                raise TimeoutError
            continue
