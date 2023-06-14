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

class Katalog:
    def __init__(self) -> None:
        pass
    
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
        
        if inline_keyboard == []:
            text = 'Kategoriyada mahsulotlar yo\'q'
            query.bot.edit_message_text(text=text, chat_id=chat_id, message_id=query.message.message_id)
            return
        text = 'Kategoriya tanlang'
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        query.edit_message_text(text=text, reply_markup=reply_markup)

    def products(self, update: Update, context: CallbackContext):
        query = update.callback_query
        chat_id = query.message.chat_id

        query.bot.edit_message_reply_markup(reply_markup=None, chat_id=chat_id, message_id=query.message.message_id)

        data = query.data.split('_')
        sub_category_id = int(data[-1])

        data_products = db.get_products(chat_id=chat_id, sub_category_id=sub_category_id)
        
        if data_products == []:
            text = 'Kategoriyada mahsulotlar yo\'q'
            query.bot.edit_message_text(text=text, chat_id=chat_id, message_id=query.message.message_id)
            return

        for product in data_products:
            image = base_url + product['image']
            name = product['name']
            price = product['price']
            discription = product['discription']
            
            caption = f"📦 Nomi: {name}\n💰 Narxi: {'{:,.0f}'.format(price)}\n📝 Ta'rif: {discription}"
            inline_keyboard = [
                [
                    InlineKeyboardButton('⬅️ Orqaga', callback_data=f"backe_{sub_category_id}_{product['id']}"),
                    InlineKeyboardButton('🛒 Savatga qo\'shish', callback_data=f"add_cart_{sub_category_id}_{product['id']}"),
                    InlineKeyboardButton('➡️ Oldinga', callback_data=f"next_{sub_category_id}_{product['id']}"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard)

            query.bot.send_photo(chat_id=chat_id, photo=image, caption=caption, reply_markup=reply_markup)
            break

    def next_product(self, update: Update, context: CallbackContext):
        query = update.callback_query
        data = query.data.split('_')
        product_id = int(data[-1])
        chat_id = query.message.chat_id
        sub_category_id = int(data[-2])

        query.bot.edit_message_reply_markup(reply_markup=None, chat_id=chat_id, message_id=query.message.message_id)

        product = db.get_next_product(product_id=product_id, chat_id=chat_id, sub_category_id=sub_category_id)[0]

        image = base_url + product['image']
        name = product['name']
        price = product['price']
        discription = product['discription']
        
        caption = f"📦 Nomi: {name}\n💰 Narxi: {'{:,.0f}'.format(price)}\n📝 Ta'rif: {discription}"
        inline_keyboard = [
            [
                InlineKeyboardButton('⬅️ Orqaga', callback_data=f"backe_{sub_category_id}_{product['id']}"),
                InlineKeyboardButton('🛒 Savatga qo\'shish', callback_data=f"add_cart_{sub_category_id}_{product['id']}"),
                InlineKeyboardButton('➡️ Oldinga', callback_data=f"next_{sub_category_id}_{product['id']}"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)

        query.bot.send_photo(chat_id=chat_id, photo=image, caption=caption, reply_markup=reply_markup)

    def back_product(self, update: Update, context: CallbackContext):
        query = update.callback_query
        data = query.data.split('_')
        product_id = int(data[-1])
        chat_id = query.message.chat_id
        sub_category_id = int(data[-2])

        query.bot.edit_message_reply_markup(reply_markup=None, chat_id=chat_id, message_id=query.message.message_id)

        product = db.get_back_product(product_id=product_id, chat_id=chat_id, sub_category_id=sub_category_id)[0]

        image = base_url + product['image']
        name = product['name']
        price = '{:,.0f}'.format(product['price'])
        discription = product['discription']
    
        caption = f"📦 Nomi: {name}\n💰 Narxi: {price}\n📝 Ta'rif: {discription}"
        inline_keyboard = [
            [
                InlineKeyboardButton('⬅️ Orqaga', callback_data=f"backe_{sub_category_id}_{product['id']}"),
                InlineKeyboardButton('🛒 Savatga qo\'shish', callback_data=f"add_cart_{sub_category_id}_{product['id']}"),
                InlineKeyboardButton('➡️ Oldinga', callback_data=f"next_{sub_category_id}_{product['id']}"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)

        query.bot.send_photo(chat_id=chat_id, photo=image, caption=caption, reply_markup=reply_markup)

    def add_cart(self, update: Update, context: CallbackContext):
        query = update.callback_query
        data = query.data.split('_')
        product_id = int(data[-1])
        sub_category_id = int(data[-2])
        chat_id = query.message.chat_id

        try:
            text = 'Iltooms kuting ...'
            
            try:
                get_product = db.get_product_id(product_id=product_id)

                query.bot.edit_message_reply_markup(reply_markup=None, chat_id=chat_id, message_id=query.message.message_id)
                query.bot.send_message(chat_id=chat_id, text=text)
                get_user = db.get_user(chat_id=chat_id)

                user_id = get_user['data']['id']
                phone = get_user['data']['phone']


                db.add_cart(chat_id=chat_id, product_id=product_id, count=0, phone=phone, user_id=user_id)

                text = "Bu mahsulotdan nechta olasiz❔\n\n"
                text += 'Sonini kriting masalan:\n\n'
                text += 'soni:100'

                query.bot.send_message(chat_id=chat_id, text=text)

            except:
                text = 'Bu mahsulot soni tugadi❗️\n\n'
                text += 'Iltimos qayta urinib ko\'ring❗️'
                query.bot.send_message(chat_id=chat_id, text=text)
        
        except:

            text = "Iltimos avval ro'yxatdan o'ting\n\n"
            text += "🔐 ro'yxatdan o'tish tubmasini bosing"

            query.bot.send_message(chat_id=chat_id, text=text, reply_markup=None)
