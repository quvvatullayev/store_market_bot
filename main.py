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

db = DB('db.json')
base_url = 'https://sanjarbekkutubxona.pythonanywhere.com'

class Shop:
    def __init__(self) -> None:
        pass

    def start(self, update: Update, context: CallbackContext) -> None:
        bot = context.bot
        chat_id = update.message.chat_id
        username = update.message.from_user.username
        get_admin = db.get_admin_by_username(username)

        if get_admin:
            text = 'Assalomu alaykum, {}!\n\nSizga qanday yordam bera olaman?\n\n'.format(update.message.from_user.first_name)
            text += 'Siz botni admin sifatida ishlatasiz'

            reply_keyboard = [
                ['📝 kelgan zakazlar', '🔐 admin'],
                ["📝 yetkazilgan zakazlar ✅", "📝 yetkazilmagan zakazlar ☑️"]
            ]
            markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
            bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)


        else:
            reply_keyboard = [
                ['📦 katalog', '🛒 karzinka'],
                ['📝 zakazlarim', '📞 aloqa'],
                ['👤 profil', "🔐 ro'yxatdan o'tish"]
            ]
            markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
            text = 'Assalomu alaykum, {}!\n\nSizga qanday yordam bera olaman?'.format(update.message.from_user.first_name)
            bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)

    def start_refresh(self, update: Update, context: CallbackContext, chat_id, first_name) -> None:
        bot = context.bot

        reply_keyboard = [
            ['📦 katalog', '🛒 karzinka'],
            ['📝 zakazlarim', '📞 aloqa'],
            ['👤 profil', "🔐 ro'yxatdan o'tish"]
        ]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        text = 'Assalomu alaykum, {}!\n\nSizga qanday yordam bera olaman?'.format(first_name)
        bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)