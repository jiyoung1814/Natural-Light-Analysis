import pymongo
import os
import numpy as np

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    def connect_DB(self):
        try:
            self.client= pymongo.MongoClient(f"mongodb://{os.getenv('mongodb_ip')}:{os.getenv('mongodb_port')}/")
            self.db= self.client[os.getenv('database_name')]
            print(f'connected with MongoDB')

        except Exception as e:
            print(f'MongoDB Connect Error: {e}')

    def save_data(self, collection_name, data):
        '''

        :param collection_name:
        :param data:
        :return:
        '''
        collection = self.db[collection_name]

        if isinstance(data, np.ndarray) or isinstance(data, list):
            # Insert multiple documents
            result = collection.insert_many([vars(d) for d in data])
            return result.inserted_ids
        else:
            # Insert a single document
            result = collection.insert_one(vars(data))
            return result.inserted_id

    def find_data_all(self, collection_name, sort = 'datetime'):
        '''
        collection의 모든 데이터 find (조건 X)
        :param collection_name:
        :param sort: sort할 field 명 (default: datetime)
        :return: class:'pymongo.cursor.Cursor'
        '''
        try:
            collection = self.db[collection_name]

            results = collection.find()
            # results = collection.find().sort(sort, pymongo.ASCENDING)
        except Exception as e:
            print(f'find_data_all Error: {e}')
            results = collection.find()

        return results

    def find_data_excluded(self, collection_name, field= 'datetime', excluded_data=[]):
        '''

        :param collection_name:
        :param field:
        :param excluded_data:
        :return:
        '''

        try:
            collection = self.db[collection_name]
            results = collection.find({field:{"$nin": excluded_data}})
        except Exception as e:
            print(f'find_data_excluded Error: {e}')

        return results

    def getCollectionList(self):
        return self.db.list_collection_names()

    def disconnect(self):
        self.client.close()
