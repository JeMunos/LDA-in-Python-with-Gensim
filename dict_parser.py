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
ioc_title_list=[]
first_row_imports=[]
first_row_ioc=[]
first_rwo_combined=[]



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
    sha = str(json_data['status']['sha256'])
    
#find the artifact value that contains our sha, store the list of dictionaries in oper_dict_list
    for k,v in json_data['artifacts'].items():
        if json_data['artifacts'][k]['sha256'] == sha:
            oper_dict_list = json_data['artifacts'][k]['forensics']['imports']
    for d in oper_dict_list:
        if sha not in final_dict.keys():
            final_dict[sha] = {}
            final_dict[sha]['dll'] = {}
            final_dict[sha]['iocs'] = {}
        final_dict[sha]['dll'][str(d['dll'])] = [str(n[0]) for n in d['entries']] #for each item in oper_dict_list create final_dict{<sha>: {<file.dll>: [import1, import2, etc]}}
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


#Get all IOC titles and store in list to add to final dictionary if title is unique
    ioc_title_list.append([str(n['title']) for n in json_data['iocs'] if n['title'] not in ioc_title_list])
#creates master list of iocs for each sha            
    final_dict[sha]['iocs'] = [str(n['title']) for n in json_data['iocs']]
    
ioc_title_list = [n for x in ioc_title_list for n in x]    
first_row = [''] + [[k] + v for k,v in dll_dict.items()]
first_row_imports = [n for x in first_row for n in x]
first_row_ioc = ioc_title_list
first_row_combined = first_row_imports + first_row_ioc

print("IOC LIST: ", ioc_title_list)


#ohh god ohh god CSV....fuck
with open('output/imports.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow([' '] + first_row_imports)
    for sha in final_dict.keys():
        row =[]
        row.append(sha)
        dll_exists = False
        #this will keep track of the true false of a dll existing in final_dict, also it will append a 1 if the dll does exist and a 0 if it does not exist for a given SHA
        for item in first_row_imports:
            if '.dll' in item:
                dll = item
                if dll in final_dict[sha]['dll'].keys():
                    row.append('1')
                    dll_exists = True
                else:
                    row.append('0')
                    dll_exists = False
            #this case will track import statments, 0 if the dll doens't exist. if the dll does exist, iterate over hte list and mark 1 or 0 where appropriate
            else:
                if dll_exists:
                    if item in final_dict[sha]['dll'][dll]:
                        row.append('1')
                    else:
                        row.append('0')
                else:
                    row.append('0')
        writer.writerow(row)

with open('output/ioc.csv','w') as f:
    writer = csv.writer(f)
    writer.writerow([' '] + first_row_ioc)
    for sha in final_dict.keys():
        row = []
        row.append(sha)
        for item in first_row_ioc:
            if item in final_dict[sha]['iocs']:
                row.append('1')
            else:
                row.append('0')
        writer.writerow(row)

with open('output/combine.csv','w') as f:
    writer = csv.writer(f)
    writer.writerow([' '] + first_row_combined)
    for sha in final_dict.keys():
        row=[]
        row.append(sha)
        dll_exists = False
        ioc_hit = False
        for item in first_row_combined:
            if ioc_title_list[0] == item:
                ioc_hit=True
            if not ioc_hit:
                if '.dll' in item:
                    dll = item
                    if dll in final_dict[sha]['dll'].keys():
                        row.append('1')
                        dll_exists = True
                    else:
                        row.append('0')
                        dll_exists = False
                else:
                    if dll_exists:
                        if item in final_dict[sha]['dll'][dll]:
                            row.append('1')
                        else:
                            row.append('0')
                    else:
                        row.append('0')
            else:
                if item in final_dict[sha]['iocs']:
                    row.append('1')
                else:
                    row.append('0')
        writer.writerow(row)











