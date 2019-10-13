from bert_serving.client import BertClient
from pymongo import MongoClient
import pandas as pd
import numpy as np
from bert_sent_enc import sentences_from_text
import tensorflow as tf


client = MongoClient('localhost', 27017)
db = client.bioArchive
m_model_path = 'classifier/maintext/bert_maintext.h5'
m_model = tf.keras.models.load_model(m_model_path)

MAIN_SENT_LEN = 100
CLASS_TYPE = 'BERT'
VEC_LENGTH = 768

##abstract collection
##bioCollection = db.bertEncodings

##maintext collection
bioBertCollection = db.bertEncodings2
bioPapers = db.bioPapers

bc = BertClient(port=7010, port_out=7011, check_length=False)

abstract_file = 'bioSentences/abstract_sentences_all.csv'
maintext_file = 'bioSentences/maintext_sentences_sample.csv'
encoding_field = 'main_sentence_smpl'
bert_emb_field = 'maintext_encoding_BERT_1'

def get_bert_encoding(sentence):
    encoding = bc.encode([sentence])
    return encoding[0]

def get_multiple_bert_encodings(sentence_list):
    encodings = bc.encode(sentence_list)

    encodings_list = []
    for enc in encodings:
        new_enc = [np_to_py_datatype(num) for num in enc]
        encodings_list.append(new_enc)

    return encodings_list

def get_data_from_csv(csv_file):
    df = pd.read_csv(csv_file,sep='\t')
    return df

def get_data_from_db(search_fields):
    papers = list(bioPapers.find({'$and':[{'cleanFullText':{'$exists':True}},{'maintext_encoding_BERT_1':{'$exists':False}}]}, search_fields))
    return papers

def save_encoding_to_db(encoding, paper_id, enc_field):
    try:
        bioPapers.update_one({'paperId': paper_id}, {'$set': {enc_field: encoding}})
    except Exception as e:
        print(str(e))
        return 0
    else:
        return 1

def np_to_py_datatype(npData):
    return npData.item()

def embed_sent_list(sent_list):
    encodings = bc.encode(sent_list)
    encodings_list = []
    for enc in encodings:
        new_enc = [np_to_py_datatype(num) for num in enc]
        encodings_list.append(new_enc)

    return encodings_list

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


def main():
    print('start')
    text_field = 'cleanFullText'
    enc_field = 'maintext_encoding01'
    bert_emb_field = 'maintext_encoding_BERT_1'
    mainfields = [text_field, 'paperSubject', 'paperId']

    papers = get_data_from_db(mainfields)
    total = len(papers)
    print('docs to embedd:',total)

    for index, paper in enumerate(papers):
        text = paper[text_field]
        pid = paper['paperId']
        sentences = sentences_from_text(text)
        embeddings = embed_sent_list(sentences)
        embeddings = pad_embeddings(embeddings, MAIN_SENT_LEN)
        embeddings = np.array([embeddings])

        prediction = m_model.predict(embeddings, batch_size=len(embeddings))
        encoded_final = prediction[0].tolist()
        save_encoding_to_db(encoded_final, pid, bert_emb_field)
        bioBertCollection.update_one({'paperId': pid}, {'$set': {'encoded': 1}})
        
        if(index % 100 == 0):
            print('papers processed:\t',index, '/', total)

    
main()
