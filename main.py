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
base_url = 'http://storemarket.pythonanywhere.com'

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

    def products(self, update: Update, context: CallbackContext):
        query = update.callback_query
        chat_id = query.message.chat_id

        data = query.data.split('_')
        sub_category_id = int(data[-1])

        data_products = db.get_products(chat_id=chat_id, sub_category_id=sub_category_id)
        
        # products carusel
        for product in data_products:
            image = base_url + product['image']
            name = product['name']
            price = product['price']
            discription = product['discription']
            
            caption = f"📦 Nomi: {name}\n💰 Narxi: {price}\n📝 Ta'rif: {discription}"
            inline_keyboard = [
                [
                    InlineKeyboardButton('⬅️ Orqaga', callback_data=f"sub_category_{sub_category_id}"),
                    InlineKeyboardButton('🛒 Savatga qo\'shish', callback_data=f"add_cart_{product['id']}"),
                    InlineKeyboardButton('➡️ Oldinga', callback_data=f"next_{product['id']}"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard)

            query.bot.send_photo(chat_id=chat_id, photo=image, caption=caption, reply_markup=reply_markup)


