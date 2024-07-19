import requests # type: ignore
import json
from pprint import PrettyPrinter
pp = PrettyPrinter()

request_url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-01-02'
file_path = '/Users/chesterfrancisco/Desktop/Capstone Py Files/Connors_Capstone_Files/testFile.json'

dictionary = {}

personalMetadata = {
    "personal_metadata": {
        "date": "06/20/2024"
    }
}

"""
This fucntion writes the request response to a file in json format
Also allows you to add your own metadata to the exisitng data within file
"""

def add_personal_metadata():
    r = requests.get(request_url)

    data = r.json()

    for d in data:
        dictionary.update({d: data[d]})

        if d == 'metadata':
            dictionary.update(personalMetadata)  

    with open(file_path, 'w', encoding="utf-8") as fd:
        fd.write(json.dumps(dictionary, indent=4))
        fd.close() 

    print(f'metadata added and updated the file: {file_path}')    

add_personal_metadata()