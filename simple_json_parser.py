import pandas as pd
import numpy
import os
import json
import glob
import scipy

import csv
from sklearn.feature_extraction.text import CountVectorizer

path = 'files/*.json'
size = len(glob.glob(path))
feature_list = []
bi_list =[]
dll_list=[]
import_list[]
sha_list[]
output_list = []
print("Number of files: ", size)

#read all files from path into a dict then iterate over them
for file in glob.glob(path):
	#open each file in turn and write the data as to the data variable, properly parsed as json
	with open (file) as data_file:
		data = json.load(data_file)
		data_file.close()

	#open each data file in turn, parse though it and grab the dll and entry values in turn, 
	#append this data to the feature_list variable
	feature_list=[]
	feature_list.append(data["status"]["sha256"])
	for imp in data["artifacts"]["1"]["forensics"]["imports"]:
		feature_list.append(imp["dll"])
		feature_list.append(imp["entries"][0][0])
	for item in data["iocs"]:
		feature_list.append(item["title"])
	#append the sha to the sha_list varible 
	feature_list.append(data["status"]["sha256"])
	output_list.append([feature_list])

#lets print the two lists and see if this works for our sample file set
#print("feature_list",feature_list)

with open('some.csv', 'w') as f:
	writer = csv.writer(f)
	for row in feature_list:
	    writer.writerow(output_list)

