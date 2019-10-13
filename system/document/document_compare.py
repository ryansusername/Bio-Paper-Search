## Component:   Document
## Module:      Document Compare Module
## Description: Module for comparing documents using cosine distance of vectors
## Author:      Ryan McCloskey, 2019

from scipy.spatial import distance
from operator import itemgetter


def wordlist_to_lower(words):
    return [w.lower() for w in words]

def compare_encoding_matrix(enc1,enc2):
    results = distance.cosine(enc1, enc2)
    return results


def sort_dist(doc_dists):
    return sorted(doc_dists,key=itemgetter(1))


def compare_all_docs(doc_enc, doc_list):
    results = []
    print('DOC COMPARE','comparing',len(doc_list), 'docs')
    for d in doc_list:
        d_enc = d['encoding']
        d_id = d['paperId']
        dist = compare_encoding_matrix(doc_enc,d_enc)

        result = (d_id,dist)
        results.append(result)
    print('DOC COMPARE','complete')
    return sort_dist(results)


def compare_keywords(kw1, kw2):
    kw1 = wordlist_to_lower(kw1)
    kw2 = wordlist_to_lower(kw2)
    return list(set(kw1) & set(kw2))


def compare_title(title1, title2):
    pass


def compare_ref(refs1, refs2):
    refs1 = wordlist_to_lower(refs1)
    refs2 = wordlist_to_lower(refs2)
    return list(set(refs1) & set(refs2))
