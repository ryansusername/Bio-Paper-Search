import fastai
from fastai import *
from fastai.text import *
fastai.torch_core.defaults.device = 'cpu'
import pandas as pd
import numpy as np
import io
import os
from pymongo import MongoClient

defaults.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

ab_learn_clas = load_learner(path='models/abstract_raw/models/classifier', file='ab_clas_fine_tuned_export.pkl')
m_learn_clas = load_learner(path='models/maintext_raw/models/classifier', file='full_body_clas_03_export.pkl') 

client = MongoClient('localhost', 27017)
db = client.bioArchive
bioCollection = db.bioPapers


def get_encoding(text, classifier):
    prediction = classifier.predict(text)
    return prediction[2].tolist()


def test():
    ab = flatten_model(ab_learn_clas.model)

    abPool = list(ab_learn_clas.model.children())[1]
    abPoolDrops = abPool
    print(type(abPool))
    out_model = nn.Sequential(*ab)


    ab_model_list = list(ab_learn_clas.model.children())[0] + out_model
    
def test2():
    p = ab_learn_clas.model.parameters
    print(p)




def main2():
    model = test()
    text = 'Migration through constrictions can clearly rupture nuclei and mis-localize nuclear proteins but damage to DNA remains uncertain as does any effect on cell cycle. Here, myosin-II inhibition rescues rupture and partially rescues the DNA damage marker γH2AX, but an apparent delay in cell cycle is unaffected. Co-overexpression of multiple DNA repair factors and antioxidant inhibition of break formation also have partial effects, independent of rupture. Complete rescue of both DNA damage and cell cycle delay by myosin inhibition plus antioxidant reveals a bimodal dependence of cell cycle on DNA damage. Migration through custom-etched pores yields the same bimodal, with ~4-um pores causing intermediate levels of damage and cell cycle delay. Micronuclei (generated in faulty division) of the smallest diameter appear similar to ruptured nuclei, with high DNA damage and entry of chromatin-binding cGAS (cyclic-GMP-AMP-synthase) from cytoplasm but low repair factor levels. Increased genomic variation after constricted migration is quantified in expanding clones and is consistent with (mis)repair of excess DNA damage and subsequent proliferation.'
  
    print(list(model.children()))

    get_encoding(text, ab_learn_clas)
    ab_learn_clas.model = model


    get_encoding(text, ab_learn_clas)
    
def main():
    #print(type(ab_learn_clas))
    print('\n\n')

    ##print(list(ab_learn_clas.model.parameters()))
    print(list(ab_learn_clas.model.children()))

    
test2()
