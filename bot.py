from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters
from main import Shop

TOKEN = '5699418530:AAF-rw_GFSO_DeL-19T4s2eiGDXLk6OSTIg'

shop = Shop()
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


dispatcher.add_handler(CommandHandler('start', shop.start))
dispatcher.add_handler(MessageHandler(Filters.text('📦 katalog'), shop.katalog))
dispatcher.add_handler(MessageHandler(Filters.text('🛒 karzinka'), shop.cart))
dispatcher.add_handler(MessageHandler(Filters.text("🔐 ro'yxatdan o'tish"), shop.get_login))
dispatcher.add_handler(MessageHandler(Filters.location, shop.add_order))
dispatcher.add_handler(MessageHandler(Filters.contact, shop.add_user))
dispatcher.add_handler(CallbackQueryHandler(shop.refresh, pattern='refresh_'))
dispatcher.add_handler(CallbackQueryHandler(shop.sub_categories, pattern='katalog_'))
dispatcher.add_handler(CallbackQueryHandler(shop.products, pattern='sub_category_'))
dispatcher.add_handler(CallbackQueryHandler(shop.next_product, pattern='next_'))
dispatcher.add_handler(CallbackQueryHandler(shop.back_product, pattern='backe_'))
dispatcher.add_handler(CallbackQueryHandler(shop.add_cart, pattern='add_cart_'))
dispatcher.add_handler(CallbackQueryHandler(shop.clear_cart, pattern='clear_cart_'))
dispatcher.add_handler(CallbackQueryHandler(shop.order, pattern='order_'))
dispatcher.add_handler(MessageHandler(Filters.text, shop.count_cart))

updater.start_polling()
updater.idle()