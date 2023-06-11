import requests
import json
from tinydb import TinyDB, Query,where
from tinydb.database import Document
from pprint import pprint

base_url = 'https://storemarket.pythonanywhere.com/shop/'

class DB:
    def __init__(self, path):
        self.db = TinyDB(path, indent=4, separators=(',', ': '))
        self.users = self.db.table('users')
        self.carts = self.db.table('carts')
        self.products = self.db.table('products')
        self.categories = self.db.table('categories')
        self.sub_categories = self.db.table('sub_categories')

    def get_start(self, chat_id):
        self.delete_start(chat_id=chat_id)
        request = requests.get(base_url + 'start/')
        data = request.json()
        for category in data['result']:
            self.categories.insert({'id': category['id'], 'name': category['name'], 'image': category['image'], "chat_id":int(chat_id)})
            for sub_category in category['sub_category']:
                self.sub_categories.insert({'id': sub_category['id'], 'name': sub_category['name'], 'image': sub_category['image'], 'category': category['id'], "chat_id":int(chat_id)})
                for product in sub_category['products']:
                    self.products.insert({'id': product['id'], 'name': product['name'],'discription': product['discription'], 'image': product['image'], 'price': product['price'], 'sub_category': sub_category['id'], 'category':category['id'], "chat_id":int(chat_id)})
        return data
           
    def get_categories(self, chat_id):
        categories = self.categories.search(Query().chat_id == chat_id)
        return categories
    
    def get_sub_categories(self, categories_id, chat_id):
        chat_id = int(chat_id)
        User = Query()
        data = self.sub_categories.search((User.category == categories_id) & (User.chat_id == chat_id))
        return data
    
    def get_product(self, sub_categories_id, chat_id):
        User = Query()
        data = self.products.search((User.sub_category == sub_categories_id) & (User.chat_id == chat_id))
        return data
    
    def get_product_by_id(self, product_id, chat_id):
        User = Query()
        data = self.products.search((User.id == product_id) & (User.chat_id == chat_id))
        return data
    
    def delete_start(self, chat_id):
        chat_id = int(chat_id)
        User = Query()
        data_categories = self.categories.search(User.chat_id == chat_id)
        data_sub_categories = self.sub_categories.search(User.chat_id == chat_id)
        data_product = self.products.search(User.chat_id == chat_id)

        for i in data_categories:
            self.categories.remove(User.chat_id == chat_id)

        for i in data_sub_categories:
            self.sub_categories.remove(User.chat_id == chat_id)

        for i in data_product:
            self.products.remove(User.chat_id == chat_id)

    def get_products(self, sub_category_id, chat_id):
        User = Query()
        data = self.products.search((User.sub_category == sub_category_id) & (User.chat_id == chat_id))
        return data
    
    def get_next_product(self, product_id, chat_id, sub_category_id):
        User = Query()
        data = self.products.search((User.id > product_id) & (User.sub_category == sub_category_id) & (User.chat_id == chat_id))
        if len(data) == 0:
            data = self.products.search((User.id > 0) & (User.sub_category == sub_category_id) & (User.chat_id == chat_id))
        return data
    
    def get_back_product(self, product_id, chat_id, sub_category_id):
        User = Query()
        data = self.products.search((User.id < product_id) & (User.sub_category == sub_category_id) & (User.chat_id == chat_id))
        if len(data) == 0:
            max_id = self.products.search((User.sub_category == sub_category_id) & (User.chat_id == chat_id))
            data = self.products.search((User.id == max_id[-1]['id']) & (User.sub_category == sub_category_id) & (User.chat_id == chat_id))
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
        user = requests.get(base_url+f'get-user/{chat_id}/')
        return user.json()

    def delete_user(self, chat_id):
        user = requests.post(base_url + 'delete-user/{}/'.format(chat_id))
        return user.json()
    
    def add_cart(self, chat_id, product_id, count, phone, user_id):
        cart_data = {
            'chat_id': chat_id,
            'product': product_id,
            'count': count,
            'phone': phone,
            'user': user_id
        }
        self.carts.insert(cart_data)
        return cart_data
        


    def get_count_cart(self, chat_id):
        User = Query()
        data = self.carts.search((User.chat_id == chat_id) & (User.count == 0))
        return data
    def update_cart(self, chat_id, count):
        User = Query()
        data = self.carts.update({'count': count}, (User.chat_id == chat_id) & (User.count == 0))
        return data

    def get_cart(self, chat_id):
        User = Query()
        data = self.carts.search((User.chat_id == chat_id) & (User.count > 0))
        return data
    
    def get_cart_list(self, chat_id):
        data = self.carts.search(Query().chat_id == chat_id)
        return data
    
    def delete_cart(self, chat_id):
        User = Query()
        data = self.carts.remove((User.chat_id == chat_id) & (User.count > 0))
        return data
    
    def add_order(self, order_list):
        print(order_list)
        # data = requests.post(base_url + 'add-order/', data=order_list)
        # print(data, True)
        return True
    
    def get_orders(self, chat_id):
        user = requests.get(base_url+f'get-user/{chat_id}/').json()
        user_id = user['data']['id']
        orders = requests.get(base_url+f'get-user-order/{user_id}/')
        return orders.json()
    
    def get_contact(self):
        contact = requests.get(base_url + 'contact-store-list/')
        return contact.json()

    def get_admin_by_username(self, username):
        admin = requests.get(base_url + f'get-admin-user/{username}/')
        if admin.status_code == 200:
            return admin.json()
        else:
            return False

# test = DB('db.json')
# get_sub_category = test.get_admin_by_username('storemarket')
# print(get_sub_category)