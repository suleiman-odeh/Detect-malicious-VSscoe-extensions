# Detecting potentially malicious extensions for Visual Studio Code

Here you will find the implementation of three techniques for detecting suspicious extensions in Visual Studio code. 


## Detection of typosquatting and name collision
This technique focuses on comparing the similarity of extension display names, which detects typosquatting when two display names are quite similar. If both display names are the same, then a name collision is detected. 

## Rule-based malware detection
This technique focuses on detecting malware in the source code of extensions using regular expressions based on rules from Guarddog https://github.com/DataDog/guarddog.

## Clustering of extensions
This technique focuses on using the K-means algorithm to cluster the main source code of extensions based on the similarity in their source code.

## Note
In each Technique Directory you will find the steps required to perform the techniques.

## Author
Suleiman Odeh
Matriculation number: 3391757