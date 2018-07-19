# -*- coding: utf-8 -*-
import os
from faker import Faker
from selenium import webdriver
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

capabilities = DesiredCapabilities.CHROME
capabilities['loggingPrefs'] = {'browser': 'ALL'}

# driver = webdriver.Chrome()

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--window-size=1600x900")
driver = webdriver.Chrome(chrome_options=options, desired_capabilities=capabilities)

time.sleep(1)
driver.implicitly_wait(1)
# driver.maximize_window()

fake = Faker('uk_UA')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
cdb_synchro = 15
