import re
import string
import nltk
text = ['a, ,abbreviations, about, again, all, almost, also, although, always, among, an, and, another, any, are, as, at\
,be, because, been, before, being, between, both, but, by\
,can, could\
,did, do, does, done, due, during\
,each, either, enough, especially, etc\
,for, found, from, further\
,had, has, have, having, here, how, however\
,i, if, in, into, is, it, its, iv, itself\
,just\
,kg, km\
,made, mainly, make, may, mg, might, ml, mm, most, mostly, must\
,nearly, neither, new, no, nor\
,obtained, of, often, on, our, overall\
,perhaps, pmid, previously\
,quite\
,rather, really, regarding, result\
,seem, seen, several, should, show, showed, shown, shows, significantly, since, so, some, such\
,than, that, the, their, theirs, them, then, there, therefore, these, they, this, those, through, thus, to\
,upon, use, used, using\
,various, very\
,was, we, were, what, when, which, while, with, within, without, would']


nltk.download('stopwords')
from nltk.corpus import stopwords

pwords = text[0].split(',')
pubmed_words = [w.strip() for w in pwords]


stop_words = set(stopwords.words("english"))


def get_pubmed_stopwords():
    return pubmed_words

def get_all_stopwords():
    return stop_words.union(pubmed_words)



def find_key_words(text):
    reg_term = r"KEY WORDS[\s\S]{250}|KEY WORD[\s\S]{250}|KEYWORD[\s\S]{250}"
    reg_false_match = r'key.*word.+based'

    regex = re.compile(reg_term, re.IGNORECASE)

    matches = re.findall(regex, text)

    if(len(matches) == 1):
        return str(matches[0])
    elif(len(matches) >= 1):
        false_matchs = re.findall(reg_false_match, matches[0])
        if(len(false_matchs) > 0):
            return str(matches[1])
        else:
            return str(matches[0])
    else:
        return ''

def remove_keyword_ref(text):
    text = re.sub(r"KEY.*WORDS", " ", text,flags=re.IGNORECASE)
    text = re.sub(r"KEY.*WORD", " ", text,flags=re.IGNORECASE)
    return text

def clean_text(text):
    text = re.sub(r"\\[a-zA-Z][0-9][0-9]+?", " ",text)
    text = re.sub(r"\\[a-zA-Z][0-9]+?", " ",text)
    text = re.sub(r"\\[a-zA-Z]", " ",text)
    text = re.sub(r" [a-z0-9]{2} ", " ", text)
    dSpace = '   '
    while(dSpace in text):
        text = text.replace(dSpace,'  ')
    return text

def clean_keyword_chunk(text):
    clean_term = re.sub(r"\\n\\n(?!.*\\n\\n).+", " ",text)
    return clean_term

def remove_email(text):
    text = re.sub(r"email.+@.+\.[a-z]{1,3}", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"e mail.+@.+\.[a-z]{1,3}", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"e-mail.+@.+\.[a-z]{1,3}", " ", text, flags=re.IGNORECASE)
    return text


def remove_ab_and_intro(text):
    text = re.sub(r"INTRODUCTION.+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"RUNNING TITLE.+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"TITLE.+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"ABSTRACT.+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"ACKNOWLEDGEMENT.+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"WORD COUNT.+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"NUMBER WORDS.+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"NUMBER WORD.+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"NUMBER PAGE.+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"NUMBER FIGURE.+", " ", text, flags=re.IGNORECASE)

    text = re.sub(r"GRANT SUPPORT.+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"CONFLICT.*INTEREST.+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"FUNDING.+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"SUMMARY.+", " ", text, flags=re.IGNORECASE)
    return text

def remove_author(text):
    text = re.sub(r"CORRESPONDING AUTHOR.+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"CORRESPONDENCE.+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"CORRESPONDENT.+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"AUTHOR.+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"CONTACT INFO.+", " ", text, flags=re.IGNORECASE)
    return text

def remove_bioarc_ref(text):
    text = re.sub(r"bioRxiv.+", " ", text, flags=re.IGNORECASE)
    return text


def remove_stop_words(token_list):
    token_list = [t for t in token_list if not t in stop_words]
    return token_list

def clean_tokens(token_list):
    token_list = [t for t in token_list if len(t) > 2]
    return token_list


def tokenise_keyword_chunk(text):
    tokens = nltk.word_tokenize(text)
    tokens = remove_stop_words(tokens)
    tokens = clean_tokens(tokens)
    return tokens


def extract_keyword_list(raw_text):
    keywords_list = []
    keyword_chunk = find_key_words(raw_text)
    if keyword_chunk != '':
        ##clean text where possible
        keyword_chunk = clean_keyword_chunk(keyword_chunk)
        keyword_chunk = remove_ab_and_intro(keyword_chunk)
        keyword_chunk = remove_email(keyword_chunk)
        keyword_chunk = remove_author(keyword_chunk)
        keyword_chunk = remove_bioarc_ref(keyword_chunk)
        keyword_chunk = clean_text(keyword_chunk)

        ##remove word: keyword
        keyword_chunk = remove_keyword_ref(keyword_chunk)


        ##tokenise to key words, removing stop words and irrelevant text where possible
        kw_list = tokenise_keyword_chunk(keyword_chunk)

        keywords_list = keywords_list + kw_list

    return keywords_list
