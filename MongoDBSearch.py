import requests # type: ignore
from pprint import PrettyPrinter
from pymongo.mongo_client import MongoClient # type: ignore
from pymongo.server_api import ServerApi # type: ignore
pp = PrettyPrinter()


response_API = requests.get("https://catalogue.dataspace.copernicus.eu/resto/api/collections/search.json?")
data = response_API.json()  # extracting the API result in JSON format 

#uri connection to the mongoDb instance you are holding your info in 
uri = "mongodb+srv://connorcoyle2014:FMuz3JuJcQjb6uD6@cluster0.3zqurog.mongodb.net/"

#Connects to Mongo
client = MongoClient(uri, server_api=ServerApi('1'))
#Connects to Cluster if proper cluster name and collection name
mydb = client["Capstone2024"]
myData = mydb["collectionTwo"]

# Dynamically asking for data that will then be queried below 
key = input("Enter the key you want to search for: \n")
value = input ("Enter a value you want associated with the key you entered in the last step \n") 

# Using above search queries looking for specific information inside a specific collection 
query = {key : value}
documents = myData.find(query)
for doc in documents:
    print(doc)

