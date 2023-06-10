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

class Contact:
    def __init__(self) -> None:
        pass
    
    def contact(self, update: Update, context: CallbackContext) -> None:
        bot = context.bot
        chat_id = update.message.chat_id
        contact_data = db.get_contact()['data']

        text = 'Biz bilan aloqa uchun quyidagi ma\'lumotlarni ishlatishingiz mumkin\n\n'
        for contact in contact_data:
            name = contact['name']
            phone = contact['phone']
            location = contact['location'].split(',')
            image = contact['image']
            address = contact['address']
        
            text += f'👤 tashkilot nomi :  {name}\n\n'
            text += f'📞 phone nommer : {phone}\n\n'
            text += f'📍 address : {address}\n\n'

            latitude = float(location[0])
            longitude = float(location[1])

            bot.send_photo(chat_id=chat_id, photo=base_url + image, caption=text)
            bot.send_location(chat_id=chat_id, latitude=latitude, longitude=longitude)
        



