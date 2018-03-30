# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import driver


def wait_for_element_xpath(xpath):
    wait = WebDriverWait(driver, 20)
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))


def wait_for_element_name(name):
    wait = WebDriverWait(driver, 20)
    wait.until(EC.element_to_be_clickable((By.NAME, name)))
