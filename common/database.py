import pymongo
from typing import List, Dict


class Database:
    """
    Database interacts with mongodb which can insert, search, update, and delete data. The port of mongodb is 27017 and the database name is rates.
    """
    URI = 'mongodb://127.0.0.1:27017/rates'
    DATABASE = pymongo.MongoClient(URI).get_database()

    @staticmethod
    def insert_one(collection: str, data: Dict) -> None:
        """
        Insert one document into the collection.
        """
        Database.DATABASE[collection].insert_one(data)

    @staticmethod
    def insert_many(collection: str, data: List[Dict]) -> None:
        """
        Insert a list of documents into the collection.
        """
        Database.DATABASE[collection].insert_many(data)

    @staticmethod
    def find_one(collection: str, query: Dict) -> Dict:
        """
        Return the first document that satisfies the query on the collection.
        """
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find(collection: str, query: Dict) -> pymongo.cursor:
        """
        Return a cursor that satisfies the query on the collection.
        """
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def update_one(collection: str, query: Dict, data: Dict) -> None:
        """
        Find the first document that matches the query and applies the specified update modifications. Create a new document if nothing matches the query.
        """
        Database.DATABASE[collection].update_one(
            query, {"$set": data}, upsert=True)

    @staticmethod
    def delete_one(collection: str, query: Dict) -> None:
        """
        Delete the first document that matches the query.
        """
        Database.DATABASE[collection].delete_one(query)
