from document.document_compare import compare_encoding_matrix
from document.document_sort import sort_by_dist
import unittest

enc_one = [0,0,0,0,0]
enc_two = [1,1,1,1,1]

enc_sort = [1,3,9,2,5,7]
enc_sorted = [1,2,3,5,7,9]

same_enc_val = 0

class Test_DocumentModule(unittest.TestCase):
    def test_document_compare_diff(self):
        dist = compare_encoding_matrix(enc_one,enc_two)
        self.assertNotEqual(dist, same_enc_val)

    def test_document_compare_same(self):
        dist = compare_encoding_matrix(enc_one,enc_two)
        self.assertEqual(dist, same_enc_val)

    def test_sort_doc(self):
        sorted = sort_by_dist(enc_sort)
        self.assertEqual(sorted, enc_sorted)

    def test_db_connection(self):
        field = '_id'
        docs = get_all_doc_encoding(field)
        self.assertNotEqual(len(docs), 0)
