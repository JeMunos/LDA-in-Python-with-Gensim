import pandas as pd
import numpy
import scipy
from sklearn.feature_extraction.text import CountVectorizer

fr = open('stopwords.csv', 'r')
text = fr.read()
stopwords = text.split()
fr.close()
df = pd.read_csv('new_function_match_functions_only.csv')
descriptionList = df['Description'].values.astype('U')
vectorizer = CountVectorizer(stop_words = None)
bag_of_words = vectorizer.fit(descriptionList)
bag_of_words = vectorizer.transform(descriptionList)
array = bag_of_words.toarray()
#print (array)
#numpy.savetxt('wordArray.csv', array, delimiter=',')
descriptionWords = vectorizer.get_feature_names()
#print(descriptionWords)
dataArray = pd.DataFrame(array, columns=descriptionWords, index= df.Function.tolist()) 
print(dataArray)
wordsInDescription = vectorizer.vocabulary_
wordList = pd.DataFrame.from_dict(wordsInDescription, orient = 'index')
#print(wordList)
#wordList.to_csv('wordOutputStopList.csv')

