from text_extraction.extract_abstract import extract_abstract
from text_extraction.extract_main_body import extract_main_body
from text_extraction.extract_keywords import extract_keyword_list
from text_extraction.extract_references import extract_reference_list
from text_extraction.extract_title import extract_title

class SearchDoc:

    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.main_body = extract_main_body(raw_text)
        self.abstract_text = extract_abstract(raw_text)
        self.keywords = extract_keyword_list(raw_text)
        self.title = extract_title(raw_text)
        self.refs = extract_reference_list(raw_text)
        self.paper_subject = ''

class SearchDocMongo:
    def __init__(self, mongodoc):
        self.raw_text = mongodoc['rawFullText']
        self.main_body = mongodoc['cleanFullText']
        self.abstract_text = mongodoc['abstract']
        self.keywords = mongodoc['keyWords']
        self.title = mongodoc['title']
        self.refs = mongodoc['references']
        self.paper_subject = mongodoc['paperSubject']
