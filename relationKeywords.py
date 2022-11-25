#!/usr/bin/env python
# coding: utf-8


from pykospacing import Spacing
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import operator

#### itxTools 
from itxTools.preProcess import *



class RelationKeywords:
    def __init__(self, analysisDataList):
        
        self.spacing = Spacing()        
        self.relationKeywordDict = dict()
        self.word_count_dict = dict()
        self.targetData = ""
        
        self.makeRelationKeyword(analysisDataList)
        self.makeCounterKeywords()
    
    
    def getRelationKeywordDict(self):
        return self.relationKeywordDict
    
    def getWordCountDict(self):
        return self.word_count_dict        
    
    
    
    def setRelationKeyword(self,word1, word2):
        if word1 in self.relationKeywordDict:
            detailKeywordList = self.relationKeywordDict[word1]
            if word2 not in detailKeywordList:
                detailKeywordList.append(word2)
        else:
            detailKeywordList = []
            detailKeywordList.append(word2)
            self.relationKeywordDict[word1] = detailKeywordList
    
    def makeRelationKeyword(self, analysisDataList):
        for analysisData in tqdm(analysisDataList):    
            file_name = analysisData['fileName']
            customer_sentence = analysisData['customer_pre_sentences']
            customer_token = analysisData['customer_token']
            for i in range(len(customer_sentence)):
                original_sentence = customer_sentence[i]
                spacing_sentence = self.spacing(original_sentence.replace(" ",""))
                utaggerStr = pos_str(spacing_sentence)
                targetKeyword = getKeywordsPOS(utaggerStr,["NNG","NNP"])
                self.targetData = self.targetData + targetKeyword + " "
                words = targetKeyword.split(" ")
                for i in range(len(words)):
                    if i < len(words)-1 :
                        word1 = words[i]
                        word2 = words[i+1]
                        if len(word1) > 1 and len(word2) > 1 and word1 != word2:
                            self.setRelationKeyword(word1, word2)        
        self.targetData = self.targetData.strip()
    
    def makeCounterKeywords(self):
        fit_target_data = np.array([self.targetData])
        transformer = CountVectorizer()
        bow_vect = transformer.fit_transform(fit_target_data)
        word_list = transformer.get_feature_names()
        count_list = bow_vect.toarray().sum(axis=0) 
        self.word_count_dict = dict(zip(word_list, count_list)) 
    
    def getRelationWords(self,keyword):
        word_list = []
        if keyword in self.relationKeywordDict:
            word_list = self.relationKeywordDict[keyword]
            word_dict = dict()
            for word in word_list:
                word_dict[word] = self.word_count_dict[word]
            word_list = sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True) 
        return word_list

