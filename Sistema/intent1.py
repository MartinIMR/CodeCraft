# Python program to read
import os
import re
import sqlite3 
import nltk
import num2words as nw

def get_data():
  conn = sqlite3.connect("minhouse.db") #Connect to database
  cr = conn.cursor() #Get cursor
  dataset = [ tupla[0] for tupla in cr.execute("SELECT descripcion FROM sjug_juego")] #Obtain the string for each tuple from the query
  conn.close()
  return dataset 

def lower_case(data):
  minus = [desc.lower() for desc in data] #A list of strings
  return minus

#Version using nltk
def tokenize1(texts):
  data = []  #List to keep each string coverted to list 
  for desc in texts:
    tokens = nltk.word_tokenize(desc,"spanish")
    data.append(tokens) 
  return data

def remove_punctuation(texts):
  data = []
  for desc in texts:
    data.append(re.sub(r'[^\w\s]','', desc))
  return data

def single_character(texts):
  data = []
  for desc in texts: ## Could it be for 2 characters?
    no_single = [word for word in desc if len(word) > 2]
    data.append(no_single)
  return data

def convert_number(texts):
  data = []
  for desc in texts:
    data.append([nw.num2words(word,lang="es") if word.isnumeric() \
    		 else word for word in desc])
  return data

def stop_words(texts):
  from nltk.corpus import stopwords
  data = []
  sw = stopwords.words("spanish")
  for desc in texts:
    data.append([word for word in desc if word not in sw])
  return data

def lemmatize(texts):
  from pickle import load
  dt = open("extern/lemmas.pkl","rb")
  lemmas = load(dt)
  dt.close()
  lemmatized = []
  for desc in texts:
    lemmatized.append([lemmas[word] if word in lemmas else \
		  word[:-2] for word in desc])
  return lemmatized

def tag_sentences(texts):
  from pickle import load
  dt = open("extern/tagger.pkl","rb")
  tagger = load(dt)
  dt.close()
  tagged = []
  for desc in texts:
    desc_tagged = tagger.tag(desc) #List of tuples (word,tag) for each description
    desc_tagged = [pair[0]+" "+pair[1][0] for pair in desc_tagged] #Simple 'string tag' instead of a tuple
    desc_tagged = [wordtag.lower() for wordtag in desc_tagged] #Lower each word+tag
    tagged.append(desc_tagged)
  return tagged


def preprocess(data):
    data = lower_case(data) #Lowercase each string
    data = remove_punctuation(data) #Remove dots and punctuation on each string
    data = tokenize1(data) #Convert each string to a list of words
    data = convert_number(data) #Convert numbers to its word's representation
    data = single_character(data) #Remove words of len 1
    data = stop_words(data) #Remove stopwords
    data = tag_sentences(data)
    data = lemmatize(data) #Lemmatize the data
    for desc in data:
      print(desc)

if __name__ == "__main__":
  texts = get_data()
  min_texts = texts[0:11]
  preprocess(min_texts)
