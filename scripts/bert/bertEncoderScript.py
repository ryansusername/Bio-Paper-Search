import tensorflow as tf
import numpy as np
from pymongo import MongoClient

ab_model_path = 'classifier/abstract/bert_abstract.h5'
m_model_path = 'classifier/maintext/bert_maintext.h5'

CLASS_TYPE = 'BERT'
VEC_LENGTH = 768

AB_SENT_LEN = 10
MAIN_SENT_LEN = 100


client = MongoClient('localhost', 27017)
db = client.bioArchive
bioCollection = db.bioPapers
bioBertAbstract = db.bertEmbeddingsAbstract
bioBertMain = db.bertEmbeddingsMain


def get_all_papers_from_db(fields, enc_field):
    text_field = 'cleanFullText'
    search_fields = get_search_fields(fields)
    papers = list(bioCollection.find({'$and':[{text_field:{'$exists':True}},{enc_field:{'$exists':False}}]}, search_fields))
    return papers

def get_search_fields(fields):
    search_fields = {'_id': 0}
    for f in fields:
        search_fields[f] = 1
    return search_fields

def get_embedding_from_db(paperId, collection):
    doc = collection.find_one({'paperId':paperId})
    if doc != None:
        if collection == bioBertAbstract:
            return doc['abstract_sentence_all']
        else:
            return doc['main_sentence_smpl']
    else:
        return []

def get_main_embedding_from_db(paperId):
    doc = bioBertMain.find_one({'paperId':paperId})
    if doc != None:
        return doc['main_sentence_smpl']
    else:
        return []
    
def np_to_py_datatype(npData):
    return npData.item()


def get_encoding(text):
    prediction = learn_clas.predict(text)
    return prediction[2].tolist()


def save_encoding_to_db(encoding, paper_id, enc_field):
    try:
        bioCollection.update_one({'paperId': paper_id}, {'$set': {enc_field: encoding}})
    except Exception as e:
        print(str(e))
        return 0
    else:
        return 1    

def pad_embeddings(paper, max_seq_length, vec_length = VEC_LENGTH):
      padding = vec_length * [0]
      paper_len = len(paper)
      outpaper = paper

      if (paper_len > max_seq_length):
        outpaper = paper[:max_seq_length]

      elif(paper_len < max_seq_length):
        pad_no = max_seq_length - paper_len

        for pad in range(pad_no):
          outpaper.append(padding)

      else:
        outpaper = paper
      return outpaper

def abstract():
    coll = bioBertAbstract
    ab_model = tf.keras.models.load_model(ab_model_path)
    print('start')
    enc_field = 'abstract_encoding_BERT_1'
    fields = ['paperSubject', 'paperId']
    paper_list = get_all_papers_from_db(fields, enc_field)

    total = len(paper_list)
    print('papers to encode', total,'\n')

    for index, paper in enumerate(paper_list):
        paperId = paper['paperId']
        embedding = get_embedding_from_db(paperId, coll)

        if(len(embedding) > 0):
            embedding = pad_embeddings(embedding, AB_SENT_LEN)
            emb = np.array([embedding])


            prediction = ab_model.predict(emb)
            encoded_final = prediction[0].tolist()

            save_encoding_to_db(encoded_final, paperId, enc_field)

            
        if(index % 100 == 0):
            print('progress:\t',index,'/',total)
            
        
    print('done')
def mainbody():
    m_model = tf.keras.models.load_model(m_model_path)
    print('start')
    fields = ['paperSubject', 'paperId']
    enc_field = 'maintext_encoding_BERT_1'
    paper_list = get_all_papers_from_db(fields, enc_field)
    total = len(paper_list)
    print('papers to encode', total,'\n')

    for index, paper in enumerate(paper_list):
        paperId = paper['paperId']
        embedding = get_main_embedding_from_db(paperId)
        
        if(len(embedding) > 0):
            embedding = pad_embeddings(embedding, MAIN_SENT_LEN)
            emb = np.array([embedding])
            prediction = m_model.predict(emb)
            encoded_final = prediction[0].tolist()
            save_encoding_to_db(encoded_final, paperId, enc_field)
            print('progress:\t',index,'/',total)
    print('done')

    
def main():
    ##abstract()
    mainbody()


main()
