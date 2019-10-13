##main text files to one csv file
##conver file to 'text' 'label' csv (get label from mongo)
import os
from os import listdir
from os.path import isfile, join
import re
import string
from pymongo import MongoClient
import csv
import pandas as pd


fullTextDir = 'bioFullTexts_clean01/'
outCSV='full_body_text_label.csv'
out_id_CSV='full_body_id_text_label.csv'

client = MongoClient('localhost', 27017)
db = client.bioArchive
bioCollection = db.bioPapers

def get_fulltext_files():
    textFiles = [f for f in listdir(fullTextDir) if isfile(join(fullTextDir, f))]
    print('total files:\t'+str(len(textFiles)))
    return textFiles

def get_id_from_file(filePath):
    f = filePath.replace('clean_','').replace('.txt','')
    return f

def import_text_from_file(filePath):
    with open(filePath, 'r') as file:
        fullText = file.read()
    return fullText 

def get_paperSubject_from_mongo(paperId):
    paper = bioCollection.find_one({'paperId':paperId})
    if paper != None:
        return paper['paperSubject']
    else:
        return 'unknown'

def get_papers_with_cleantext():
    papers = list(bioCollection.find({'cleanFullText':{'$exists':True}}))
    paperOutput = [{'label':p['paperSubject'],'text':p['cleanFullText']} for p in papers]
    return paperOutput
    
def main_text_to_dataframe():
    allFiles = get_fulltext_files()
    output=[]
    for f in allFiles:
        text = import_text_from_file(join(fullTextDir, f))
        paperId = get_id_from_file(f)
        paperLabel = get_paperSubject_from_mongo(paperId)
        textlabel = {
                        'text':text,
                        'label':paperLabel
                    }
        output.append(textlabel)
    df = pd.Dataframe(output)
    return df
        
def list_to_csv(textlabel_list):
    keys = textlabel_list[0].keys()
    with open(out_id_CSV, 'w+', newline='') as myfile:
        dict_writer = csv.DictWriter(myfile, keys,delimiter="\t")
        dict_writer.writeheader()
        dict_writer.writerows(textlabel_list)
        
    print('finished writing')

def add_cleantext_to_db(text,paperId):
    try:
        bioCollection.update_one({'paperId':paperId},{'$set':{'cleanFullText':text}})
    except Exception as e:
        print(str(e))
        return 0
    else:
        return 1

def update_db_with_texts():
    allFiles = get_fulltext_files()
    print(allFiles[:5])
    output=[]
    count=0
    failed = len(allFiles)
    for f in allFiles:
        text = import_text_from_file(join(fullTextDir, f))
        paperId = get_id_from_file(f)
        add_cleantext_to_db(text,paperId)
    print('success',count)
    print('failed',failed-count)

        
def import_csv(filePath):
    with open(filePath, 'r') as f:
        reader = csv.reader(f)
        linenumber = 1

        for row in reader:
            linenumber += 1
        
def main():
    paperList = get_papers_with_cleantext()
    list_to_csv(paperList)
    
    
    
main()
