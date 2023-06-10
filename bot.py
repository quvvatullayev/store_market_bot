from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters
from main import Shop
from katalog import Katalog
from user import UserClass
from cart import Cart
from order import Order

TOKEN = '5699418530:AAF-rw_GFSO_DeL-19T4s2eiGDXLk6OSTIg'

shop = Shop()
katalog = Katalog()
user = UserClass()
cart = Cart()
order = Order()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


dispatcher.add_handler(CommandHandler('start', shop.start))
dispatcher.add_handler(MessageHandler(Filters.text('📦 katalog'), katalog.katalog))
dispatcher.add_handler(MessageHandler(Filters.text('🛒 karzinka'), cart.cart))
dispatcher.add_handler(MessageHandler(Filters.text("🔐 ro'yxatdan o'tish"), user.get_login))
dispatcher.add_handler(MessageHandler(Filters.text('👤 profil'), user.profil))
dispatcher.add_handler(MessageHandler(Filters.text("🏠 Bosh sahifa"), shop.start))
dispatcher.add_handler(MessageHandler(Filters.text("📝 zakazlarim"), order.get_order))
dispatcher.add_handler(MessageHandler(Filters.location, cart.add_order))
dispatcher.add_handler(MessageHandler(Filters.contact, user.add_user))
dispatcher.add_handler(CallbackQueryHandler(cart.refresh, pattern='refresh_'))
dispatcher.add_handler(CallbackQueryHandler(katalog.sub_categories, pattern='katalog_'))
dispatcher.add_handler(CallbackQueryHandler(katalog.products, pattern='sub_category_'))
dispatcher.add_handler(CallbackQueryHandler(katalog.next_product, pattern='next_'))
dispatcher.add_handler(CallbackQueryHandler(katalog.back_product, pattern='backe_'))
dispatcher.add_handler(CallbackQueryHandler(katalog.add_cart, pattern='add_cart_'))
dispatcher.add_handler(CallbackQueryHandler(cart.clear_cart, pattern='clear_cart_'))
dispatcher.add_handler(CallbackQueryHandler(cart.order, pattern='order_'))
dispatcher.add_handler(MessageHandler(Filters.text, cart.count_cart))

updater.start_polling()
updater.idle()