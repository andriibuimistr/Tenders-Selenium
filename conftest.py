# -*- coding: utf-8 -*-
from tender_initial_data.tender_data import create_tender_data
import pytest
import allure


def pytest_addoption(parser):
    parser.addoption("--pmt", action="store", default="reporting", help="procurementMethodType")
    parser.addoption("--broker", action="store", default="dzo_broker", help="broker")
    parser.addoption("--role", action="store", default="owner", help="role")


@pytest.fixture(scope='class')
def pmt(request):
    request.cls.pmt = create_tender_data(request.config.getoption("--pmt"))


@pytest.fixture(scope='class')
def broker(request):
    request.cls.broker = request.config.getoption("--broker")


@pytest.fixture(scope='class')
def role(request):
    request.cls.role = request.config.getoption("--role")


def pytest_exception_interact(node, call, report):
    driver = node.instance.driver
    # ...
    allure.attach(
        name='Скриншот',
        contents=driver.get_screenshot_as_png(),
        type=allure.constants.AttachmentType.PNG,
    )
