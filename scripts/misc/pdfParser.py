import textract
from pymongo import MongoClient
import os.path
from os import listdir
from os.path import isfile, join
import re

client = MongoClient('localhost', 27017)
db = client.bioArchive
bioCollection = db.bioPapers
fullTextDir = 'bioFullTexts_textract/'
pdfDir = 'bioPDFs/'

logSuccess = 'papersFullTextConverted_textract.txt'
logFail = 'papersFullTextFailed_textract.txt'

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

def main():
    files = [f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(), f))]
    pdfFiles = [f for f in listdir(pdfDir) if isfile(join(pdfDir, f))]

    with open(logSuccess, 'r') as f:
        insertedPapers = [line.strip() for line in f]
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
        text = ''
        if(paperId not in insertedPapers and paperId not in failedPapers):##skip failed for now
            print('attempting: ' + paperId)
            try:
                text = str(textract.process(file))
            except UnicodeDecodeError:
                fail +=1
                logPaperId(paperId,logFail)
                print('unicode error failure: '+paperId)
            except TypeError:
                fail +=1
                logPaperId(paperId,logFail)
                print('type error failure: '+paperId)
            else:
                #insert_full_text_to_db(text,paperId)
                write_to_file(paperId,text)
                success +=1
                logPaperId(paperId,logSuccess)
                print('extract success: '+paperId)
        processed +=1
        print('processed: ' + str(processed) +'\tid: ' + paperId + '\n')
            
    print('success:\t'+str(success))
    print('failed: \t'+str(fail))
            
main()
