import requests
import json
from tinydb import TinyDB, Query
from tinydb.database import Document

base_url = 'http://storemarket.pythonanywhere.com/shop/'

class DB:
    def __init__(self, path):
        self.db = TinyDB(path)

    def get_start(self):
        request = requests.get(base_url + 'start/')
        data = request.json()
        print(data)
        print(type(data))

    def add_user(self, username, name, chat_id, phone_number=11):
        user_data = {
            'username': username,
            'name': name,
            'chat_id': chat_id,
            'phone': phone_number
        }

        user = requests.post(base_url + 'add-user/', data=user_data)
        return user.json()
    
    def updeate_user(self,chat_id, phone_number):
        user_data = {
            'chat_id': chat_id,
            'phone': phone_number
        }
        user = requests.post(base_url + 'update-user/', data=user_data)
        return user.json()
    
    def get_user(self, chat_id):
        user = requests.get(base_url + 'get-user/{}/'.format(chat_id))
        return user.json()

    def delete_user(self, chat_id):
        user = requests.post(base_url + 'delete-user/{}/'.format(chat_id))
        return user.json()

test = DB('db.json')
# start = test.get_start()
# add_user = test.updeate_user(123456)
# add_user = test.add_user('test', 'test', 123456)
# add_user = test.add_user('test', 'test', 123456)
# get_user = test.get_user(123456)
# delete_user = test.delete_user(123456)