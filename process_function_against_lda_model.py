#!/usr/bin/env pypy
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim.models import LdaMulticore
from gensim.models import LdaModel
from gensim import corpora
import csv
import re
import string
import stopwords
import logging


# Set up some basic logging so we know how long things are taking us
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Use this to store our data post processing
function_names = []
per_row_data = []
description = []
doc_lda = []
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


# remove any odd non ascii characters, remove all punctuation, remove any odd spacing
def clean_data(data_set):
	clean_list = []
	for item in data_set:
		printable = set(string.printable)
		temp = re.sub(' +',' ', item[1])
		cleaned = temp.translate(None, string.punctuation)
		cleaned = ''.join([i if ord(i) < 128 else ' ' for i in cleaned])
		cleaned = [item[0],cleaned]
		clean_list.append(cleaned)
	return clean_list


# process the data
def prep_data(doc_set):
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
	return texts


def gen_corpora(texts):
	# turn our tokenized documents into a id <-> term dictionary
	return corpora.Dictionary(texts)


def corp_data(dict_data, texts):
	# convert tokenized documents into a document-term matrix
	return [dict_data.doc2bow(text) for text in texts]


def lda_model(token_docs, dict_docs):
	# return LdaMulticore(token_docs, num_topics=200, id2word=dict_docs, passes=150, workers=3, minimum_probability=0)
	# I had issues with LdaMulticore hanging during processing, so if that happens switch to using single thread mode
	# by uncommenting the line below this comment, and commenting the one above.
	return LdaModel(token_docs, num_topics=200, id2word=dict_docs, passes=200, minimum_probability=0)

def get_function_names(documents):
	return [i[0] for i in doc_set]


def format_output_lists(function_names, doc_lda):
	return(zip(function_names, doc_lda))

### Main Calls ###

# File name and location that we want to process:
filename = 'longDescriptionFunc.csv'
print("File we are going to process "+filename)
output_filename = "output/full_set_t200_p200.csv"
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

text_data = prep_data(description)
dict_docs = gen_corpora(text_data)
token_docs = corp_data(dict_docs, text_data)
model = lda_model(token_docs, dict_docs)

print("Model is trained and saved to variable. Attempting to evaluate new document")
for item in token_docs:
	doc_lda.append(model[item])

print("getting function headers to append to the output data")
#function_names = get_function_names(doc_set)

#final_data = format_output_lists(function_names, doc_lda)

print("Writing model to file 200 topics, 5 words per topic")
with open("model_alpha.csv", "w") as f:
	writer = csv.writer(f, lineterminator='\n')
	writer.writerows(model.print_topics(num_topics=200, num_words=5))

print("doc_lda", doc_lda)
print("Writing the per row relation to the model")
with open("per_row_alpha.csv", "w") as f:
	writer = csv.writer(f, lineterminator='\n')
	writer.writerows(doc_lda)
