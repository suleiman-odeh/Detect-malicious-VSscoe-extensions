import requests
import zipfile
import io
import json
import os
import numpy as np
import sys
from tempfile import TemporaryDirectory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
import matplotlib.pyplot as plt


#read the main source code
def read_source_code(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

# save the main source code in the directory
def save_source_code(file_path, source_code):
    with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
        file.write(source_code)

# save the extracted feauters in a text file
def save_features_to_file(feature_names, file_path="feu.txt"):
    with open(file_path, 'w', encoding='utf-8') as file:
        for feature in feature_names:
            file.write(f"{feature}\n")

def main():
    os.environ['OMP_NUM_THREADS'] = '1'
    p = 0
    sys.setrecursionlimit(1500000)
    # every element has the extensions identifier and their source code
    source_dict = {}
    api_endpoint = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json;api-version=7.2-preview.1"
    }

    # Directory to save source files
    source_dir = "vscodesources"
    os.makedirs(source_dir, exist_ok=True)

    # Fetching the extensions
    for j in range(1, 30):
        payload = {
            "filters": [
                {
                    "criteria": [
                        {"filterType": 8, "value": "Microsoft.VisualStudio.Code"},
                    ],
                    "pageNumber": j,
                    "pageSize": 1000,
                    "sortBy": 0,
                    "sortOrder": 0
                }
            ],
            "assetTypes": [],
            "flags": 214 | 0x100 | 0x200 | 0x20
        }
        try:
            # sending a http request and check if it is successful
            response = requests.post(api_endpoint, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                extensions = data.get("results", [])[0].get("extensions", [])
                """
                it will go through the extensions with a main source code
                """
                for extension in extensions:
                    found_source = False
                    p += 1
                    print(f"Number of analysed extensions now is {p}")
                    extension_publisher_username = extension["publisher"]['publisherName']
                    extension_name=extension["extensionName"]
                    extension_identifier = f"{extension_publisher_username}.{extension_name}"
                    extension_version = extension["versions"][0]["version"]
    
                    vsix_package_url = f"https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{extension_publisher_username}/vsextensions/{extension_name}/{extension_version}/vspackage"
                    # Check if the main source file already exists in the direcotry vscodesources to save time
                    source_file_path = os.path.join(source_dir, f"[{extension_identifier}].js")
                    if os.path.exists(source_file_path):
                        print(f"Source file for {extension_identifier} already exists.")
                        source_code = read_source_code(source_file_path)
                        source_dict[extension_identifier] = source_code
                        continue
                    # get request is sent to the extension's endpoint
                    response = requests.get(vsix_package_url, headers=headers, stream=True)
                    if response.status_code == 200:
                        vsix_package_buffer = io.BytesIO()
                        for chunk in response.iter_content(1024):
                            vsix_package_buffer.write(chunk)
                        vsix_package_buffer.seek(0)
                        with TemporaryDirectory() as temp_dir:
                            try:
                                
                                with zipfile.ZipFile(vsix_package_buffer, 'r') as zip_ref:
                                    found_package_json = False
                                    source = ""
                                    # in this stage it will search for the package.json file, which has the path for the main file
                                    for file in zip_ref.infolist():
                                        if file.filename.casefold() == 'extension/package.json'.casefold():
                                            print(f"File found: {file.filename} in {extension_identifier}")
                                            with zip_ref.open(file) as f:
                                                found_package_json = True
                                                package_content = f.read().decode('utf-8', errors='ignore')
                                                package_json = json.loads(package_content)
                                                if "main" in package_json:
                                                    main_file = package_json["main"]
                                                    main_file_path = os.path.normpath(os.path.join(os.path.dirname(file.filename), main_file))
                                                    source = main_file_path.replace('\\', '/')
                                                    print(f"Main file: {source}")
                                                    found_source = True
                                                else:
                                                    print(f"No 'main' key found in {file.filename}")
                                                    break
                                    if not found_package_json:
                                        print(f"No package.json found in {extension_identifier}")

                                    # it will be true if a main file has been found
                                    if found_source:
                                        for file in zip_ref.infolist():
                                            if source in file.filename and file.filename.endswith('.js'):
                                                print(f"The source is {file.filename}")
                                                extracted_path = os.path.join(temp_dir, file.filename)
                                                os.makedirs(os.path.dirname(extracted_path), exist_ok=True)
                                                with zip_ref.open(file) as source_file:
                                                    with open(extracted_path, 'wb') as temp_file:
                                                        temp_file.write(source_file.read())
                                                source_code = read_source_code(extracted_path)
                                                source_dict[extension_identifier] = source_code
                                                save_source_code(source_file_path, source_code)
                                                print("file saved")
                                                break
                            except Exception as e1:
                                print(f"Error processing {extension_identifier}: {e1}")
                                continue
                    else:
                        print(f"Failed to download VSIX package of {extension_identifier}")
            else:
                print("Failed to retrieve data")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download VSIX package of {extension_identifier}: {e}")
    print(f"{len(source_dict)} extensions were saved")

    # Tokenize and vectorize the source code
    vectorizer = TfidfVectorizer(
        token_pattern=r'\b[a-zA-Z_][a-zA-Z]*\b',
        stop_words=[
            'function', 'class', 'var', 'let', 'const', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'default',
            'break', 'continue', 'return', 'try', 'catch', 'finally', 'throw', 'new', 'delete', 'typeof', 'instanceof',
            'in', 'this', 'super', 'import', 'export', 'extends', 'static', 'get', 'set', 'async', 'await', 
            'void', 'null', 'true', 'false', 'undefined', 'i', 'j', 'k'
        ]
    )

    # it put the source codes in a TF-IDF matrix
    source_codes = list(source_dict.values())
    X = vectorizer.fit_transform(source_codes)
    feature_names = vectorizer.get_feature_names_out()
    print(f"Total number of features: {len(feature_names)}")
    save_features_to_file(feature_names)

    # The K-means is applied on the first 1000 main source codes
    # The optimal number of clusters based on the line graph in my thesis is 12
    first_sources = source_codes[:1000]
    first_X = X[:1000]
    kmeans = KMeans(n_clusters=12)
    kmeans.fit(first_X)
    first_labels = kmeans.labels_

    # The rest source codes
    rest_sources = source_codes[1000:]
    rest_X = X[1000:]
    rest_labels = kmeans.predict(rest_X)

    # every source code with a distance higher the one will be exculded from the clusters and considered as suspicious
    distances = np.min(pairwise_distances(rest_X, kmeans.cluster_centers_), axis=1)
    additional_cluster = np.where(distances > 1.0)[0]
    all_labels = np.concatenate([first_labels, rest_labels])
    for idx in additional_cluster:
        all_labels[len(first_labels) + idx] = -1  

    extension_indices = {i: extension for i, extension in enumerate(source_dict)}
    cluster_labels = np.unique(all_labels)
 
  
    # print the clusters and save in text file
    with open("output.txt", 'w', encoding='utf-8', errors='ignore') as file:
        for label in cluster_labels:
            if label == -1:
                file.write("Additional Cluster (far from cluster centers):\n")
                for idx in additional_cluster:
                    ext = extension_indices[len(first_labels) + idx]
                    file.write(f"  - Extension: {ext}\n")
            else:
                indices = [i for i, cluster in enumerate(all_labels) if cluster == label]
                file.write(f"Cluster {label+1}:\n")
                for index in indices:
                    ext = extension_indices[index]
                    file.write(f"  - Extension: {ext}\n")


if __name__ == '__main__':
    main()
