import pymongo
import certifi

mongo_url = "mongodb+srv://bbryant572:DartNinja$9821!@cluster0.j081n.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

client = pymongo.MongoClient(mongo_url, tlsCAFile=certifi.where())

db = client.get_database("DartWizardSuppliesCh25")
