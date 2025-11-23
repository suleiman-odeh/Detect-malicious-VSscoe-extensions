# Detection of typosquatting and name collision

## Description
This technique involves detecting typosquatting and name collision in Visual Studio Code extensions

## all_extensions.py
This python code is used to extract 60 thousand extensions display names and their identifiers through calling an API

## typo_tectnique.py
This python code is used to compare a comparison set of display names with the idnetified display names in the all_extensions.py .

## Steps: 
1- Run all_extensions.py, which will result two text files

2- From both text files take the first 100 most installed extensions display name with their identifiers based on their order in The Visual Studio Code Marketplace https://marketplace.visualstudio.com/vscode

3- Open typo_tectnique.py

4- Remove the strings in the list first100_extension_names and put your taken display names in step 2

5- Run typo_tectnique.py

6- The output is found in typoresults.txt

## Autor
Suleiman Odeh