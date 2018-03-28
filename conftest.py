from initial_data.tender_data import create_tender_data
from selenium import webdriver
import pytest
import time


def pytest_addoption(parser):
    parser.addoption("--pmt", action="store", default="reporting", help="procurementMethodType")


@pytest.fixture(scope='class')
def pmt(request):
    request.cls.pmt = create_tender_data(request.config.getoption("--pmt"))


host = 'http://www.dzo.byustudio.in.ua'
driver = webdriver.Chrome()
time.sleep(1)
driver.implicitly_wait(30)
driver.maximize_window()
driver.get(host)
