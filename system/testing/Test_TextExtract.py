## Component:   Tester
## Module:      Tester Class for Text Extract Module
## Description: Test various functions of text extraction module
## Author:      Ryan McCloskey, 2019


from pdf_input import pdf_to_text
import unittest

pdf_file = 'test_input/test_pdf'
pdf_text = 'EXAMPLE TEXT FROM EXTRACTED FROM PDF'

class Test_TextExtractModule(unittest.TestCase):
    pdf_file_path = pdf_file
    def test_extract_from_pdf(self):
        text = pdf_to_text(pdf_file_path)
        self.assertEqual(text, pdf_text)
