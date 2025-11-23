import requests
import zipfile
import io
import json
import os
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

    # it will fetch until reaching 1000 extensions that have a main source code
    for j in range(1, 60):
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
                it will go through the extensions and if it reached 1000 extensions 
                with a main source code, it will stop
                """
                for extension in extensions:
                    found_source = False
                    p += 1
                    if(len(source_dict) == 1000):
                        break
                    print(f"Number of analysed extensions now is {p}")
                    extension_publisher_username = extension["publisher"]['publisherName']
                    extension_name=extension["extensionName"]
                    extension_identifier = f"{extension_publisher_username}.{extension_name}"
                    extension_version = extension["versions"][0]["version"]

                    # second call to get the extensions source code
                    vsix_package_url = f"https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{extension_publisher_username}/vsextensions/{extension_name}/{extension_version}/vspackage"

                    # through long analysis and running the extensions multiple times it will check if already the extension is analysed
                    source_file_path = os.path.join(source_dir, f"[{extension_identifier}].js")
                    if os.path.exists(source_file_path):
                        print(f"Source file for {extension_identifier} already exists.")
                        source_code = read_source_code(source_file_path)
                        source_dict[extension_identifier] = source_code
                        continue
                    # send a get request to the extension's endpoint
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
    source_codes = list(source_dict.values())
    # X has now a TF-IDF matrix
    X = vectorizer.fit_transform(source_codes)
    feature_names = vectorizer.get_feature_names_out()
    print(f"Total number of features: {len(feature_names)}")


    first_sources = source_codes
    first_X = X
    K = range(1, 31)
    inertia = []

    #The k-mean algorithm will be running starting from 1 until 30 cluster and inertia is calculated
    for k in K:
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X)
        inertia.append(kmeans.inertia_)

    # The cluster and their inertia is plotted
    plt.figure(figsize=(10, 6))
    plt.plot(K, inertia, 'bx-')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.xticks(K)
    plt.grid(True)
    plt.show()



if __name__ == '__main__':
    main()
