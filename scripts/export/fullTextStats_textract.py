import os
from os import listdir
from os.path import isfile, join

fullTextDir = 'bioFullTexts_textract/'
pdfDir = 'bioPDFs/'

logSuccess = 'papersFullTextConverted_textract.txt'
logFail = 'papersFullTextFailed_textract.txt'

def main():
    
    #get all pdf file names
    pdfFiles = [f for f in listdir(pdfDir) if isfile(join(pdfDir, f))]

    #get all textract extracted texts
    textFiles = [f for f in listdir(fullTextDir) if isfile(join(fullTextDir, f))]

    
    print('total pdf  files:\t' + str(len(pdfFiles)))
    print('total text files:\t' + str(len(textFiles)))

    #get logs of fails/successes
    with open(logSuccess, 'r') as f:
        fullTextPapers = [line.strip() for line in f]
        fullTextPapers = list(set(fullTextPapers))
    with open(logFail, 'r') as f:
        failedPapers = [line.strip() for line in f]
        failedPapers = list(set(failedPapers))

    print('textract_full texts extracted:\t' + str(len(fullTextPapers)))
    print('textract_full texts failed:   \t' + str(len(failedPapers)))


main()
