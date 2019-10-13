# import libraries
from urllib.request import urlopen
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import re
import textract
from pymongo import MongoClient

import os
from os.path import isfile, join
from os import listdir
import time
from datetime import datetime


##bioIndex = 'https://www.biorxiv.org/content/early/recent?page=2927' ##lastPosition 16/01/19
bioIndex = 'https://www.biorxiv.org/content/early/recent'
bioLastIndex = 'https://www.biorxiv.org/content/early/recent?page=3951'
baseURL = 'https://www.biorxiv.org'
bioPaper = 'https://www.biorxiv.org/content/early/2018/11/20/375006'

pdfSuffix = '.full.pdf'
metricsSuffix = '.article-metrics'
infoSuffix = '.article-info'

client = MongoClient('localhost', 27017)
db = client.bioArchive
bioCollection = db.bioPapers

pdfDir = 'bioPDFs/'

def get_abstract(url):
    try:
        abstractPage = urlopen(url)
    except HTTPError as e:
        print('failed opening: ' + url)
        print('Error: ' + e)
        return 'ERROR GETTING ABSTRACT'
    except URLError as e:
        print('failed opening: ' + url)
        print('Error: ' + e)
        a=b
        return 'ERROR GETTING ABSTRACT'
    else:
        abSoup = BeautifulSoup(abstractPage,'html.parser')
        abstractText = abSoup.find('p', attrs={'id':'p-2'})
        return abstractText.get_text()

    
def get_full_text_pdf(paperURL,paperId):##try catch here
    pdfURL = paperURL + pdfSuffix
    pdfPath = str(paperId) + '.pdf'
    filePath = join(pdfDir,pdfPath)
    
    if(os.path.exists(filePath) == False):   
        try:
            pdfResponse = requests.get(pdfURL)
        except HTTPError:
            print('could not get pdf: ' + pdfURL)
            return False
        else:
            file = open(filePath,'wb+')
            file.write(pdfResponse.content)
            file.close
            print('written ' + str(paperId))
            return True
    else:
        return True

def get_text_from_pdf(file):
    text = textract.process(file,encoding = 'unicode_escape')
    return(text)


def get_full_text(paperURL,paperId):
    file = get_full_text_pdf(paperURL,paperId)
    text = get_text_from_pdf(file)
    return text

def get_paper_info(paperURL):
    paperPage = urlopen(paperURL)
    soup = BeautifulSoup(paperPage,'html.parser')

    doi = get_paper_doi(soup)
    paperDate = get_paper_date(soup)
    paperType = get_paper_type(soup)
    paperSubject = get_paper_subject(soup)

    now = int(time.time())
    bioPaper = {
        'paperId':'',
        'title':'',
        'abstract':'',
        'rawFullText':'',
        'metrics':{
            'abstractLink':'',
            'pdfLink':''
        },
        'lastModifiedDate':now,
        'url':paperURL,
        'doi':doi,
        'publishedDate':paperDate,
        'paperType':paperType,
        'paperSubject':paperSubject,
        'pdfDownloaded':False
    }

    return bioPaper

def get_paper_doi(soup):
    doiAttrs = {'class':'highwire-cite-metadata-doi highwire-cite-metadata'}
    doiSpan = soup.find('span',doiAttrs)
    if doiSpan != None:
        doiStr = doiSpan.get_text()
        doiRegex = re.compile('https:\/\/doi\.org\/.+$')
        matches = doiRegex.findall(doiStr)
        return matches[0].strip()
    else:
        return ''

def get_paper_date(soup):
    dateAttrs = {'class':'pane-content'}
    paneContentDivs = soup.findAll('div',dateAttrs)
    for pane in paneContentDivs:
        if('Posted' in pane.get_text()):
            dateStr = pane.get_text()
            dateSpl = dateStr.split('Posted')
            dateStr = dateSpl[1].strip()
            dateStr = dateStr.replace('.','').replace(',','')
            date = datetime.strptime(dateStr, '%B %d %Y').date()
            return str(date)
    return ''

def get_paper_type(soup):
    typeAttrs = {'class':'biorxiv-article-type'}
    typeSpan = soup.find('span',typeAttrs)
    if typeSpan != None:
        typeStr = typeSpan.get_text().strip().lower()
        return typeStr
    else:
        return ''

def get_paper_subject(soup):
    subAttrs = {'class':'highwire-article-collection-term'}
    subSpan = soup.find('span',subAttrs)
    if subSpan != None:
        children = subSpan.findChildren('a' , recursive=False)
        subStr = children[0].get_text().strip().lower()
        return subStr
    else:
        return ''

def get_paper_metrics(paperURL):##not used
    metricsURL = paperURL + metricsSuffix
    metricsPage = urlopen(metricsURL)
    soup = BeautifulSoup(metricsPage,'html.parser')
    
    attrs = {'class':'cshl_total'}
    tableRow = soup.find('tr',attrs)
    print(soup)

    
    
def new_biopaper_object(paperId,abstract,paperURL,doi,paperDate,paperType):
    now = int(time.time())
    bioPaper = {
        'paperId':paperId,
        'abstract':abstract,
        'rawFullText':'',
        'metrics':{
            'abstractLink':'',
            'pdfLink':''
        },
        'lastModifiedDate':now,
        'url':paperURL,
        'doi':'',
        'publishedDate':paperDate,
        'paperType':'',
        'paperSubject':'',
        'pdfDownloaded':False
    }
    return bioPaper

def insert_into_db(bioPaper):
    bioCollection.insert_one(bioPaper)

def get_paper_id(abstractURL):
    idRegex = re.compile('[0-9]+$')
    matches = idRegex.findall(abstractURL)
    return matches[0]

def get_next_link(soup,nextLinkAttrs):
    linkText = 'Next '
    pageLinks = soup.findAll('a',attrs=nextLinkAttrs)
    for link in pageLinks:
        if (link.get_text() == linkText):
            return(link.get('href'))
    return ''

def get_page_count(soup):
    lastPageLi= soup.find('li',attrs={'class':'pager-last last odd'})
    children = lastPageLi.findChildren('a' , recursive=False)
    lastPageNo = children[0].get_text()
    return int(lastPageNo)

def get_all_downloaded_pdfs():
    pdfFiles = [f for f in listdir(pdfDir) if isfile(join(pdfDir, f))]
    pdfIds = [f.split('.')[0] for f in pdfFiles]
    return pdfIds


def main():
    paperAttrs = {'class':'highwire-article-citation highwire-citation-type-highwire-article tooltip-enable'}
    abstractAttrs = {'href':re.compile("/content/early")}
    nextLinkAttrs = {'href':re.compile("/content/early/recent\\?page=")}
    
    firstPage = urlopen(bioIndex)

    soup = BeautifulSoup(firstPage,'html.parser')
    get_next_link(soup,nextLinkAttrs)

    pageCount = get_page_count(soup)
    paperCount = pageCount*10
    count=0

    #get all pdf file names
    #downloadedPdfs = get_all_downloaded_pdfs()
        
    while(soup.find('a',attrs=nextLinkAttrs) != None):
        nextPageURL = baseURL + get_next_link(soup,nextLinkAttrs)
        print('page: {0}'.format(nextPageURL))
        
        ##get paper links
        for paper in soup.findAll('div',attrs=paperAttrs):
            paperURL = baseURL + (paper.find('a',attrs=abstractAttrs)).get('href')
            print('attempting: {0}'.format(paperURL))
            paperId = get_paper_id(paperURL)
            title = paper.get('title')
            abstract = get_abstract(paperURL)
            newPaper = get_paper_info(paperURL)
            newPaper['title'] = title
            newPaper['paperId'] = paperId
            newPaper['abstract'] = abstract
            newPaper['pdfDownloaded'] = get_full_text_pdf(paperURL,paperId)

            insert_into_db(newPaper)
            count+=1
            print('processed: {0}'.format(count))
            
        nextPage = urlopen(nextPageURL)
        soup = BeautifulSoup(nextPage,'html.parser')
        



main()
