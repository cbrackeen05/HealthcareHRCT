# ---
# Author: Cristina Ross
# ---

import spacy
from pdfminer.high_level import extract_text
import os
import pandas as pd


class NotesBackground():
    
    def __init__(self,corpus_path):
        self.word_dictionary = []
        self.noun_chunks = []
        self.word_count = {}
        self.word_distribution = {}
        self.total_words = 0  
        self.file_directory = corpus_path
        self.nlp = spacy.load("en_core_web_sm")
        return
    
    def countWords(self, wordlist):
        for word in wordlist:
            if word in self.word_count:
                self.word_count[word]=self.word_count[word]+wordlist.count(word)
            else:
                self.word_count[word]=1
        return

    def readPDFPages(self,path):
        all_words = self.word_dictionary
        
        raw_text = extract_text(path)
        doc = self.nlp(raw_text)
           
        all_words= all_words+[t.text.lower() for t in doc 
                            if t.is_punct ==False and t.is_space ==False]
            # noun_chunks = noun_chunks + [nc for nc in doc.noun_chunks]
        
        self.countWords(all_words.copy())
        self.word_dictionary = list(set(all_words))
        return

    def calcWordDistribution(self):
        for (key,val) in self.word_count.items():
            self.word_distribution[key] = val/self.total_words
        return
    
    def build_distribution(self):
        for filename in os.listdir(self.file_directory):
            if 'pdf' not in filename:
                continue
            self.readPDFPages(self.file_directory+filename)
            
        for item in self.word_count.items():
            self.total_words = self.total_words+item[1]
            
        self.calcWordDistribution()
        return


# +
class NotesTopicModel():
    
    def __init__(self,document_path):
        self.word_dictionary = []
        self.noun_chunks = []
        self.word_distribution = {}
        self.total_words = 0  
        self.doucment_word_counts = pd.DataFrame([])
        self.nlp = spacy.load("en_core_web_sm")
        self.files_path = document_path
        self.inverse_doc_freq = {}
         
    def countWords(self,wordlist):
        word_count = {}
        for word in wordlist:
            if word in word_count:
                word_count[word]=word_count[word]+wordlist.count(word)
            else:
                word_count[word]=1
        return word_count
    
    def processDocument(self,docPath,docIDX):
        word_dic = []
        raw_text = extract_text(docPath)
        doc = self.nlp(raw_text)
            
        word_dic= word_dic+[t.text.lower() for t in doc 
                            if t.is_punct ==False and t.is_space ==False and t.is_alpha==True]
        
        countedWords = self.countWords(word_dic.copy())
        word_dic = list(set(word_dic))
        self.word_dictionary = self.word_dictionary+word_dic
        self.word_dictionary = list(set(self.word_dictionary))
        
        doc_word_counts = pd.DataFrame(countedWords,index=[docIDX])
        return doc_word_counts

    def flipThruFiles(self):
        fileidx = 1
        for filename in os.listdir(self.files_path):
            if 'pdf' not in filename:
                continue
            filepath = self.files_path+filename
            doc_word_counts = self.processDocument(filepath,fileidx)
            self.doucment_word_counts = pd.concat([self.doucment_word_counts,doc_word_counts],axis=0)
            # fileidx+=1
            # if fileidx==75:
            #     break
        return
    
    def calcTopicWordDistribution(self):
        topicWordCounts = self.doucment_word_counts.sum()
        allWordCounts = topicWordCounts.sum()
        topicWordCounts = topicWordCounts/allWordCounts
        
        self.word_distribution = topicWordCounts.to_dict()
        return 
    
    def calcTopicIDF(self):
        doucment_word_binary = self.doucment_word_counts.copy().ge(1).astype(int)
        sepsis_idf = doucment_word_binary.sum()
        num_docs = doucment_word_binary.index.max()

        self.inverse_doc_freq=(num_docs/sepsis_idf).to_dict()
        return
    
    def build_distribution(self):
        self.flipThruFiles()
        self.calcTopicWordDistribution()
        self.calcTopicIDF()



# -

class processedNote():

    def __init__(self,single_document_path):
        self.word_dictionary = []
        self.noun_chunks = []
        self.word_distribution = {}
        self.total_words = 0  
        self.doucment_word_counts = pd.DataFrame([])
        self.nlp = spacy.load("en_core_web_sm")
        self.file_path = single_document_path
        self.inverse_doc_freq = {}
        
    def countWords(self,wordlist):
        word_count = {}
        for word in wordlist:
            if word in word_count:
                word_count[word]=word_count[word]+wordlist.count(word)
            else:
                word_count[word]=1
        return word_count
    
    def processDocument(self):
        word_dic = []
        raw_text = extract_text(self.file_path)
        doc = self.nlp(raw_text)
            
        word_dic= word_dic+[t.text.lower() for t in doc 
                                  if t.is_punct ==False and t.is_space ==False and t.is_alpha==True]
        
        countedWords = self.countWords(word_dic.copy())
        word_dic = list(set(word_dic))
        self.word_dictionary = self.word_dictionary+word_dic
        self.word_dictionary = list(set(self.word_dictionary))
        self.doucment_word_counts = pd.DataFrame(countedWords, index=[0])
        
        return 
        
    def calcTopicWordDistribution(self):
        topicWordCounts = self.doucment_word_counts.sum()
        allWordCounts = topicWordCounts.sum()
        topicWordCounts = topicWordCounts/allWordCounts
        
        self.word_distribution = topicWordCounts.to_dict()
        return 
    
    def build_distribution(self):
        self.processDocument()
        self.calcTopicWordDistribution()

