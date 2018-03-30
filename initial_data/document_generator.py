# -*- coding: utf-8 -*-
import random
import string
import os
from faker import Faker
from definitions import ROOT_DIR
from initial_data.tender_additional_data import tender_documents_types
import pytest


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


def generate_files(number_of_files):
    documents_data = []
    for x in range(number_of_files):
        file_data = create_file()
        # time.sleep(10)
        # os.remove(file_data[2])
        documents_data.append({
            "document_name": file_data[0],
            "content": file_data[1],
            "file_path": file_data[2],
            "type": tender_documents_types[x]
        })
    return documents_data


def delete_documents(document_data):
    with pytest.allure.step('Delete documents from temporal folder'):
        for doc in range(len(document_data)):
            os.remove(document_data[doc]['file_path'])
