import requests

def main():
    # API endpoint
    url = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"

    # Headers for the request
    headers = {
        "Content-Type": "application/json",
        "Accept": f"application/json;api-version=7.2-preview.1"
    }

   
    # here two text files are created and filled with extensions identifier and display names
    with open('all_extensions.txt', 'w',encoding='utf-8') as f: 
        with open('all_extensions_identifier.txt','w',encoding='utf-8') as f2:
            # to send 60 requests
            for j in range(1, 61):
                body = {
                    "filters": [
                        {
                            "criteria": [
                                {
                                    "filterType": 8,
                                    "value": "Microsoft.VisualStudio.Code"
                                }
                            ],
                            "pageNumber": j,
                            "pageSize": 1000,  
                            "sortBy": 0, 
                            "sortOrder": 0  
                        }
                    ],
                    "assetTypes": [],
                    "flags": 0x100 | 0x200 | 0x20  
                }

                # send a POST request
                response = requests.post(url, headers=headers, json=body)
                # Check if the request was successful
                if response.status_code == 200:
                    data = response.json()
                    # Extract the 1000 extensions in the request
                    extensions = data.get("results", [])[0].get("extensions", [])

                    # to extract the display names and idnetifier
                    for extension in extensions:
                        extension_publisher_username = extension["publisher"]['publisherName']
                        extensiondisplay=extension["displayName"]
                        extensionname=extension["extensionName"]


                        extension_identifer = f"{extension_publisher_username}.{extensionname}"
                        f.write(f"{extensiondisplay}\n")
                        f2.write(f"{extension_identifer}\n")
                else:
                    print(f"Failed to fetch extensions: {response.status_code}")
        


if __name__ == '__main__':
    main()
    print("ready")




