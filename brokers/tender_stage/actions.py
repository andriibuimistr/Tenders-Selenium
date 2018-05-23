# -*- coding: utf-8 -*-
# from config import host
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
from selenium_helper import *
from initial_data.tender_additional_data import key_path, key_password, document_path


def login(user_email, user_pass):
    click_by_xpath('//a[contains(@href, "/login")]')
    driver.find_element_by_name('LoginForm[username]').clear()
    send_keys_name('LoginForm[username]', user_email)
    send_keys_name('LoginForm[password]', user_pass)
    click_by_name('login-button')


# def find_tender_by_id(uid):
#     driver.get(host)
#     Select(driver.find_element_by_name('filter[object]')).select_by_value('tenderID')
#     wait_for_element_present_name('filter[object]')
#     send_keys_name('filter[search]', uid)
#     click_by_xpath('(//button[contains(text(), "Пошук")])[1]')
#     wait_for_element_clickable_xpath('//span[contains(text(), "{}")]'.format(uid))
#     click_by_xpath('//span[contains(text(), "{}")]/ancestor::div[5]/descendant::h2[@class="title"]/a'.format(uid))
#     return get_text_xpath('//a[@title="Оголошення на порталі Уповноваженого органу"]/span')
#
#
# def open_tender_edit_page(uid):
#     tender_edit_button = driver.find_element_by_xpath('//a[contains(@class, "save")]')
#     driver.execute_script("arguments[0].scrollIntoView();", tender_edit_button)  # scroll to tender edit button
#     tender_edit_button.click()
#     wait_for_element_clickable_xpath('//h3[contains(@class, "bigTitle")]')
#
#
# def eds_sign(eds_button):
#     driver.execute_script("arguments[0].scrollIntoView();", eds_button)
#     eds_button.click()
#
#     main_window = driver.current_window_handle  # set tender window
#
#     # sign page
#     driver.switch_to.window(driver.window_handles[-1])  # swith to eds tab
#     driver.find_element_by_class_name('js-oldPageLink').click()  # open old eds page
#     for x in range(5):
#         Select(driver.find_element_by_id('CAsServersSelect')).select_by_index(17)  # select eds entity
#         add_docs_id('PKeyFileInput', key_path)  # add sign file
#         send_keys_id('PKeyPassword', key_password)  # type password
#         click_by_id('PKeyReadButton')  # click read key button
#
#         if driver.find_element_by_id('PKStatusInfo').text == u'Ключ успішно завантажено':  # check successful read key message
#             time.sleep(2)
#             click_by_id('SignDataButton')  # click sign button
#             time.sleep(5)
#             if driver.find_element_by_id('PKStatusInfo').text == u'Підпис успішно накладено та передано у ЦБД':
#                 driver.close()  # close sign page tab
#                 driver.switch_to_window(main_window)  # switch to tender window
#                 break
#             else:
#                 driver.find_element_by_xpath('//button[@id="PKeyReadButton"][contains(text(), "Зтерти")]').click()
#                 continue
#
#
# def add_participant_info_limited(data):
#     add_participant_info_button = driver.find_element_by_xpath('//a[@class="button reverse addAward"]')  # path of "add info" button
#     driver.execute_script("arguments[0].scrollIntoView();", add_participant_info_button)  # scroll to button
#     add_participant_info_button.click()
#     click_by_xpath('//div[@class="jBtnWrap"]/a[1]')
#     wait_for_element_not_visible_xpath('//div[@class="jBtnWrap"]/a[1]')
#     send_keys_name('data[suppliers][0][name]', 'Name of participant\'s organization')
#     Select(driver.find_element_by_name('data[suppliers][0][identifier][scheme]')).select_by_value('UA-EDR')  # select country of registration
#     send_keys_name('data[suppliers][0][identifier][id]', '00000000')  # identifier
#     Select(driver.find_element_by_name('data[suppliers][0][address][countryName]')).select_by_value(u'Україна')  # select country
#     wait_for_element_clickable_name('data[suppliers][0][address][region]')
#     Select(driver.find_element_by_name('data[suppliers][0][address][region]')).select_by_value(u'м. Київ')  # select region
#     send_keys_name('data[suppliers][0][address][locality]', u'Київ')  # locality
#     send_keys_name('data[suppliers][0][address][streetAddress]', u'Адрес')  # address
#     send_keys_name('data[suppliers][0][address][postalCode]', '00000')  # postal code
#     send_keys_name('data[suppliers][0][contactPoint][name]', u'Контактное Лицо')  # contact point
#     send_keys_name('data[suppliers][0][contactPoint][email]', 'i@i.ua')  # email
#     send_keys_name('data[suppliers][0][contactPoint][telephone]', '+380200000000')  # phone number
#     send_keys_name('data[suppliers][0][contactPoint][faxNumber]', '+380200000000')  # fax
#     send_keys_name('data[suppliers][0][contactPoint][url]', 'https://www.google.com.ua/?gws_rd=ssl')  # site
#
#     # amount as in tender
#     offer_amount = data['data']['value']['amount']
#     driver.find_element_by_name('data[value][amount]').send_keys(str("%.2f" % offer_amount))
#
#     # tax included as in tender
#     tax_included = data['data']['value']['valueAddedTaxIncluded']
#     if tax_included is True:
#         tax_included = '1'
#     else:
#         tax_included = '0'
#     Select(driver.find_element_by_name('data[value][valueAddedTaxIncluded]')).select_by_value(str(tax_included))
#
#     # currency as in tender
#     tender_currency = data['data']['value']['currency']
#     Select(driver.find_element_by_name('data[value][currency]')).select_by_value(tender_currency)
#
#     # save information
#     click_by_xpath('//tr[@class="line submitButton"]/td[2]/button')
#
#     # close modal window
#     wait_for_element_not_visible_xpath('//body[contains(@class, "blocked")]')
#     wait_for_element_clickable_xpath('//div[@class="info"]/a')
#     click_by_xpath('//div[@class="info"]/a')
#
#
# # sign award with EDS
# def qualify_winner_limited():
#     wait_for_element_clickable_xpath('//div[@class="btn2 awardActionItem"]/a')
#     winner_button = driver.find_element_by_xpath('//div[@class="btn2 awardActionItem"]/a')
#     driver.execute_script("arguments[0].scrollIntoView();", winner_button)  # scroll to click winner
#     winner_button.click()
#
#     # open EDS window
#     wait_for_element_clickable_xpath('//div[@class="sign"]/a')
#     eds_button = driver.find_element_by_xpath('//div[@class="sign"]/a')
#     eds_sign(eds_button)
#     count = 0
#     for x in range(20):
#         count += 1
#         try:
#             refresh_page()
#             if check_presence_xpath('//a[@class="reverse grey setDone"]') is True:
#                 break
#         except Exception as e:
#             time.sleep(2)
#             if count == 20:
#                 print(''.format(e))
#                 raise TimeoutError
#
#
# # add contract for limited reporting procedure
# def add_contract():
#     add_contract_button = driver.find_element_by_xpath('//a[@class="reverse grey setDone"]')
#     driver.execute_script("arguments[0].scrollIntoView();", add_contract_button)
#     add_contract_button.click()
#     add_docs_xpath('//div[@class="inp l relative"]/input[2]', document_path)
#     send_keys_xpath('//div[@class="inp langSwitch langSwitch_uk dataFormatHelpInside"]/input', 'Contract')
#     Select(driver.find_element_by_name('documentType')).select_by_value('contractSigned')
#     click_by_xpath('//button[@class="icons icon_upload relative"]')
#     wait_for_element_not_visible_xpath('//body[contains(@class, "blocked")]')
#
#     click_by_name('data[contractNumber]')
#     send_keys_name('data[contractNumber]', '123456')
#
#     # add date of sign
#     date_signed_path = driver.find_element_by_name('data[dateSigned]')
#     date_signed = datetime.now().strftime('%d/%m/%Y')
#     driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", date_signed_path)
#     date_signed_path.send_keys(date_signed)
#
#     # contract start date
#     wait_for_element_clickable_name('data[period][startDate]')
#     contract_start_date_path = driver.find_element_by_name('data[period][startDate]')
#     contract_start_date = (datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')
#     driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", contract_start_date_path)
#     contract_start_date_path.send_keys(contract_start_date)
#
#     # contract end date
#     wait_for_element_clickable_name('data[period][endDate]')
#     contract_end_date_path = driver.find_element_by_name('data[period][endDate]')
#     contract_end_date = (datetime.now() + timedelta(days=30)).strftime('%d/%m/%Y')
#     driver.execute_script("arguments[0].removeAttribute('readonly','readonly')", contract_end_date_path)
#     contract_end_date_path.send_keys(contract_end_date)
#
#     # submit form button
#     click_by_xpath('//button[@class="bidAction"]')
#
#     # click "ok" in modal window
#     wait_for_element_not_visible_xpath('//div[@class="jAlertWrap"]')
#     wait_for_element_clickable_xpath('//div[@class="jBtnWrap"]/a[1]')
#     click_by_xpath('//div[@class="jBtnWrap"]/a[1]')
#     wait_for_element_not_visible_xpath('//div[@class="jBtnWrap"]/a[1]')
#
#
# # sign contract for limited reporting procedure
# def sign_contract():
#     count = 0
#     for x in range(20):
#         count += 1
#         try:
#             driver.refresh()
#             wait_for_element_clickable_xpath('//a[@class="reverse grey setDone"]')
#             add_contract_button = driver.find_element_by_xpath('//a[@class="reverse grey setDone"]')
#             driver.execute_script("arguments[0].scrollIntoView();", add_contract_button)
#             add_contract_button.click()
#             sign_contract_button = driver.find_element_by_xpath('//div[@class="sign"]/a')
#             driver.execute_script("arguments[0].scrollIntoView();", sign_contract_button)
#             if sign_contract_button:
#                 eds_sign(sign_contract_button)
#                 break
#             else:
#                 continue
#         except Exception as e:
#             if count == 20:
#                 print(e)
#                 raise TimeoutError
#
#     # close modal window
#     wait_for_element_clickable_xpath('//*[@id="modal"]/div[2]/a')
#     click_by_xpath('//button[@class="icons icon_upload relative"]')
#
#
# def add_documents(document_data):
#     add_documents_tender_section = driver.find_element_by_xpath('//h3[contains(text(), "Тендерна документація")]/following-sibling::a')
#     scroll_into_view_xpath('//h3[contains(text(), "Тендерна документація")]/following-sibling::a')
#     add_documents_tender_section.click()
#     for doc in range(len(document_data)):
#         scroll_into_view_xpath('(//input[@ name="upload"])')
#         add_docs_xpath('(//input[@ name="upload"])', document_data[doc]['file_path'])
#         wait_for_element_clickable_xpath('//input[@class="js-title"][contains(@value, "{}")]'.format(document_data[doc]['document_name']))
#         Select(driver.find_element_by_xpath('(//select[@class="js-documentType"])[last()]')).select_by_value(document_data[doc]['type'])
#     save_changes_button = driver.find_element_by_xpath('//button[text()="Зберегти"]')
#     scroll_into_view_xpath('//button[text()="Зберегти"]')
#     save_changes_button.click()
#     wait_for_element_clickable_xpath('//h1[@class="t_title"]')
