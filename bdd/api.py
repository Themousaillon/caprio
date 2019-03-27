from pymongo import MongoClient

class mongoApi():
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.caprio
        self.position = self.db.position

    def insertPosition(self, position):
        self.position.insert_one(position)

