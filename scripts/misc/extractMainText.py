import os
from os import listdir
from os.path import isfile, join
import re
import string

fullTextDir = 'bioFullTexts_textract/'
pdfDir = 'bioPDFs/'
outputDir = 'bioFullTexts_clean01'


logSuccess = 'papersFullTextConverted_textract.txt'
logFail = 'papersFullTextFailed_textract.txt'




def get_fulltext_files():
    textFiles = [f for f in listdir(fullTextDir) if isfile(join(fullTextDir, f))]
    print('total files:\t'+str(len(textFiles)))
    return textFiles

def get_single_file(bioId):
    textFile = fullTextDir + bioId + '.txt'
    return import_file(textFile)
    

def import_text_from_file(filePath):
    with open(filePath, 'r') as file:
        fullText = file.read()
    return fullText 

def export_text_to_file(fileName,text):
    fileName = 'clean_' + fileName
    filePath = join(outputDir,fileName)
    with open(filePath, 'w+') as file:
        file.write(text)

def experiment():
    fullTextFiles = get_fulltext_files()
    text = import_file(fullTextFiles[0])
    count = 0
    ratios = []
    ratioObjs = []
    print(str(len(fullTextFiles)))
    for file in fullTextFiles:
        text = import_file(file)
        text = clean_text(text)
        textLen = len(text)
        refLen = remove_references(text,file)
        if refLen != 0:
            ratio = refLen/textLen
            ratioObj = {'ratio':ratio,'file':file}
            ratios.append(ratio)
            ratioObjs.append(ratioObj)

    print(str(len(ratios)))
    avg = sum(ratios) / len(ratios)
    maxR = max(ratios)
    minR = min(ratios)
    maxFile = [f['file'] for f in ratioObjs if f['ratio'] == maxR]
    minFile = [f['file'] for f in ratioObjs if f['ratio'] == minR]

    nine = [f for f in ratios if f > 0.9]
    eight = [f for f in ratios if f > 0.8]
    seven = [f for f in ratios if f > 0.7]
    six = [f for f in ratios if f > 0.6]
    five = [f for f in ratios if f > 0.5]
    four = [f for f in ratios if f > 0.4]
    three = [f for f in ratios if f > 0.3]
    two = [f for f in ratios if f > 0.2]
    one = [f for f in ratios if f > 0.1]

    #print('total: '+ str(len(ratios)))
    #print('number > 0.9: '+ str(len(nine)))

    #nineFiles = [f['file'] for f in ratioObjs if 0.8 <= f['ratio'] <= 0.9 ]
    for f in ratioObjs[0:20]:
        print(f['file'])


      
def remove_bioarch_text(text):
    regString01 = 'bioRxiv preprint first posted online[\s\S]+?No reuse allowed without permission|'
    regString02 = 'bioRxiv preprint first posted online[\s\S]+?It is made available under.+?license|'
    regString03 = 'bioRxiv preprint first posted online[\s\S]+?without crediting the original authors|'
    regString04 = 'bioRxiv[\s\S]+?for use under a CC.+?license|'
    regString05 = 'bioRxivpreprint[\s\S]+?all rights reserved. No reuse allowed without permission'

    pattern = regString01 + regString02 + regString03 + regString04 + regString05
    regAll = r"{}".format(pattern)
    regex = re.compile(regAll,re.IGNORECASE)
    matches = re.findall(pattern,text)
    
    text = re.sub(regex,' ',text)

    return text

def remove_references_at_end(text):
    regString01 = 'LITERATURE\WCITED[\s\S]+|'
    regString02 = 'ACKNOLEDGMENT[\s\S]+|Acknoledgment[\s\S]+|ACKNOWLEDGMENT[\s\S]+|Acknowledgment[\s\S]+|Acknowledgement[\s\S]+|ACKNOWLEDGEMENT[\s\S]+|'
    regString03 = 'Reference[\s\S]+|REFERENCE[\s\S]+|R eference[\s\S]+|R EFERENCE[\s\S]+|REFERNCE[\s\S]+|Refernce[\s\S]+|Citations[\s\S]+|CITATIONS[\s\S]+|'
    regString04 = 'literature\Wreferences[\s\S]+|Literature\Wreferences[\s\S]+|Bibliography[\s\S]+|BIBLIOGRAPHY[\s\S]+|bibliography[\s\S]+|'
    regString05 = 'Works\WCited[\s\S]+|Literature\WCited[\s\S]+|LITERATURE\WCITED[\s\S]+|Literature\Wcited[\s\S]+|literature\Wcited[\s\S]+|'
    regString06 = 'Literature\Wcitation|Liturature Cited|LITURATURE\WCITED'

    pattern = regString02 + regString03 + regString04 + regString05 + regString06
    regAll = r"{}".format(pattern)
    regex = re.compile(regAll)
    matches = re.findall(pattern,text)
    if(len(matches) == 1):
        if(len(matches[0]) < (len(text)/2)):
            text = re.sub(regex,' ',text)
    return text

           
def remove_references_at_beginning(text):
    regString01 = 'reference[\s\S]+?introduction|'
    regString02 = 'literature\Wcited[\s\S]+?introduction|literature\Wcitation[\s\S]+?introduction|'
    regString03 = 'work\Wcited[\s\S]+?introduction|works\Wcited[\s\S]+?introduction'
    
    pattern = regString01 + regString02 + regString03
    regAll = r"{}".format(pattern)
    regex = re.compile(regAll,re.IGNORECASE)
    matches = re.findall(pattern,text)
    if(len(matches) == 1):
        if(len(matches[0]) < (len(text)/2)):
            text = re.sub(regex,' ',text)
    return text


def clean_text(text):
    text = text.replace('. ',' *SENTENCE* ')
    text = re.sub(r"\\[a-zA-Z][0-9]+?", " ",text)
    text = re.sub(r"\\[a-zA-Z]", " ",text)
    text = re.sub(r"[^a-zA-Z\*]", " ",text)
    text = re.sub(r" [a-zA-Z] ", " ",text)
    text = re.sub(r"^[a-zA-Z] ", " ",text)
    text = text.replace(' *SENTENCE* ','. ')
    dSpace = '   '
    while(dSpace in text):
        text = text.replace(dSpace,'  ')
    return text

def main():
    fullTextFiles = get_fulltext_files()

    count = 0
    bioT = 0
    refB = 0
    refE = 0
           
    for file in fullTextFiles:
        text = import_text_from_file(join(fullTextDir,file))
        text = remove_bioarch_text(text)
        text = clean_text(text)

        text1 = remove_references_at_beginning(text)
        if(len(text1) < len(text)):
            refB +=1

        text2 = remove_references_at_end(text1)
        if(len(text2) < len(text1)):
            refE +=1

        export_text_to_file(file,text2)

        

    print('finished')    
    print('references removed from beginning',refB)
    print('references removed from end',refE)

    


main()
