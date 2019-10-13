import os
from os import listdir
from os.path import isfile, join
import re
import string
from pymongo import MongoClient
import csv
import pandas as pd
import json

outJSON = 'bert_abstract_all.json'
outJSON2 = 'bert_maintext_smpl.json'

client = MongoClient('localhost', 27017)
db = client.bioArchive
bioCollection = db.bertEncodings2

encoding_field = 'abstract_sentence_all'
encoding_field2 = 'main_sentence_smpl'

##get papers with id, abstract text and label
def get_all_papers_from_db(encoding_field):
    papers = list(bioCollection.find({encoding_field:{'$exists':True}},{'paperId':1, encoding_field:1,'label':1, '_id':0}))
    print(len(papers))
    return papers

def get_paper_ids(encoding_field):
    print('getting paper ids...')
    docs = list(bioCollection.find({encoding_field:{'$exists':True}},{'paperId':1,'_id':0}))
    outlist = [d['paperId'] for d in docs]
    print('retrieved', len(outlist), 'papers')
    return outlist
    
def write_to_json(outpath, doc_list):
    with open(outpath, 'w+') as outfile:
        json.dump(doc_list, outfile)

def export_as_stream(idList, outpath, encoding_field):
    count = 0
    total = len(idList)
    print('exporting')
    with open(outpath, 'w+') as outfile:
        outfile.write("[")
        for pid in idList:
            paper = dict(bioCollection.find_one({ 'paperId':pid },{'paperId':1, encoding_field:1,'label':1, '_id':0}))

            json.dump(paper, outfile)
            outfile.write(",\n")
            count += 1

            if(count % 100 == 0):
                print('progress:\t', count, '/', total)

        outfile.seek(0, os.SEEK_END)
        outfile.seek(outfile.tell() - 2, os.SEEK_SET)
        outfile.write("]")
        outfile.truncate()
    print('done')       

def test_output_as_json():
    with open(outJSON2) as json_file:
        papers = json.load(json_file)
        print('json converted successfully')

def main():

    ##papers = get_all_papers_from_db(encoding_field2)
    ##write_to_json(outJSON2, papers)
    paperIds = get_paper_ids(encoding_field2)
    export_as_stream(paperIds, outJSON2, encoding_field2)

    #test_output_as_json()


                  
main()
