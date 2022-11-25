#!/usr/bin/env python
# coding: utf-8

import requests
import json
import sys
import os
import pickle 

from tqdm import tqdm 

from kss import split_sentences
from pykospacing import Spacing

# UTagger load
global_session = requests.Session()

def pos_str(sentence,pos_str):
    """pos tagging"""    
    
    sentences=[sentence]
    headers = {'Content-type': 'application/json'}
    data = {'text': sentences,
            'tagger': 'utagger', #utagger, mecab, twitter
            'type' : 'line',
            'withEng':False}
    
    pos = ''
    try:
        response = global_session.post(pos_url, json=data, headers=headers)
        if (response.status_code == requests.codes.ok):
            pos = " /DEL"
            if len(json.loads(response.text)['result']) != 0 :
                pos = json.loads(response.text)['result'][0]
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(-1)
        
    return pos.replace("+", " ")

class PreprocessResult:
    
    def __init__(self, origin_sentences, csr_sentences, customer_sentences,pos_str, ic_type=True):
        
        self.spacing = Spacing()
        self.pos_str = pos_str
        
        self.origin_sentences = origin_sentences
        self.csr_sentences = csr_sentences
        self.customer_sentences = customer_sentences
        self.origin_pre_sentences, self.origin_token = self.preprocessing_sentences(origin_sentences, ic_type)
        self.csr_pre_sentences, self.csr_token = self.preprocessing_sentences(csr_sentences, ic_type)
        self.customer_pre_sentences,self.customer_token = self.preprocessing_sentences(customer_sentences, ic_type)

    
    def preprocessing_sentences(self, sentences, ic_type=True):
        after_sentence = ""
        after_token = ""
        splitSentences = split_sentences(sentences)
        for sent in splitSentences:
            sent = self.spacing(sent)            
            for token in sent.split(' '):
                token_info = pos_str(token,self.pos_str)
                if ic_type :
                    if token_info.find('/IC') > 0:
                        continue
                after_sentence = after_sentence + token + " "
                after_token = after_token + token_info + " "
        return after_sentence, after_token
  
    def getOriginSentences(self):
        return self.origin_sentences    
    def getOriginPreSentences(self):
        return self.origin_pre_sentences    
    def getOriginToken(self):
        return self.origin_token
    
    def getCsrSentences(self):
        return self.csr_sentences
    def getCsrPreSentences(self):
        return self.csr_pre_sentences
    def getCsrToken(self):
        return self.csr_token
    
    def getCustomerSentences(self):
        return self.customer_sentences
    def getCustomerPreSentences(self):
        return self.customer_pre_sentences
    def getCustomerToken(self):
        return self.customer_token
    
    def getDictData(self):
        data = dict()
        # csr + costomer
        data['origin_sentence'] = self.origin_sentences
        data['origin_pre_sentence'] = self.origin_pre_sentences
        data['origin_token'] = self.origin_token
        
        # csr
        data['csr_sentences'] = self.csr_sentences
        data['csr_pre_sentences'] = self.csr_pre_sentences
        data['csr_token'] = self.csr_token
        
        # costomer
        data['customer_sentences'] = self.customer_sentences
        data['customer_pre_sentences'] = self.customer_pre_sentences
        data['customer_token'] = self.customer_token
        
        return data
        
class PreprocessResult_list:
    
    def __init__(self, origin_sentences, csr_sentences, customer_sentences,pos_str, ic_type=True):
        
        self.spacing = Spacing()
        self.pos_str = pos_str
        
        self.origin_sentences = origin_sentences
        self.csr_sentences = csr_sentences
        self.customer_sentences = customer_sentences
        self.origin_pre_sentences, self.origin_token = self.preprocessing_sentences(origin_sentences, ic_type)
        self.csr_pre_sentences, self.csr_token = self.preprocessing_sentences(csr_sentences, ic_type)
        self.customer_pre_sentences,self.customer_token = self.preprocessing_sentences(customer_sentences, ic_type)

    
    def preprocessing_sentences(self, sentences, ic_type=True):
        after_sentence = []
        after_token = []
        splitSentences = split_sentences(sentences)
        for sent in splitSentences:
            sent = self.spacing(sent)   
            temp_sentence = ""
            temp_token = ""
            for token in sent.split(' '):
                token_info = pos_str(token,pos_str)
                if ic_type :
                    if token_info.find('/IC') > 0:
                        continue
                temp_sentence = temp_sentence + token + " "
                temp_token = temp_token + token_info + " "
            if(len(temp_sentence.strip())>0):
                after_sentence.append(temp_sentence.strip())
            if(len(temp_token.strip())>0):
                after_token.append(temp_token.strip())
        return after_sentence, after_token
  
    def getOriginSentences(self):
        return self.origin_sentences    
    def getOriginPreSentences(self):
        return self.origin_pre_sentences    
    def getOriginToken(self):
        return self.origin_token
    
    def getCsrSentences(self):
        return self.csr_sentences
    def getCsrPreSentences(self):
        return self.csr_pre_sentences
    def getCsrToken(self):
        return self.csr_token
    
    def getCustomerSentences(self):
        return self.customer_sentences
    def getCustomerPreSentences(self):
        return self.customer_pre_sentences
    def getCustomerToken(self):
        return self.customer_token
    
    def getDictData(self):
        data = dict()
        # csr + costomer
        data['origin_sentence'] = self.origin_sentences
        data['origin_pre_sentence'] = self.origin_pre_sentences
        data['origin_token'] = self.origin_token
        
        # csr
        data['csr_sentences'] = self.csr_sentences
        data['csr_pre_sentences'] = self.csr_pre_sentences
        data['csr_token'] = self.csr_token
        
        # costomer
        data['customer_sentences'] = self.customer_sentences
        data['customer_pre_sentences'] = self.customer_pre_sentences
        data['customer_token'] = self.customer_token
        
        return data


# data load
def load_data(path):
    total_sentences = ""
    rx_sentences = ""
    tx_sentences = ""
    with open(path) as file:
        for line in file:
            try:
                sentence_type = line.split('=')[0]
                sentence = line.split('=')[1]
                if len(line) >3 :
                    total_sentences = total_sentences + sentence
                    if sentence_type == 'C':
                        rx_sentences = rx_sentences+sentence
                    elif sentence_type == 'A':
                        tx_sentences = tx_sentences+sentence
            except Exception as e:
                print(str(e))
                print("line : ",line)
                print("path : ", path)
    return total_sentences, rx_sentences, tx_sentences


def load_folder(path, ic_type=True):
    analysisDataList = []
    for (root, directories, files) in os.walk(path):
        for file in tqdm(files):
            total_sentences, rx_sentences, tx_sentences = load_data(os.path.join(path,file))
            preprocessResult = PreprocessResult(total_sentences, tx_sentences, rx_sentences,ic_type)
            analysisDataDict = preprocessResult.getDictData()
            analysisDataDict['fileName'] = file
            analysisDataDict['filePath'] = os.path.join(path,file)
            analysisDataList.append(analysisDataDict)
    return analysisDataList

def load_folder_list(path, ic_type=True):
    analysisDataList = []
    for (root, directories, files) in os.walk(path):
        for file in tqdm(files):
            total_sentences, rx_sentences, tx_sentences = load_data(os.path.join(path,file))
            preprocessResult = PreprocessResult_list(total_sentences, tx_sentences, rx_sentences,ic_type)
            analysisDataDict = preprocessResult.getDictData()
            analysisDataDict['fileName'] = file
            analysisDataDict['filePath'] = os.path.join(path,file)
            analysisDataList.append(analysisDataDict)
    return analysisDataList


def getKeywordsPOS(keywords,pos_type=['NNG']):
    returnKeywords = ""
    for keyword in keywords.split(" "):
        if keyword.find("/") > -1:
            token = keyword.split("/")[0]
            pos = keyword.split("/")[1]
            if pos in pos_type:
                returnKeywords = returnKeywords + token + " "
    return returnKeywords.strip()
