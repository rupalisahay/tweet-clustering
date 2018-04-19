#tweet_datas clustering

import json
import sys

# k = 25
k = sys.argv[1]
# filenametweet_datas = 'inputFiles//tweets.json'
filenametweet_datas = sys.argv[3]
# filenameCentroid = "inputFiles//initialCentroids.txt" 
filenameCentroid = sys.argv[2]
# outputFile = "outputtweet_dataClustering.txt"
outputFile = sys.argv[4]

print("K:", k)
print("Loading tweet_datas from", filenametweet_datas)
print("Loading Initial Centroids from", filenameCentroid)

with open(filenametweet_datas) as f:
    tweet_datass = [x.strip() for x in f] 

tweet_datas = []

for tweet_data in tweet_datass:
    tweet_dataDict = json.loads(tweet_data)
    tweet_datas.append(tweet_dataDict)

tweet_dataIDs = []
tweet_dataText = []

for tweet_data in tweet_datas:
    tweet_dataIDs.append(tweet_data['id_str'])
    tweet_dataText.append(tweet_data['text'])

def computing_SSE(assign_values_toCluster, clusterId_list):
    sse = 0
    for c_id in range(len(clusterId_list)):
        for point in range(len(assign_values_toCluster)):
            if(assign_values_toCluster[point] == clusterId_list[c_id]):
                sse = sse + arrJD[getting_index_ofID(clusterId_list[c_id])][getting_index_ofID(tweet_dataIDs[point])]*arrJD[getting_index_ofID(clusterId_list[c_id])][getting_index_ofID(tweet_dataIDs[point])]
    return sse

def getting_index_ofID(tweet_data_id):
    return tweet_dataIDs.index(tweet_data_id)

def jaccard_distance_computation(a, b):
#     if(a == b):
#         return 0
    
    a = a.split()
    b = b.split()
#     print("String 1", a)
#     print("String 2", b)
    
    common_words = list(set([word for word in a if word in b]))
    all_words = list(set(a).union(b))
#     print(common_words)
#     print(all_words)
    
    intersect = len(common_words)
    union = len(all_words)
#     print(intersect)
#     print(union)
    return (1 - intersect/union)

totaltweet_datas = len(tweet_dataText)
arrJD = [[] for i in range(totaltweet_datas)]
for i in range(len(arrJD)):
    for j in range(len(arrJD)):
        arrJD[i].append(jaccard_distance_computation(tweet_dataText[i], tweet_dataText[j]))

clusterId_list = []



f = open(filenameCentroid)
lines = f.read().splitlines()  

for i in range(len(lines)):
    lines[i] = lines[i].rstrip(",")
    clusterId_list.append(lines[i])

assign_values_toCluster = [ 'void' for i in range(len(tweet_dataIDs))]

# until convergence
# assign_values_toCluster
# update centroids
count = 0
while(True):
    count = count+1
    for i in range(len(tweet_dataIDs)):
        minimum_distance = 2
        for j in range(len(clusterId_list)):
            distance = arrJD[getting_index_ofID(clusterId_list[j])][getting_index_ofID(tweet_dataIDs[i])]
            if(minimum_distance > distance):
                minimum_distance = distance
                assign_values_toCluster[i] = clusterId_list[j]
    # Each cluster ID

    new_clusterID = []

    for m in range(len(clusterId_list)):
        thisClusterID = clusterId_list[m]
        cluster_list = []

        for i in range(len(tweet_dataIDs)):
            if(assign_values_toCluster[i] == thisClusterID):
                cluster_list.append(tweet_dataIDs[i])

        listdistance_summation = []

        for i in range(len(cluster_list)):
            distance_summation = 0
            thistweet_dataID = cluster_list[i]
            for j in range(len(cluster_list)):
                distance_summation = distance_summation + arrJD[getting_index_ofID(cluster_list[i])][getting_index_ofID(cluster_list[j])]
                listdistance_summation.append(distance_summation)

        new_clusterID.append(cluster_list[listdistance_summation.index(min(listdistance_summation))])
        
    if(new_clusterID == clusterId_list):
        break
    clusterId_list = new_clusterID
    
# print(count)

print("Output file is: ", outputFile)
text_file = open(outputFile, "w")
for m in range(len(new_clusterID)):
    string = str(m+1)+'\t\t'
    for i in range(len(tweet_dataIDs)):
        if(assign_values_toCluster[i] == new_clusterID[m]):
            string = string + tweet_dataIDs[i]+','
    string = string + '\n\n'
    text_file.write(string)

sse = "SSE Value:" + str(computing_SSE(assign_values_toCluster, clusterId_list))
print(sse)
text_file.write(sse)
text_file.close()
print("Done Clustering Process")