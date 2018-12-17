import datetime
import pymongo
# import config

# myclient = pymongo.MongoClient(config.dbtoken)
myclient = pymongo.MongoClient('mongodb://mtaranovsky:963852741t@ds125693.mlab.com:25693/debtsbot')


mydb = myclient["debtsbot"]

mycol = mydb["Users"]


class MongoManager:
    @classmethod
    def save(cls, record, col):
        col.insert_one(record)

    @classmethod
    def partner_debt_update(cls, username, partner, value, col):
        col.update_one(
            {
                'username': username, 'debts.partner': partner
            },
            {
                "$set": {"debts.$.debt": value, 'debts.$.data': datetime.datetime.now()}})

    @classmethod
    def debt_update(cls, username, debt, col):
        col.update_one(
            {
                'username': username
            },
            {
                "$set": {"debts": debt}})

    def request(self, username, partner, summ):
        debts_u = []
        debts_p = []
        sumo_p = 0
        sumo_u = 0
        dict_user = {"partner": partner, "debt": summ, 'data': datetime.datetime.now()}
        dict_p = {"partner": username, "debt": summ, 'data': datetime.datetime.now()}
        users_u = {'username': username, 'debts': debts_u}
        users_p = {'username': partner, 'debts': debts_p}
        get_debt_u = mycol.find_one({'username': username, 'debts.partner': partner},
                                    {'_id': 0, 'debts.debt': 1, 'debts.partner': 1})
        get_debt_p = mycol.find_one({'username': partner, 'debts.partner': username},
                                    {'_id': 0, 'debts.debt': 1, 'debts.partner': 1})

        if mycol.find_one({'username': username}, {'_id': 0, 'username': 1}) is None:
            debts_u.append(dict_user)
            debts_p.append(dict_p)
            # mycol.insert_one(users_u)
            self.save(users_u, mycol)
            if mycol.find_one({'username': partner}, {'_id': 0, 'username': 1}) is None:
                # mycol.insert_one(users_p)
                self.save(users_p, mycol)
            else:
                array = dict(mycol.find_one({'username': partner}, {'_id': 0, 'debts': 1}))

                asd1 = array['debts']
                asd1.append(dict_p)
                self.debt_update(partner, asd1, mycol)
                # mycol.update_one(
                #     {
                #         'username': partner
                #     },
                #     {
                #         "$set": {"debts": asd1}})

        elif get_debt_u is None:
            array = dict(mycol.find_one({'username': username}, {'_id': 0, 'debts': 1}))
            asd = array['debts']
            asd.append(dict_user)
            mycol.update_one(
                {
                    'username': username
                },
                {
                    "$set": {"debts": asd}})
            if mycol.find_one({'username': partner}, {'_id': 0, 'username': 1}) is None:
                debts_p.append(dict_p)
                # y = mycol.insert_one(users_p)
                self.save(users_p, mycol)
            else:
                array = dict(mycol.find_one({'username': partner}, {'_id': 0, 'debts': 1}))

                asd1 = array['debts']
                asd1.append(dict_p)
                mycol.update_one(
                    {
                        'username': partner
                    },
                    {
                        "$set": {"debts": asd1}})

        else:
            for i in dict(get_debt_u)['debts']:
                if i['partner'] == partner:
                    sumo_u = i['debt']

            for i in dict(get_debt_p)['debts']:
                if i['partner'] == username:
                    sumo_p = i['debt']

        # mycol.update_one(
        #     {
        #         'username': username, 'debts.partner': partner
        #     },
        #     {
        #         "$set": {"debts.$.debt": sumo_u + sum, 'debts.$.data': datetime.datetime.now()}})
        self.partner_debt_update(username, partner, sumo_u + summ, mycol)
        self.partner_debt_update(partner, username, sumo_p - summ, mycol)
        # mycol.update_one(
        #     {
        #         'username': partner, 'debts.partner': username
        #     },
        #     {
        #         "$set": {"debts.$.debt": sumoP - sum, 'debts.$.data': datetime.datetime.now()}})
        #
        for row in mycol.find():
            print(row)

    @classmethod
    def feedback(cls, username):
        get_debt = mycol.find_one({'username': username},
                                  {'_id': 0, 'debts.debt': 1, 'debts.partner': 1})
        result = "Твій фінансовий журнал: \n"
        for i in dict(get_debt)['debts']:
            if i["debt"] < 0:
                result += "Ти заборгував "+i["partner"]+" "+str(-i["debt"])+"грн.\n"
            if i["debt"] >= 0:
                result += i["partner"]+" заборгував тобі"+" "+str(i["debt"])+"грн.\n"
        return result
