from telegram import (
    Update, 
    ReplyKeyboardMarkup, 
    ReplyMarkup, 
    KeyboardButton, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    )
from telegram.ext import CallbackContext
from db import DB
from main import Shop

shop = Shop()
db = DB('db.json')
base_url = 'https://storemarket.pythonanywhere.com'

class Order:
    def __init__(self) -> None:
        pass

    def get_order(self, update: Update, context: CallbackContext):
        bot = context.bot
        chat_id = update.message.chat_id

        text = 'Iltimos kuting...'
        bot.send_message(chat_id=chat_id, text=text)
        
        try:
            user = db.get_user(chat_id=chat_id)['data']

            text = f'📝 Zakazlarim\n\n'
            text += f'👤 Foydalanuvchi: {user["name"]}\n\n'
            text += f"👤 Username: @{user['username']}\n\n"
            text += f'📞 Telefon raqam: {user["phone"]}\n\n'
            text += f'📦 Buyurtmalar:\n\n'

            orders = db.get_orders(chat_id=chat_id)['data']

            sum_all = 0
            if orders:
                for order in orders:
                    text += f'🧩 {order["product"]["name"]}\n'
                    text += f'💵 Narxi: {order["product"]["price"]} so\'m\n'
                    text += f'🧮 Soni: {order["count"]} ta\n'
                    text += f'💰 {order["count"]} x {order["product"]["price"]} = {order["count"] * order["product"]["price"]} so\'m\n\n'
                    sum_all += order["count"] * order["product"]["price"]
                text += f'💰 Jami: {sum_all} so\'m\n\n'

            else:
                text += '📦 Siz hali buyurtma bermagansiz'

            keyboard = [
                [KeyboardButton('✅ yuborilgan buyurtmalar')],
                [KeyboardButton('☑️ yuborilmagan buyurtmalar')],
                [KeyboardButton('🏠 Bosh sahifa')],
            ]

            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
            bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        except:
            text = '📦 Siz hali buyurtma bermagansiz\n\n'
            text += '❗️ Yoki siz ro\'yxatdan o\'tmagansiz\n\n'
            text += '🔐 Ro\'yxatdan o\'tish tugmasini bosing'
            bot.send_message(chat_id=chat_id, text='📦 Siz hali buyurtma bermagansiz')

    def get_information(self, update: Update, context: CallbackContext):
        bot = context.bot
        chat_id = update.message.chat_id

        text = '🆔 Buyurtma id raqamini kiriting\n\n'
        text += 'Masalan: 1'
        bot.send_message(chat_id=chat_id, text=text)

    def get_order_by_id(self, update: Update, context: CallbackContext):
        bot = context.bot
        chat_id = update.message.chat_id
        text = update.message.text

        try:
            order_id = int(text)
            order = db.get_order_by_id(order_id=order_id)['data']
            product = order['product']
            user = order['user']

            text = f'📝 Zakazlarim\n\n'
            if order['status']:
                text += f'📦 Buyurtma yuborilgan🆗\n\n'
            else:
                text += f'📦 Buyurtma yuborilmagan🚫\n\n'
            text += f'🆔 Buyurtma id: {order["id"]}\n'
            text += f'👤 Foydalanuvchi: {user["name"]}\n'
            text += f"👤 Username: @{user['username']}\n"
            text += f'📞 Telefon raqam: {user["phone"]}\n'
            text += f'📦 Buyurtma:\n\n'
            text += f'🧩 {product["name"]}\n'
            text += f'💵 Narxi: {product["price"]} so\'m\n'
            text += f'🧮 Soni: {order["count"]} ta\n'
            text += f'💰 {order["count"]} x {product["price"]} = {order["count"] * product["price"]} so\'m\n\n'

            reply_markup = ReplyKeyboardMarkup([[KeyboardButton('🏠 Bosh sahifa')]], resize_keyboard=True)
            bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        except:
            text = '❗️ Xatolik yuz berdi\n'
            text += "Bu buyurtma id raqami mavjud emas\n\n"
            text += '🆔 Buyurtma id raqamini kiriting\n\n'
            text += 'Masalan: 1'
            bot.send_message(chat_id=chat_id, text=text)
    
    def get_order_status_false(self, update: Update, context: CallbackContext):
        bot = context.bot
        chat_id = update.message.chat_id

        text = 'Iltimos kuting...'
        bot.send_message(chat_id=chat_id, text=text)

        try:
            user = db.get_user(chat_id=chat_id)['data']

            text = f'📝 Kelgan zakazlar\n\n'
            text += f'👤 Foydalanuvchi: {user["name"]}\n\n'
            text += f"👤 Username: @{user['username']}\n\n"
            text += f'📞 Telefon raqam: {user["phone"]}\n\n'
            text += f'📦 Buyurtmalar:\n\n'

            orders = db.get_orders(chat_id=chat_id)['data']

            sum_all = 0
            if orders:
                text += f'☑️ Buyurtma yetkazib berilmagan\n\n'

                for order in orders:
                    if not order['status']:
                        text += f'🆔 Buyurtma id: {order["id"]}\n'
                        text += f'🧩 {order["product"]["name"]}\n'
                        text += f'💵 Narxi: {order["product"]["price"]} so\'m\n'
                        text += f'🧮 Soni: {order["count"]} ta\n'
                        text += f'💰 {order["count"]} x {order["product"]["price"]} = {order["count"] * order["product"]["price"]} so\'m\n\n'
                        sum_all += order["count"] * order["product"]["price"]
                text += f'💰 Jami: {sum_all} so\'m\n\n'

            else:
                text += '📦 Siz hali buyurtma bermagansiz'

            keyboard = [
                [KeyboardButton('✅ yuborilgan buyurtmalar')],
                [KeyboardButton('☑️ yuborilmagan buyurtmalar')],
                [KeyboardButton('🏠 Bosh sahifa')],
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
            bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        except:
            text = '📦 Siz hali buyurtma bermagansiz\n\n'
            text += '❗️ Yoki siz ro\'yxatdan o\'tmagansiz\n\n'
            text += '🔐 Ro\'yxatdan o\'tish tugmasini bosing'
            bot.send_message(chat_id=chat_id, text='📦 Siz hali buyurtma bermagansiz')

    def get_order_status_true(self, update: Update, context: CallbackContext):
        bot = context.bot
        chat_id = update.message.chat_id

        text = 'Iltimos kuting...'
        bot.send_message(chat_id=chat_id, text=text)

        try:
            user = db.get_user(chat_id=chat_id)['data']

            text = f'📝 Kelgan zakazlar\n\n'
            text += f'👤 Foydalanuvchi: {user["name"]}\n\n'
            text += f"👤 Username: @{user['username']}\n\n"
            text += f'📞 Telefon raqam: {user["phone"]}\n\n'
            text += f'📦 Buyurtmalar:\n\n'

            orders = db.get_orders(chat_id=chat_id)['data']

            sum_all = 0
            if orders:
                text += f'✅ Buyurtma yetkazib berilgan\n\n'

                for order in orders:
                    if order['status']:
                        text += f'🆔 Buyurtma id: {order["id"]}\n'
                        text += f'🧩 {order["product"]["name"]}\n'
                        text += f'💵 Narxi: {order["product"]["price"]} so\'m\n'
                        text += f'🧮 Soni: {order["count"]} ta\n'
                        text += f'💰 {order["count"]} x {order["product"]["price"]} = {order["count"] * order["product"]["price"]} so\'m\n\n'
                        sum_all += order["count"] * order["product"]["price"]
                text += f'💰 Jami: {sum_all} so\'m\n\n'

            else:
                text += '📦 Siz hali buyurtma bermagansiz'
            keyboard = [
                [KeyboardButton('✅ yuborilgan buyurtmalar')],
                [KeyboardButton('☑️ yuborilmagan buyurtmalar')],
                [KeyboardButton('🏠 Bosh sahifa')],
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
            bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        except:
            text = '📦 Siz hali buyurtma bermagansiz\n\n'
            text += '❗️ Yoki siz ro\'yxatdan o\'tmagansiz\n\n'
            text += '🔐 Ro\'yxatdan o\'tish tugmasini bosing'
            bot.send_message(chat_id=chat_id, text='📦 Siz hali buyurtma bermagansiz')