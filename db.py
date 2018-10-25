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





#
# sumo=70

#
#

#
def request(username,partner,sum):
    mydict = {"partner": partner, "debt": sum, 'data': datetime.datetime.now()}
    users = {'username': username, 'debts': debts}

    getDebt = mycol.find_one({'username': username, 'debts.partner': partner}, {'_id': 0, 'debts.debt': 1, 'debts.partner': 1})

    if mycol.find_one({'username': username}, {'_id': 0, 'username': 1}) == None:
        debts.append(mydict)
        x = mycol.insert_one(users)
    elif getDebt == None:
        array = dict(mycol.find_one({'username': username}, {'_id': 0, 'debts': 1}))
        asd = array['debts']
        asd.append(mydict)
        mycol.update_one(
            {
                'username': username
            },
            {
                "$set": {"debts": asd}})

    else:
        for i in dict(getDebt)['debts']:
            if i['partner'] == partner:
                sumo = i['debt']

    mycol.update_one(
        {
            'username': username, 'debts.partner': partner
        },
        {
            "$set": {"debts.$.debt": sumo + sum, 'debts.$.data': datetime.datetime.now()}})
    #
    for x in mycol.find():
        print(x)



def feedback(username,partner):
    getDebt = mycol.find_one({'username': username, 'debts.partner': partner},
                             {'_id': 0, 'debts.debt': 1, 'debts.partner': 1})
    for i in dict(getDebt)['debts']:
        if i['partner'] == partner:
            sumo = i['debt']

    return sumo







