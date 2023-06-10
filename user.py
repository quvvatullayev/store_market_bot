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

class UserClass:
    def __init__(self) -> None:
        pass   

    def get_login(self, update: Update, context: CallbackContext):
        bot = context.bot
        chat_id = update.message.chat_id

        text = '📞 Iltimos telefon raqamingizni kiriting\n\n'

        reply_markup = ReplyKeyboardMarkup([[KeyboardButton('📞 Telefon raqamni yuborish', request_contact=True)]], resize_keyboard=True)
        bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

    def add_user(self, update: Update, context: CallbackContext):
        bot = context.bot
        chat_id = update.message.chat_id

        phone_number = update.message.contact.phone_number
        username = update.message.from_user.username
        name = update.message.from_user.first_name

        user = db.add_user(username=username, name=name, chat_id=chat_id, phone_number=phone_number)

        if user['status']:
            text = 'Siz muvaffaqiyatli ro\'yxatdan o\'tdingiz\n\n'
            text += '✅ Buyurtma berishingiz mumkin\n\n'
            bot.send_message(chat_id=chat_id, text=text)

            shop.start_refresh(update=update, context=context, chat_id=chat_id, first_name=update.message.from_user.first_name)

        else:
            text = 'Siz allaqachon ro\'yxatdan o\'tgansiz\n\n'
            text += '✅ Buyurtma berishingiz mumkin\n\n'
            bot.send_message(chat_id=chat_id, text=text)
            shop.start_refresh(update=update, context=context, chat_id=chat_id, first_name=update.message.from_user.first_name)

    def profil(self, update: Update, context: CallbackContext):
        bot = context.bot
        chat_id = update.message.chat_id

        try:
            user = db.get_user(chat_id=chat_id)['data']
            
            text = f'👤 Profil\n\n'
            text += f'👤 Foydalanuvchi: {user["name"]}\n'
            text += f'👤 Username: {user["username"]}\n'
            text += f'📞 Telefon raqam: {user["phone"]}\n\n'
            
            reply_markup = ReplyKeyboardMarkup([[KeyboardButton('📝 zakazlarim'), KeyboardButton('🏠 Bosh sahifa')]], resize_keyboard=True)
            bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        except:
            text = '❗️ Siz ro\'yxatdan o\'tmagansiz\n\n'
            text += '🔐 Ro\'yxatdan o\'tish tugmasini bosing'
            bot.send_message(chat_id=chat_id, text=text)