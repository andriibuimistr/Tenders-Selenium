from initial_data.tender_data import create_tender_data


def pytest_namespace():
    # print(create_tender_data('limited'))
    return {'data': create_tender_data('reporting')}
