# -*- coding: utf-8 -*-
import random
import string
from faker import Faker
import pytest
import urllib.request
from api.cdb_requests import *


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


def document_data(filename=None):
    if not filename:
        filename = 'doc.pdf'
    file_for_upload = open(os.path.join(ROOT_DIR, 'documents', filename), 'rb').read()
    data = "----------------------------1507111922.4992\nContent-Disposition: form-data;" \
           "name=\"file\"; filename=\"{}\"\nContent-Type: application/pdf\n\n{}\n" \
           "----------------------------1507111922.4992--".format(filename, file_for_upload)
    return data


tender_documents_type = {'technicalSpecifications': 'Технічний опис предмету закупівлі',
                         'eligibilityCriteria': 'Кваліфікаційні критерії', 'contractProforma': 'Проект договору',
                         'biddingDocuments': 'Тендерна документація', 0: 'Інші'}


# upload document from ds to tender
def patch_tender_documents_from_ds(type_for_doc, name_for_doc, added_tender_doc, t_id_long, t_token, lot_id, doc_of, ds):
    add_document_json = added_tender_doc.json()
    if type_for_doc != 0:
        add_document_json['data']['documentType'] = type_for_doc
    add_document_json['data']['title'] = name_for_doc
    if doc_of == 'lot':
        add_document_json['data']['relatedItem'] = lot_id
        add_document_json['data']['documentOf'] = 'lot'
    elif doc_of == 'item':
        add_document_json['data']['relatedItem'] = lot_id
        add_document_json['data']['documentOf'] = 'item'
    else:
        add_document_json['data']['documentOf'] = 'tender'
    ds.add_document_from_ds_to_tender(t_id_long, t_token, add_document_json, 'Add document from DS to tender - {}'.format(name_for_doc))


def add_documents_to_tender(tender_id_long, tender_token, list_of_id_lots, api_version):
    # doc_publish_info = []
    files = generate_files()
    ds = TenderRequests(api_version)
    for doc in range(len(files)):  # add one document for every document type
        doc_type = files[doc]['type']
        doc_name = '{}.txt'.format(files[doc]['document_name'])
        with pytest.allure.step('Add documents to tender SD'):
            added_tender_document = ds.add_tender_document_to_ds(document_data(doc_name))
        with pytest.allure.step('Add documents from DS to tender (patch)'):
            patch_tender_documents_from_ds(doc_type, doc_name, added_tender_document, tender_id_long, tender_token, 0, 'tender', ds)
    return files

    # lot_number = 0
    # for lot in range(len(list_of_id_lots)):
    #     lot_number += 1
    #     lot_id = list_of_id_lots[lot]
    #     for doc_type in tender_documents_type:  # add one document for every document type
    #         doc_type_name = '{}{}{}'.format(tender_documents_type[doc_type], ' Лот ', lot_number)
    #         added_tender_document = ds.add_tender_document_to_ds(document_data())
    #         patch_tender_documents_from_ds(doc_type, doc_type_name, added_tender_document, tender_id_long, tender_token, lot_id, 'lot', ds)
    #
    # return doc_publish_info
