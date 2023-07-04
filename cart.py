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


class Cart:
    def __init__(self) -> None:
        pass   

    def clear_cart(self, update: Update, context: CallbackContext):
        query = update.callback_query
        chat_id = query.message.chat_id

        db.delete_cart(chat_id=chat_id)

        query.bot.edit_message_reply_markup(reply_markup=None, chat_id=chat_id, message_id=query.message.message_id)

        text = '🧹 Savat tozalandi\n\n'
        query.bot.send_message(chat_id=chat_id, text=text)

    def order(self, update: Update, context: CallbackContext):
        query = update.callback_query
        chat_id = query.message.chat_id
        try:
            get_user = db.get_user(chat_id=chat_id)

            if get_user['status'] == False:
                text = 'Iltimos avval ro\'yxatdan o\'ting❗️\n\n'
                query.bot.send_message(chat_id=chat_id, text=text)

            else:
                query.bot.edit_message_reply_markup(reply_markup=None, chat_id=chat_id, message_id=query.message.message_id)
                text = '📍 Buyurtma qilish uchun locatsiyangizni yuboring\n\n'
                reply_markup = ReplyKeyboardMarkup([[KeyboardButton('📍 Locatsiyani yuborish', request_location=True)]], resize_keyboard=True)
                query.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
                

        except:
            query.edit_message_reply_markup(reply_markup=None)
            text = 'Iltimos avval ro\'yxatdan o\'ting❗️\n\n'
            query.bot.send_message(chat_id=chat_id, text=text)

    def count_cart(self, update: Update, context: CallbackContext):
        bot = context.bot
        chat_id = update.message.chat_id
        count = update.message.text

        coun_data = db.get_count_cart(chat_id=chat_id)
        if len(coun_data) == 0:
            pass
        else:
            db.update_cart(chat_id=chat_id, count=int(count))

            text = 'Mahsulot savatga qo\'shildi\n\n'
            text += '📦 katalog'
            bot.send_message(chat_id=chat_id, text=text)

    def cart(self, update: Update, context: CallbackContext):
        bot = context.bot
        chat_id = update.message.chat_id

        data_cart = db.get_cart(chat_id=chat_id)


        if len(data_cart) == 0:
            text = '📭 Savat bo\'sh\n\n'
            
            bot.send_message(chat_id=chat_id, text=text)
            return True
        else:
            text = 'Savatdagi mahsulotlar:\n\n'
            inline_keyboarddelete = []
            for cart in data_cart:
                products = db.get_product_by_id(product_id=cart['product'], chat_id=chat_id)
                for product in products:
                    text += f"📦 Nomi: {product['name']}\n💰 Narxi: {'{:,.0f}'.format(product['price'])} so'm\n📝 Ta'rif: {product['discription']}\n🧮 Mahsulot soni: {cart['count']}\n\n"
                    inline_keyboarddelete.append([InlineKeyboardButton(f"🗑 {product['name']}", callback_data=f"delete_{product['id']}")])

            inline_keyboard = [
                [
                    InlineKeyboardButton('📝 Buyurtma', callback_data=f"order_{chat_id}"),
                    InlineKeyboardButton('🔄 Yangilash', callback_data=f"refresh_{chat_id}"),
                    InlineKeyboardButton('🗑 Tozalash', callback_data=f"clear_cart_{chat_id}"),
                ]
            ]
            inline_keyboard = inline_keyboarddelete + inline_keyboard

            reply_markup = InlineKeyboardMarkup(inline_keyboard)
            bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

    def add_order(self, update: Update, context: CallbackContext):
        bot = context.bot
        chat_id = update.message.chat_id
        get_user = db.get_user(chat_id=chat_id)
        user_id = get_user['data']['id']
        cart_list = db.get_cart_list(chat_id=chat_id)
        location = update.message.location
        bot.send_message(chat_id=chat_id, text='Iltimos kuting ...', reply_markup=None)
        order_list = []
        for cart in cart_list:
            order_list.append({
                'user': user_id,
                'product': cart['product'],
                'count': cart['count'],
                'phone': cart['phone'],
                'address': f"{location.latitude},{location.longitude}"
            })
        db.add_order(order_list=order_list)

        text = '✅Buyurtmangiz qabul qilindi\n\n'
        text += '✅ Buyurtmangizni qabul qilish uchun operator siz bilan bog\'lanadi\n\n'
        db.delete_cart(chat_id=chat_id)
        bot.send_message(chat_id=chat_id, text=text)
        shop.start_refresh(update=update, context=context, chat_id=chat_id, first_name=update.message.from_user.first_name)

    def refresh(self, update: Update, context: CallbackContext):
        query = update.callback_query
        chat_id = query.message.chat_id
        query.bot.edit_message_reply_markup(reply_markup=None, chat_id=chat_id, message_id=query.message.message_id)
        shop.start_refresh(update=update, context=context, chat_id=chat_id, first_name=query.from_user.first_name)

    def delete_card_product(self, update: Update, context: CallbackContext):
        query = update.callback_query
        bot = context.bot
        product_id = query.data.split('_')[1]
        
        chat_id = query.message.chat_id
        db.delete_product_card(chat_id=chat_id, product_id=int(product_id))
        
        data_cart = db.get_cart(chat_id=chat_id)
        query.bot.edit_message_reply_markup(reply_markup=None, chat_id=chat_id, message_id=query.message.message_id)


        if len(data_cart) == 0:

            text = '📭 Savat bo\'sh\n\n'
            
            bot.send_message(chat_id=chat_id, text=text)
            return True
        else:
            text = 'Savatdagi mahsulotlar:\n\n'
            inline_keyboarddelete = []
            for cart in data_cart:
                products = db.get_product_by_id(product_id=cart['product'], chat_id=chat_id)
                for product in products:
                    text += f"📦 Nomi: {product['name']}\n💰 Narxi: {'{:,.0f}'.format(product['price'])} so'm\n📝 Ta'rif: {product['discription']}\n🧮 Mahsulot soni: {cart['count']}\n\n"
                    inline_keyboarddelete.append([InlineKeyboardButton(f"🗑 {product['name']}", callback_data=f"delete_{product['id']}")])

            inline_keyboard = [
                [
                    InlineKeyboardButton('📝 Buyurtma', callback_data=f"order_{chat_id}"),
                    InlineKeyboardButton('🔄 Yangilash', callback_data=f"refresh_{chat_id}"),
                    InlineKeyboardButton('🗑 Tozalash', callback_data=f"clear_cart_{chat_id}"),
                ]
            ]
            inline_keyboard = inline_keyboarddelete + inline_keyboard

            reply_markup = InlineKeyboardMarkup(inline_keyboard)
            bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)