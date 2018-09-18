import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["Debts"]

mycol = mydb["Users"]
mydict = { "name": "Kolya","partner": "Andrew","debts": 30}

x = mycol.insert_one(mydict)
