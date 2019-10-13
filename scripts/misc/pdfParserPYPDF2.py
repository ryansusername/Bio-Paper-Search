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
pdfDir = 'bioPDFs/'
logSuccess = 'papersFullTextConverted.txt'
logFail = 'papersFullTextFailed.txt'

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
    pdfFiles = [f for f in listdir(pdfDir) if isfile(join(pdfDir, f))]


    with open(logSuccess, 'r') as f:
        fullTextPapers = [line.strip() for line in f]
    with open(logFail, 'r') as f:
        failedPapers = [line.strip() for line in f]

    processed = 0
    success = 0
    fail = 0
    print('papers:\t' + str(len(pdfFiles)))     

    for paper in pdfFiles:
        file = join(pdfDir, paper)
        paperStrs = paper.split('.')
        paperId = paperStrs[0]
        pageTexts = []
        print('attempting: ' + paperId)
        if(paperId not in fullTextPapers and paperId not in failedPapers):##skip failed for now
            pdfFileObj = open(file, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            if pdfReader.isEncrypted:
                pdfReader.decrypt('')

            failedParse = False
            for page in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(page)
                try:
                    text = pageObj.extractText()
                except ValueError:
                    failedParse = True
                else:
                    pageTexts.append(text)
                    
            if failedParse:
                logPaperId(paperId,logFail)
                fail +=1
            else:
                fullText =  ' '.join(pageTexts)
                pdfFileObj.close() 
                write_to_file(paperId,fullText)
                logPaperId(paperId,logSuccess)
                success +=1
        processed +=1
        print('processed: ' + str(processed) +'\tid: ' + paperId)

    print('success:\t'+str(success))
    print('failed: \t'+str(fail))
        

            
main()
