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
base_url = 'https://storemarket.pythonanywhere.com'

class Shop:
    def __init__(self) -> None:
        pass

    def start(self, update: Update, context: CallbackContext) -> None:
        bot = context.bot
        chat_id = update.message.chat_id

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