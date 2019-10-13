import textract
import PyPDF2 
from pymongo import MongoClient
import os.path
from os import listdir
from os.path import isfile, join
import re

client = MongoClient('localhost', 27017)
db = client.bioArchive
bioCollection = db.bioPapers

#textract methods
tMethods = ['pdftotext','tesseract']
mPDF2Text = 'pdftotext'
mPDFMiner = 'pdfminer'
mTess = 'tesseract'
fullTextDir = 'bioFullTexts/'

def insert_full_text_to_db(fullText,paperId):
    bioCollection.update_one({'paperId':paperId},{'$set':{'rawFullText':fullText}},upsert=False)
    #print('inserted text for id:\t'+paperId)
    

def logPaperId(paperId,logFile):
    with open(logFile, 'a') as file:
        file.write(paperId)
        file.write('\n')

def get_paper_id(fileName):
    paperStrs = fileName.split('.')
    paperId = paperStrs[0]
    return paperId

def write_to_file(paperId,text):
    fullTextFile = fullTextDir + paperId+'.txt'
    with open(fullTextFile, 'w+') as file:
        file.write(text)
        file.write('\n')

def logPaperId(paperId,logFile):
    with open(logFile, 'a') as file:
        file.write(paperId)
        file.write('\n')

def main():
    files = [f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(), f))]
    pdfFiles = [f for f in files if f.endswith('.pdf')]
    logFiles = [f for f in files if f.endswith('.txt')]

    for f in logFiles:
        if 'papersFullTextConverted' in f:
            fullTextLogFile = f

    with open(fullTextLogFile, 'r') as f:
        fullTextPapers = [line.strip() for line in f]

    success = 0
    fail = 0
    print('papers:\t' + str(len(pdfFiles)))     

    for paper in pdfFiles:
        paperStrs = paper.split('.')
        paperId = paperStrs[0]
        pageTexts = []
        if(paperId not in fullTextPapers):
            pdfFileObj = open(paper, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            
            for page in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(page)
                text = pageObj.extractText()
                pageTexts.append(text)
            
            fullText =  ' '.join(pageTexts)
            pdfFileObj.close() 

            write_to_file(paperId,fullText)
            logPaperId(paperId,fullTextLogFile)
        success +=1
        print('processed: ' + str(success) +'\tid: ' + paperId)
        

            
main()
