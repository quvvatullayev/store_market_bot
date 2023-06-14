from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters
from main import Shop
from katalog import Katalog
from user import UserClass
from cart import Cart
from order import Order
from contact import Contact
from user_aouth import Auth_bot


TOKEN = '5699418530:AAF-rw_GFSO_DeL-19T4s2eiGDXLk6OSTIg'

shop = Shop()
katalog = Katalog()
user = UserClass()
cart = Cart()
order = Order()
contact = Contact()
auth_bot = Auth_bot()


updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


dispatcher.add_handler(CommandHandler('start', shop.start))
dispatcher.add_handler(MessageHandler(Filters.text('📦 katalog'), katalog.katalog))
dispatcher.add_handler(MessageHandler(Filters.text('🛒 karzinka'), cart.cart))
dispatcher.add_handler(MessageHandler(Filters.text('👤 profil'), user.profil))
dispatcher.add_handler(MessageHandler(Filters.text('✏️ Profelni taxrirlash'), auth_bot.edit_user))
dispatcher.add_handler(MessageHandler(Filters.text('📤 profelni tark etish'), auth_bot.logout))
dispatcher.add_handler(MessageHandler(Filters.text("🏠 Bosh sahifa"), shop.start))
dispatcher.add_handler(MessageHandler(Filters.text("📝 zakazlarim"), order.get_order))
dispatcher.add_handler(MessageHandler(Filters.text("📞 aloqa"), contact.contact))
dispatcher.add_handler(MessageHandler(Filters.text("📝 kelgan zakazlar"), user.admin_order_list))
dispatcher.add_handler(MessageHandler(Filters.text('📝 Buyurtma informations'), order.get_information))
dispatcher.add_handler(MessageHandler(Filters.text('✅ Buyurtmani tekshirish'), order.get_order))
dispatcher.add_handler(MessageHandler(Filters.text('☑️ yuborilmagan buyurtmalar'), order.get_order_status_false))
dispatcher.add_handler(MessageHandler(Filters.text('✅ yuborilgan buyurtmalar'), order.get_order_status_true))
dispatcher.add_handler(MessageHandler(Filters.text('📝 yetkazilgan zakazlar ✅'), order.get_order_status_true_admin))
dispatcher.add_handler(MessageHandler(Filters.text('📝 yetkazilmagan zakazlar ☑️'), order.get_order_status_false_admin))
dispatcher.add_handler(MessageHandler(Filters.text('🔐 admin'), user.admin_site))
dispatcher.add_handler(MessageHandler(Filters.text('✏️ Buyurtmalarni taxrirlash'), user.get_edit_order_text))
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
dispatcher.add_handler(MessageHandler(Filters.regex(r'^\d+u$'), order.edit_order))
dispatcher.add_handler(MessageHandler(Filters.regex(r'^\d+U$'), order.edit_order))
dispatcher.add_handler(MessageHandler(Filters.regex(r'^\d+t$'), order.get_order_by_id))
dispatcher.add_handler(MessageHandler(Filters.regex(r'^\d+$'), cart.count_cart))
dispatcher.add_handler(MessageHandler(Filters.text("🔐 ro'yxatdan o'tish"), auth_bot.auth_user))
dispatcher.add_handler(MessageHandler(Filters.text, auth_bot.auth_user))
dispatcher.add_handler(CallbackQueryHandler(auth_bot.yes, pattern='yes'))
dispatcher.add_handler(CallbackQueryHandler(auth_bot.no, pattern='no'))

updater.start_polling()
updater.idle()