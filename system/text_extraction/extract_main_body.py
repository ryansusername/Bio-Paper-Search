import re

##Function for general cleaning of text string, removing image data from pdf extracting etc
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

##Method for removing default strings found on most papers in bioarchive        
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

##Function for removing references found at end of file
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

##Function for removing references found at start of file       
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

##Get main body from text
def extract_main_body(text):
    text = remove_bioarch_text(text)
    text = clean_text(text)
    text = remove_references_at_beginning(text)
    text = remove_references_at_end(text)
    return text
