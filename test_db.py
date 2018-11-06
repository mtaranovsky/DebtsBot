import mongomock
import unittest
import datetime

from db import MongoManager


mock_collection = mongomock.MongoClient().db.collection



class MockMongoManager(MongoManager):

    def __init__(self):
        self.db_conn = mock_collection


class TestStuff(unittest.TestCase):

    def test_partner_debt_update(self):
        debtsTest = []
        mydictTest = {"partner": "B", "debt": 10, 'data': datetime.datetime.now()}
        debtsTest.append(mydictTest)
        usersTest = {'username': "A", 'debts': debtsTest}
        mock_collection.insert_one(usersTest)
        mongo = MockMongoManager()
        mongo.partner_debt_update("A", "B", 20, mongo.db_conn)
        result=mock_collection.find_one({'username': "A"},{'_id': 0,"username":1,"debts.partner":1,"debts.debt":1})
        print(result)
        self.assertDictEqual(result, {'username': 'A', 'debts': [{'partner': 'B', 'debt': 20}]})

    def test_debt_update(self):
        debtsTest = []
        mydictTest = {"partner": "B", "debt": 10, 'data': datetime.datetime.now()}
        debtsTest.append(mydictTest)
        usersTest = {'username': "A", 'debts': []}
        mock_collection.insert_one(usersTest)
        mongo = MockMongoManager()
        mongo.debt_update("A", debtsTest, mongo.db_conn)
        result = mock_collection.find_one({'username': "A"},
                                          {'_id': 0, "username": 1, "debts.partner": 1, "debts.debt": 1})
        self.assertDictEqual(result, {'username': 'A', 'debts': [{'partner': 'B', 'debt': 10}]})

    def test_save(self):
        mongo = MockMongoManager()
        a = {'a': 123}
        mongo.save(a, mongo.db_conn)
        result = mock_collection.find_one({'a': 123}, {'_id': 0})
        self.assertDictEqual(result, {'a': 123})


if __name__ == '__main__':
    unittest.main()