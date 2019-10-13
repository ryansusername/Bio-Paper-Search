## Component:   Testing
## Module:      Validation Test
## Description: Script to run validation of results and save to csv
## Author:      Ryan McCloskey, 2019

import numpy as np
import io
import os
from pymongo import MongoClient
import csv

from encoder.encoder_bert import *
from encoder.encoder_fastai import *
from encoder.encoder_bow import *
from document.document_compare import compare_all_docs
from document.document_finder import get_all_doc_encoding
from search_document import SearchDocMongo

from search_function import search, raw_results_to_documents

client = MongoClient('localhost', 27017)
db = client.bioArchive
bioCollection = db.bioPapers

bert_ab_class = BertAbstract()
fastai_ab_class = EncoderAbstract()
bow_ab_class = BoWAbstract()

bert_m_class = BertMainText()
fastai_m_class = EncoderMainText()
bow_m_class = BoWMainText()


def get_paper_from_db(paper_id):
    return dict(bioCollection.find_one({'paperId':paper_id}))

def model_search(search_doc, model, res_limit=20000):
    raw_res = search(search_doc, model, result_limit=res_limit)
    result_docs = raw_results_to_documents(raw_res,search_doc)
    return result_docs

def model_bert_search(search_doc, model, res_limit=20000):
    raw_res = search(search_doc, model, search_t=2 ,result_limit=res_limit)
    result_docs = raw_results_to_documents(raw_res,search_doc)
    return result_docs

def get_results(search_doc, result_docs, stype):
    print('generating results...')
    result_list = []
    for r in result_docs:
        class_match = 0
        if(r.paper_subject == search_doc.paper_subject):
            class_match = 1

        row = { 'input_doc': search_doc.paper_subject,
                'distance': r.distance,
                'class': r.paper_subject,
                'class_match': class_match,
                'keyword_match': r.keyword_match_num,
                'ref_match': r.ref_match_num }

        result_list.append(row)
    print('generating results done')
    return result_list


def get_result_top_paper(search_doc, result_docs, stype):
    print('generating results...')
    result_list = []
    for r in result_docs[1:]:
        print(stype,r.paperId)
        #print(stype,'\tpaperid:\t',r.paperId)
        #print(stype,'\title:\t',r.title)
        #print(stype,'\tkeywords:\t',r.keywords)

def write_to_csv(result_list, path):
    keys = result_list[0].keys()
    with open(path, 'w+', newline='') as myfile:
        dict_writer = csv.DictWriter(myfile, keys,delimiter="\t")
        dict_writer.writeheader()
        dict_writer.writerows(result_list)


def paper_id_res(paper_id):
    paper = get_paper_from_db(paper_id)
    search_doc = SearchDocMongo(paper)

    print('input','\title:\t',search_doc.title)
    print('input','\tkeywords:\t',search_doc.keywords)

    fastai_docs = model_bert_search(search_doc, fastai_ab_class, res_limit=10)
    fastai_res = get_result_top_paper(search_doc, fastai_docs,'ULMFIT')

    bert_docs = model_bert_search(search_doc,bert_ab_class,res_limit=10)
    bert_res = get_result_top_paper(search_doc, bert_docs, 'BERT')

    bow_docs = model_bert_search(search_doc,bow_ab_class,res_limit=10)
    bow_res = get_result_top_paper(search_doc, bow_docs, 'BOW')


def paper_id_res_maintext(paper_id):
    paper = get_paper_from_db(paper_id)
    search_doc = SearchDocMongo(paper)

    print('input','\title:\t',search_doc.title)
    print('input','\tkeywords:\t',search_doc.keywords)

    fastai_docs = model_bert_search(search_doc, fastai_m_class, res_limit=10)
    fastai_res = get_result_top_paper(search_doc, fastai_docs,'ULMFIT')

    bert_docs = model_bert_search(search_doc, bert_m_class, res_limit=10)
    bert_res = get_result_top_paper(search_doc, bert_docs, 'BERT')

    bow_docs = model_bert_search(search_doc, bow_m_class, res_limit=10)
    bow_res = get_result_top_paper(search_doc, bow_docs, 'BOW')


def maintext(paper_id, results=1001):
    paper = get_paper_from_db(paper_id)
    search_doc = SearchDocMongo(paper)

    f_res_dir = 'results/fastai/'
    b_res_dir = 'results/bert/'
    bow_res_dir = 'results/bow/'

    fastai_res_file = 'fastai_m_results' + paper_id + '.csv'
    bert_res_file = 'bert_m_results' + paper_id + '.csv'
    bow_res_file = 'bow_m_results' + paper_id + '.csv'

    fastai_docs = model_search(search_doc, fastai_m_class, res_limit=results)
    fastai_res = get_results(search_doc, fastai_docs, 'ULMFIT')
    write_to_csv(fastai_res, os.path.join(f_res_dir, fastai_res_file))

    bert_docs = model_search(search_doc, bert_m_class, res_limit=results)
    bert_res = get_results(search_doc, bert_docs, 'BERT')
    write_to_csv(bert_res, os.path.join(b_res_dir, bert_res_file))

    bow_docs = model_search(search_doc, bow_m_class, res_limit=results)
    bow_res = get_results(search_doc, bow_docs, 'BOW')
    write_to_csv(bow_res, os.path.join(bow_res_dir, bow_res_file))

def maintext2(paper_id, results=1001):
    paper = get_paper_from_db(paper_id)
    search_doc = SearchDocMongo(paper)

    f_res_dir = 'results/fastai/'
    b_res_dir = 'results/bert/'
    bow_res_dir = 'results/bow/'

    fastai_res_file = 'fastai_m3_results' + paper_id + '.csv'
    bert_res_file = 'bert_m3_results' + paper_id + '.csv'
    bow_res_file = 'bow_m3_results' + paper_id + '.csv'

    fastai_docs = model_bert_search(search_doc, fastai_m_class, res_limit=results)
    fastai_res = get_results(search_doc, fastai_docs, 'ULMFIT')
    write_to_csv(fastai_res, os.path.join(f_res_dir, fastai_res_file))

    bert_docs = model_bert_search(search_doc, bert_m_class, res_limit=results)
    bert_res = get_results(search_doc, bert_docs, 'BERT')
    write_to_csv(bert_res, os.path.join(b_res_dir, bert_res_file))

    bow_docs = model_bert_search(search_doc, bow_m_class, res_limit=results)
    bow_res = get_results(search_doc, bow_docs, 'BOW')
    write_to_csv(bow_res, os.path.join(bow_res_dir, bow_res_file))

def abstract(paper_id, results=1001):
    paper = get_paper_from_db(paper_id)
    search_doc = SearchDocMongo(paper)

    f_res_dir = 'results/fastai/'
    b_res_dir = 'results/bert/'
    bow_res_dir = 'results/bow/'

    fastai_res_file = 'fastai_ab_results' + paper_id + '.csv'
    bert_res_file = 'bert_ab_results' + paper_id + '.csv'
    bow_res_file = 'bow_ab_results' + paper_id + '.csv'

    fastai_docs = model_search(search_doc, fastai_ab_class, res_limit=results)
    fastai_res = get_results(search_doc, fastai_docs, 'ULMFIT')
    write_to_csv(fastai_res, os.path.join(f_res_dir, fastai_res_file))

    bert_docs = model_search(search_doc, bert_ab_class, res_limit=results)
    bert_res = get_results(search_doc, bert_docs, 'BERT')
    write_to_csv(bert_res, os.path.join(b_res_dir, bert_res_file))

    bow_docs = model_search(search_doc, bow_ab_class, res_limit=results)
    bow_res = get_results(search_doc, bow_docs, 'BOW')
    write_to_csv(bow_res, os.path.join(bow_res_dir, bow_res_file))

def abstract2(paper_id, results=1001):
    paper = get_paper_from_db(paper_id)
    search_doc = SearchDocMongo(paper)

    f_res_dir = 'results/fastai/'
    b_res_dir = 'results/bert/'
    bow_res_dir = 'results/bow/'

    fastai_res_file = 'fastai_ab3_results' + paper_id + '.csv'
    bert_res_file = 'bert_ab3_results' + paper_id + '.csv'
    bow_res_file = 'bow_ab3_results' + paper_id + '.csv'

    fastai_docs = model_bert_search(search_doc, fastai_ab_class, res_limit=results)
    fastai_res = get_results(search_doc, fastai_docs, 'ULMFIT')
    write_to_csv(fastai_res, os.path.join(f_res_dir, fastai_res_file))

    bert_docs = model_bert_search(search_doc, bert_ab_class, res_limit=results)
    bert_res = get_results(search_doc, bert_docs, 'BERT')
    write_to_csv(bert_res, os.path.join(b_res_dir, bert_res_file))

    bow_docs = model_bert_search(search_doc, bow_ab_class, res_limit=results)
    bow_res = get_results(search_doc, bow_docs, 'BOW')
    write_to_csv(bow_res, os.path.join(bow_res_dir, bow_res_file))


def main():
    paper_id = '486506'
    results = 1001
    ##abstract(paper_id)
    ##maintext(paper_id, results)

    ##abstract2(paper_id, results)
    ##maintext2(paper_id, results)

    paper_id_res(paper_id)
    paper_id_res_maintext(paper_id)

main()
