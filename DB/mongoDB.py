from pymongo import errors, MongoClient
import os
import numpy as np


class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    def connect_DB(self, data_type = 'Natural'):
        try:
            self.client= MongoClient(f"mongodb://{os.getenv('mongodb_ip')}:{os.getenv('mongodb_port')}/")
            if data_type == 'Natural':
                self.db= self.client[os.getenv('database_name')]
            elif data_type == 'Natural_Satellite':
                self.db = self.client[os.getenv('database_Natural_satellite_name')]
            elif data_type == 'Satellite':
                self.db = self.client[os.getenv('database_satellite_name')]
            print(f'connected with MongoDB_{data_type}')

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
            try:
                if isinstance(data[0], dict):
                    result = collection.insert_many(data.tolist())
                else:
                    result = collection.insert_many([vars(d) for d in data])
                return result.inserted_ids
            except Exception as e:
                print(f"Save Somethings to DB Error: {e}")
        else:
            try:
                # Insert a single document
                if isinstance(data, dict):
                    result = collection.insert_one(data)
                else:
                    result = collection.insert_one(vars(data))
                return result.inserted_id
            except Exception as e:
                print(f"Save Something to DB Error: {e}")

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

    def find_data_between_fields(self, collection_name, start, end, field = 'datetime'):
        """
        DB 검색 시 원하는 필드의 사이값 추출
        :param collection_name:
        :param start:
        :param end:
        :param field: str ex) "datetime", "timestamp"
        :return:
        """

        try:
            collection = self.db[collection_name]
            results = collection.find({field:{"$gte": start, "$lte": end}})
        except Exception as e:
            print(f'find_data_during_dates Error: {e}')

        return results

    def find_data_excluded(self, collection_name, field= 'datetime', excluded_data=[]):
        """

        :param collection_name:
        :param field:
        :param excluded_data:
        :return:
        """

        try:
            collection = self.db[collection_name]
            results = collection.find({field:{"$nin": excluded_data}})
        except Exception as e:
            print(f'find_data_excluded Error: {e}')

        return results

    def check_unique_data(self, collection_name, field, value):
        """
        DB의 해당 필드값의 동일한 값을 가진 것이 있는지 확인 (True: 동일한 값이 없음)
        :param collection_name:
        :param field:
        :param value:
        :return:
        """
        try:
            collection = self.db[collection_name]
            existing_data  = collection.find_one({field: value})

            if existing_data is None:
                return True
            else:
                return False

        except Exception as e:
            print(f'check_unique_data Error: {e}')

    def getCollectionList(self):
        return self.db.list_collection_names()

    def disconnect(self):
        self.client.close()

