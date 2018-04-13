# -*- coding: utf-8 -*-
from selenium import webdriver
import time


host = 'http://www.dzo.byustudio.in.ua'
# driver = webdriver.Chrome()

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--window-size=1600x900")
driver = webdriver.Chrome(chrome_options=options)

time.sleep(1)
driver.implicitly_wait(30)
# driver.maximize_window()
driver.get(host)

td = dict()
json_cdb = dict()
