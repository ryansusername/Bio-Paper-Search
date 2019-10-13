## Component:   Document
## Module:      Document Sort Module
## Description: Module for sorting result list of documents by distance, keyword matches or reference matches
## Author:      Ryan McCloskey, 2019

import operator
##input list of Result_Doc
##sort by val of variable
SORT_OPTIONS = [
    'distance',
    'keywords',
    'references'
    ]

def sort_by_dist(doc_list):
    print('DOC SORT:', 'sorting by distance')
    sorted_list = sorted(doc_list, key=operator.attrgetter('distance'))
    return sorted_list

def sort_by_keyword(doc_list):
    print('DOC SORT:', 'sorting by keyword match')
    sorted_list = sorted(doc_list, key=operator.attrgetter('keyword_match_num'), reverse=True)
    print(sorted_list[0].title)
    return sorted_list

def sort_by_ref(doc_list):
    print('DOC SORT:', 'sorting by reference match')
    sorted_list = sorted(doc_list, key=operator.attrgetter('ref_match_num'), reverse=True)
    print(sorted_list[0].title)
    return sorted_list


def sort_by_field(doc_list, field='distance'):
    if(field == SORT_OPTIONS[0]):
        return sort_by_dist(doc_list)
    elif(field == SORT_OPTIONS[1]):
        return sort_by_keyword(doc_list)
    elif(field == SORT_OPTIONS[2]):
        return sort_by_ref(doc_list)
