

import tkinter
import pandas as pd
import numpy
import string
import os
import pdfplumber
import re
import unicodedata
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from win32com import client
import spacy
import sys,fitz
import en_core_web_sm
import en_core_web_lg
import en_core_web_trf
from gensim.parsing.preprocessing import remove_stopwords
import shutil
from collections import Counter


# In[ ]:

# In[ ]:


#Coversion of doc to pdf

#Count of files
def n_files(directory):
    total = 0
    for file in os.listdir(directory):
        if (file.endswith('.doc') or file.endswith('.docx') or file.endswith('.pdf')):
            total += 1
    return total
       





#List of all the values respect to the key
def getList(data):
    l=[]
    for d in data:
        d=d.lower()
        d = d.replace(","," ")
        d=d.replace(".","")
        d=d.replace("&"," and ")
        d.translate(str.maketrans(' ',' ',string.punctuation))
        d=re.sub(' +',' ',d)
        l.append(d.strip())     
    return l 




#reading and extracting pdf content 
def pdfExtract(file):
    doc=fitz.open(file)
    text=""
    for page in doc:
        text+=page.getText()
    return text


# In[ ]:


#Function to generate all entities using en_core_web_trf
def ModelApply(content):
    #enc_core_web_trf separation
    nlp = spacy.load("en_core_web_trf")
    doc = nlp(content)
    text = [ent.text for ent in doc.ents]
    entity = [ent.label_ for ent in doc.ents]
    data = Counter(zip(entity))
    unique_entity= list(data.keys())
    unique_entity=[x[0] for x in unique_entity]  
    d={}
    for val in unique_entity:
        d[val]=[]
    for key,val in dict(zip(text, entity)).items():
        if val in unique_entity:
            d[val].append(key)
            
    #en_core_web_lg separation
    nlp2 = spacy.load("en_core_web_lg")
    doc = nlp2(content)
    for ent in doc.ents:
        if(ent.label_ not in d.keys()):
            d[ent.label_]=[]
        if(ent.text not in d[ent.label_]):
            d[ent.label_].append(ent.text)
    
    #en_core_web_sm separation
    nlp3 = spacy.load("en_core_web_sm")
    doc = nlp3(content)
    for ent in doc.ents:
        if(ent.label_ not in d.keys()):
            d[ent.label_]=[]
        if(ent.text not in d[ent.label_]):
            d[ent.label_].append(ent.text)
    
    return d 




#USing  en_core_web_trf and en_core_web_lg and en_core_web_sm

#For fetching ORG list and cleaning the strings
#returns ORG list
def ORG(file):
    file= file.replace("-"," ")
    file  = file.replace("&"," and ")
    file = re.sub(" +"," ",file)
    dictionary={"Vishwavidyalaya":"University","Mahavidyalaya":"University","GCOE":"Government College of Engineering","COET":"College of Engineering and Technology"}
    for i in dictionary.keys():
        file = file.replace(i,dictionary[i])
        
    #fetching data specifically 'ORG'
    org=ModelApply(file)
    org=org['ORG']
    
    #replacing abbreviations 
    abbr ={"ltd":"limited","pvt":"private","govt":"government","inc":"incorporation","inst":"institute","engg":"engineering","tech":"technology","clg":"college"}
    dictionary={}
    for i in range(len(org)):
        org[i]=org[i].translate(str.maketrans(' ',' ',string.punctuation))
        org[i]=re.sub(r'[^\w\s]', ' ', org[i])
        org[i] =org[i].replace("\n"," ")
        org[i]=org[i].lower()
        newpat =""
        for word in org[i].split():
            if word in abbr:
                newpat+=abbr[word]+" "
            else:
                newpat+=word+" "
        org[i]=newpat.strip() 
    if '' in org:
        org.remove('')
    return org


# In[ ]:


#cleaning function for the acronyms
def clean(list):
    l=[]
    for i in list:
        i=i.replace('.',' ')
        i=i.lower()
        if('it' in i):
            i.replace('it', 'information technology')
        l.append(i)
    return l







