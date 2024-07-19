import requests
from pprint import PrettyPrinter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
pp = PrettyPrinter()

API_KEY = 'qlixy9IOFgoVXpZZoK2osukQN5bPokAAnysH3ia6'
START_DATE = '2015-09-07'
END_DATE = '2015-09-08'

# response = requests.get('https://api.nasa.gov/neo/rest/v1/feed?start_date=2015-09-07&end_date=2015-09-08&api_key=qlixy9IOFgoVXpZZoK2osukQN5bPokAAnysH3ia6')
response = requests.get(f'https://api.nasa.gov/neo/rest/v1/feed?start_date={START_DATE}&end_date={END_DATE}&api_key={API_KEY}')

uri = "mongodb+srv://aidancdodds:R2mAnrD0dzu1TX9K@cluster0.wvgiffx.mongodb.net/"
# uri = "mongodb+srv://connorcoyle2014:FMuz3JuJcQjb6uD6@cluster0.3zqurog.mongodb.net/"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["test_db"]
nasaData = db["NASA_Data"]
# db = client["Capstoneproject2024"]
# nasaData = db["collectionTwo"]

data = response.json()

def insertOrUpdateRow(dictionary):
    newValue = {"$set": dictionary}
    nasaData.update_one(dictionary, newValue, upsert=True)

# Function which loops through a list and yields each dictionary in the list.
def retrieveDictionariesInList(data):
    # This for loop retrieves the dictionaries within the list, and a
    # separate for loop inserts these dictionaries into a PyMongo table.
    for i in range(len(data)):
        dictionary = data[i]
        yield dictionary

# Iterates through key-value pairs in a dictionary.
for d in data:
    if isinstance(data[d], dict):
        # Iterates through key-value pairs in a nested dictionary.
        # (A dictionary inside another dictionary)
        for n in data[d]:
            # Checks if the value in the key value pair is a list.
            if isinstance(data[d][n], list):
                # Loops through the retrieveDictionariesInList function and inserts
                # dictionaries within a list.
                for nn in retrieveDictionariesInList(data[d][n]):
                    insertOrUpdateRow(nn)
            # Else, the value is not a list and the key and value of the dictionary are inserted.
            else:
                # Insert dictionary if it is not already in the PyMongo table, else
                # update the dictionary with itself.
                dictionary = {d: data[d]}
                insertOrUpdateRow(dictionary)
    else:
        # Insert the key value pair on the top level if the value is not a dictionary.
        dictionary = {d: data[d]}
        insertOrUpdateRow(dictionary)             

# In case you need to clear out the collection in the database.
# deleteData = nasaData.delete_many({})