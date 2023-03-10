# -*- coding: utf-8 -*-
"""Copy of YAKE-Ext Summary.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xzO1zPXcTAfKa4MzVWLwzwOoXeesWPzR
"""

pip install yake rouge

import nltk
nltk.download('stopwords')
nltk.download('punkt')

text = "On Friday, Business Insider reported that Microsoft has held talks to buy GitHub — a $2 billion startup that claims 24 million software developers as users. It's not immediately clear what will come of these talks. Microsoft declined to comment, but you can read the full Business Insider report here. While we wait for further word on the future of GitHub, one thing is very clear: It would make perfect sense for Microsoft to buy the startup. If the stars align, and GitHub is integrated intelligently into Microsoft's products, it could give the company a big edge against Amazon Web Services, the leading player in the fast-growing cloud market. Just to catch you up: GitHub is an online service that allows developers to host their software projects. From there, anyone from all over the world can download those projects and submit their own improvements. That functionality has made GitHub the center of the open source software. development world."
print(text)

# import yake

# kw_extractor = yake.KeywordExtractor()
# keywords = kw_extractor.extract_keywords(text)

# for kw in keywords:
# 	print(kw)

# import yake

# language = "en"
# max_ngram_size = 1
# #deduplication_threshold = 0.9
# #deduplication_algo = 'seqm'
# #windowSize = 1
# #numOfKeywords = 20

# custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, features=None)
# keywords = custom_kw_extractor.extract_keywords(text)

# for kw in keywords:
#     print(kw)

import nltk
import os
import re
import math
import yake
import pandas as pd
import numpy as np
import operator
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
Stopwords = set(stopwords.words('english'))
wordlemmatizer = WordNetLemmatizer()

"""#Retain numbers and see"""

def remove_special_characters(text):
    regex = r'[^a-zA-Z0-9\s]'
    text = re.sub(regex,'',text)
    return text
    
def word_importance(text):
  language = "en"
  max_ngram_size = 1
  numOfKeywords = 40
  custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, top = numOfKeywords,features=None)
  keywords = custom_kw_extractor.extract_keywords(text)
  word_imp = {}
  for k in keywords:
    word_imp[k[0]] = 1/k[1]

  return word_imp
  
def yake_score(word_imp,word,sentence):

  if word_imp.get(word)==None:
    score = 0.001

  else:
    score = word_imp[word]

  return score

def sentence_importance(sentence,word_imp):
     sentence_score = 0
     sentence = remove_special_characters(str(sentence))
     sentence = re.sub(r'\d+', '', sentence)
     #print(sentence)
     #pos_tagged_sentence = []
     #no_of_sentences = len(sentences)
     #pos_tagged_sentence = pos_tagging(sentence)
     for word in sentence.split():
         if word.lower() not in Stopwords and word not in Stopwords and len(word)>1:
             #word = word.lower() 
             #word = wordlemmatizer.lemmatize(word)
             #print(word)
             sentence_score = sentence_score + yake_score(word_imp,word,sentence)
             #print(sentence_score)

     return sentence_score

def get_summary(text):

    # file = 'input.txt'
    # file = open(file , 'r')
    # text = file.read()
    tokenized_sentence = sent_tokenize(text)
    #print(tokenized_sentence)
    text = remove_special_characters(str(text))
    text = re.sub(r'\d+', '', text)
    tokenized_words_with_stopwords = word_tokenize(text)
    tokenized_words = [word for word in tokenized_words_with_stopwords if word not in Stopwords]
    #tokenized_words = [word for word in tokenized_words if len(word) > 1]
    #tokenized_words = [word.lower() for word in tokenized_words]

    word_score = word_importance(text)
    no_of_sentences = 4
    sentence_with_importance = {}
    c = 1
    for sent in tokenized_sentence:
      #print(sent)
      sentenceimp =  sentence_importance(sent,word_score)
      #print(sentenceimp)
      sentence_with_importance[c] = sentenceimp
      #print(sentence_with_importance)
      c = c+1

    sentence_with_importance =  sorted(sentence_with_importance.items(), key=operator.itemgetter(1),reverse=True)
    cnt = 0
    summary = []
    sentence_no = []
    for word_prob in sentence_with_importance:
      if cnt < no_of_sentences:
        sentence_no.append(word_prob[0])
        cnt = cnt+1
      else:
        break
            
    sentence_no.sort()

    cnt = 1
    for sentence in tokenized_sentence:
        if cnt in sentence_no:
            summary.append(sentence)
        cnt = cnt+1

    summary = " ".join(summary)
    #print("\n")
    #print("Summary:")
    #print(summary)

    return summary
    # outF = open('summary.txt',"w")
    # outF.write(summary)

# get_summary(text,2)

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv('/content/drive/MyDrive/CNN DM (Summarisation)/test.csv')
df

#df['article'][0]

#get_summary(df['article'][0] ,3)

len_highlights = [] 
len_highlights = [len(sent_tokenize(df['highlights'][i])) for i in range(len(df)) ]

df['len_highlights'] = len_highlights

df

from rouge import Rouge
rouge = Rouge()

rouge1,rouge2,rougeL = [],[],[]

for i in range(1000):

  hypothesis = get_summary(df['article'][i])
  scores = rouge.get_scores(hypothesis, df['highlights'][i])
  #print(scores)
  print(i)

  rouge1.append(scores[0]['rouge-1']['f'])
  rouge2.append(scores[0]['rouge-2']['f'])
  rougeL.append(scores[0]['rouge-l']['f'])

print(len(rouge1),len(rouge2),len(rougeL))

print(sum(rouge1)/len(rouge1),sum(rouge2)/len(rouge2),sum(rougeL)/len(rougeL))

