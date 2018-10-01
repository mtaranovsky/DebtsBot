import pymongo
import datetime
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["Debts"]
debts=[]
mycol = mydb["Users"]
mydict = {"partner": "Andrew","debts": 70, 'data':datetime.datetime.now()}
# mydict1 = {"partner": "Andrew","debts": 520}
# mydict2 = {"partner": "Andrew","debts": 50}
# mydict3 = {"partner": "Andrew","debts": 90}
# mydict4 = {"partner": "Andrew","debts": 80}
debts.append(mydict)
# debts.append(mydict1)
# debts.append(mydict2)
# debts.append(mydict3)
# debts.append(mydict4)
users = {'username': 'User', 'debts': debts}
x = mycol.insert_one(users)

def request(username,partner,sum):
    for x in mycol.find({}, {"username":username}):