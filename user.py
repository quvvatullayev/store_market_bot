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
from pprint import pprint

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
            text += f'👤 Username: @{user["username"]}\n'
            text += f'👤 Ism: {user["first_name"]}\n'
            text += f'👤 Familiya: {user["last_name"]}\n'
            text += f'📞 Telefon raqam: {user["phone"]}\n'
            text += f'📍 Manzil: {user["address"]}\n\n'

            keyboard = [
                ['📝 zakazlarim', '✏️ Profelni taxrirlash'],
                ['📤 profelni tark etish','🏠 Bosh sahifa']
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        except:
            text = '❗️ Siz ro\'yxatdan o\'tmagansiz\n\n'
            text += '🔐 Ro\'yxatdan o\'tish tugmasini bosing'
            bot.send_message(chat_id=chat_id, text=text)

    def admin_order_list(self, update: Update, context: CallbackContext):
        bot = context.bot
        chat_id = update.message.chat_id

        bot.send_message(chat_id=chat_id, text='Iltoimos kuting...')

        orders = db.get_order_list()['data']
        text = '📝 Kelgan zakazlar\n\n'
        data = {}
        for order in orders:
            if data.get(order['user']['last_name']):
                data[order['user']['last_name']].append(order)
            else:
                data[order['user']['last_name']] = [order]
        n = 1
        for key, value in data.items():
            # chack status
            user = value[0]['user']
            text += f'🪪 {n} - zakazlar\n'
            text += "-----------------------------------------------------\n"
            text += f'👤 {user["first_name"]} {user["last_name"]}\n'
            text += f'📞 {user["phone"]}\n'
            text += f'📍 {user["address"]}\n\n'
            # len
            for order in value:
                if not order['status']:
                    # buyurtma id
                    text += f'🆔 Buyurtma id {order["id"]}\n'
                    # buyurtma nomi
                    text += f'🧩 Buyurtma nomi {order["product"]["name"]}\n'
                    # buyurtma narxi
                    price = '{:,.0f}'.format(order['product']['price'])
                    text += f'💰 Buyurtma narxi {price} so\'m\n'
                    # buyurtma soni
                    text += f'🧮 Buyurtma soni {order["count"]} ta\n'
                    # buyurtma summasi
                    price = '{:,.0f}'.format(order['count'] * order['product']['price'])
                    text += f'💰 Buyurtma summasi {price} so\'m\n'  
                    # buyurtma holati
                    if order['status']:
                        text += f'📝 Buyurtma holati ✅\n\n'
                    else:
                        text += f'📝 Buyurtma holati ☑️\n\n'
            n += 1

        keyboard = [
            ['📝 Buyurtma informations','🏠 Bosh sahifa']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

    def admin_site(self, update: Update, context: CallbackContext):
        bot = context.bot
        chat_id = update.message.chat_id

        inline_keyboard = [
            [InlineKeyboardButton(url=base_url+'/admin/', text='🌐 Saytga kirish')]
        ]

        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        text = '🌐 Saytga kirish uchun pastdagi tugmani bosing'
        bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

    def get_edit_order_text(self, update: Update, context: CallbackContext):
        bot = context.bot
        chat_id = update.message.chat_id

        text = "✏️ Mijozga yetqizilgan maxsulotning id siniga 'u' yoki 'U' ni qo'shib kriting.\n\n"
        text += "Masalan: 7u"

        bot.send_message(chat_id, text)
