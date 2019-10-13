import nltk
from nltk.corpus import movie_reviews
import random
import os
import csv
import pandas as pd
import numpy as np
from IPython.core.display import display


def get_abstract_words():
    path = 'bioAbstracts/bioExport_text_label.csv'
    df = pd.read_csv(path)
    doc = df[['text']]
    abstracts = list(np.array(doc).flat)
    joined = " ".join(abstracts)
    words = nltk.word_tokenize(joined)
    return words


wordsAb = get_abstract_words()
allAbstractWords = nltk.FreqDist(w.lower() for w in wordsAb)
wordFeaturesAb = list(allAbstractWords)[:2000]

def get_film_documents():
    documents = []
    for category in movie_reviews.categories():
        for fileId in movie_reviews.fileids(category):
            documents.append((list(movie_reviews.words(fileId)),category))

    random.shuffle(documents)
    return documents

def get_abstract_documents():
    path = 'bioAbstracts/bioExport_text_label.csv'
    df = pd.read_csv(path)
    #display(df.head())
    doc = [list(x) for x in df.values]
    
    documents = [(nltk.word_tokenize(x[0]),x[1]) for x in doc]
    random.shuffle(documents)
    return documents
        

def document_features(document,allWords):
    wordFeatures = list(allWords)[:2000]
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features

def abstract_features(document):
    #wordFeatures = list(allAbstractWords)[:2000]
    documentWords = set(document)
    features = {}
    for word in wordFeaturesAb:
        features['contains({})'.format(word)] = (word in documentWords)
    return features

def abstract_no_label():
    path = 'bioAbstracts/bioExport_text_label.csv'
    df = pd.read_csv(path)
    docs = df['text'].tolist()
    return docs
    
def do_movie():
    allWords = nltk.FreqDist(w.lower() for w in movie_reviews.words())
    wordFeatures = list(allWords)[:2000]

    allMovies = get_film_documents()
    example = allMovies[0]

    featuresets = [(document_features(d), c) for (d,c) in documents]

def do_abstract():
    #wordsAb = get_abstract_words()
    #allWords = nltk.FreqDist(w.lower() for w in words)
    #wordFeatures = list(allWords)[:2000]
    
    allAbstracts_labelled = get_abstract_documents()
    
    allAbstracts_unlabelled = abstract_no_label()
    example = allAbstracts_unlabelled[0]

    featureSets = [(abstract_features(d,), c) for (d,c) in allAbstracts_labelled]
    trainSet, testSet = featureSets[100:], featureSets[:100]
    classifier = nltk.NaiveBayesClassifier.train(trainSet)
    classifier.show_most_informative_features(10)
    #print(abstract_features(example))
          
def main():
          
    #nltk.download('punkt')
    #abstracts = get_abstract_documents()
    #print(movie_reviews.words())
    #print(movie_reviews[0])
    #print(get_film_documents()[0])

    do_abstract()
    #print(list(movie_reviews.words('pos/cv957_8737.txt')))
    #print(allAbstracts[0])






    
main()
