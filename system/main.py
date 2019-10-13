## Component:   Main
## Module:      Main Module
## Description: Access point for system, module handles GUI using TKInter and main search function
## Author:      Ryan McCloskey, 2019

import tkinter as tk
from PIL import ImageTk, Image
import os
from os import listdir
from pdf_input import pdf_to_text, open_file_explorer
import webbrowser

from text_extraction.extract_abstract import extract_abstract, clean_before_processing
from text_extraction.extract_main_body import extract_main_body

from encoder.encoder_fastai import EncoderAbstract, EncoderMainText
from encoder.encoder_bert import BertAbstract
from encoder.encoder_bow import BoWAbstract, BoWMainText

from document.document_sort import SORT_OPTIONS, sort_by_field

from search_document import SearchDoc
search_doc = SearchDoc('none')

from search_function import search, raw_results_to_documents, get_res_doc_sample

text_file_path = 'upload pdf file'
raw_text = 'placeholder_text'
text_to_search = 'placeholder_text'

paper_icon_path = 'resources/document-icon.png'
img = None



ENC_AI_ABSTRACT_01 = 'encAiAb01'
ENC_AI_ABSTRACT_02 = 'encAiAb02'

ENC_AI_MAINTEXT_01 = 'encAiMt01'
ENC_AI_MAINTEXT_02 = 'encAiMt01'

ENC_BERT_ABSTRACT_01 = 'encBertAb01'
ENC_BERT_ABSTRACT_02 = 'encBertAb02'

ENC_BERT_MAINTEXT_01 = 'encBertMt01'

ABSTRACT_CLASSIFIER = EncoderAbstract()
ABSTRACT_CLASSIFIER_SUB = EncoderAbstract(out_type = 2)
MAINTEXT_CLASSIFIER = EncoderMainText()


BERT_AB_CLASSIFIER = BertAbstract()
BERT_MAIN_CLASSIFIER = BertAbstract()

BOW_AB_CLASSIFIER = BoWAbstract()
BOW_MAIN_CLASSIFIER = BoWMainText()

text_classifier = ABSTRACT_CLASSIFIER

text_colour = 'snow'
text_font = 'ariel'
background_colour = 'gray9'
btn_colour = 'gray15'
btn_act_colour = 'gray10'
act_colour = 'gray20'



def open_pdf_file(textbox):
    global raw_text
    global text_to_search
    global text_file_path
    global search_doc

    text_file_path = open_file_explorer()
    raw_text = pdf_to_text(text_file_path)
    text_to_search = raw_text
    set_input(text_file_path, textbox)

    search_doc = SearchDoc(raw_text)
    return raw_text

def web_search(url):
    webbrowser.open_new(url)

def ab_text(raw_text):
    text = 'abstract_text'
    return text

def get_text_to_search(class_type, search_type, textbox):
    global text_to_search

    ##keep classifier consistent with change for fastai, irelevent for bert
    if(class_type == 1):
        set_classifier(class_type, search_type)


    if(text_to_search != 'placeholder_text'):
        if(search_type.get() == 1):
            print('searching by abstract')
            text_to_search = extract_abstract(raw_text)
            print(text_to_search[:30])

        elif(search_type.get() == 2):
            print('searching by main body')
            text_to_search = extract_main_body(raw_text)
            print(text_to_search[:30])

    set_input(text_to_search, textbox)
    return text_to_search

def set_classifier(class_type,search_type):
    global text_classifier

    ##if FastAi Encoder
    if(class_type.get() == 1):
        ##Abstract
        if(search_type.get() == 1):
            text_classifier = ABSTRACT_CLASSIFIER
        ##Main Text
        elif(search_type.get() == 2):
            text_classifier = MAINTEXT_CLASSIFIER
        else:
            print('No Selection:','Please select a seach text')

    ##Bert Encoder
    elif(class_type.get() == 2):
        ##Abstract
        if(search_type.get() == 1):
            text_classifier = BERT_AB_CLASSIFIER
        ##Main Text
        elif(search_type.get() == 2):
            text_classifier = BERT_MAIN_CLASSIFIER
        else:
            print('No Selection:','Please select a seach text')

    elif(class_type.get() == 3):
        if(search_type.get() == 1):
            text_classifier = BOW_AB_CLASSIFIER
        ##Main Text
        elif(search_type.get() == 2):
            text_classifier = BOW_MAIN_CLASSIFIER
        else:
            print('No Selection:','Please select a seach text')
    else:
        print('No Encoder Selected')
    print('using classifier:',text_classifier.get_details())

def start_search():
    #print(text_to_search[:20])
    print(text_classifier.get_details())
    raw_res = search(search_doc, text_classifier)
    ##raw_res = []
    open_results_window(raw_res,search_doc)

def sort_results(var, res_list, text_view):
    res_list = sort_by_field(res_list, field=var.get())
    populate_result_view(text_view, res_list)


def populate_result_view(text_view, result_docs):
    print('POPULATING RESULTS')
    text_view.configure(state="normal")
    text_view.delete('1.0', tk.END)
    for doc in result_docs:
        doc_view = new_document_view(text_view, doc)
        text_view.window_create("end", window=doc_view)
        text_view.insert("end", "\n\n")
    text_view.configure(state="disabled")
    print('POPULATING RESULTS: COMPLETE')

def set_input(text, textbox):
    textbox.delete(1.0, tk.END)
    textbox.insert(tk.END, text)


def new_frame(root):
    return tk.Frame(root, background=background_colour, bd=0, highlightbackground=background_colour)

def new_btn(root, text):
    return tk.Button(root, bg=btn_colour, fg=text_colour, text=text,
                           activebackground=btn_act_colour,
                           activeforeground=text_colour,
                           highlightbackground=btn_act_colour,
                           highlightthickness = 1)

def new_lbl(root, text, font_size, anchor='w',  justify=tk.LEFT):
    return tk.Label(root, text=text, font=(text_font, font_size),
                          anchor=anchor, justify=justify,
                          fg=text_colour, bg=background_colour)

def new_res_lbl(root, text, font_size):
    return tk.Label(root, text=text,
                          width=80, wraplength=500,
                          anchor='w', justify=tk.LEFT,
                          font=(text_font, font_size),
                          fg=text_colour, bg=background_colour)

def new_s_lbl(root, text, font_size):
    return tk.Label(root, text=text, width=10,
                          wraplength=190, anchor='w',
                          justify=tk.LEFT, font=(text_font, font_size),
                          fg=text_colour, bg=background_colour)


def new_img_lbl(root, img, url):
    lbl = tk.Label(root, image=img, fg=text_colour, bg=background_colour,cursor="hand1")
    lbl.bind("<Button-1>",lambda e,url=url:web_search(url))
    return lbl


def new_radio_btn(root, text, var, val):
    return tk.Radiobutton(root,bg=background_colour,
                               fg = text_colour,highlightbackground=background_colour,
                               activebackground=act_colour,
                               activeforeground=text_colour,
                               selectcolor=background_colour,bd=0,
                               text=text, variable=var,value=val,
                               anchor='w', justify=tk.LEFT)

def new_document_view(root,result_doc):
    doc_frame = tk.Frame(root, background=background_colour, highlightbackground='gray36', highlightthickness = 1)
    doc_frame.grid_rowconfigure(0, weight=1)
    doc_frame.grid_rowconfigure(1, weight=1)
    doc_frame.grid_rowconfigure(2, weight=1)
    doc_frame.grid_rowconfigure(3, weight=1)
    doc_frame.grid_rowconfigure(4, weight=1)
    doc_frame.grid_rowconfigure(5, weight=1)
    doc_frame.grid_rowconfigure(6, weight=1)
    doc_frame.grid_rowconfigure(7, weight=1)

    doc_frame.grid_columnconfigure(0, weight=1)
    doc_frame.grid_columnconfigure(1, weight=1)
    doc_frame.grid_columnconfigure(2, weight=3)


    lbl_img = new_img_lbl(doc_frame, img, url=result_doc.doi)

    lbl_docid = new_lbl(doc_frame,'paper id:',10)
    lbl_val_docid = new_res_lbl(doc_frame, result_doc.paperId, 10)

    lbl_doctitle = new_lbl(doc_frame,'title:',10)
    lbl_val_doctitle = new_res_lbl(doc_frame, result_doc.title, 10)

    lbl_class = new_lbl(doc_frame,'class:',10)
    lbl_val_class = new_res_lbl(doc_frame, result_doc.paper_subject, 10)

    lbl_diff = new_lbl(doc_frame,'difference:',10)
    lbl_val_diff = new_res_lbl(doc_frame, result_doc.distance, 10)

    lbl_kw = new_lbl(doc_frame,'keywords:',10)
    lbl_kw_val = new_res_lbl(doc_frame,str(result_doc.keywords),10)

    lbl_kwm = new_lbl(doc_frame,'keyword match:',10)
    lbl_kwm_val = new_res_lbl(doc_frame,str(result_doc.keyword_match),10)

    lbl_ref = new_lbl(doc_frame,'references:',10)
    lbl_ref_val = new_res_lbl(doc_frame,str(result_doc.references),10)

    lbl_refm = new_lbl(doc_frame,'reference match:',10)
    lbl_refm_val = new_res_lbl(doc_frame,str(result_doc.ref_match),10)

    ##vsb = tk.Scrollbar(doc_frame, orient="vertical")

    lbl_img.grid(row=0, column=0,columnspan=1,rowspan=5, padx=5, pady=5)

    lbl_docid.grid(row=0, column=1, padx=5, pady=5)
    lbl_val_docid.grid(row=0, column=2, padx=5, pady=5)

    lbl_doctitle.grid(row=1, column=1, padx=5, pady=5)
    lbl_val_doctitle.grid(row=1, column=2, padx=5, pady=5)

    lbl_class.grid(row=2, column=1, padx=5, pady=5)
    lbl_val_class.grid(row=2, column=2, padx=5, pady=5)

    lbl_diff.grid(row=3, column=1, padx=5, pady=5)
    lbl_val_diff.grid(row=3, column=2, padx=5, pady=5)

    lbl_kw.grid(row=4, column=1, padx=5, pady=5)
    lbl_kw_val.grid(row=4, column=2, padx=5, pady=5)

    lbl_kwm.grid(row=5, column=1, padx=5, pady=5)
    lbl_kwm_val.grid(row=5, column=2, padx=5, pady=5)

    lbl_ref.grid(row=6, column=1, padx=5, pady=5)
    lbl_ref_val.grid(row=6, column=2, padx=5, pady=5)

    lbl_refm.grid(row=7, column=1, padx=5, pady=5)
    lbl_refm_val.grid(row=7, column=2, padx=5, pady=5)
    ##vsb.grid(row=1, column=3, rowspan=7, padx=5, pady=5)
    return doc_frame

def new_searched_doc_view(root, search_doc):
    sdoc_frame = tk.Frame(root, background=background_colour, highlightbackground='gray36', highlightthickness = 1)
    sdoc_frame.grid_rowconfigure(0, weight=1)
    sdoc_frame.grid_rowconfigure(1, weight=1)
    sdoc_frame.grid_rowconfigure(2, weight=1)
    sdoc_frame.grid_rowconfigure(3, weight=1)
    sdoc_frame.grid_rowconfigure(4, weight=1)
    sdoc_frame.grid_rowconfigure(5, weight=1)

    sdoc_frame.grid_columnconfigure(0, weight=1)
    lbl_title = new_lbl(sdoc_frame, 'Input Document', 14)

    lbl_img = new_img_lbl(sdoc_frame, img, url='')

    lbl_kw = new_lbl(sdoc_frame,'keywords:',10)
    lbl_kw_val = new_s_lbl(sdoc_frame,str(search_doc.keywords),10)

    lbl_ref = new_lbl(sdoc_frame,'references:',10)
    lbl_ref_val = new_s_lbl(sdoc_frame,str(search_doc.refs[:5]),10)

    lbl_title.grid(row=0, column=0, padx=(20, 5), pady=(20, 5), sticky='nsew')
    lbl_img.grid(row=1, column=0, padx=5, pady=5,sticky='nsew')
    lbl_kw.grid(row=2, column=0, padx=5, pady=2,sticky='nsew')
    lbl_kw_val.grid(row=3, column=0, padx=5, pady=2,sticky='nsew')
    lbl_ref.grid(row=4, column=0, padx=5, pady=2,sticky='nsew')
    lbl_ref_val.grid(row=5, column=0, padx=5, pady=2,sticky='nsew')
    return sdoc_frame

def open_results_window(raw_result_list, searched_doc):
    #print(len(raw_result_list))
    print('RESULTS WINDOW:', 'opening...')
    result_docs = raw_results_to_documents(raw_result_list,searched_doc)
    ##result_docs = get_res_doc_sample()
    print(len(result_docs))

    res_window = tk.Toplevel(root)
    res_window.geometry("1100x600")
    res_window.grid_rowconfigure(0, weight=1)
    res_window.grid_columnconfigure(0, weight=2)
    res_window.grid_columnconfigure(1, weight=5)
##define frames
    fram_searched_doc = tk.Frame(res_window, background=background_colour, bd=0, highlightbackground='gray15', highlightthickness = 1)
    fram_searched_doc.grid_rowconfigure(0, weight=1)
    fram_searched_doc.grid_columnconfigure(0, weight=1)

    searched_doc_view = new_searched_doc_view(fram_searched_doc, searched_doc)
    searched_doc_view.grid(row=0, column=0, sticky='nsew')

    fram_doc_list = tk.Frame(res_window, background=background_colour, bd=0, highlightbackground='gray15', highlightthickness = 1)
    fram_doc_list.grid_rowconfigure(0, weight=1)
    fram_doc_list.grid_rowconfigure(1, weight=4)
    fram_doc_list.grid_columnconfigure(0, weight=2)
    fram_doc_list.grid_columnconfigure(1, weight=1)
    fram_doc_list.grid_columnconfigure(2, weight=1)
    fram_doc_list.grid_columnconfigure(3, weight=1)


##Add frames to parent window
    fram_searched_doc.grid(row=0, column=0, sticky='nsew')
    fram_doc_list.grid(row=0, column=1, sticky='nsew')

    lbl_results_title = new_lbl(fram_doc_list, 'Results', 14)

    var_sort = tk.StringVar(fram_doc_list)
    var_sort.set(SORT_OPTIONS[0]) # default value

    ##result list view
    txt_results_view = tk.Text(fram_doc_list, background=background_colour, bd=0)
    vsb = tk.Scrollbar(fram_doc_list, orient="vertical", command=txt_results_view.yview)
    txt_results_view.configure(yscrollcommand=vsb.set)


    ##option sort by field
    rb_dist = new_radio_btn(fram_doc_list,'distance',var_sort,SORT_OPTIONS[0])
    rb_dist['command'] = lambda: sort_results(var_sort, result_docs, txt_results_view)
    rb_kw = new_radio_btn(fram_doc_list,'keywords',var_sort,SORT_OPTIONS[1])
    rb_kw['command'] = lambda: sort_results(var_sort, result_docs, txt_results_view)
    rb_ref = new_radio_btn(fram_doc_list,'references',var_sort,SORT_OPTIONS[2])
    rb_ref['command'] = lambda: sort_results(var_sort, result_docs, txt_results_view)




    lbl_results_title.grid(row=0, column=0, columnspan=1, sticky='nsew', padx=5, pady=5)
    rb_dist.grid(row=0, column=1, columnspan=1, sticky='nsew', padx=5, pady=5)
    rb_kw.grid(row=0, column=2, columnspan=1, sticky='nsew', padx=5, pady=5)
    rb_ref.grid(row=0, column=3, columnspan=1, sticky='nsew', padx=5, pady=5)

    txt_results_view.grid(row=1, column=0, columnspan=4,sticky='nsew')
    vsb.grid(row=1, column=4,sticky='nsew')

    populate_result_view(txt_results_view, result_docs)
    print('RESULTS WINDOW:', 'opened')

class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window(root)

    #Creation of init_window
    def init_window(self,root):
        global text_to_search
        global raw_text
    ##FRAMES root window
        ##Input frame
        frame_input = new_frame(root)
        frame_input.grid_rowconfigure(0, weight=1)
        frame_input.grid_rowconfigure(1, weight=1)
        frame_input.grid_rowconfigure(2, weight=1)
        frame_input.grid_columnconfigure(0, weight=1)
        frame_input.grid_columnconfigure(1, weight=1)
        frame_input.grid_columnconfigure(2, weight=1)
        frame_input.grid_columnconfigure(3, weight=1)

        ##Options frame
        frame_options = new_frame(root)
        frame_options.config(highlightbackground='gray15', highlightthickness = 1)
        frame_options.grid_rowconfigure(0, weight=1)
        frame_options.grid_rowconfigure(1, weight=1)
        frame_options.grid_rowconfigure(2, weight=3)
        frame_options.grid_columnconfigure(0, weight=1)
        frame_options.grid_columnconfigure(1, weight=1)
        frame_options.grid_columnconfigure(2, weight=1)
        frame_options.grid_columnconfigure(3, weight=1)

        ##Text frame
        frame_text = new_frame(root)
        frame_text.config(highlightbackground='gray15', highlightthickness = 1)
        frame_text.grid_rowconfigure(0, weight=1)
        frame_text.grid_rowconfigure(1, weight=8)
        frame_text.grid_columnconfigure(0, weight=1)

        #define grid layout of frames
        frame_input.grid(row=0, column=0,columnspan=2, sticky="nsew", padx=2, pady=5)
        frame_options.grid(row=1, column=0,columnspan=2, sticky="nsew", padx=2, pady=5)
        frame_text.grid(row=2, column=0,columnspan=2, sticky="nsew", padx=2, pady=5)

   ##WIDGETS frame_input (0)
        ##labels frame_input
        lbl_title = new_lbl(frame_input, 'Bio-Paper Search', 18)

        ##textbox frame_input
        txt_file = tk.Text(frame_input, height=1, width=80, wrap=tk.CHAR)
        txt_file.insert(tk.END, text_file_path)

        ##buttons frame_input
        #btn_upload = tk.Button(frame_input, bg=btn_colour, fg=text_colour, text="upload pdf", command=lambda: open_pdf_file(txt_file))
        #btn_search = tk.Button(frame_input, bg=btn_colour, fg=text_colour, text="search", command=lambda: start_search())

        ##buttons frame_input
        btn_upload = new_btn(frame_input, "upload pdf")
        btn_upload.config( height = 1, width = 3 )
        btn_upload['command'] = lambda: open_pdf_file(txt_file)
        btn_search = new_btn(frame_input, "search")
        btn_search.config( height = 1, width = 3 )
        btn_search['command'] = lambda: start_search()
        ##grid layout of frame_input
        lbl_title.grid(row=0, column=0,columnspan=4, padx=5, pady=5)
        txt_file.grid(row=1,column=0,columnspan=4, padx=5, pady=5)
        btn_upload.grid(row=2, column=2, sticky="ew", padx=10, pady=5)
        btn_search.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

    ##WIDGETS frame_options (1)
        ##labels frame_options
        lbl_title2 = new_lbl(frame_options,'Options',14)
        lbl_clss = new_lbl(frame_options,'Classifier Options',10)
        lbl_text = new_lbl(frame_options,'Text Options',10)

        ##option variables
        textOption = tk.IntVar()
        classifOption = tk.IntVar()

        ##option group 1-classifier
        rb_ai = new_radio_btn(frame_options,'fast_ai',classifOption,1)
        rb_ai['command'] = lambda: set_classifier(classifOption, textOption)
        rb_bert = new_radio_btn(frame_options,'bert',classifOption,2)
        rb_bert['command'] = lambda: set_classifier(classifOption, textOption)
        rb_bow = new_radio_btn(frame_options,'bag of words',classifOption,3)
        rb_bow['command'] = lambda: set_classifier(classifOption, textOption)
        ##option group 2-text to use

        rb_ab = new_radio_btn(frame_options, 'abstract', textOption, 1)
        rb_ab['command'] = lambda: get_text_to_search(classifOption, textOption, txt_inText)
        rb_full = new_radio_btn(frame_options,'full text',textOption,2)
        rb_full['command'] = lambda: get_text_to_search(classifOption, textOption,txt_inText)

        ##grid layout of frame_options
        lbl_title2.grid(row=0, column=0,columnspan=2, padx=5, pady=5,sticky="nsew")

        lbl_clss.grid(row=1, column=0, padx=5, pady=5,sticky="nsew")
        rb_ai.grid(row=2, column=0, padx=5, pady=5,sticky="nsew")
        rb_bert.grid(row=3, column=0, padx=5, pady=5,sticky="nsew")
        rb_bow.grid(row=4, column=0, padx=5, pady=5,sticky="nsew")

        lbl_text.grid(row=1, column=1, padx=5, pady=5,sticky="nsew")
        rb_ab.grid(row=2, column=1, padx=5, pady=5,sticky="nsew")
        rb_full.grid(row=3, column=1, padx=5, pady=5,sticky="nsew")

     ##WIDGETS frame_text (2)
        ##labels frame_text
        lbl_title3 = new_lbl(frame_text,'Input Text',14)

        ##textbox for frame_text
        txt_inText = tk.Text(frame_text, borderwidth=3, relief="sunken",height=5,width=30, highlightbackground='gray36', highlightthickness = 1)
        txt_inText.config(undo=True, wrap='word')
        set_input('none loaded',txt_inText)

        ##scrollbar for textbox
        scroll = tk.Scrollbar(frame_text, command = txt_inText.yview)

        ##grid layout for frame_text
        lbl_title3.grid(row=0, column=0,padx=5, pady=5,sticky='nsew')
        txt_inText.grid(row=1, column=0,padx=5, pady=5,sticky='nsew')

        scroll.grid(row=1, column=1, sticky="nsew")
        txt_inText['yscrollcommand'] = scroll.set


if __name__ == '__main__':
    print('MAIN:','loading ui...')
    root = tk.Tk()
    root.geometry("600x700")
    root.configure(background=background_colour)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=10)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)


    img = tk.PhotoImage(file = paper_icon_path)

    app = Window(root)
    print('MAIN:','loaded ui')
    root.mainloop()
