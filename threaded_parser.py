#!/usr/bin/env python3
#import pandas as pd
#import numpy
import json
#import scipy
from sklearn.feature_extraction.text import CountVectorizer
import glob,csv, queue
from threading import Thread

#lets declare some variables
sha_list = []
feature_list = []
file_dir = 'files/'
outfile = 'output/outfile.csv'
outdata = {}
dll_list = []
num_threads = 2
file_queue = queue.Queue()
threads = []




#this block will take incoming data and dump the important bits into a couple of lists. I'm not sure where to put this yet, but I'm sure I need it.
#for imp in data["artifacts"]["1"]["forensics"]["imports"]:
#    if imp["dll"] not in list:
#            feature_list.append(imp["dll"])
#    if imp["entries"][0][0] not in list:
#            feature_list.append(imp["entries"][0][0])
#sha_list.append(data["status"]["sha256"])






# include trailing / - adds files in directory to queue
def get_files(directory,q):
	path = directory + '*'
	files = glob.glob(path)
	count = 0
	for f in files:
		q.put(f)
		count += 1
	return count

# pass 'file' - a JSON encoded filepath - print out needed values
def parse_data(q,outdata):
	while not q.empty():
		f = q.get()
		# output list - add elements to list, then append list to master list: [sha256[item1,item2[thing1,thing2],item3]]
		output = {"name": "", "dll_list": []}
		name_list = []
		info_j=[]

		try:
			with open (f) as data_file:
				data = json.load(data_file)
				data_file.close()
			#print(data)
			for imp in data["artifacts"]["1"]["forensics"]["imports"]:
				if imp["dll"] not in info_j:
					info_j.append(imp["dll"])
				if imp["entries"][0][0] not in info_j:
					info_j.append(imp["entries"][0][0])
			#info_j = data["additional_info"]["imports"]
			sha_j = data["status"]["sha256"]
			output.update({"name":sha_j})
			output.update({"additional_info":info_j})

			#
			output["name"] = sha_j
			for key in info_j.keys():
				dll_list.append(key)
				output["dll_list"].append(key)

			#print("Additional_info imports:\n", json.dumps(info_j, indent=2, sort_keys=True))
			#print("SHA256:\t", sha_j)
			print(output)
			q.task_done()
		except Exception as e:
			print("unable to open file!", f)
			print("Error from system:\n",str(e))
			q.task_done()


def build_threads(q,outdata,batch):
	for i in range(batch):
		worker = Thread(target=parse_data,args=(q,outfile))
		worker.setDaemon(True)
		threads.append(worker)

def start_threads():
	count = 0
	for i in range(len(threads)):
		threads[i].start()
		count += 1

def main():
	thread_count = 0
	# get_files populates queue, returns an integer of amount of items put in queue
	num_files = get_files(file_dir,file_queue)
	#while not file_queue.empty():
		# set up threads
	if num_threads <= num_files:
		build_threads(file_queue,outdata,num_threads)
	elif num_threads > num_files:
		build_threads(file_queue,outfile,num_files)
	print("total threads:", len(threads))
	start_threads()
	# join threads
	for i in range(len(threads)):
		threads[i].join()

	sorted_dll = set(dll_list)
	print(sorted_dll)


print("Starting main loop")
main()
print("passed main, joining queue")
file_queue.join()
print("done!")
