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

class Shop:
    def __init__(self) -> None:
        pass

    def start(self, update: Update, context: CallbackContext) -> None:
        bot = context.bot
        chat_id = update.message.chat_id

        reply_keyboard = [
            ['📦 katalog', '🛒 karzinka'],
            ['📝 zakazlarim', '📞 aloqa'],
        ]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        text = 'Assalomu alaykum, {}!\n\nSizga qanday yordam bera olaman?'.format(update.message.from_user.first_name)
        bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)

    def katalog(self, update: Update, context: CallbackContext) -> None:
        bot = context.bot
        chat_id = update.message.chat_id

        db.get_start(chat_id=str(chat_id))
        katalogs = db.get_categories(chat_id=chat_id)

        inline_keyboard = []
        
        for katalog in katalogs:
            inline_keyboard.append([InlineKeyboardButton(katalog['name'], callback_data=f"katalog_{katalog['id']}")])
         
        text = 'Kataloglarni tanlang'
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        bot.send_message(chat_id, text, reply_markup=reply_markup)

    def sub_categories(self, update: Update, context: CallbackContext):
        query = update.callback_query
        chat_id = query.message.chat_id

        data = query.data.split('_')
        katalog_id = int(data[-1])

        data_sub_categories = db.get_sub_categories(chat_id=chat_id, categories_id=katalog_id)

        inline_keyboard = []
        for sub_category in data_sub_categories:
            inline_keyboard.append([InlineKeyboardButton(sub_category['name'], callback_data=f"sub_category_{sub_category['id']}")])
        
        text = 'Kategoriya tanlang'
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        query.edit_message_text(text=text, reply_markup=reply_markup)

        
