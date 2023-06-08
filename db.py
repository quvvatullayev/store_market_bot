import requests
import json
from tinydb import TinyDB, Query
from tinydb.database import Document
from pprint import pprint

base_url = 'http://storemarket.pythonanywhere.com/shop/'

class DB:
    def __init__(self, path):
        self.db = TinyDB(path, indent=4, separators=(',', ': '))
        self.users = self.db.table('users')
        self.carts = self.db.table('carts')
        self.products = self.db.table('products')
        self.categories = self.db.table('categories')

    def get_start(self):
        request = requests.get(base_url + 'start/')
        data = request.json()
        category_list = []
        for category in data['result']:
            self.categories.insert(category)
        return category_list
    
    def get_categories(self):
        categories = self.categories.all()
        data = []
        for category in categories:
            data.append({'id': category['id'], 'name': category['name'], 'image': category['image']})
        return data

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
    
    def add_cart(self, chat_id, product_id, count):
        cart_data = {
            'chat_id': chat_id,
            'product': product_id,
            'count': count
        }
        cart = requests.post(base_url + 'add-cart/', data=cart_data)
        return cart

test = DB('db.json')
# start = test.get_start()
# add_user = test.updeate_user(123456)
# add_user = test.add_user('test', 'test', 123456)
# add_user = test.add_user('test', 'test', 123456)
# get_user = test.get_user(123456)
# delete_user = test.delete_user(123456)
# add_cart = test.add_cart(2342, 1, 1)
get_categories = test.get_categories()
print(get_categories)