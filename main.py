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
        price = product['price']
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
        chat_id = query.message.chat_id

        try:
            get_user = db.get_user(chat_id=chat_id)

            user_id = get_user['data']['id']
            phone = get_user['data']['phone']

            query.bot.edit_message_reply_markup(reply_markup=None, chat_id=chat_id, message_id=query.message.message_id)

            db.add_cart(chat_id=chat_id, product_id=product_id, count=0, phone=phone, user_id=user_id)

            text = "Bu mahsulotdan nechta olasiz❔\n\n"
            text += 'Sonini kriting masalan:\n\n'
            text += 'soni:100'

            query.bot.send_message(chat_id=chat_id, text=text)
        
        except:
            query.bot.edit_message_reply_markup(reply_markup=None, chat_id=chat_id, message_id=query.message.message_id)

            text = "Iltimos avval ro'yxatdan o'ting\n\n"
            text += "🔐 ro'yxatdan o'tish tubmasini bosing"

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
            text = 'Savat bo\'sh\n\n'
            text += '📦 katalog'
            bot.send_message(chat_id=chat_id, text=text)
            return True
        else:
            text = 'Savatdagi mahsulotlar:\n\n'
            for cart in data_cart:
                product = db.get_product_by_id(product_id=cart['product'], chat_id=chat_id)[0]
                text += f"📦 Nomi: {product['name']}\n💰 Narxi: {product['price']} so'm\n📝 Ta'rif: {product['discription']}\n🧮 Mahsulot soni: {cart['count']}\n\n"

            inline_keyboard = [
                [
                    InlineKeyboardButton('📝 Buyurtma', callback_data=f"order_{chat_id}"),
                    InlineKeyboardButton('🔄 Yangilash', callback_data=f"refresh_{chat_id}"),
                    InlineKeyboardButton('🗑 Tozalash', callback_data=f"clear_cart_{chat_id}"),
                ]
            ]

            reply_markup = InlineKeyboardMarkup(inline_keyboard)
            bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

    def clear_cart(self, update: Update, context: CallbackContext):
        query = update.callback_query
        chat_id = query.message.chat_id

        db.delete_cart(chat_id=chat_id)

        query.bot.edit_message_reply_markup(reply_markup=None, chat_id=chat_id, message_id=query.message.message_id)

        text = 'Savat tozalandi\n\n'
        text += '📦 katalog'
        query.bot.send_message(chat_id=chat_id, text=text)

    def order(self, update: Update, context: CallbackContext):
        query = update.callback_query
        chat_id = query.message.chat_id
        try:
            get_user = db.get_user(chat_id=chat_id)

            if get_user['status'] == False:
                text = 'Iltimos avval ro\'yxatdan o\'ting\n\n'
                query.bot.send_message(chat_id=chat_id, text=text)

            else:
                query.bot.edit_message_reply_markup(reply_markup=None, chat_id=chat_id, message_id=query.message.message_id)
                text = 'Buyurtma qilish uchun locatsiyangizni yuboring\n\n'
                reply_markup = ReplyKeyboardMarkup([[KeyboardButton('📍 Locatsiyani yuborish', request_location=True)]], resize_keyboard=True)
                query.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
                

        except:
            query.edit_message_reply_markup(reply_markup=None)
            text = 'Iltimos avval ro\'yxatdan o\'ting❗️\n\n'
            query.bot.send_message(chat_id=chat_id, text=text)

    def get_login(self, update: Update, context: CallbackContext):
        bot = context.bot
        chat_id = update.message.chat_id

        text = 'Iltimos telefon raqamingizni kiriting\n\n'

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
            text += '📦 katalog'
            bot.send_message(chat_id=chat_id, text=text)
            self.start(update=update, context=context)
        else:
            text = 'Siz allaqachon ro\'yxatdan o\'tgansiz\n\n'
            text += '📦 katalog'
            bot.send_message(chat_id=chat_id, text=text)
            self.start(update=update, context=context)
        
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
        text += '📦 katalog'
        bot.send_message(chat_id=chat_id, text=text)
        self.start(update=update, context=context)