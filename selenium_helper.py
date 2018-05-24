from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pytest
import allure
import time
import json

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
                time.sleep(1)
                if attempt == 20:
                    allure.attach('EXCEPTION: ', str(e))


def wait_for_element_clickable_name(name):
    with pytest.allure.step('Wait for element is clickable (by name)'):
        allure.attach('NAME: ', '{}'.format(name))
        attempt = 0
        for x in range(20):
            attempt += 1
            allure.attach('ATTEMPT: ', str(attempt))
            try:
                wait = WebDriverWait(driver, 1)
                wait.until(EC.element_to_be_clickable((By.NAME, name)))
                break
            except Exception as e:
                time.sleep(1)
                if attempt == 20:
                    allure.attach('EXCEPTION: ', str(e))


def wait_for_element_clickable_id(element_id):
    with pytest.allure.step('Wait for element is clickable (by ID)'):
        allure.attach('ID: ', '{}'.format(element_id))
        attempt = 0
        for x in range(20):
            attempt += 1
            allure.attach('ATTEMPT: ', str(attempt))
            try:
                wait = WebDriverWait(driver, 1)
                wait.until(EC.element_to_be_clickable((By.ID, element_id)))
                break
            except Exception as e:
                time.sleep(1)
                if attempt == 20:
                    allure.attach('EXCEPTION: ', str(e))


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
                if attempt == 20:
                    allure.attach('EXCEPTION: ', str(e))
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
                time.sleep(1)
                if attempt == 20:
                    allure.attach('EXCEPTION: ', str(e))


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
                time.sleep(1)
                if attempt == 20:
                    allure.attach('EXCEPTION: ', str(e))


def wait_for_element_present_id(element_id):
    with pytest.allure.step('Wait for element is present (by id)'):
        allure.attach('ID: ', '{}'.format(element_id))
        attempt = 0
        for x in range(20):
            attempt += 1
            allure.attach('ATTEMPT: ', str(attempt))
            try:
                wait = WebDriverWait(driver, 1)
                wait.until(EC.presence_of_element_located((By.ID, element_id)))
                break
            except Exception as e:
                time.sleep(1)
                if attempt == 20:
                    allure.attach('EXCEPTION: ', str(e))


def check_presence_xpath(xpath):
    with pytest.allure.step('Check presence of element by xpath'):
        allure.attach('XPATH: ', xpath)
        try:
            wait = WebDriverWait(driver, 1)
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            allure.attach('IS PRESENT: ', str(True))
            return True
        except Exception as e:
            allure.attach('IS PRESENT: ', '{}'.format(e))
            print(e)


def scroll_into_view_xpath(xpath):
    with pytest.allure.step('Scroll into view by xpath'):
        allure.attach('XPATH', xpath)
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath(xpath))


def click_by_xpath(xpath):
    with pytest.allure.step('Find element by xpath and click'):
        wait_for_element_clickable_xpath(xpath)
        with pytest.allure.step('Click element'):
            driver.find_element_by_xpath(xpath).click()


def click_by_name(name):
    with pytest.allure.step('Find element by name and click'):
        wait_for_element_clickable_name(name)
        with pytest.allure.step('Click element'):
            driver.find_element_by_name(name).click()


def click_by_id(element_id):
    with pytest.allure.step('Find element by id and click'):
        wait_for_element_clickable_id(element_id)
        with pytest.allure.step('Click element'):
            driver.find_element_by_id(element_id).click()


def click_and_wait_for_disappear_xpath(xpath):
    with pytest.allure.step('Click and wait for element to disappear after click'):
        allure.attach('XPATH: ', '{}'.format(xpath))
        attempt = 0
        for x in range(20):
            attempt += 1
            allure.attach('ATTEMPT: ', str(attempt))
            try:
                driver.find_element_by_xpath(xpath).click()
                wait_for_element_not_visible_xpath(xpath)
                # if driver.find_element_by_xpath(xpath).is_displayed():
                #     raise Exception
                break
            except Exception as e:
                time.sleep(1)
                if attempt == 20:
                    allure.attach('EXCEPTION: ', str(e))


def add_docs_xpath(xpath, docs):
    with pytest.allure.step('Add docs by xpath'):
        wait_for_element_present_xpath(xpath)
        allure.attach('DATA: ', 'XPATH: {}, DOC: {}'.format(xpath, docs))
        driver.find_element_by_xpath(xpath).send_keys(docs)


def add_docs_name(name, docs):
    with pytest.allure.step('Add docs by name'):
        wait_for_element_present_name(name)
        allure.attach('DATA: ', 'NAME: {}, DOC: {}'.format(name, docs))
        driver.find_element_by_name(name).send_keys(docs)


def add_docs_id(element_id, docs):
    with pytest.allure.step('Add docs by element_id'):
        wait_for_element_present_id(element_id)
        allure.attach('DATA: ', 'ID: {}, DOC: {}'.format(element_id, docs))
        driver.find_element_by_id(element_id).send_keys(docs)


def send_keys_xpath(xpath, keys):
    with pytest.allure.step('Send keys by xpath'):
        wait_for_element_clickable_xpath(xpath)
        allure.attach('DATA: ', 'XPATH: {}, KEYS: {}'.format(xpath, keys))
        driver.find_element_by_xpath(xpath).send_keys(keys)


def send_keys_name(name, keys):
    with pytest.allure.step('Send keys by name'):
        wait_for_element_clickable_name(name)
        allure.attach('DATA: ', 'NAME: {}, KEYS: {}'.format(name, keys))
        driver.find_element_by_name(name).send_keys(keys)


def send_keys_id(element_id, keys):
    with pytest.allure.step('Send keys by id'):
        wait_for_element_clickable_id(element_id)
        allure.attach('DATA: ', 'ID: {}, KEYS: {}'.format(element_id, keys))
        driver.find_element_by_id(element_id).send_keys(keys)


def get_text_xpath(xpath):
    with pytest.allure.step('Get text by xpath'):
        allure.attach('DATA: ', 'XPATH: {}'.format(xpath))
        return driver.find_element_by_xpath(xpath).text


def get_text_name(name):
    with pytest.allure.step('Get text by name'):
        allure.attach('DATA: ', 'NAME: {}'.format(name))
        return driver.find_element_by_name(name).text


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


def refresh_page():
    with pytest.allure.step('Refresh page'):
        driver.refresh()


def screenshot(message=''):
    with pytest.allure.step('Screenshot: {}'.format(message)):
        allure.attach(
            name='Screenshot',
            contents=driver.get_screenshot_as_png(),
            type=allure.constants.AttachmentType.PNG,
        )


def log_javascript():
    with pytest.allure.step('Log Javascript from console'):
        for entry in driver.get_log('browser'):
            allure.attach('Javascript: ', json.dumps(entry))
