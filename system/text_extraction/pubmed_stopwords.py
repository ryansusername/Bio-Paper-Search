#Stopword list from pubmed

#pubmed stopwords
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

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

pwords = text[0].split(',')
pubmed_words = [w.strip() for w in pwords]


stop_words = set(stopwords.words("english"))


def get_pubmed_stopwords():
    return pubmed_words

def get_all_stopwords():
    return stop_words.union(pubmed_words)
