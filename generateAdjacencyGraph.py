import csv
import matplotlib.pyplot as plt
import pylab as pl
from matplotlib import collections as mc
import numpy as np
import math

inData=open("countyLatLong.csv",'r')
parsedData=csv.reader(inData,delimiter=",")

x=[]
y=[]
for index,row in enumerate(parsedData):
	x.append(float(row[1]))
	y.append(float(row[2]))
	
adjacencyData=open("adjacencyList.txt",'r')
adjacencyLists=[]

for index,element in enumerate(x):
	lineOfAdjacency=adjacencyData.readline()
	interData=lineOfAdjacency.split("\t")[1]
	interData=interData.split(",")
	interData.pop()
	adjacencyLists.append(interData)
	
lineCollections=[]

dx=0.015
contraction=0.9
	
for index,element in enumerate(adjacencyLists):
	for innerIndex,innerElement in enumerate(element):
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
		#x1=xMid+length*math.cos(direction)
		#y1=yMid+length*math.sin(direction)
		
		lineCollections.append([(x1,y1),[x2,y2]])
		#lineCollections.append([(x[index],y[index]),(x[int(innerElement)],y[int(innerElement)])])
lc=mc.LineCollection(lineCollections,linewidths=1)
fig, ax=pl.subplots()
ax.add_collection(lc)
ax.autoscale()
plt.show()


