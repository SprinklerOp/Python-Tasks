import pymongo
client=pymongo.MongoClient(host="mongodb://localhost:27017")
myDB = client.["Vistor"]
myDB.create_collection("collection")
while True:
    myname=input("Enter Your Name:")
    myphone=int(input("Enter your number"))
    mypurpose=input("Enter your query")


    data={
        "name":myname,
        "phone":myphone,
        "purpose":mypurpose
        
        }
    myDB["collection"].insert_one(data)
print(a)
