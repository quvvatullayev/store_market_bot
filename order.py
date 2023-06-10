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

            reply_markup = ReplyKeyboardMarkup([[KeyboardButton('🏠 Bosh sahifa')]], resize_keyboard=True)
            bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        except:
            text = '📦 Siz hali buyurtma bermagansiz\n\n'
            text += '❗️ Yoki siz ro\'yxatdan o\'tmagansiz\n\n'
            text += '🔐 Ro\'yxatdan o\'tish tugmasini bosing'
            bot.send_message(chat_id=chat_id, text='📦 Siz hali buyurtma bermagansiz')
