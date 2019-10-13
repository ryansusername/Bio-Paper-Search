from bert_serving.client import BertClient
bc = BertClient(port=7010, port_out=7011, check_length=False)
from encoder.extract_sentences import sentences_from_text
import tensorflow as tf
import numpy as np

ab_model_path = 'models/bert/abstract/bert_abstract.h5'
ab_model = tf.keras.models.load_model(ab_model_path)

m_model_path = 'models/bert/mainbody/bert_maintext.h5'
m_model = tf.keras.models.load_model(m_model_path)

CLASS_TYPE = 'BERT'
TEXT_MAIN = 'MAINTEXT'
TEXT_AB = 'ABSTRACT'
VEC_LENGTH = 768

ENC_BERT_ABSTRACT_01 = 'abstract_encoding_BERT_1'
ENC_BERT_ABSTRACT_02 = 'abstract_encoding_BERT_1'

ENC_BERT_MAINTEXT_01 = 'maintext_encoding_BERT_1'
ENC_BERT_MAINTEXT_02 = 'maintext_encoding_BERT_1'

def np_to_py_datatype(npData):
    return npData.item()


def get_detail_string(encoder):
    details = '\nMODEL:\tBERT' + '\n' + 'ENCODER:\t' + encoder
    return details.expandtabs(20)


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

class BertEncoder:
    def __init__(self, out_type = 1, text_type='NONE'):
        self.text_type = text_type
        self.out_type = out_type
        self.model_type = CLASS_TYPE

    def get_details(self):
        details = '\nMODEL:\t' + self.model_type  + '\n' + 'TEXT:\t' + self.text_type + '\nOUTPUT TYPE:\t' + str(self.out_type)
        return details.expandtabs(20)

    def get_class_type(self):
        return CLASS_TYPE

    def get_encoding_type(self):
        if(self.text_type == TEXT_AB):
            if(self.out_type == 1):
                return ENC_BERT_ABSTRACT_01
            elif(self.out_type == 2):
                return ENC_BERT_ABSTRACT_02
        elif(self.text_type == TEXT_MAIN):
            if(self.out_type == 1):
                return ENC_BERT_MAINTEXT_01
            elif(self.out_type == 2):
                return ENC_BERT_MAINTEXT_02


class BertAbstract(BertEncoder):
    def __init__(self, out_type = 1):
        super().__init__(out_type, text_type=TEXT_AB)
        print(self.get_encoding_type())

    def get_embeddings(self, text, text_type=TEXT_AB):
        if(text_type == TEXT_AB):
            total_sent = 10
        else:
            total_sent = 100

        sentences = self.get_sentences(text)
        embeddings = embed_sent_list(sentences)
        embeddings = pad_embeddings(embeddings, total_sent)
        embeddings = np.array([embeddings])
        return embeddings

    def get_encoding(self, sent_embed_list):
        encoding = ab_model.predict(sent_embed_list)
        encoding = encoding[0].tolist()
        return encoding

    def get_sentences(self, text):
        return sentences_from_text(text)

class BertMainText(BertEncoder):
    def __init__(self, out_type = 1):
        super().__init__(out_type, text_type=TEXT_MAIN)
        print(self.get_encoding_type())

    def get_embeddings(self, text, text_type=TEXT_MAIN):
        if(text_type == TEXT_AB):
            total_sent = 10
        else:
            total_sent = 100

        sentences = self.get_sentences(text)
        embeddings = embed_sent_list(sentences)
        embeddings = pad_embeddings(embeddings, total_sent)
        embeddings = np.array([embeddings])
        return embeddings

    def get_encoding(self, sent_embed_list):
        encoding = m_model.predict(sent_embed_list)
        encoding = encoding[0].tolist()
        return encoding

    def get_sentences(self, text):
        return sentences_from_text(text)



def main():
    print(ab_model.summary())


main()
