from initial_data.tender_data import create_tender_data
from selenium import webdriver
import pytest


def pytest_addoption(parser):
    parser.addoption("--pmt", action="store", default="reporting", help="procurementMethodType")


@pytest.fixture(scope='class')
def pmt(request):
    request.cls.pmt = create_tender_data(request.config.getoption("--pmt"))
