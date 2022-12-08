#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 20:35:45 2022

@author: Cristina Ross
"""


import os
import numpy as np
import pandas as pd
import pickle

from hrct_distribution import NotesTopicModel, NotesBackground, processedNote



class HRCTmodel():
    def __init__(self, positive_path, negative_path, background_path=None):
        if background_path != None:
            ## Build Background word_distribution
            self.background_distribution = NotesBackground(background_path)
            self.background_distribution.build_distribution()
        
        ## Build Two Topic Models
        self.positive_distribution = NotesTopicModel(positive_path)
        self.positive_distribution.build_distribution()
        self.negative_distribution = NotesTopicModel(negative_path)
        self.negative_distribution.build_distribution()
        self.scored_docs = []

    def cosineSim(self,testWords,ABWords):
        AB=0
        A=0
        B=0
        for wd in testWords.word_dictionary:
            if wd in ABWords.word_distribution.keys():
                AB+=testWords.word_distribution[wd]*ABWords.word_distribution[wd]
                A+=testWords.word_distribution[wd]**2
                B+=ABWords.word_distribution[wd]**2
        return AB/(np.sqrt(A)*np.sqrt(B))
    
    def calculateSimilarity(self,posWords,negWords,testWords):
        posSim = self.cosineSim(testWords,posWords)
        negSim = self.cosineSim(testWords,negWords)
        if posSim>=negSim:
            return 1
        else:
            return 0
       
    def score(self,documents_path,save_file=True,save_file_location=None):
        scores = []
        for filename in os.listdir(documents_path):
            if 'pdf' not in filename:
                continue
            docPath = documents_path+filename
            S1 = processedNote(docPath)
            S1.build_distribution()
            if len(S1.word_dictionary) == 0:
                print(filename)
            scores.append([filename,self.calculateSimilarity(self.positive_distribution,
                                                            self.negative_distribution,
                                                            S1)])
            del S1
        self.scored_docs = scores
       
        if save_file == True:
            scores_df = pd.DataFrame(self.scored_docs)
            if save_file_location == None:
                scores_df.to_csv(documents_path+'scored_documents.csv')
            else:
                scores_df.to_csv(save_file_location+'scored_documents.csv')


