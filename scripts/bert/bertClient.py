from bert_serving.client import BertClient
from pymongo import MongoClient
import pandas as pd
import numpy as np
from bert_sent_enc import sentences_from_text

client = MongoClient('localhost', 27017)
db = client.bioArchive

##abstract collection
##bioCollection = db.bertEncodings

##maintext collection
bioCollection = db.bertEncodings2
bioPapers = df.bioPapers

bc = BertClient(port=7010, port_out=7011, check_length=False)

abstract_file = 'bioSentences/abstract_sentences_all.csv'
maintext_file = 'bioSentences/maintext_sentences_sample.csv'

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

def get_data_from_db(search_fields)
    papers = list(bioCollection.find({'$and':[{'cleanFullText':{'$exists':True}},{'paperSubject':'epidemiology'}]}, search_fields))

def insert_encoding_to_db(encoding, paperId, label):
    try:
        bioCollection.update_one({'paperId':str(paperId)},{'$set':{'main_sentence_smpl':encoding, 'label': label}},upsert=True)
    except Exception as e:
        print('error when trying to update',str(e))
        return 0
    else:
        return 1

def np_to_py_datatype(npData):
    return npData.item()

def get_paper_ids(file_path):
    sentences = get_data_from_csv(file_path)
    idList = sentences['paper_id'].tolist()

    print(type(idList[0]))
    print(len(idList))
    if(isinstance(idList[0], int) != True):
        idList = [int(l) for l in idList]

    print(type(idList[0]))
    idList = list(set(idList))
    print(len(idList))
    return idList


def get_label_sentence_from_id(paper_id,df):
    out_df = df.loc[df['paper_id'] == paper_id]
    sent_list = out_df['text'].tolist()
    label_list = out_df['label'].tolist()
    label_list = list(set(label_list))
    if(len(label_list) > 1):
        print('somethings broken',label_list)

    return label_list[0], sent_list

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
    maintexts = get_data_from_csv(maintext_file)
    no_sentences = maintexts.shape[0]

    print('sentences',no_sentences)

    count = 0
    sent_count = 0

    paper_id_list = get_paper_ids(maintext_file)
    no_paper_ids = len(paper_id_list)
    print('papers to process',no_paper_ids)


    for paper_id in paper_id_list:
        label, sentences = get_label_sentence_from_id(paper_id, maintexts)
        encodings_list = get_multiple_bert_encodings(sentences)

        #print(len(sentences), len(encodings_list))
        insert_encoding_to_db(encodings_list, paper_id, label)

        count +=1
        sent_count += len(sentences)
        if(count % 100 == 0):
            print('papers processed:\t',count, '/', no_paper_ids, '\tsentences encoded:\t', sent_count, '/', no_sentences)

def modified_main():
    text_field = 'cleanFullText'
    enc_field = 'maintext_encoding01'
    bert_emb_field = 'maintext_encoding_BERT_1'
    mainfields = [m_field, 'paperSubject', 'paperId']

    papers = get_data_from_db(mainfields)
    total = len(papers)
    print('docs to embedd:',total)

    for index, paper in enumerate(papers):
        text = paper[text_field]
        sentences = sentences_from_text(text)
        embeddings = embed_sent_list(sentences)
        embeddings = pad_embeddings(embeddings, total_sent)
        embeddings = np.array([embeddings])
        


    
test()
