import pymongo
import datetime
myclient = pymongo.MongoClient("mongodb://mtaranovsky:963852741t@ds125693.mlab.com:25693/debtsbot")
mydb = myclient["debtsbot"]
debtsU=[]
debtsP=[]
mycol = mydb["Users"]


def request(username,partner,sum):
    sumoP=0
    sumoU=0
    mydictUser = {"partner": partner, "debt": sum, 'data': datetime.datetime.now()}
    mydictP = {"partner": partner, "debt": sum, 'data': datetime.datetime.now()}
    usersU = {'username': username, 'debts': debtsU}
    mydictP = {"partner": username, "debt": -sum, 'data': datetime.datetime.now()}
    usersP = {'username': partner, 'debts': debtsP}
    getDebtU = mycol.find_one({'username': username, 'debts.partner': partner}, {'_id': 0, 'debts.debt': 1, 'debts.partner': 1})
    getDebtP = mycol.find_one({'username': partner, 'debts.partner': username},
                              {'_id': 0, 'debts.debt': 1, 'debts.partner': 1})

    if mycol.find_one({'username': username}, {'_id': 0, 'username': 1}) == None:
        debtsU.append(mydictUser)
        debtsP.append(mydictP)
        x = mycol.insert_one(usersU)
        y = mycol.insert_one(usersP)
    elif getDebtU == None:
        array = dict(mycol.find_one({'username': username}, {'_id': 0, 'debts': 1}))
        asd = array['debts']
        asd.append(mydictUser)
        mycol.update_one(
            {
                'username': username
            },
            {
                "$set": {"debts": asd}})

        array = dict(mycol.find_one({'username': partner}, {'_id': 0, 'debts': 1}))
        asd = array['debts']
        asd.append(mydictP)
        mycol.update_one(
            {
                'username': partner
            },
            {
                "$set": {"debts": asd}})

    else:
        for i in dict(getDebtU)['debts']:
            if i['partner'] == partner:
                sumoU = i['debt']

        for i in dict(getDebtP)['debts']:
            if i['partner'] == username:
                sumoP = i['debt']

    mycol.update_one(
        {
            'username': username, 'debts.partner': partner
        },
        {
            "$set": {"debts.$.debt": sumoU + sum, 'debts.$.data': datetime.datetime.now()}})

    mycol.update_one(
        {
            'username': partner, 'debts.partner': username
        },
        {
            "$set": {"debts.$.debt": sumoP - sum, 'debts.$.data': datetime.datetime.now()}})
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







