# Data Science Project

## Data:

Basic county and adjacency data is given in "county_adjacency.txt". This data is for the whole country. The script "generateCounties.py" reads through the file, finds the state that you wish to analyze, splits up the counties, generates a labeling system, and an easily implemented list adjacency node set. These are placed in the files "countyLabels.txt" and "adjacencyList.txt". Data is loaded by "loadExperimentalData.py". Data for individual counties are available, and plottable with their labels as defined in the countyLabels file.

## To Run:

First, run generateCounties.py, then loadExperimentalData.py. You should download the current data into a csv in the folder git folder, and produce a graph of Ashland County, OH's total cases. 

Now, loadExperimentalData.py computes the average values, k_i, for the transfer coefficients using a simple formula. Say that a county has N neighbors. We load in the data for N consequective time points for the county. We then seek to form I_a(t+1)=k_iI_i(t), where I_a(t+1) is the number of cases at the next day, k_i are the transfer coefficients, and I_a(t) are each of the number of cases in the N neighboring counties. We build a N dimensional vector from I_a(t), I_a(t+!),..., I_a(t+N). Then, if we assume that the coefficients are stationary, we can write that \vec{X}_a(t+!)=\mathbf{X}_{ia} \vec{k}(t). 

We can invert this equation to get a list of the coefficients. This can be done many times and averaged to get an aggregate number. I'm not sure that it makes sense yet, but we shall see. Currently, it runs and produces the average transfer coefficient over all N dimensional snapshots that have invertible \mathbf{X}_{ia}. More work to follow.

Now, loadExperimentalData.py visualizes the data around Ohio. Blue indicates that a high number of covid cases increases the number in the receiving county. Red means that a high number of COVID cases decreases the number in the receiving county. I have to add arrows so that this graph is understandable.

## Needed to do

Clean out the old data files automatically. Combine these scripts into a single run to preprocess data and get ready to analyze. Arrows added to plots. 
