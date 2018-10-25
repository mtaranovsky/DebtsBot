import pymongo
import datetime
myclient = pymongo.MongoClient("mongodb://mtaranovsky:963852741t@ds125693.mlab.com:25693/debtsbot")
mydb = myclient["debtsbot"]
debts=[]
mycol = mydb["Users"]
# mydict = {"partner": "Andrew","debt": 70, 'data':datetime.datetime.now()}
# mydict1 = {"partner": "Petro","debt": 520, 'data':datetime.datetime.now()}
# mydict2 = {"partner": "Ivan","debt": 50, 'data':datetime.datetime.now()}
#
# debts.append(mydict)
# debts.append(mydict1)
# debts.append(mydict2)
# debts.append(mydict3)
# debts.append(mydict4)
# users = {'username': 'Kolya', 'debts': debts}
#
# x = mycol.insert_one(users)
# myquery = { "debt.debts.debt": 50 }
# newvalues = { "$set": {"debt.debts.debt": 800}}
# # myquery = {"debts.debt": 50}
# #
# #  = mycol.find(myquery)
# mydoc = mycol.update_one(myquery, newvalues)
#
testsum=mycol.find_one({'username':'Vasyl','debts.partner':'Andrew'},{'_id':0,'debts.debt':1,'debts.partner':1})
print(testsum)
sumo=70
if testsum==None:
    mydict = {"partner": "Andrew", "debt": sumo, 'data': datetime.datetime.now()}
    debts.append(mydict)
    users = {'username': 'Vasyl', 'debts': debts}
    x = mycol.insert_one(users)
else:
    array=dict(testsum)
    asd = array['debts']
    print(asd)
    for i in asd:
        if i['partner']=='Andrew':
            print(i['debt'])
            sumo=i['debt']
# print(type(list[2]))

# mycol.update_one(
#   {
#     "debts.debt": 50
#   },
#   {
#     "$set" : { "debts.$.debt": 800 }
#   }
# )
mycol.update_one(
      {
        'username':'Vasyl','debts.partner':'Andrew'
      },
      {
        "$set" : { "debts.$.debt": sumo+5,'data':datetime.datetime.now()}})

for x in mycol.find():
  print(x)
#
#

#
def request(username,partner,sum):
  testsum = mycol.find_one({'username': username, 'debts.partner': partner},{'_id': 0, 'debts.debt': 1, 'debts.partner': 1})
  array = dict(testsum)
  asd = array['debts']
  for i in asd:
    if i['partner'] == partner:
      print(i['debt'])
      sumo = i['debt']
  mycol.update_one(
      {
        'username':username,'debts.$.partner':partner
      },
      {
        "$set" : { "debts.$.debt": sumo+sum,'data':datetime.datetime.now()}})



