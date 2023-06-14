from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import re
from user_db import DB
from db import DB as Base_db

db = DB('user_data.json')
base_db = Base_db('db.json')

class Auth_bot:
    def __init__(self) -> None:
        pass
    
    def direction_user(self, update: Update, context: CallbackContext):
        username = update.message.from_user.username
        if username:
            bot = context.bot
            chat_id = update.message.chat_id
            text = "Quydagi namuna asosida malumotni\nto'ldiring va botga yuboring📝\n\n"
            text += "ism:Muhammad\n"
            bot.send_message(chat_id=chat_id, text=text)

        else:
            update.message.reply_text(
                'Iltimos, telegramdagi ismingizni\n shaxsiy kabinetga kiriting va /start \nbuyrug\'ini qayta bering ‼️'
            )

    def auth_user(self, update: Update, context: CallbackContext):
        text = update.message.text
        telegram = update.message.from_user.username
        chat_id = update.message.chat_id
        try:
            try:
                get_user = base_db.get_user(chat_id=chat_id)
                if get_user:
                    update.message.reply_text(
                        'Siz allaqachon ro\'yxatdan o\'tgansiz\n\n'
                        '✅ Buyurtma berishingiz mumkin\n\n'
                        '📝 Zakaz berish uchun 📦 katalog buyrug\'ini yuboring'
                    )
            except:
                if telegram:
                    get_append = db.get_user_append(chat_id)
                    if text == "🔐 ro'yxatdan o'tish":
                        if db.chack_user(chat_id) == "200":
                            update.message.reply_text(
                                'Siz ro\'yxatdan o\'tgansiz ‼️'
                            )
                        elif db.chack_user(chat_id) == "401":
                            db.user_append(chat_id)
                            update.message.reply_text(
                                'Iltimos, ismingizni 📝\n\nNamuna: Muhammad'
                            )
                    elif text == '✏️ Profelni taxrirlash':
                        db.user_append(chat_id)
                        update.message.reply_text(
                            'Iltimos, ismingizni 📝\n\nNamuna: Muhammad'
                        )
                
                    elif get_append.get("name") == None:
                        db.user_append(chat_id, name=text, telegram=telegram)
                        update.message.reply_text(
                            'Familiyangizni kiriting📝\n\nNamuna: Abdullayev'
                        )
                    elif get_append.get("surname") == None:
                        db.user_append(chat_id, surname=text)
                        update.message.reply_text(
                            'Telefon raqamingizni kiriting📲\n\nNamuna: +998 99 999 99 99'
                        )
                    elif get_append.get("phone") == None:
                        pattern = r'\+998\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}'
                        telefonlar = re.findall(pattern, text)
                        if telefonlar:
                            db.user_append(chat_id, phone=text)
                            update.message.reply_text(
                                'Yashash manzilingizni kiriting(shahar yoki tuman)📍\n\nNamuna: Toshkent shahar'
                            )
                        else:
                            update.message.reply_text(
                                'Telefon raqamingizni noto\'g\'ri kiritdingiz❌\n\nNamuna: +998 99 999 99 99'
                            )

                    elif get_append.get("area") == None:
                        db.user_append(chat_id, area=text)

                        get_append_user = db.get_user_append(chat_id)

                        name = get_append_user.get("name")
                        surname = get_append_user.get("surname")
                        phone = get_append_user.get("phone")
                        area = get_append_user.get("area")
                        username = update.message.from_user.username

                        inline_keyboard = [
                            [
                                InlineKeyboardButton(
                                    text="Yes", callback_data=f"yes_{telegram}_/{username}"
                                ),
                                InlineKeyboardButton(
                                    text="No", callback_data="no"
                                )
                            ]
                        ]

                        reply_markup = InlineKeyboardMarkup(inline_keyboard)


                        update.message.reply_text(
                            f'Ma\'lumotlaringizni tekshirib yuboring✅\n\nIsm: {name}\nFamiliya: {surname}\nTelefon raqam: {phone}\nYashash manzil: {area}\n\nAgar ma\'lumotlar to\'g\'ri bo\'lsa yes, to\'g\'ri emas bo\'lsa no ni bosing👇',
                            reply_markup=reply_markup
                        )
                else:
                    update.message.reply_text(
                        'Iltimos, telegramdagi ismingizni\n shaxsiy kabinetga kiriting va /start \nbuyrug\'ini qayta bering ‼️'
                    )
        except:
            pass

    def yes(self, update: Update, context: CallbackContext):
        query = update.callback_query
        chat_id = query.message.chat_id
        data = query.data
        username = data.split("_/")[-1]
        
        get_user_append = db.get_user_append(chat_id)
        
        name = get_user_append.get("name")
        surname = get_user_append.get("surname")
        phone = get_user_append.get("phone")
        area = get_user_append.get("area")

        query.message.edit_text(
            f'Ma\'lumotlaringiz bazaga saqlanmoqda⏳',
            reply_markup=None
        )
        
        base_db.add_user(username=username, first_name=name, last_name=surname, chat_id=chat_id, address=area, phone=phone)
        query.message.reply_text(
            'Sizning ma\'lumotlaringiz bazaga saqlandi✅'
        )
        db.delete_user_append(chat_id)

    def no(self, update: Update, context: CallbackContext):
        query = update.callback_query
        chat_id = query.message.chat_id
        query.message.edit_text(
            'Ma\'lumotlaringizni qayta to\'ldiring📝',
            reply_markup=None
        )
        db.delete_user_append(chat_id)
        query.message.reply_text(
            'Iltimos, ro\'yxatdan o\'tish uchun\n pasdagi tugmani bosing👇'
        )

    def edit_user(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        base_db.delete_user(chat_id)
        self.auth_user(update=update, context=context)

    def logout(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        base_db.delete_user(chat_id)
        update.message.reply_text(
            'Siz muvaffaqiyatli chiqdingiz✅'
        )
        self.auth_user(update=update, context=context)