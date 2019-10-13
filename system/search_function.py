from document.document_finder import *
from document.document_compare import *

from encoder.encoder_fastai import EncoderAbstract, EncoderMainText
from encoder.encoder_bert import BertAbstract

from pymongo import MongoClient

from result_document import Result_Doc
from search_document import SearchDoc

client = MongoClient('localhost', 27017)
db = client.bioArchive
bioCollection = db.bioPapers

bert_ab_Collection = db.bertEmbeddingsAbstract
bert_main_Collection = db.bertEmbeddingsMain

ctype_bert = 'BERT'
ctype_fast = 'FASTAI'
ctype_bow = 'BOW'

TEXT_MAIN = 'MAINTEXT'
TEXT_AB = 'ABSTRACT'

def search(doc, classifier, search_t=1, result_limit=400):
    print('SEARCH:','searching...')
    class_type = classifier.get_class_type()
    text_type = classifier.text_type

    print('SEARCH:','classifier:',class_type)
    print('SEARCH:','text type:',text_type)

    if(text_type == TEXT_AB):
        text = doc.abstract_text
    else:
        text = doc.main_body

    if(class_type == ctype_bert):
        embeddings = classifier.get_embeddings(text, text_type)
        text_enc = classifier.get_encoding(embeddings)
        enc_field = classifier.get_encoding_type()

    else:
        text_enc = classifier.get_encoding(text)
        enc_field = classifier.get_encoding_type()

    print('SEARCH:','enc field:',enc_field)
    if search_t == 1:
        docs = get_all_doc_encoding(enc_field)
    else:
        docs = get_bertmain_doc_encoding(enc_field)

    raw_results = compare_all_docs(text_enc,docs)

    print('SEARCH:','search complete, returning', len(raw_results), 'results')
    if(result_limit == 0):
        return raw_results
    else:
        return raw_results[:result_limit]



def raw_results_to_documents(raw_results_list,searched_doc):
    total = len(raw_results_list)
    print('SEARCH:', 'converting', total, 'results to documents')
    print(searched_doc)
    result_docs = []

    for index, res in enumerate(raw_results_list):
        paperId = str(res[0])
        distance = res[1]

        mongo_doc = dict(bioCollection.find_one({'paperId':paperId}))

        res_doc = Result_Doc(mongo_doc,distance,searched_doc)

        result_docs.append(res_doc)
        if(index % 100 == 0):
            print('SEARCH', 'conversion progress:', index, '/', total, end='\r')

    print('SEARCH:', 'conversion complete')
    return result_docs


def get_res_doc_sample():
    ex_doc = SearchDoc('blahblahblahblah')
    result_docs = []
    mongo_docs = list(bioCollection.find({}).limit(50))
    for d in mongo_docs:
        res_doc = Result_Doc(d,0,ex_doc)
        result_docs.append(res_doc)
    return result_docs
