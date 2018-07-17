# -*- coding: utf-8 -*-
from datetime import datetime


def convert_date_with_dots_from__page(date):
    date = datetime.strptime(date, '%d.%m.%Y')
    return datetime.strftime(date, '%Y-%m-%d')


tender_document_type_names = {"Тендерна документація": "biddingDocuments", "Технічний опис предмету закупівлі": "technicalSpecifications",
                              "Кваліфікаційні критерії": "eligibilityCriteria", "Критерії оцінки": "evaluationCriteria", "Проект договору": "contractProforma"}

contract_document_types_names = {"notice": "Повідомлення", "contractSigned": "Підписаний контракт", "contractArrangements": "Умови припинення контракту", "contractSchedule": "Графіки та етапи",
                                 "contractAnnexe": "Додатки до контракту", "contractGuarantees": "Гарантії", "subContract": "Субконтракти"}
