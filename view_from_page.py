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
