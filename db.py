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
        self.sub_categories = self.db.table('sub_categories')

    def get_start(self):
        request = requests.get(base_url + 'start/')
        data = request.json()
        for category in data['result']:
            self.categories.insert({'id': category['id'], 'name': category['name'], 'image': category['image']})
            for sub_category in category['sub_category']:
                self.sub_categories.insert(Document({'id': sub_category['id'], 'name': sub_category['name'], 'image': sub_category['image'], 'category': category['id']}, doc_id=sub_category['id']))
                for product in sub_category['products']:
                    self.products.insert(Document({'id': product['id'], 'name': product['name'], 'image': product['image'], 'price': product['price'], 'sub_category': sub_category['id'], 'category':category['id']}, doc_id=product['id']))
        return data
           
    def get_categories(self):
        categories = self.categories.all()
        return categories
    
    def get_sub_categories(self, categories_id):
        data = self.sub_categories.search(Query().category == categories_id)
        return data
    
    def get_product(self, sub_categories_id):
        data = self.products.search(Query().sub_category == sub_categories_id)
        return data

    def get_products(self, category_id):
        products = self.categories

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

# test = DB('db.json')
# get_sub_category = test.get_product(5)
# print(get_sub_category)