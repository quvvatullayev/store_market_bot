from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters
from main import Shop

TOKEN = '5699418530:AAF-rw_GFSO_DeL-19T4s2eiGDXLk6OSTIg'

shop = Shop()
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


dispatcher.add_handler(CommandHandler('start', shop.start))
dispatcher.add_handler(MessageHandler(Filters.text('📦 katalog'), shop.katalog))

updater.start_polling()
updater.idle()