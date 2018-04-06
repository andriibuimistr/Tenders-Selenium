# -*- coding: utf-8 -*-
import time

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from cdb_requests import TenderRequests
from config import driver
from initial_data.document_generator import download_and_open_file


def wait_for_element_xpath(xpath):
    wait = WebDriverWait(driver, 20)
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))


def wait_for_element_name(name):
    wait = WebDriverWait(driver, 20)
    wait.until(EC.element_to_be_clickable((By.NAME, name)))


def compare_document_content(docs_data, tender_id):
    time.sleep(240)
    docs_cdb = TenderRequests('2.4').get_tender_info(tender_id).json()['data']['documents']
    number = 0
    for doc in range(len(docs_data)):
        number += 1
        for cdb_doc in range(len(docs_cdb)):
            if docs_cdb[cdb_doc]['title'].split('.')[0] == docs_data[doc]['document_name']:
                with pytest.allure.step('Compare content of document {}'.format(number)):
                    cdb_content = download_and_open_file(docs_cdb[cdb_doc]['url'])
                    allure.attach(docs_data[doc]['content'], 'Generated content')
                    allure.attach(cdb_content, 'Content of file in cdb', )
                    assert docs_data[doc]['content'] == cdb_content