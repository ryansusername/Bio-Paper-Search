import re
import string
import nltk

def find_refs(text, doi):
    reg_term = r"doi[\s\S]{60}"
    regex = re.compile(reg_term)

    matches = re.findall(regex, text)
    matches = [m for m in matches if doi not in m and 'doing' not in m]

    if(len(matches) > 0):
        return matches

def clean_ref(ref_chunk):
    ref_chunk = re.sub(r"\\[a-zA-Z]",' ',ref_chunk)
    return ref_chunk

def get_ref_from_chunk(ref_chunk):
    reg_term = r"[0-9]+\.[0-9]+\/[^\s]+"
    match = re.findall(reg_term,ref_chunk)
    if(len(match) > 0):
        return match[0]
    else:
        return ''

def get_doi(text):
    reg_term = 'doi.+\/10\.1101\/[0-9]{1,10}'
    match = re.findall(reg_term,text)
    if(len(match) > 0):
        return match[0]
    else:
        return ''


def extract_reference_list(raw_text):
    doi = get_doi(raw_text)
    ref_chunks = find_refs(raw_text,doi)
    ref_list = []

    if(ref_chunks != None):
        for r in ref_chunks:
            r = clean_ref(r)
            r = get_ref_from_chunk(r)
            if(r != ''):
                ref_list.append(r)

    return ref_list
