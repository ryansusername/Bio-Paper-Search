## Component:   Document
## Module:      Document Finder Module
## Description: Module for connecting to mongo database to return documents
## Author:      Ryan McCloskey, 2019

from pymongo import MongoClient
import pandas as pd
import numpy as np

client = MongoClient('localhost', 27017)
db = client.bioArchive
bioCollection = db.bioPapers


ENC_AI_ABSTRACT_01 = 'abstract_encoding01'
ENC_AI_ABSTRACT_02 = 'abstract_encoding02'

ENC_AI_MAINTEXT_01 = 'maintext_encoding01'
ENC_AI_MAINTEXT_02 = 'maintext_encoding02'

ENC_BERT_ABSTRACT_01 = 'abstract_encoding_BERT_1'
ENC_BERT_ABSTRACT_02 = 'encBertAb02'

ENC_BERT_MAINTEXT_01 = 'encBertMt01'
ENC_BERT_MAINTEXT_02 = 'encBertMt01'


##function that maps 'encoding field' to general 'encoding' for processing
## due to different encoding fields for different encodings
def map_to_general_doc(doc_list, enc_field):
    docs = [{'paperId':d['paperId'], 'encoding':d[enc_field]} for d in doc_list]
    return docs

def get_all_doc_encoding(enc_field):
    docs = list(bioCollection.find({enc_field: { '$exists': True }}, { '_id':0, 'paperId':1, enc_field:1 }))
    docs = map_to_general_doc(docs, enc_field)
    return docs


def get_bertmain_doc_encoding(enc_field):
    docs = list(bioCollection.find({'$and':[{enc_field:{'$exists':True}},{'cleanFullText':{'$exists':True}}]}, { '_id':0, 'paperId':1, enc_field:1 }))
    docs = map_to_general_doc(docs, enc_field)
    return docs
