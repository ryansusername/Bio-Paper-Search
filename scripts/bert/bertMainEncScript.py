import tensorflow as tf
import numpy as np
from pymongo import MongoClient

m_model_path = 'classifier/maintext/bert_maintext.h5'
m_model = tf.keras.models.load_model(m_model_path)

MAIN_SENT_LEN = 100
CLASS_TYPE = 'BERT'
VEC_LENGTH = 768

client = MongoClient('localhost', 27017)
db = client.bioArchive
bioCollection = db.bioPapers
bioBertMain = db.bertEmbeddingsMain

encoding_field = 'main_sentence_smpl'

bert_emb_field = 'maintext_encoding_BERT_1'

def pad_paper(paper, max_seq_length, vec_length = VEC_LENGTH):
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


def save_encoding_to_db(encoding, paper_id, enc_field):
    try:
        bioCollection.update_one({'paperId': paper_id}, {'$set': {enc_field: encoding}})
    except Exception as e:
        print(str(e))
        return 0
    else:
        return 1

    
def get_paper_ids_encdb():
    print('getting paper ids from enc collection...')
         
    docs = list(bioBertMain.find({'$and':[{encoding_field:{'$exists':True}},{'encoded':{'$exists':False}}]},{'paperId':1,'_id':0}))
    outlist = [d['paperId'] for d in docs]
    print('retrieved', len(outlist), 'paper ids')
    return outlist

def get_paper_ids_maindb():
    print('getting paper ids from main db...')
    docs = list(bioCollection.find({bert_emb_field:{'$exists':False}},{'paperId':1,'_id':0}))
    outlist = [d['paperId'] for d in docs]
    print('retrieved', len(outlist), 'paper ids')
    return outlist


def get_ids_to_enc():
    encoded_docs = get_paper_ids_encdb()
    return list(set(encoded_docs))


def main():
    paper_ids = get_ids_to_enc()
    total = len(paper_ids)
    print('docs to embedd:',total)

    for index, pid in enumerate(paper_ids):
        paper = dict(bioBertMain.find_one({ 'paperId':pid },{encoding_field:1,'paperId':1, '_id':0}))
        emb = paper[encoding_field]
        emb = pad_paper(emb, MAIN_SENT_LEN)
        emb = np.array([emb])
        prediction = m_model.predict(emb, batch_size=len(emb))
        encoded_final = prediction[0].tolist()
        save_encoding_to_db(encoded_final, pid, bert_emb_field)
        bioBertMain.update_one({'paperId': pid}, {'$set': {'encoded': 1}})
        print('progress:\t',index,'/',total)

        



                
main()
