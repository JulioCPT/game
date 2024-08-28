import pymongo

class HighscoreModel:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="game_db", collection_name="highscores"):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_highscores(self, limit=10):
        return list(self.collection.find().sort("tempo", pymongo.DESCENDING).limit(limit))

    def save_highscore(self, tempo):
        self.collection.insert_one({"tempo": tempo})

