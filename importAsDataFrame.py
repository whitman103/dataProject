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
import pandas as pd


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
	inData=inData[0].split(',')[0]
	inData=inData.split("\"")[1]
	countyNames.append(inData)
	

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
		
dataDictionary={}

for index,data in enumerate(timeSeriesData):
	dataDictionary[countyNames[index]]=timeSeriesData[index][1]

dataFrame=pd.DataFrame(data=dataDictionary)

print(dataFrame['Franklin County'])
""" Data for each county is listed in the columns, can be accessed by calls to the name of the county, as above. """