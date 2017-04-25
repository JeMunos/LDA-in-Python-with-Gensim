import pandas as pd

#read csv into panda format, chose csv file to process
data = pd.read_csv('WekaCluster.csv', index_col=0)

#return list of unique functions and get length of unique functions
clusterData=data.Cluster.unique()
len(data.Cluster)

#checks to see if cluster data for a function matches the each unique cluser
for c in clusterData:
    data[c] = 0
    i = 0
    while i < len(data.Cluster):

#If the function cluster matches cluster (c) set one 
#as the value into the cell of that function row and 
#that cluster column
  
        if data.Cluster[i] == c:
            data.ix[[i],[c]] = 1
        i = i+1

#output vectorized information into csv
data.to_csv('WekaBinaryClusters1.csv')

