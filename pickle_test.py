# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 10:42:45 2022

@author: Cristina Ross
"""

import pickle
import pathlib
import os
import pandas as pd

os.chdir('/Users/Maria/Downloads/sepsis_model_linux/')
from sepsis_model import sepsisHRCTmodel

with open ('sepsis_model_linux.pickle', 'rb') as handle:
    sepsis = pickle.load(handle)

#Check performance
sepsis_scores = pd.read_csv(
    "/Users/Maria/Desktop/NLPmodel/scored_documents.csv")
sepsis_scores.columns = ['OldIndex','Filename','Prediction']
sepsis_scores.loc[:,['Truth']] = sepsis_scores.Filename.apply(lambda x: 0 if 'nonsep' in x else 1)
sepsis_scores = sepsis_scores.loc[:,['Truth','Prediction']]

TP = sepsis_scores.loc[(sepsis_scores.Truth==1)&(sepsis_scores.Prediction==1),:].Prediction.count()
FN = sepsis_scores.loc[(sepsis_scores.Truth==1)&(sepsis_scores.Prediction==0),:].Prediction.count()
FP = sepsis_scores.loc[(sepsis_scores.Truth==0)&(sepsis_scores.Prediction==1),:].Prediction.count()
TN = sepsis_scores.loc[(sepsis_scores.Truth==0)&(sepsis_scores.Prediction==0),:].Prediction.count()

precision = TP/(TP+FP)
recall = TP/(TP+FN)
accuracy = (TP+TN)/(TP+FP+FN+TN)
f1 = (2*precision*recall)/(precision+recall)

print("Precision: {}\nRecall: {}\nAccuracy: {}\nF1-score: {}".format(
    precision,recall,accuracy,f1))
