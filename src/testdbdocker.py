import pymongo
import unittest
import datetime
import config

from db import MongoManager

myclient = pymongo.MongoClient(config.testdbtoken)
mydb = myclient["debtsbot"]
mycol = mydb["Users"]


class TestMongoManager(MongoManager):

    def __init__(self):
        self.db_conn = mycol


class TestStuff(unittest.TestCase):

    def test_partner_debt_update(self):
        debtsTest = []
        mydictTest = {"partner": "B", "debt": 10, 'data': datetime.datetime.now()}
        debtsTest.append(mydictTest)
        usersTest = {'username': "A", 'debts': debtsTest}
        mycol.insert_one(usersTest)
        mongo = TestMongoManager()
        mongo.partner_debt_update("A", "B", 20, mongo.db_conn)
        result=mycol.find_one({'username': "A"},{'_id': 0,"username":1,"debts.partner":1,"debts.debt":1})
        print(result)
        self.assertDictEqual(result, {'username': 'A', 'debts': [{'partner': 'B', 'debt': 20}]})

    def test_debt_update(self):
        debtsTest = []
        mydictTest = {"partner": "B", "debt": 10, 'data': datetime.datetime.now()}
        debtsTest.append(mydictTest)
        usersTest = {'username': "A", 'debts': []}
        mycol.insert_one(usersTest)
        mongo = TestMongoManager()
        mongo.debt_update("A", debtsTest, mongo.db_conn)
        result = mycol.find_one({'username': "A"},
                                          {'_id': 0, "username": 1, "debts.partner": 1, "debts.debt": 1})
        self.assertDictEqual(result, {'username': 'A', 'debts': [{'partner': 'B', 'debt': 10}]})

    def test_save(self):
        mongo = TestMongoManager()
        a = {'a': 123}
        mongo.save(a, mongo.db_conn)
        result = mycol.find_one({'a': 123}, {'_id': 0})
        self.assertDictEqual(result, {'a': 123})


if __name__ == '__main__':
    unittest.main()