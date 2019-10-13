import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


def remove_tab_etc(string):
  return ' '.join(string.split())

def remove_short_sentences(sent_list, min_len=20):
    sentences = [s for s in sent_list if len(s) >= min_len]
    return sentences


def sentences_from_text(text):
    sentences = sentence_tokenizer.tokenize(text)
    clean_sent = [remove_tab_etc(s) for s in sentences]
    clean_sent = remove_short_sentences(clean_sent)
    return clean_sent
