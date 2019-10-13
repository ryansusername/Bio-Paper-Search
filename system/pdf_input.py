## Component:   Text Extraction
## Module:      PDF to Text
## Description: For extracting text data from PDF
## Author:      Ryan McCloskey, 2019
import textract
import re
from tkinter.filedialog import askopenfilename

##Use tkinter module to access file explorer
def open_file_explorer():
    fileName = askopenfilename()
    print(fileName)
    return fileName

def pdf_to_text(file):
    error_text = 'Unable to extract text from this file'
    text = 'placeholder'
    try:
        text = str(textract.process(file))
    except UnicodeDecodeError:
        print('UnicodeDecodeError',error_text)
    except TypeError:
        print('TypeError',error_text)
    else:
        print('Success','text extracted')
    return text
