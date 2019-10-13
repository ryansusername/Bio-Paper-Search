from document.document_compare import compare_keywords, compare_ref

class Result_Doc:

    def __init__(self, mongo_doc, distance, searched_doc):
        self.paperId = mongo_doc['paperId']
        self.distance = distance
        self.title = mongo_doc['title']
        self.paper_subject = mongo_doc['paperSubject']
        self.doi = mongo_doc['doi']
        self.paper_pdf = 'directory_link'
        self.keywords = []
        self.keyword_match = []
        self.keyword_match_num = 0

        self.references = []
        self.ref_match = []
        self.ref_match_num = 0

        if('keyWords' in mongo_doc):
            self.keywords = mongo_doc['keyWords']
            self.keyword_match = compare_keywords(searched_doc.keywords, self.keywords)
            self.keyword_match_num = len(self.keyword_match)

        if('references' in mongo_doc):
            self.references = mongo_doc['references']
            self.ref_match = compare_ref(searched_doc.refs, self.references)
            self.ref_match_num = len(self.ref_match)


    def keyword_similarity(self):
        pass

    def title_similarity(self):
        pass

    def ref_similarity(self):
        pass
