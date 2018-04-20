from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pytest
import allure
import time

from config import driver


def wait_for_element_clickable_xpath(xpath):
    with pytest.allure.step('Wait for element is clickable (by xpath)'):
        allure.attach('XPATH: ', '{}'.format(xpath))
        attempt = 0
        for x in range(20):
            attempt += 1
            allure.attach('ATTEMPT: ', str(attempt))
            try:
                wait = WebDriverWait(driver, 1)
                wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                break
            except Exception as e:
                print(e)


def wait_for_element_not_visible_xpath(xpath):
    with pytest.allure.step('Wait for element not visible (by xpath)'):
        allure.attach('XPATH: ', '{}'.format(xpath))
        attempt = 0
        for x in range(20):
            attempt += 1
            allure.attach('ATTEMPT: ', str(attempt))
            try:
                time.sleep(1)
                wait = WebDriverWait(driver, 1)
                wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            except Exception as e:
                print(e)
                break


def wait_for_element_present_xpath(xpath):
    with pytest.allure.step('Wait for element is present (by xpath)'):
        allure.attach('XPATH: ', '{}'.format(xpath))
        attempt = 0
        for x in range(20):
            attempt += 1
            allure.attach('ATTEMPT: ', str(attempt))
            try:
                wait = WebDriverWait(driver, 1)
                wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                break
            except Exception as e:
                print(e)


def wait_for_element_present_name(name):
    with pytest.allure.step('Wait for element is present (by name)'):
        allure.attach('NAME: ', '{}'.format(name))
        attempt = 0
        for x in range(20):
            attempt += 1
            allure.attach('ATTEMPT: ', str(attempt))
            try:
                wait = WebDriverWait(driver, 1)
                wait.until(EC.presence_of_element_located((By.NAME, name)))
                break
            except Exception as e:
                print(e)


def wait_for_element_clickable_name(name):
    wait = WebDriverWait(driver, 20)
    wait.until(EC.element_to_be_clickable((By.NAME, name)))


def scroll_into_view_xpath(xpath):
    with pytest.allure.step('Scroll into view by xpath'):
        allure.attach('XPATH', xpath)
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath(xpath))


def click_by_xpath(xpath):
    with pytest.allure.step('Find element by xpath and click'):
        wait_for_element_clickable_xpath(xpath)
        with pytest.allure.step('Click element'):
            driver.find_element_by_xpath(xpath).click()


def send_keys_xpath(xpath, keys):
    with pytest.allure.step('Send keys by xpath'):
        wait_for_element_present_xpath(xpath)
        allure.attach('DATA: ', 'XPATH: {}, KEYS: {}'.format(xpath, keys))
        driver.find_element_by_xpath(xpath).send_keys(keys)


def send_keys_name(name, keys):
    with pytest.allure.step('Send keys by name'):
        wait_for_element_present_name(name)
        allure.attach('DATA: ', 'NAME: {}, KEYS: {}'.format(name, keys))
        driver.find_element_by_name(name).send_keys(keys)


def wait_jquery():
    with pytest.allure.step('Wait for Jquery execution'):
        attempt = 0
        for x in range(20):
            attempt += 1
            allure.attach('ATTEMPT: ', str(attempt))
            if driver.execute_script('return jQuery.active') == 0:
                break
            else:
                time.sleep(1)
                continue
