import os
from os import listdir
from os.path import isfile, join
import re
import string
from pymongo import MongoClient
import csv
import pandas as pd



client = MongoClient('localhost', 27017)
db = client.bioArchive
bioCollection = db.bertEmbeddingsMain

encoding_field = 'abstract_sentence_all'
encoding_field2 = 'main_sentence_smpl'

outCSV = 'bert_maintext.csv'


def get_paper_ids(encoding_field):
    print('getting paper ids...')
    docs = list(bioCollection.find({encoding_field:{'$exists':True}},{'paperId':1,'_id':0}))
    outlist = [d['paperId'] for d in docs]
    print('retrieved', len(outlist), 'papers')
    return outlist

def export_as_csv(idList, outpath, encoding_field):
    count = 0
    total = len(idList)
    print('exporting')
    with open(outpath, 'w+') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t')
        
        for index, pid in enumerate(idList):
            paper = dict(bioCollection.find_one({ 'paperId':pid },{encoding_field:1,'label':1, '_id':0}))
            enc = paper[encoding_field]
            paper[encoding_field] = pad_paper(enc, 100, 768)
            csv_line = (paper['label'],paper[encoding_field])
            writer.writerow(csv_line)
            
            if(index % 100 == 0 and index != 0):
                print('progress',index,'/',total)
            
    print('done')       


def pad_paper(paper, max_seq_length, vec_length):
  padding = vec_length * [0]
  paper_len = len(paper)
  outpaper = paper
  
  if (paper_len > max_seq_length):
    outpaper = paper[:max_seq_length]

  else:
    outpaper = paper
  return outpaper

def main():
    paperIds = get_paper_ids(encoding_field2)
    export_as_csv(paperIds, outCSV, encoding_field2)


           
main()
