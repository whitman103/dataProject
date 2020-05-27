import csv
import urllib.request
from datetime import date
import os
from os import path
import pylab as pl
from matplotlib import collections as mc
import matplotlib.pyplot as plt
import numpy as np
import math


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

aggregateHold=[]

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
	aggregateHold.append(aggregateCoeffs/(averageCount+1))


dx=0.015
contraction=0.9
c=[]

inData=open("countyLatLong.csv",'r')
parsedData=csv.reader(inData,delimiter=",")

x=[]
y=[]

for index,row in enumerate(parsedData):
	x.append(float(row[1]))
	y.append(float(row[2]))
	
adjacencyData=open("adjacencyList.txt",'r')
adjacencyLists=[]
lineCollections=[]

for index,element in enumerate(x):
	lineOfAdjacency=adjacencyData.readline()
	interData=lineOfAdjacency.split("\t")[1]
	interData=interData.split(",")
	interData.pop()
	adjacencyLists.append(interData)
	


for index,element in enumerate(adjacencyLists):
	for innerIndex,innerElement in enumerate(element):
		interList=aggregateHold[index].tolist()
		if(len(interList)==len(element)):
			if(interList[innerIndex]>0):
				c.append((0,0,1,1))
			else:
				c.append((1,0,0,1))
		
		x1=x[index]
		y1=y[index]
		x2=x[int(innerElement)]
		y2=y[int(innerElement)]
		direction=np.arctan((y2-y1)/(x2-x1))
		if(x2>x1):
			offsetDirection=direction-math.pi/2.
		if(x2<x1):
			offsetDirection=direction+math.pi/2.
		x1+=dx*math.cos(offsetDirection)
		y1+=dx*math.sin(offsetDirection)
		x2+=dx*math.cos(offsetDirection)
		y2+=dx*math.sin(offsetDirection)
		xMid,yMid= (x1+x2)/2., (y1+y2)/2.
		length=math.sqrt((x1-x2)**2+(y1-y2)**2)
		length=length*contraction
		x1=xMid+length/2.*math.cos(direction)
		y1=yMid+length/2.*math.sin(direction)
		x2=xMid+length/2.*math.cos(direction+math.pi)
		y2=yMid+length/2.*math.sin(direction+math.pi)
		lineCollections.append([(x1,y1),[x2,y2]])

lc=mc.LineCollection(lineCollections,linewidths=1,color=c)
fig, ax=pl.subplots()
ax.add_collection(lc)
ax.autoscale()
plt.show()





	