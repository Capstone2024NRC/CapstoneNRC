import requests

"""
Change these two variables
"""
file_path = "/Users/chesterfrancisco/Desktop/Capstone Py Files/Connors_Capstone_Files/test.json"
api_data_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Name%20eq%20%27SP07_NAO_MS4_2A_20210729T064948_20210729T064958_TOU_1234_90f0.DIMA%27&$expand=Attributes"

# this function writes the return value of the request to a file in json format
def write_json():     
    response = requests.get(api_data_url)

    # create a dictionary  
    json_data = response.json()

    #write the file to a path of your choosing    
    with open(file_path, 'w', encoding="utf-8") as fd:

        # loop through json_data and write to file
        for i in json_data["value"]:
            fd.write(response.text)

        fd.close()      
        print(f'File created at: {file_path}')

# run the function
write_json()