import os
from os import listdir
from os.path import isfile, join
import re
import string
from pymongo import MongoClient
import csv
import pandas as pd

outCSV='bert_abstract_all.csv'



client = MongoClient('localhost', 27017)
db = client.bioArchive
bioCollection = db.bioPapers

##get papers with id, abstract text and label
def get_all_papers_from_db():
    papers = list(bioCollection.find({'cleanFullText':{'$exists':True}},{'paperId':1,'paperSubject':1,'cleanFullText':1, '_id':0}))
    print(len(papers))
    return papers

def get_all_ab_papers_from_db():
    papers = list(bioCollection.find({'abstract':{'$exists':True}}))
    print(len(papers))
    return papers
    

def modify_paperList(paperList):
    paperOut = [{'paper_id':p['paperId'], 'text':p['cleanFullText'], 'label':p['paperSubject']} for p in paperList]
    return paperOut

def list_to_csv(textlabel_list):
    keys = textlabel_list[0].keys()
    with open(outCSV, 'w+', newline='') as myfile:
        dict_writer = csv.DictWriter(myfile, keys,delimiter="\t")
        dict_writer.writeheader()
        dict_writer.writerows(textlabel_list)

def main():
    papers = get_all_papers_from_db()
    papers = modify_paperList(papers)

    list_to_csv(papers)

                  
def test():
    get_all_ab_papers_from_db()

                  
test()
