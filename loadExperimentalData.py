import csv
import urllib.request
from datetime import date
import os
from os import path
import matplotlib.pyplot as plt
import numpy as np


url="https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv"

if(not path.exists("data_"+str(date.today())+".csv")):
	urllib.request.urlretrieve(url,"data_"+str(date.today())+".csv")




inLabels=open("countyLabels.txt",'r')
countyNum=int(inLabels.readline())
countyNames=[]
adjacencyMap=[]


for county in range(0,countyNum):
	inData=inLabels.readline().split("\t")
	countyID=inData[1].split("\n")[0]
	adjacency=inData[2].split("\n")[0]
	adjacencyMap.append((int(countyID),int(adjacency)))
	countyNames.append(inData[0])
	

caseDataCsv=open("data_"+str(date.today())+".csv",newline='\n')
parsedData=csv.reader(caseDataCsv,delimiter=",")

timeSeriesData=[]


# first, point to the first line of the data in counties we have already identified
inState=False
listIndex=0

contFlag=True
for index,row in enumerate(parsedData):
	if(index>2):
		for listCheck in adjacencyMap:
			if(int(row[0])==listCheck[0]):
				timeSeriesData.append([listCheck[1]])
				timeSeriesData[listCheck[1]].append(row[4:])

for firstIndex,data in enumerate(timeSeriesData):
	for secondIndex,secondData in enumerate(timeSeriesData[firstIndex][1]):
		timeSeriesData[firstIndex][1][secondIndex]=int(timeSeriesData[firstIndex][1][secondIndex])

adjacencyFile=open("adjacencyList.txt",'r')

adjacencyFile.readline()
adjacencyFile.readline()


fig=plt.figure()
ax=plt.axes()
plt.xticks(np.arange(0,200,5))
#plt.plot(np.arange(0,len(timeSeriesData[2][1]),1),timeSeriesData[2][1],label=countyNames[2])
plt.plot(np.arange(0,len(timeSeriesData[2][1]),1),timeSeriesData[2][1],label=countyNames[2])


connections=adjacencyFile.readline().split('\t')
connections=connections[1].split(',')
connections.pop()
for index,data in enumerate(connections):
	connections[index]=int(connections[index])
	#plt.plot(np.arange(0,len(timeSeriesData[int(connection)][1]),1),timeSeriesData[int(connection)][1],label=connection)
	plt.plot(np.arange(0,len(timeSeriesData[connections[index]][1]),1),np.array(timeSeriesData[connections[index]][1]),label=data)
adjacencyFile.close()
adjacencyFile=open("adjacencyList.txt",'r')

for county in range(0,88):
	connections=adjacencyFile.readline().split('\t')
	connections=connections[1].split(',')
	connections.pop()
	for index,data in enumerate(connections):
		connections[index]=int(connections[index])
	baseCounty=county

	check=False
	startIndex=0
	while(not check):
		if(timeSeriesData[baseCounty][1][startIndex]!=0):
			check=True
		else:
			startIndex+=1

	numOfConnections=len(connections)
	numOfSets=len(timeSeriesData[baseCounty][1])-startIndex-numOfConnections

	baseData=timeSeriesData[baseCounty][1][startIndex+1:startIndex+1+numOfConnections]
	dataSet=np.empty([numOfConnections,numOfConnections])

	for index,connection in enumerate(connections):
		dataSet[index]=timeSeriesData[connection][1][startIndex:startIndex+numOfConnections]
	dataSet=dataSet.transpose()

	aggregateCoeffs=np.array([numOfConnections])
	averageCount=0
	check=False
	while(not check):
		baseData=timeSeriesData[baseCounty][1][startIndex+1:startIndex+1+numOfConnections]
		dataSet=np.empty([numOfConnections,numOfConnections])

		for index,connection in enumerate(connections):
			dataSet[index]=timeSeriesData[connection][1][startIndex:startIndex+numOfConnections]
		if(np.linalg.matrix_rank(dataSet)==numOfConnections):
			outCoeffs=np.dot(np.linalg.inv(dataSet),baseData)
			aggregateCoeffs=aggregateCoeffs+outCoeffs
			averageCount+=1
			if(startIndex<len(timeSeriesData[baseCounty][1])-numOfConnections-1):
				startIndex+=1
			else:
				check=True
		else:
			if(startIndex<len(timeSeriesData[baseCounty][1])-numOfConnections-1):
				startIndex+=1
			else:
				check=True
	print(aggregateCoeffs/(averageCount+1))









	