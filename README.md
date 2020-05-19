# Data Science Project

## Data:

Basic county and adjacency data is given in "county_adjacency.txt". This data is for the whole country. The script "generateCounties.py" reads through the file, finds the state that you wish to analyze, splits up the counties, generates a labeling system, and an easily implemented list adjacency node set. These are placed in the files "countyLabels.txt" and "adjacencyList.txt". Data is loaded by "loadExperimentalData.py". Data for individual counties are available, and plottable with their labels as defined in the countyLabels file.

## To Run:

First, run generateCounties.py, then loadExperimentalData.py. You should download the current data into a csv in the folder git folder, and produce a graph of Ashland County, OH's total cases. 

## Needed to do

Clean out the old data files automatically. Combine these scripts into a single run to preprocess data and get ready to analyze. 
