import requests # type: ignore
from pprint import PrettyPrinter
from pymongo.mongo_client import MongoClient # type: ignore
from pymongo.server_api import ServerApi # type: ignore
pp = PrettyPrinter()


"""
Possible APIS to get info from 

USGS API
https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-01-02

Base Copernicus API
https://catalogue.dataspace.copernicus.eu/resto/api/collections/search.json?

Nasa API
https://api.nasa.gov/neo/rest/v1/feed?start_date=2015-09-07&end_date=2015-09-08&api_key=qlixy9IOFgoVXpZZoK2osukQN5bPokAAnysH3ia6

"""
response_API = requests.get("https://catalogue.dataspace.copernicus.eu/resto/api/collections/search.json?")
data = response_API.json()  # extracting the API result in JSON format 

# #Mongo Setup

#Special password Mongo gave you and work email goes here
uri = "mongodb+srv://connorcoyle2014:FMuz3JuJcQjb6uD6@cluster0.3zqurog.mongodb.net/"

#Connects to Mongo
client = MongoClient(uri, server_api=ServerApi('1'))
#Connects to Cluster if proper cluster name and collection name
mydb = client["Capstone2024"]
myData = mydb["collectionTwo"]

#retrieves Dictionaries in the List
def retrieveDictionariesInList(data):
    for i in range(len(data)):
        dictionary = data[i]
        yield dictionary

#Iterates through elements in a dictionary. Adds them to myData variable which is your current collection
#Keep uncommented if you don't need to currently add anything 

for d in data:
    if isinstance(data[d], dict):
        for n in data[d]:
            if isinstance(data[d][n], list):
                for nn in retrieveDictionariesInList(data[d][n]):
                    insertedData = myData.insert_one(nn)
            else:
                dictionary = {d: data[d]}
                newValue = { "$set": dictionary}
                myData.update_one(dictionary, newValue, upsert=True)
    else:
        dictionary = {d: data[d]}
        insertedData = myData.insert_one(dictionary) 

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

# # In case you need to clear out the collection in the database.
#deleteData = myData.delete_many({})
print("done!")

