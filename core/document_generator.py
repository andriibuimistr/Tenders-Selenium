# -*- coding: utf-8 -*-
import random
import string
from faker import Faker
from tender_initial_data.tender_additional_data import *
import pytest
import urllib.request


fake = Faker('uk_UA')


def generate_document_name():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))


def create_file():
    filename = generate_document_name()
    file_path = os.path.join(ROOT_DIR, 'documents', '{}.txt'.format(filename))

    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    f = open(file_path, "w+")
    content = fake.text(300)
    f.write(content)
    f.close()
    return filename, content, file_path


def generate_files(entity=None):
    types = tender_documents_types
    if entity == 'contract':
        types = contract_documents_types
    documents_data = []
    with pytest.allure.step('Generate files'):
        for x in range(len(types)):
            file_data = create_file()
            documents_data.append({
                "document_name": file_data[0],
                "content": file_data[1],
                "file_path": file_data[2],
                "type": types[x]
            })
    return documents_data


def delete_documents(document_data):
    with pytest.allure.step('Delete documents from temporal folder'):
        for doc in range(len(document_data)):
            os.remove(document_data[doc]['file_path'])


def download_and_open_file(url):
    f_name = generate_document_name()
    file_path = os.path.join(ROOT_DIR, 'documents', 'downloads', '{}.txt'.format(f_name))
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    urllib.request.urlretrieve(url, file_path)

    f = open(file_path, "r")
    content = f.read()
    f.close()
    os.remove(file_path)
    return content
