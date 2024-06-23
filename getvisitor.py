import pymongo
client=pymongo.MongoClient(host="mongodb://localhost:27017")
myDB = client.["Vistor"]
myDB.create_collection("collection")
