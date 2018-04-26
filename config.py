# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

capabilities = DesiredCapabilities.CHROME
capabilities['loggingPrefs'] = {'browser': 'ALL'}

# host = 'http://www.dzo.byustudio.in.ua'
# driver = webdriver.Chrome()

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--window-size=1600x900")
driver = webdriver.Chrome(chrome_options=options, desired_capabilities=capabilities)

time.sleep(1)
driver.implicitly_wait(1)
# driver.maximize_window()
# driver.get(host)
