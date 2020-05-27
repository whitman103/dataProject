import csv
import numpy as np

f=open("county_adjacency.txt",'r')

wantedState="OH"
"""Takes us to the state we want, currently OH"""


countyIndex=0
countyList=[]
inState=False
while inState!=True:
	inLine=f.readline()
	indexOut=inLine.find("\t")
	if(inLine[indexOut-3:indexOut-1]==wantedState):
		inState=True

"""countyList Structure is (named of County, countyID)"""

def firstLineParse(fileStream):
	splitList=fileStream.split("\t")
	splitList[-1]=splitList[-1].split("\n")[0]
	countyName=[splitList[0],splitList[1]]
	firstNeighbor=[splitList[2],splitList[3]]
	return(countyName,firstNeighbor)


	
while inState==True:
	interList=[]
	newCounty,startingNeighbor=firstLineParse(inLine)
	countyList.append(newCounty)
	interList.append(startingNeighbor)


	finished=False
	while finished!=True:
		inLine=f.readline()
		if(inLine[0]=="\t"):
			splitList=inLine.split("\t")
			splitList[-1]=splitList[-1].split("\n")[0]
			interList.append([splitList[2],splitList[3]])
		else:
			finished=True
	countyList[countyIndex].append(interList)
	countyIndex+=1
	indexOut=inLine.find("\t")
	if(inLine[indexOut-3:indexOut-1]!=wantedState):
		inState=False
	
outCountyLabels=open("countyLabels.txt",'w')	
outCountyLabels.write("%s\n" % len(countyList))
for i in range(0,len(countyList)):
	outCountyLabels.write("%s\t%s\t%i\n" % (countyList[i][0],countyList[i][1],i))
outCountyLabels.close()

labelToIndex=[]

inCountyLabels=open("countyLabels.txt",'r')
indexMax=int(inCountyLabels.readline())
for i in range(0,indexMax):
	inData=inCountyLabels.readline().split("\t")
	labelToIndex.append((int(inData[1]),i))
inCountyLabels.close()

adjacencyList=[]

for index,county in enumerate(countyList):
	for label in labelToIndex:
		if(int(county[1])==label[0]):
			adjacencyList.append([label[1],])
	
	neighborList=[]
	for neighbor in county[2]:
		for label in labelToIndex:
			if(int(neighbor[1])==label[0] and (int(label[1])!=index)):
				neighborList.append(label[1])
	adjacencyList[index].append(neighborList)


outAdjacency=open("adjacencyList.txt",'w')

for element in adjacencyList:
	outAdjacency.write("%s \t" % element[0])
	for adjacent in element[1]:
		outAdjacency.write("%s," % adjacent)
	outAdjacency.write("\n")
outAdjacency.close()
	

	





