import pickle
import tensorflow as tf
import numpy as np
from text_extraction.pubmed_stopwords import get_all_stopwords
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import WordNetLemmatizer
import re
import nltk
nltk.download('wordnet')

ab_model_path = 'models/bagofword/bagofwords_classifier_ab.pkl'
ab_vecvocab_path = 'models/bagofword/ab_vocab.pkl'

m_model_path = 'models/bagofword/bagofwords_classifier_maintext.pkl'
m_vecvocab_path = 'models/bagofword/main_vocab.pkl'

CLASS_TYPE = 'BAGOFWORD'
TEXT_MAIN = 'MAINTEXT'
TEXT_AB = 'ABSTRACT'

ENC_BOW_ABSTRACT_01 = 'abstract_encoding_BOW'
ENC_BOW_MAINTEXT_01 = 'maintext_encoding_BOW'

ENC_BOW_ABSTRACT_02 = 'abstract_encoding_BOW'
ENC_BOW_MAINTEXT_02 = 'maintext_encoding_BOW'

def preprocess_text(text):
    stemmer = WordNetLemmatizer()
    document = re.sub(r'\W', ' ', str(text))
    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)
    document = re.sub(r'\s+', ' ', document, flags=re.I)
    document = re.sub(r'^b\s+', '', document)
    document = document.lower()
    document = document.split()
    document = [stemmer.lemmatize(word) for word in document]
    document = ' '.join(document)
    return document

def get_ab_model():
    with open(ab_model_path, 'rb') as ab_classifier:
        ab_model = pickle.load(ab_classifier)

    with open(ab_vecvocab_path, 'rb') as vfile:
        ab_vec_vocab = pickle.load(vfile)

    ab_vectorizer = CountVectorizer(vocabulary = ab_vec_vocab,
                                    max_features=2000,
                                    min_df=1)
    return ab_model, ab_vectorizer


def get_maintext_model():
    with open(m_model_path, 'rb') as m_classifier:
        m_model = pickle.load(m_classifier)

    with open(m_vecvocab_path, 'rb') as m_vfile:
        m_vec_vocab = pickle.load(m_vfile)

    m_vectorizer = CountVectorizer(vocabulary = m_vec_vocab,
                                   max_features=2000,
                                   min_df=1)
    return m_model, m_vectorizer

def get_detail_string(encoder):
    details = '\nMODEL:\t'+ CLASS_TYPE + '\n' + 'ENCODER:\t' + encoder
    return details.expandtabs(20)


class BoWEncoder:
    def __init__(self, out_type = 1, text_type='NONE'):
        self.text_type = text_type
        self.out_type = out_type
        self.model_type = CLASS_TYPE

    def get_details(self):
        details = '\nMODEL:\t' + self.model_type  + '\n' + 'TEXT:\t' + self.text_type + '\nOUTPUT TYPE:\t' + str(self.out_type)
        return details.expandtabs(20)

    def get_class_type(self):
        return self.model_type

    def get_encoding_type(self):
        if(self.text_type == TEXT_AB):
            if(self.out_type == 1):
                return ENC_BOW_ABSTRACT_01
            elif(self.out_type == 2):
                return ENC_BOW_ABSTRACT_02
        elif(self.text_type == TEXT_MAIN):
            if(self.out_type == 1):
                return ENC_BOW_MAINTEXT_01
            elif(self.out_type == 2):
                return ENC_BOW_MAINTEXT_02

class BoWAbstract(BoWEncoder):
    def __init__(self, out_type = 1):
        super().__init__(out_type, text_type=TEXT_AB)
        print(self.get_encoding_type())
        self.encoder, self.enc_vec = get_ab_model()

    def get_encoding(self, text):
        vec = self.enc_vec.transform([text]).toarray()
        vec = self.encoder.predict_proba(vec)
        return vec[0].tolist()

class BoWMainText(BoWEncoder):
    def __init__(self, out_type = 1):
        super().__init__(out_type, text_type=TEXT_MAIN)
        print(self.get_encoding_type())
        self.encoder, self.enc_vec = get_maintext_model()

    def get_encoding(self, text):
        vec = self.enc_vec.transform([text]).toarray()
        vec = self.encoder.predict_proba(vec)
        return vec[0].tolist()
