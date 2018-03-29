from selenium import webdriver
import time

host = 'http://www.dzo.byustudio.in.ua'
driver = webdriver.Chrome()
time.sleep(1)
driver.implicitly_wait(30)
driver.maximize_window()
driver.get(host)

td = dict()
json_cdb = dict()
