import fastai
from fastai import *
from fastai.text import *
fastai.torch_core.defaults.device = 'cpu'
import pandas as pd
import numpy as np
import io
import os
from pymongo import MongoClient
import operator
import time
defaults.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

ab_learn_clas = load_learner(path='models/abstract_raw/models/classifier', file='ab_clas_fine_tuned_export.pkl')
m_learn_clas = load_learner(path='models/maintext_raw/models/classifier', file='full_body_clas_03_export.pkl') 

client = MongoClient('localhost', 27017)
db = client.bioArchive
bioCollection = db.bioPapers


def get_all_papers_from_db(fields, text_field, enc_field):
    search_fields = get_search_fields(fields)
    ##papers = list(bioCollection.find({'$and':[{text_field:{'$exists':True}},{enc_field:{'$exists':False}},{'maintext_encoding_BERT_1':{'$exists':True}}]}, search_fields))
    papers = list(bioCollection.find({'$and':[{text_field:{'$exists':True}},{enc_field:{'$exists':False}}]}, search_fields))

    return papers


def get_search_fields(fields):
    search_fields = {'_id': 0}
    for f in fields:
        search_fields[f] = 1
    return search_fields


def get_encoding(text, classifier):
    prediction = classifier.predict(text)
    return prediction[2].tolist()


def save_encoding_to_db(encoding, paper_id, new_encoding_field):
    try:
        bioCollection.update_one({'paperId': paper_id}, {'$set': {new_encoding_field: encoding}})
    except Exception as e:
        print(str(e))
        return 0
    else:
        return 1    

def abstract():
    ab_field = 'abstract'
    new_enc_field = 'abstract_encoding01'
    abfields = [ab_field, 'paperSubject', 'paperId']
    paper_list = get_all_papers_from_db(abfields, ab_field, new_enc_field)
    total = len(paper_list)
    print('papers to encode', total)
    success_count=0
    for paper in paper_list:
        abstract_text = paper[ab_field]
        paper_id = paper['paperId']
        enc = get_encoding(abstract_text, ab_learn_clas)

        success_count += save_encoding_to_db(enc, paper_id, new_encoding_field=new_enc_field)

    print('finished loading encodings')
    print('success', success_count)
    print('fails', total - success_count)

def maintext():
    m_field = 'cleanFullText'
    new_enc_field = 'maintext_encoding01'
    mainfields = [m_field, 'paperSubject', 'paperId']
    paper_list = get_all_papers_from_db(mainfields, m_field, new_enc_field)
    new_list = sorted(paper_list, key=lambda x: len(x[m_field]))

    total = len(paper_list)
    print('papers to encode', total)
    success_count=0
    time_for_10 = 0
    for index, paper in enumerate(new_list):
        start_time = time.time()
        fulltext = paper[m_field]
        paper_id = paper['paperId']
        enc = get_encoding(fulltext, m_learn_clas)
        success_count += save_encoding_to_db(enc, paper_id, new_encoding_field=new_enc_field)
        end_time = time.time()
        time_for_one = end_time - start_time
        time_for_10+=time_for_one
        
        if(index % 10 == 0):
            avg_time = (time_for_10 / 10)
            print('progress:',index,'/',total,'\tavg time:',avg_time)
            time_for_10 = 0

    print('finished loading encodings')
    print('success', success_count)
    print('fails', total - success_count)

    
def main():
    ##abstract()
    maintext()



main()
