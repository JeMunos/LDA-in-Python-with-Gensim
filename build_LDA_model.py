#!/usr/bin/env pypy
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import csv
import re
import string
import stopwords

# Use this to store our data post processing
per_row_data = []
description = []
#  segments a document into its atomic elements.
tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = stopwords.get_stopwords("en")
stop_words = [x.encode('utf-8') for x in en_stop]

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# Read in the CSV data 
def read_csv_data(filename):
	with open(filename, 'rb') as f:
		reader = csv.reader(f)
		doc_set = list(reader)
		return doc_set

# This is example data 
def example_data():
	# example code for creating our list of documents    
	# create sample documents
	doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
	doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
	doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
	doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
	doc_e = "Health professionals say that brocolli is good for your health." 

	# compile sample documents into a list
	doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]
	return doc_set


#remove any odd non ascii characters, remove all punctuation, remove any odd spacing
def clean_data(data_set):
	clean_list = []
	for item in data_set:
		printable = set(string.printable)
		temp=re.sub(' +',' ', item[1])
		cleaned = temp.translate(None, string.punctuation)
		cleaned = ''.join([i if ord(i) < 128 else ' ' for i in cleaned])
		cleaned = [item[0],cleaned]
		clean_list.append(cleaned)
	return clean_list


# process the data
def lda_per_function(doc_set):
	# list for tokenized documents in loop
	texts = []
	# loop through document list
	for i in doc_set:
		# clean and tokenize document string
		raw = i.lower()
		tokens = tokenizer.tokenize(raw)
		# remove stop words from tokens
		stopped_tokens = [i for i in tokens if not i in stop_words]
		# stem tokens
		stemmed_tokens = [p_stemmer.stem(i).encode('utf-8') for i in stopped_tokens]
		# add tokens to list
		texts.append(stemmed_tokens)
	# turn our tokenized documents into a id <-> term dictionary
	dictionary = corpora.Dictionary(texts)
	# convert tokenized documents into a document-term matrix
	corpus = [dictionary.doc2bow(text) for text in texts]
	# generate LDA model
	lda_model = gensim.models.ldamodel.LdaModel(corpus, num_topics=200, id2word = dictionary, passes=200)
	return(lda_model.print_topics(num_topics=200, num_words=5))

### Main Calls ###

# File name and location that we want to process:
filename = 'longDescriptionFunc.csv'
print("File we are going to process "+filename)
output_filename = "output/full_set_t200_w5_p200.csv"
print("File we are going to write to "+output_filename)
print("---------------------------------------------------")
# Read the data from the file
doc_set = read_csv_data(filename)
print("First we will clean the data: remove non ASCII char, punctuation, and any odd spacing")
clean_doc_set = clean_data(doc_set)
print("data has been cleaned")
print("---------------------------------------------------")
print("Removing any function labels and creating a list of the description column to pass to LDA algorithm")
for row in clean_doc_set:
	description.append(row[1])
print("---------------------------------------------------")
print("Passing data to LDA and Prepping File Output")
with open(output_filename, "w") as f:
	writer = csv.writer(f, lineterminator='\n')
	writer.writerows(lda_per_function(description))

