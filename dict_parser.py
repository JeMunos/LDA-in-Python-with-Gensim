#!/usr/bin/env python
import pandas as pd
import numpy
import os
import json
import glob
import scipy
import csv
from sklearn.feature_extraction.text import CountVectorizer

final_dict={}
dll_dict = {}
dll_list = []
path = 'files/*.json'
#path = '../Malware_Project/TG_Json_Data/*.json'
size = len(glob.glob(path))
print("Number of files: ", size)

for file in glob.glob(path):
#open each file in turn and write the data as to the data variable, properly parsed as json
    with open (file) as data_file:
        json_data = json.load(data_file)
        data_file.close()

#Get the sha from the bottom fo the file and store it in sha variable
    sha = json_data['status']['sha256']

#find the artifact value that contains our sha, store the list of dictionaries in oper_dict_list
    for k,v in json_data['artifacts'].items():
        if json_data['artifacts'][k]['sha256'] == sha:
            oper_dict_list = json_data['artifacts'][k]['forensics']['imports']
    for d in oper_dict_list:
        if sha not in final_dict.keys():
            final_dict[sha] = {}
        final_dict[sha][str(d['dll'])] = [str(n[0]) for n in d['entries']] #for each item in oper_dict_list create final_dict{<sha>: {<file.dll>: [import1, import2, etc]}}
        #if dll_dict doesn't contain a dll, add it to the dll_dict and populate the import entries
        #if dll_dict does contain the dll, check all imports and add new imports as necessary
        if d['dll'] not in dll_dict.keys():
            dll_dict[str(d['dll'])] = [str(n[0]) for n in d['entries']]
        else:
            for n in d['entries']:
                if n[0] not in dll_dict[d['dll']]:
                    dll_dict[d['dll']].append(str(n[0]))
        #build list of all DLL's contained in the dll_dict
        if d['dll'] not in dll_list:
            dll_list.append(str(d['dll']))
print("dll dict ", dll_dict)
print("dll_list", dll_list)


