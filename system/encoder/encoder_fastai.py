## Component:   Encoder
## Module:      ULMFiT Encoder Module
## Description: Module for handling and creating Sequence of Sentence document emedding model using ULMFiT
## Author:      Ryan McCloskey, 2019


import fastai
from fastai.text import *
print(fastai.__version__)
fastai.torch_core.defaults.device = 'cpu'
CLASS_TYPE = 'FASTAI'
defaults.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

ab_model = load_learner(path='models/abstract_raw/models/classifier', file='ab_clas_fine_tuned_export.pkl')
m_model = load_learner(path='models/mainbody_raw/models/classifier', file='full_body_clas_03_export.pkl')

ENC_AI_ABSTRACT_01 = 'abstract_encoding01'
ENC_AI_ABSTRACT_02 = 'abstract_encoding02'

ENC_AI_MAINTEXT_01 = 'maintext_encoding01'
ENC_AI_MAINTEXT_02 = 'maintext_encoding02'

TEXT_MAIN = 'MAINTEXT'
TEXT_AB = 'ABSTRACT'

class FastAiEncoder:
    def __init__(self, out_type = 1, text_type='NONE'):
        self.text_type = text_type
        self.out_type = out_type
        self.model_type = CLASS_TYPE

    def get_details(self):
        details = '\nMODEL:\t' + self.model_type  + '\n' + 'TEXT:\t' + self.text_type + '\nOUTPUT TYPE:\t' + str(self.out_type)
        return details.expandtabs(20)

    def get_class_type(self):
        return self.model_type

    def get_encoding_type(self):
        if(self.text_type == TEXT_AB):
            if(self.out_type == 1):
                return ENC_AI_ABSTRACT_01
            elif(self.out_type == 2):
                return ENC_AI_ABSTRACT_02
        elif(self.text_type == TEXT_MAIN):
            if(self.out_type == 1):
                return ENC_AI_MAINTEXT_01
            elif(self.out_type == 2):
                return ENC_AI_MAINTEXT_02


class EncoderMainText(FastAiEncoder):
    def __init__(self, out_type = 1):
        super().__init__(out_type, text_type=TEXT_MAIN)

    ##Returns matrix of encoding
    def get_matrix(self, encoding):
        return encoding[2].tolist()

    ##Returns predicted class of encoding
    def get_predicted_class(self, encoding):
        return encoding[0]

    ##Uses classifier built on main text data
    def get_encoding(self, text):
        prediction = m_model.predict(text)
        return prediction[2].tolist()


    ##Uses classifier built on main text data
    ##returns sub layer of classifier model as encoding
    def get_sub_encoding(self, text):
        prediction = m_model.predict(text)
        return prediction[2].tolist()


##abstract encoder
class EncoderAbstract(FastAiEncoder):

    def __init__(self, out_type = 1):
        super().__init__(out_type, text_type=TEXT_AB)

    ##Returns matrix of encoding
    def get_matrix(self, encoding):
        return encoding[2].tolist()

    ##Returns predicted class of encoding
    def get_predicted_class(self, encoding):
        return encoding[0]

    ##Uses classifier built on main text data
    def get_encoding(self, text):
        prediction = ab_model.predict(text)
        return prediction[2].tolist()

    ##Uses classifier built on main text data
    ##returns sub layer of classifier model as encoding
    def get_sub_encoding(self, text):
        prediction = ab_model.predict(text)
        return prediction[2].tolist()


def main():
    abst1 = EncoderAbstract()
    abst2 = EncoderAbstract(2)
    maint1 = EncoderMainText()
    maint2 = EncoderMainText(2)

    print(abst1.get_details())
    print(abst2.get_details())
    print(maint1.get_details())
    print(maint2.get_details())


main()
