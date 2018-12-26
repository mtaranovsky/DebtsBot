import datetime
import functools
import logging
import time
import pymongo
import config



MAX_AUTO_RECONNECT_ATTEMPTS = 8
MAX_TIMEOUT = 120

def graceful_auto_reconnect(mongo_op_func):
    @functools.wraps(mongo_op_func)
    def wrapper(*args, **kwargs):
        attempt = 0
        # for attempt in range(MAX_AUTO_RECONNECT_ATTEMPTS):
        while True:
            try:
                return mongo_op_func(*args, **kwargs)
            except pymongo.errors.AutoReconnect as err:

                wait_t = pow(2, attempt)        # exponential back off
                if MAX_AUTO_RECONNECT_ATTEMPTS > attempt and MAX_TIMEOUT > wait_t:
                    attempt = attempt + 1
                else:
                    wait_t = MAX_TIMEOUT

                logging.warning("PyMongo auto-reconnecting... %s. Waiting %.1f seconds.",
                                str(err), wait_t)
                time.sleep(wait_t)
    return wrapper

myclient = pymongo.MongoClient(config.testdbtoken)


mydb = myclient["debtsbot"]

mycol = mydb["Users"]


class MongoManager:
    @classmethod
    @graceful_auto_reconnect
    def save(cls, record, col):
        col.insert_one(record)

    @classmethod
    @graceful_auto_reconnect
    def partner_debt_update(cls, user_id, partner_id, value, col):
        col.update_one(
            {
                'user_id': user_id, 'debts.partner_id': partner_id
            },
            {
                "$set": {"debts.$.debt": value, 'debts.$.data': datetime.datetime.now()}})

    @classmethod
    @graceful_auto_reconnect
    def debt_update(cls, user_id, debt, col):
        col.update_one(
            {
                'user_id': user_id
            },
            {
                "$set": {"debts": debt}})

    @graceful_auto_reconnect
    def request(self, user_id, partner_id, summ):
        debts_u = []
        debts_p = []
        sumo_p = 0
        sumo_u = 0
        dict_user = {"partner_id": partner_id, "debt": summ, 'data': datetime.datetime.now()}
        dict_p = {"partner_id": user_id, "debt": summ, 'data': datetime.datetime.now()}
        users_u = {'user_id': user_id, 'debts': debts_u}
        users_p = {'user_id': partner_id, 'debts': debts_p}
        get_debt_u = mycol.find_one({'user_id': user_id, 'debts.partner_id': partner_id},
                                    {'_id': 0, 'debts.debt': 1, 'debts.partner_id': 1})
        get_debt_p = mycol.find_one({'user_id': partner_id, 'debts.partner_id': user_id},
                                    {'_id': 0, 'debts.debt': 1, 'debts.partner_id': 1})

        if mycol.find_one({'user_id': user_id}, {'_id': 0, 'user_id': 1}) is None:
            debts_u.append(dict_user)
            debts_p.append(dict_p)
            self.save(users_u, mycol)
            if mycol.find_one({'user_id': partner_id}, {'_id': 0, 'user_id': 1}) is None:
                self.save(users_p, mycol)
            else:
                array = dict(mycol.find_one({'user_id': partner_id}, {'_id': 0, 'debts': 1}))

                asd1 = array['debts']
                asd1.append(dict_p)
                self.debt_update(partner_id, asd1, mycol)
        elif get_debt_u is None:
            array = dict(mycol.find_one({'user_id': user_id}, {'_id': 0, 'debts': 1}))
            asd = array['debts']
            asd.append(dict_user)
            mycol.update_one(
                {
                    'user_id': user_id
                },
                {
                    "$set": {"debts": asd}})
            if mycol.find_one({'user_id': partner_id}, {'_id': 0, 'user_id': 1}) is None:
                debts_p.append(dict_p)
                self.save(users_p, mycol)
            else:
                array = dict(mycol.find_one({'user_id': partner_id}, {'_id': 0, 'debts': 1}))

                asd1 = array['debts']
                asd1.append(dict_p)
                mycol.update_one(
                    {
                        'user_id': partner_id
                    },
                    {
                        "$set": {"debts": asd1}})

        else:
            for i in dict(get_debt_u)['debts']:
                if i['partner_id'] == partner_id:
                    sumo_u = i['debt']

            for i in dict(get_debt_p)['debts']:
                if i['partner_id'] == user_id:
                    sumo_p = i['debt']

        self.partner_debt_update(user_id, partner_id, sumo_u + summ, mycol)
        self.partner_debt_update(partner_id, user_id, sumo_p - summ, mycol)

        for row in mycol.find():
            print(row)

    @classmethod
    @graceful_auto_reconnect
    def feedback(cls, user_id):
        get_debt = mycol.find_one({'user_id': user_id},
                                  {'_id': 0, 'debts.debt': 1, 'debts.partner_id': 1})
        result = "Твій фінансовий журнал: \n"
        for i in dict(get_debt)['debts']:
            if i["debt"] < 0:
                result += "Ти заборгував "+i["partner_id"]+" "+str(-i["debt"])+"грн.\n"
            if i["debt"] >= 0:
                result += i["partner_id"]+" заборгував тобі"+" "+str(i["debt"])+"грн.\n"
        return result
