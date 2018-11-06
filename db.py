import pymongo
import datetime
import config
myclient = pymongo.MongoClient(config.dbtoken)
mydb = myclient["debtsbot"]

mycol = mydb["Users"]

class MongoManager:
    def save(self,a,v):
        v.insert_one(a)

    def partnerDebtUdate(self,username, partner, sum,col):
        col.update_one(
            {
                'username': username, 'debts.partner': partner
            },
            {
                "$set": {"debts.$.debt": sum, 'debts.$.data': datetime.datetime.now()}})

    def debtUpdate(self,username, debt,col):
        col.update_one(
            {
                'username': username
            },
            {
                "$set": {"debts": debt}})

    def request(self, username, partner, summ):
        debtsU = []
        debtsP = []
        sumoP=0
        sumoU=0
        mydictUser = {"partner": partner, "debt": summ, 'data': datetime.datetime.now()}
        mydictP = {"partner": username, "debt": summ, 'data': datetime.datetime.now()}
        usersU = {'username': username, 'debts': debtsU}
        usersP = {'username': partner, 'debts': debtsP}
        getDebtU = mycol.find_one({'username': username, 'debts.partner': partner}, {'_id': 0, 'debts.debt': 1, 'debts.partner': 1})
        getDebtP = mycol.find_one({'username': partner, 'debts.partner': username},
                                  {'_id': 0, 'debts.debt': 1, 'debts.partner': 1})

        if mycol.find_one({'username': username}, {'_id': 0, 'username': 1}) == None:
            debtsU.append(mydictUser)
            debtsP.append(mydictP)
            # mycol.insert_one(usersU)
            self.save(usersU,mycol)
            if mycol.find_one({'username': partner}, {'_id': 0, 'username': 1}) == None:
                # mycol.insert_one(usersP)
                self.save(usersP, mycol)
            else:
                array = dict(mycol.find_one({'username': partner}, {'_id': 0, 'debts': 1}))

                asd1 = array['debts']
                asd1.append(mydictP)
                self.debtUpdate(partner,asd1,mycol)
                # mycol.update_one(
                #     {
                #         'username': partner
                #     },
                #     {
                #         "$set": {"debts": asd1}})

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
            if mycol.find_one({'username': partner}, {'_id': 0, 'username': 1}) == None:
                debtsP.append(mydictP)
                # y = mycol.insert_one(usersP)
                self.save(usersP, mycol)
            else:
                array = dict(mycol.find_one({'username': partner}, {'_id': 0, 'debts': 1}))

                asd1 = array['debts']
                asd1.append(mydictP)
                mycol.update_one(
                    {
                        'username': partner
                    },
                    {
                        "$set": {"debts": asd1}})

        else:
            for i in dict(getDebtU)['debts']:
                if i['partner'] == partner:
                    sumoU = i['debt']

            for i in dict(getDebtP)['debts']:
                if i['partner'] == username:
                    sumoP = i['debt']

        # mycol.update_one(
        #     {
        #         'username': username, 'debts.partner': partner
        #     },
        #     {
        #         "$set": {"debts.$.debt": sumoU + sum, 'debts.$.data': datetime.datetime.now()}})
        self.partnerDebtUdate(username, partner, sumoU + summ, mycol)
        self.partnerDebtUdate(partner, username, sumoP - summ, mycol)
        # mycol.update_one(
        #     {
        #         'username': partner, 'debts.partner': username
        #     },
        #     {
        #         "$set": {"debts.$.debt": sumoP - sum, 'debts.$.data': datetime.datetime.now()}})
        #
        for x in mycol.find():
            print(x)





    def feedback(username):
        getDebt = mycol.find_one({'username': username}, {'_id': 0, 'debts.debt': 1, 'debts.partner': 1})
        a="Твій фінансовий журнал: \n"

        for i in dict(getDebt)['debts']:
            if i["debt"]<0:

                a += "Ти заборгував "+i["partner"]+" "+str(-i["debt"])+"грн.\n"
            if i["debt" ]>= 0:

                a += i["partner"]+" заборгував тобі"+" "+str(i["debt"])+"грн.\n"

        return a




