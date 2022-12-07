#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 20:35:45 2022

@author: Maria
"""

from hrct_model import HRCTmodel
from pdfminer.high_level import extract_text
import os
import pandas as pd

#Create gout model
pos_dir = "/Users/Maria/Downloads/sepsis_model_linux/TestDocuments/positive/"
neg_dir = "/Users/Maria/Downloads/sepsis_model_linux/TestDocuments/negative/"

gout_model = HRCTmodel(pos_dir,neg_dir)

#Score documents using gout model
score_dir = "/Users/Maria/Downloads/sepsis_model_linux/TestDocuments/to_score/"

gout_model.score(score_dir,True)

#Check performance
gout_scores = pd.read_csv(
    "/Users/Maria/Downloads/sepsis_model_linux/TestDocuments/to_score/scored_documents.csv")
gout_scores.columns = ['OldIndex','Filename','Prediction']
gout_scores.loc[:,['Truth']] = gout_scores.Filename.apply(lambda x: 1 if 'Y' in x else 0)
gout_scores = gout_scores.loc[:,['Truth','Prediction']]

TP = gout_scores.loc[(gout_scores.Truth==1)&(gout_scores.Prediction==1),:].Prediction.count()
FN = gout_scores.loc[(gout_scores.Truth==1)&(gout_scores.Prediction==0),:].Prediction.count()
FP = gout_scores.loc[(gout_scores.Truth==0)&(gout_scores.Prediction==1),:].Prediction.count()
TN = gout_scores.loc[(gout_scores.Truth==0)&(gout_scores.Prediction==0),:].Prediction.count()

precision = TP/(TP+FP)
recall = TP/(TP+FN)
accuracy = (TP+TN)/(TP+FP+FN+TN)
f1 = (2*precision*recall)/(precision+recall)

print("Precision: {}\nRecall: {}\nAccuracy: {}\nF1-score: {}".format(
    precision,recall,accuracy,f1))
