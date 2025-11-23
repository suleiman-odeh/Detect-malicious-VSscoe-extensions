# Clustering of extensions

## Description
This technique involves clustering the extensions using the K-means algorithm. Every extensions far from the cluster centers will be considered as suspicious. 
## optimal_clusters.py
This python code will perform The K-mean algorithm with an input of 1 until 30 on thr first 1000 extensions with a main source code. Then it will show a line graph, which shows the rate of inertia.

## clustering_technique.py
This python code will perform the K-mean algorithm with the input determined from the line graph resulted in optimal_clusters.py
## Steps: 
1- run optimal_clusters.py, which will result a line graph

2- Determine the elbow point based on the graph, which was in the case of the line graph in the thesis 12

3- open clustering_technique.py

4- adjust the number of clusters k-mean in line 172

5- ignore this step in case you choose 12 also as optimal number of clusters.

5- run clustering_technique.py

6- The output is found in ouptput.txt. In addition, feu.txt shows which feauters has been extracted

## Author
Suleiman Odeh