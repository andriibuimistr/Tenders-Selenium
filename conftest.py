# -*- coding: utf-8 -*-
# from config import host, driver
from initial_data.tender_data import create_tender_data
import pytest
import allure


def pytest_addoption(parser):
    parser.addoption("--pmt", action="store", default="reporting", help="procurementMethodType")


@pytest.fixture(scope='class')
def pmt(request):
    request.cls.pmt = create_tender_data(request.config.getoption("--pmt"))

#
# def pytest_exception_interact(node, call, report):
#     driver = node.instance.driver
#     # ...
#     allure.attach(
#         name='Скриншот',
#         contents=driver.get_screenshot_as_png(),
#         type=allure.constants.AttachmentType.PNG,
#     )
