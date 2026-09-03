# ==============================================================================
#  _  __ _____ _   _   _____ __  __  ___  ____  
# | |/ /|_   _| \ | | |_   _|  \/  |/ _ \|  _ \ 
# | ' /   | | |  \| |   | | | |\/| | | | | | | |
# | . \   | | | |\  |   | | | |  | | |_| | |_| |
# |_|\_\  |_| |_| \_|   |_| |_|  |_|\___/|____/ 
# ==============================================================================
# 👑 المطور : @BBH_S
# 📞 الدعم الفني : @BBH_S
# 📢 القناة : https://t.me/TATYCODEX
# ==============================================================================
# النسخة: 7.3 - اشتراك إجباري مطلق لقناة TATYCODEX
# ==============================================================================
import telebot
from telebot import types
import json
import time
import os
import random
import string

TOKEN = "8863180629:AAGp4xc5OAfwa3IHbYO1JCHVva5yVjHPUi4"
ADMIN_ID = "5174813723"  # غير ده بالايدي بتاعك
CHANNEL_ID = "@TATYCODEX"  # القناة الأساسية
bot = telebot.TeleBot(TOKEN, parse_mode='Markdown')

# ============ البيانات ============
user_points = {}
user_languages = {}
user_currencies = {}  # تخزين عملة كل مستخدم
daily_gift_cooldown = {}
transfer_data = {}
promo_codes = {}
store_items = {}
admin_create_code = {}
admin_create_product = {}

# ✅ القنوات الإجبارية ثابتة ولا تتغير ولا تُحمل من ملف
force_channels = ["@TATYCODEX"]  

pending_broadcast = {}
pending_points = {}

# إعدادات إضافية - نستخدم dictionary عشان نقلل استخدام global
settings = {
    "daily_gift_amount": 5,
    "transfer_fee_percent": 5
}

# قائمة العملات المدعومة
CURRENCIES = {
    "usd": {"symbol": "$", "name": "دولار أمريكي", "flag": "🇺🇸"},
    "egp": {"symbol": "ج.م", "name": "جنيه مصري", "flag": "🇪🇬"},
    "iqd": {"symbol": "د.ع", "name": "دينار عراقي", "flag": "🇮🇶"},
    "syp": {"symbol": "ل.س", "name": "ليرة سورية", "flag": "🇸🇾"},
    "sar": {"symbol": "ر.س", "name": "ريال سعودي", "flag": "🇸🇦"},
    "aed": {"symbol": "د.إ", "name": "درهم إماراتي", "flag": "🇦🇪"},
    "kwd": {"symbol": "د.ك", "name": "دينار كويتي", "flag": "🇰🇼"},
    "jod": {"symbol": "د.أ", "name": "دينار أردني", "flag": "🇯🇴"},
    "lbp": {"symbol": "ل.ل", "name": "ليرة لبنانية", "flag": "🇱🇧"},
    "try": {"symbol": "₺", "name": "ليرة تركية", "flag": "🇹🇷"},
    "eur": {"symbol": "€", "name": "يورو", "flag": "🇪🇺"},
    "gbp": {"symbol": "£", "name": "جنيه إسترليني", "flag": "🇬🇧"},
}

bot_settings = {
    "buy_numbers": True,
    "buy_sessions": True,
    "daily_gift": True,
    "recharge": True,
    "transfer": True,
    "invite": True,
    # ✅ تفعيل الاشتراك الإجباري بشكل دائم (لن يظهر في الإعدادات للتعديل)
    "force_subscribe": True,  
    "redeem_code": True
}

# تحميل الملفات (تم حذف تحميل force_channels)
def load_data():
    global user_points, user_languages, user_currencies, bot_settings, promo_codes, store_items, settings
    
    try:
        with open('points.json', 'r') as f:
            user_points = json.load(f)
    except:
        user_points = {}
    
    try:
        with open('languages.json', 'r') as f:
            user_languages = json.load(f)
    except:
        user_languages = {}
    
    try:
        with open('currencies.json', 'r') as f:
            user_currencies = json.load(f)
    except:
        user_currencies = {}
    
    try:
        with open('settings.json', 'r') as f:
            loaded = json.load(f)
            for key in bot_settings:
                if key not in loaded:
                    loaded[key] = bot_settings[key]
            # منع تغيير force_subscribe من الملف
            loaded['force_subscribe'] = True
            if 'daily_gift_amount' in loaded:
                settings['daily_gift_amount'] = loaded['daily_gift_amount']
            if 'transfer_fee_percent' in loaded:
                settings['transfer_fee_percent'] = loaded['transfer_fee_percent']
            bot_settings = loaded
    except:
        bot_settings = {
            "buy_numbers": True,
            "buy_sessions": True,
            "daily_gift": True,
            "recharge": True,
            "transfer": True,
            "invite": True,
            "force_subscribe": True,
            "redeem_code": True
        }
        save_data()
    
    try:
        with open('promo_codes.json', 'r') as f:
            promo_codes = json.load(f)
    except:
        promo_codes = {}
    
    try:
        with open('store_items.json', 'r') as f:
            store_items = json.load(f)
    except:
        store_items = {}

def save_data():
    # التأكد من أن force_subscribe دائماً True قبل الحفظ
    bot_settings['force_subscribe'] = True
    bot_settings['daily_gift_amount'] = settings['daily_gift_amount']
    bot_settings['transfer_fee_percent'] = settings['transfer_fee_percent']
    
    with open('points.json', 'w') as f:
        json.dump(user_points, f)
    with open('languages.json', 'w') as f:
        json.dump(user_languages, f)
    with open('currencies.json', 'w') as f:
        json.dump(user_currencies, f)
    with open('settings.json', 'w') as f:
        json.dump(bot_settings, f)
    with open('promo_codes.json', 'w') as f:
        json.dump(promo_codes, f)
    with open('store_items.json', 'w') as f:
        json.dump(store_items, f)

load_data()

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def get_user_currency(user_id):
    """الحصول على عملة المستخدم"""
    return user_currencies.get(str(user_id), "usd")

def format_price(amount, user_id):
    """تنسيق السعر مع رمز العملة"""
    currency_code = get_user_currency(user_id)
    currency = CURRENCIES.get(currency_code, CURRENCIES["usd"])
    return f"{amount} {currency['symbol']}"

# ============ التحقق من الاشتراك (دائم ومطلق) ============
def check_all_subscriptions(user_id):
    # تم إلغاء شرط bot_settings["force_subscribe"] لأنه دائماً مفعل
    for channel in force_channels:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except:
            return False
    return True

def get_channels_text():
    # نص ثابت للقناة الإجبارية
    return "\n• @TATYCODEX"

# ============ الكيبوردات ============
def main_kb(chat_id=None, lang='ar'):
    kb = types.InlineKeyboardMarkup(row_width=2)
    if lang == 'ar':
        # ===== العروض في صف كامل =====
        kb.add(types.InlineKeyboardButton("🛒 العروض التي يقدمها المتجر", callback_data="buy_numbers", style="success"))
        
        # ===== صفين =====
        kb.add(
            types.InlineKeyboardButton("هدية يومية 🎁", callback_data="daily_gift", style="danger"),
            types.InlineKeyboardButton("حسابي 💰", callback_data="my_account", style="danger")
        )
        # ===== صف واحد =====
        kb.add(types.InlineKeyboardButton("شحن رصيد 💬", callback_data="recharge", style="primary"))
        # ===== صفين =====
        kb.add(
            types.InlineKeyboardButton("دعوة صديق 👤", callback_data="invite", style="success"),
            types.InlineKeyboardButton("تحويل رصيد 💸", callback_data="transfer", style="success")
        )
        kb.add(
            types.InlineKeyboardButton("الشروط ⚠️", callback_data="terms", style="danger"),
            types.InlineKeyboardButton("تغيير اللغة 🌐", callback_data="change_lang", style="danger")
        )
        kb.add(
            types.InlineKeyboardButton("قناة التفعيلات 🔎", callback_data="channel", style="primary"),
            types.InlineKeyboardButton("التحديثات 🔥", callback_data="updates", style="primary")
        )
        kb.add(
            types.InlineKeyboardButton("استبدال كود 💳", callback_data="redeem_code_public", style="success"),
            types.InlineKeyboardButton("الدعم الفني 📞", callback_data="support", style="success")
        )
        # ===== صف واحد =====
        kb.add(types.InlineKeyboardButton("تغيير العملة 🪙", callback_data="change_currency", style="danger"))
        
        # ===== لوحة التحكم للأدمن فقط =====
        if str(chat_id) == ADMIN_ID:
            kb.add(types.InlineKeyboardButton("لوحة التحكم 📢", callback_data="admin", style="primary"))
    else:
        # ===== نفس الترتيب بالإنجليزية =====
        kb.add(types.InlineKeyboardButton("🛒 Store Offers", callback_data="buy_numbers", style="success"))
        kb.add(
            types.InlineKeyboardButton("Daily Gift 🎁", callback_data="daily_gift", style="danger"),
            types.InlineKeyboardButton("My Account 💰", callback_data="my_account", style="danger")
        )
        kb.add(types.InlineKeyboardButton("Recharge 💬", callback_data="recharge", style="primary"))
        kb.add(
            types.InlineKeyboardButton("Invite 👤", callback_data="invite", style="success"),
            types.InlineKeyboardButton("Transfer 💸", callback_data="transfer", style="success")
        )
        kb.add(
            types.InlineKeyboardButton("Terms ⚠️", callback_data="terms", style="danger"),
            types.InlineKeyboardButton("Change Lang 🌐", callback_data="change_lang", style="danger")
        )
        kb.add(
            types.InlineKeyboardButton("Channel 🔎", callback_data="channel", style="primary"),
            types.InlineKeyboardButton("Updates 🔥", callback_data="updates", style="primary")
        )
        kb.add(
            types.InlineKeyboardButton("Redeem Code 💳", callback_data="redeem_code_public", style="success"),
            types.InlineKeyboardButton("Support 📞", callback_data="support", style="success")
        )
        kb.add(types.InlineKeyboardButton("Change Currency 🪙", callback_data="change_currency", style="danger"))
        if str(chat_id) == ADMIN_ID:
            kb.add(types.InlineKeyboardButton("Admin 📢", callback_data="admin", style="primary"))
    
    return kb

def back_kb(lang='ar'):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🔙 رجوع" if lang == 'ar' else "🔙 Back", callback_data="back"))
    return kb

def sub_kb(lang='ar'):
    kb = types.InlineKeyboardMarkup()
    # ✅ فقط القناة الثابتة
    kb.add(types.InlineKeyboardButton("📢 اشترك في @TATYCODEX", url="https://t.me/TATYCODEX"))
    kb.add(types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_sub", style="danger"))
    return kb

def confirm_kb(product_id, lang='ar'):
    kb = types.InlineKeyboardMarkup(row_width=2)
    if lang == 'ar':
        kb.add(
            types.InlineKeyboardButton("✅ نعم", callback_data=f"buy_confirm_{product_id}", style="success"),
            types.InlineKeyboardButton("❌ لا", callback_data=f"buy_cancel_{product_id}", style="success")
        )
    else:
        kb.add(
            types.InlineKeyboardButton("✅ Yes", callback_data=f"buy_confirm_{product_id}", style="danger"),
            types.InlineKeyboardButton("❌ No", callback_data=f"buy_cancel_{product_id}", style="danger")
        )
    return kb

def currency_kb(lang='ar'):
    """كيبورد اختيار العملة"""
    kb = types.InlineKeyboardMarkup(row_width=3)
    for code, currency in CURRENCIES.items():
        kb.add(types.InlineKeyboardButton(
            f"{currency['flag']} {currency['name']} ({currency['symbol']})",
            callback_data=f"set_currency_{code}"
        ))
    kb.add(types.InlineKeyboardButton("🔙 رجوع" if lang == 'ar' else "🔙 Back", callback_data="back"))
    return kb

# ============ أمر start ============
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = str(message.chat.id)
    user = message.from_user
    
    # ===== التحقق من وجود المستخدم =====
    is_new_user = chat_id not in user_points
    
    # ===== إشعار الدخول الجديد (مرة واحدة فقط) =====
    if is_new_user:
        try:
            username = f"@{user.username}" if user.username else "لا يوجد"
            full_name = user.full_name if user.full_name else "لا يوجد"
            
            admin_notify = f"""
🎉 **مستخدم جديد دخل البوت!**

━━━━━━━━━━━━━━━━━━━━━
🆔 **المعرف:** `{chat_id}`
📛 **اليوزر:** {username}
👤 **الاسم:** {full_name}
🕐 **الوقت:** {time.strftime('%Y-%m-%d %H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━
"""
            bot.send_message(ADMIN_ID, admin_notify, parse_mode='Markdown')
            
            # ===== شعار ترحيب للمستخدم الجديد =====
            welcome_new = f"""
🎉 **أهلاً بك في بوتTATY!**

نحن سعداء بانضمامك إلينا 🦇
استمتع بتجربة مميزة مع أفضل العروض.

📢 **قناتنا:** {CHANNEL_ID}
📞 **الدعم:** @BBH_S
"""
            bot.send_message(chat_id, welcome_new, parse_mode='Markdown')
        except Exception as e:
            print(f"خطأ في إرسال الترحيب: {e}")
    
    # ===== تسجيل المستخدم =====
    if chat_id not in user_languages:
        user_languages[chat_id] = 'ar'
        save_data()
    if chat_id not in user_points:
        user_points[chat_id] = 0
        save_data()
    if chat_id not in user_currencies:
        user_currencies[chat_id] = "usd"
        save_data()
    
    lang = user_languages[chat_id]
    
    if len(message.text.split()) > 1:
        ref = message.text.split()[1]
        if ref != chat_id and ref in user_points:
            user_points[ref] = user_points.get(ref, 0) + 1
            save_data()
            try:
                bot.send_message(ref, "🎉 تم دعوة شخص جديد!")
            except:
                pass
    
    # ===== ✅ التحقق من الاشتراك الإجباري (مباشر بدون شرط) =====
    if not check_all_subscriptions(chat_id):
        channels_text = get_channels_text()
        text = f"""
⚠️ **يجب الاشتراك في القنوات التالية أولاً!**

{channels_text}

👇 اشترك في القنوات ثم اضغط تحقق:
"""
        bot.send_message(chat_id, text, reply_markup=sub_kb(lang), parse_mode='Markdown')
        return
    
    points = user_points.get(chat_id, 0)
    currency = CURRENCIES.get(get_user_currency(chat_id), CURRENCIES["usd"])
    
    welcome_text = f"""
مرحباً بك في عالم بوت متجر 😊

بوت مخصص لملفات بايثون ملفات بوتات وادوات وسكريبتات.. ثقتكم هي سر نجاحنا.

🌟 **منتج متجر 𝑵𝑮 𝑴𝑶𝑫𝑺 يرحب بكم!** 🌟
استكشف أقسامنا المتنوعة واحصل على ملف فوراً.

**اختر من القائمة أدناه للبدء:**

━━━━━━━━━━━━━━━━━━━━━━
🆔 **معرفك:** `{chat_id}`
💰 **رصيدك:** `{points}` {currency['symbol']}
━━━━━━━━━━━━━━━━━━━━━━
"""
    bot.send_message(chat_id, welcome_text, reply_markup=main_kb(chat_id, lang), parse_mode='Markdown')

# ============ الكولباك ============
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = str(call.message.chat.id)
    lang = user_languages.get(chat_id, 'ar')
    
    # ✅ التحقق من الاشتراك قبل أي أمر (باستثناء زر التحقق نفسه)
    if not check_all_subscriptions(chat_id) and call.data not in ["check_sub"]:
        bot.answer_callback_query(call.id, "⚠️ اشترك في جميع القنوات أولاً!", show_alert=True)
        return
    
    # ===== تغيير العملة =====
    if call.data == "change_currency":
        current_currency = get_user_currency(chat_id)
        current = CURRENCIES.get(current_currency, CURRENCIES["usd"])
        text = f"""
💱 **تغيير العملة**

العملة الحالية: {current['flag']} {current['name']} ({current['symbol']})

اختر العملة التي تريدها:
"""
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=currency_kb(lang))
        return
    
    if call.data.startswith("set_currency_"):
        new_currency = call.data.replace("set_currency_", "")
        if new_currency in CURRENCIES:
            user_currencies[chat_id] = new_currency
            save_data()
            currency = CURRENCIES[new_currency]
            bot.answer_callback_query(call.id, f"✅ تم تغيير العملة إلى {currency['name']}")
            start(call.message)
        return
    
    # ===== تحقق اشتراك =====
    if call.data == "check_sub":
        if check_all_subscriptions(chat_id):
            bot.answer_callback_query(call.id, "✅ تم التحقق! مرحباً بك 🎉", show_alert=True)
            start(call.message)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في جميع القنوات! اشترك ثم اضغط تحقق", show_alert=True)
        return
    
    # ===== استبدال كود =====
    if call.data == "redeem_code_public":
        if not bot_settings["redeem_code"]:
            bot.answer_callback_query(call.id, "⛔ معطل", show_alert=True)
            return
        bot.edit_message_text("🔄 **استبدال كود**\n\nأرسل الكود الذي تريد استبداله:", chat_id, call.message.message_id, reply_markup=back_kb(lang), parse_mode='Markdown')
        bot.register_next_step_handler(call.message, redeem_code)
        return
    
    # ===== تأكيد الشراء =====
    if call.data.startswith("buy_confirm_"):
        product_id = call.data.replace("buy_confirm_", "")
        
        if product_id not in store_items:
            bot.answer_callback_query(call.id, "❌ المنتج غير موجود")
            return
        
        item = store_items[product_id]
        
        if user_points.get(chat_id, 0) < item["price"]:
            bot.answer_callback_query(call.id, f"❌ رصيدك غير كافي! تحتاج {item['price']} نقطة", show_alert=True)
            return
        
        user_points[chat_id] = user_points.get(chat_id, 0) - item["price"]
        save_data()
        
        # ===== إرسال الملف تلقائياً =====
        if item.get('file_path'):
            try:
                if os.path.exists(item['file_path']):
                    with open(item['file_path'], 'rb') as f:
                        bot.send_document(chat_id, f, caption="📎 **ملف المنتج**")
                else:
                    bot.send_message(chat_id, f"⚠️ الملف غير موجود: `{item['file_path']}`")
            except Exception as e:
                print(f"خطأ في إرسال الملف: {e}")
                bot.send_message(chat_id, "⚠️ حدث خطأ في إرسال الملف، تواصل مع الدعم.")
        
        currency = CURRENCIES.get(get_user_currency(chat_id), CURRENCIES["usd"])
        
        success_text = f"""
✅ **تم شراء بنجاح!**

📂 ملف: {item['country']}
⭐ السعر: {item['price']} نقطة
💰 رصيدك المتبقي: {user_points[chat_id]} {currency['symbol']}

📩 سيتم التواصل معك من قبل المطور قريباً لتسليم الملف.
"""
        bot.edit_message_text(success_text, chat_id, call.message.message_id, reply_markup=back_kb(lang))
        bot.answer_callback_query(call.id, "✅ تم الشراء بنجاح!")
        
        try:
            user = call.from_user
            username = f"@{user.username}" if user.username else "لا يوجد"
            full_name = user.full_name if user.full_name else "لا يوجد"
            
            admin_text = f"""
🛒 **طلب شراء جديد!**

━━━━━━━━━━━━━━━━━━━━━
👤 **المستخدم:** `{chat_id}`
📛 **اليوزر:** {username}
👤 **الاسم:** {full_name}
📂 **ملف:** {item['country']}
⭐ **السعر:** {item['price']} نقطة
💰 **رصيده المتبقي:** {user_points[chat_id]} نقطة
🕐 **الوقت:** {time.strftime('%Y-%m-%d %H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━

📌 **ملاحظة:** قم بالتواصل مع المستخدم لتسليم الملف.
"""
            bot.send_message(ADMIN_ID, admin_text, parse_mode='Markdown')
        except Exception as e:
            print(f"خطأ في إرسال إشعار الأدمن: {e}")
        
        return
    
    # ===== إلغاء الشراء =====
    if call.data.startswith("buy_cancel_"):
        product_id = call.data.replace("buy_cancel_", "")
        
        if product_id not in store_items:
            bot.answer_callback_query(call.id, "❌ المنتج غير موجود")
            return
        
        item = store_items[product_id]
        
        text = f"""
❌ **تم إلغاء الشراء!**

📂 ملف: {item['country']}
⭐ السعر: {item['price']} نقطة

تم إلغاء عملية الشراء بنجاح.
"""
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=back_kb(lang))
        bot.answer_callback_query(call.id, "❌ تم الإلغاء")
        return
    
    # ===== شراء أرقام (العروض) =====
    if call.data == "buy_numbers":
        if not bot_settings["buy_numbers"]:
            bot.answer_callback_query(call.id, "⛔ معطل", show_alert=True)
            return
        if not store_items:
            bot.edit_message_text("❌ لا توجد عروض حالياً", chat_id, call.message.message_id, reply_markup=back_kb(lang))
            return
        kb = types.InlineKeyboardMarkup(row_width=2)
        for pid, item in store_items.items():
            kb.add(types.InlineKeyboardButton(f"📂 {item['country']} - {item['price']}⭐", callback_data=f"buy_{pid}"))
        kb.add(types.InlineKeyboardButton("رجوع", callback_data="back", style="danger"))
        bot.edit_message_text("🛍️ اختر العرض المناسب:", chat_id, call.message.message_id, reply_markup=kb)
    
    elif call.data.startswith("buy_"):
        product_id = call.data.replace("buy_", "")
        if product_id not in store_items:
            bot.answer_callback_query(call.id, "❌ غير موجود")
            return
        
        item = store_items[product_id]
        
        text = f"""
📂 **{item['country']}** اسم السلعة:
📝 وصف السلعة: لا يوجد

💰 السعر الحالي: {item['price']} نقطة
📦 حالة التوفير: عند طلب

✦━━━━━━━━━━━━━━━━━━✦
هل أنت متأكد من رغبتك في الشراء؟
"""
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=confirm_kb(product_id, lang))
    
    # ===== حسابي =====
    elif call.data == "my_account":
        points = user_points.get(chat_id, 0)
        currency = CURRENCIES.get(get_user_currency(chat_id), CURRENCIES["usd"])
        text = f"""
✦━━━━━━━━━━━━━━━━━━✦
👤 **حسابي**
✦━━━━━━━━━━━━━━━━━━✦

🆔 **المعرف:** `{chat_id}`
⭐ **النقاط:** {points}
💰 **الرصيد:** {points} {currency['symbol']}

✦━━━━━━━━━━━━━━━━━━✦
"""
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=back_kb(lang), parse_mode='Markdown')
    
    # ===== هدية يومية =====
    elif call.data == "daily_gift":
        if not bot_settings["daily_gift"]:
            bot.answer_callback_query(call.id, "⛔ معطل", show_alert=True)
            return
        now = time.time()
        if chat_id in daily_gift_cooldown and (now - daily_gift_cooldown[chat_id]) < 86400:
            remaining = int(86400 - (now - daily_gift_cooldown[chat_id]))
            h = remaining // 3600
            m = (remaining % 3600) // 60
            bot.answer_callback_query(call.id, f"⏳ انتظر {h}h {m}m", show_alert=True)
            return
        
        points = settings['daily_gift_amount']
        user_points[chat_id] = user_points.get(chat_id, 0) + points
        daily_gift_cooldown[chat_id] = now
        save_data()
        currency = CURRENCIES.get(get_user_currency(chat_id), CURRENCIES["usd"])
        bot.answer_callback_query(call.id, f"🎁 حصلت على {points} {currency['symbol']}!", show_alert=True)
    
    # ===== شحن رصيد =====
    elif call.data == "recharge":
        if not bot_settings["recharge"]:
            bot.answer_callback_query(call.id, "⛔ خاصية الشحن معطلة حالياً", show_alert=True)
            return
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("📩 تواصل مع المطور", url="https://t.me/BBH_S", style="success"))
        kb.add(types.InlineKeyboardButton("رجوع", callback_data="back", style="danger"))
        bot.edit_message_text("💰 **شحن رصيد**\n\nللشحن تواصل مع المطور مباشرة:", chat_id, call.message.message_id, reply_markup=kb)
    
    # ===== تحويل رصيد =====
    elif call.data == "transfer":
        if not bot_settings["transfer"]:
            bot.answer_callback_query(call.id, "⛔ خاصية التحويل معطلة حالياً", show_alert=True)
            return
        
        transfer_data[chat_id] = {"step": "waiting_id"}
        text = f"""
💸 **خدمة تحويل الرصيد**

> العطاء لا ينقص من المال شيئاً.. شارك رصيدك مع أصدقائك وادعمهم في الحصول على أرقامهم المفضلة.

تتيح لك هذه الخدمة تحويل جزء من رصيدك الحالي لمستخدم آخر داخل البوت بشكل فوري.

✦━━━━━━━━━━━━━━━━━━✦

📝 **الرجاء إرسال ID المستخدم الذي تود التحويل إليه:**

📌 **ملاحظة:** سيتم خصم {settings['transfer_fee_percent']}% رسوم تحويل.
"""
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=back_kb(lang), parse_mode='Markdown')
    
    # ===== دعوة صديق =====
    elif call.data == "invite":
        if not bot_settings["invite"]:
            bot.answer_callback_query(call.id, "⛔ خاصية الدعوة معطلة حالياً", show_alert=True)
            return
        link = f"https://t.me/{bot.get_me().username}?start={chat_id}"
        text = f"""
🤝 **دعوة صديق**

🎁 كل شخص يدخل عبر رابطك تحصل على نقطة!

🔗 رابط الدعوة الخاص بك:
`{link}`

📤 شارك الرابط مع أصدقائك!
"""
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=back_kb(lang), parse_mode='Markdown')
    
    # ===== شروط =====
    elif call.data == "terms":
        text = """
✦━━━━━━━━━━━━━━━━━━✦
🌟 **ميثاق الاستخدام والقوانين** 🌟
✦━━━━━━━━━━━━━━━━━━✦

1️⃣ **شحن الرصيد:** يتم حصراً عبر المطور الرسمي.
2️⃣ **المسؤولية:** بمجرد استلامك للحساب، تنتهي مسؤولية المطور.
3️⃣ **الدعم الفني:** تواصل مع الدعم الرسمي.
4️⃣ **الضمان:** 8 ساعات على تجميد الأرقام.
✦━━━━━━━━━━━━━━━━━━✦
📩 **للتواصل مع الدعم:** `@BBH_S`
✦━━━━━━━━━━━━━━━━━━✦
"""
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=back_kb(lang), parse_mode='Markdown')
    
    # ===== لغة =====
    elif call.data == "change_lang":
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb.add(
            types.InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar", style="success"),
            types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en", style="success")
        )
        kb.add(types.InlineKeyboardButton("رجوع", callback_data="back", style="danger"))
        bot.edit_message_text("🌐 اختر اللغة:", chat_id, call.message.message_id, reply_markup=kb)
    
    elif call.data.startswith("lang_"):
        new_lang = call.data.split("_")[1]
        user_languages[chat_id] = new_lang
        save_data()
        bot.answer_callback_query(call.id, "✅ تم")
        start(call.message)
    
    # ===== قناة =====
    elif call.data == "channel":
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("📢 اشترك الآن", url="https://t.me/TATYCODEX", style="success"))
        kb.add(types.InlineKeyboardButton("رجوع", callback_data="back", style="danger"))
        bot.edit_message_text("📢 قناة التفعيلات:\n\nhttps://t.me/TATYCODEX", chat_id, call.message.message_id, reply_markup=kb)
    
    # ===== تحديثات =====
    elif call.data == "updates":
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🔄 قناة التحديثات", url="https://t.me/TATYCODEX", style="success"))
        kb.add(types.InlineKeyboardButton("رجوع", callback_data="back", style="danger"))
        bot.edit_message_text("🔄 **آخر التحديثات:**\n\n• تم إضافة عروض جديدة\n• تحسينات في الأداء\n• إصلاح بعض الأخطاء", chat_id, call.message.message_id, reply_markup=kb)
    
    # ===== دعم فني =====
    elif call.data == "support":
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("📩 تواصل مع الدعم", url="https://t.me/BBH_S", style="success"))
        kb.add(types.InlineKeyboardButton("رجوع", callback_data="back", style="danger"))
        bot.edit_message_text("🆘 **الدعم الفني**\n\nللاستفسارات أو المشاكل تواصل مع الدعم:", chat_id, call.message.message_id, reply_markup=kb)
    
    # ===== رجوع =====
    elif call.data == "back":
        start(call.message)
    
    # ===== لوحة التحكم =====
    elif call.data == "admin" and str(chat_id) == ADMIN_ID:
        admin_panel(call.message)
    
    elif call.data.startswith("admin_") and str(chat_id) == ADMIN_ID:
        handle_admin_callbacks(call)

# ============ دوال الأدمن ============
def admin_panel(message):
    chat_id = str(message.chat.id)
    if chat_id != ADMIN_ID:
        return
    
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("➕ إضافة منتج", callback_data="admin_add_product", style="success"),
        types.InlineKeyboardButton("➖ حذف منتج", callback_data="admin_del_product", style="success")
    )
    kb.add(
        types.InlineKeyboardButton("📋 عرض المنتجات", callback_data="admin_list_products", style="danger"),
        types.InlineKeyboardButton("💰 إدارة النقاط", callback_data="admin_points", style="danger")
    )
    kb.add(
        types.InlineKeyboardButton("🎫 إنشاء كود", callback_data="admin_create_code", style="primary"),
        types.InlineKeyboardButton("📊 الكودات", callback_data="admin_list_codes", style="primary")
    )
    kb.add(
        types.InlineKeyboardButton("📢 إرسال جماعي", callback_data="admin_broadcast", style="success"),
        types.InlineKeyboardButton("⚙️ الإعدادات", callback_data="admin_settings", style="success")
    )
    kb.add(
        types.InlineKeyboardButton("🎁 تعديل الهدية", callback_data="admin_daily_gift", style="danger"),
        types.InlineKeyboardButton("💸 رسوم التحويل", callback_data="admin_transfer_fee", style="danger")
    )
    kb.add(
        types.InlineKeyboardButton("💱 تغيير العملة للجميع", callback_data="admin_currency", style="primary")
    )
    kb.add(types.InlineKeyboardButton("رجوع", callback_data="back", style="success"))
    
    bot.edit_message_text("⚙️ **لوحة التحكم**", chat_id, message.message_id, reply_markup=kb, parse_mode='Markdown')

def handle_admin_callbacks(call):
    chat_id = str(call.message.chat.id)
    lang = user_languages.get(chat_id, 'ar')
    data = call.data
    
    # ===== تغيير العملة للجميع (الأدمن) =====
    if data == "admin_currency":
        kb = types.InlineKeyboardMarkup(row_width=3)
        for code, currency in CURRENCIES.items():
            kb.add(types.InlineKeyboardButton(
                f"{currency['flag']} {currency['name']}",
                callback_data=f"admin_set_currency_{code}"
            ))
        kb.add(types.InlineKeyboardButton("رجوع", callback_data="admin", style="danger"))
        bot.edit_message_text(
            "💱 **تغيير العملة للجميع**\n\nاختر العملة التي تريد تعيينها لجميع المستخدمين:",
            chat_id, call.message.message_id, reply_markup=kb
        )
        return
    
    if data.startswith("admin_set_currency_"):
        new_currency = data.replace("admin_set_currency_", "")
        if new_currency in CURRENCIES:
            count = 0
            for user_id in user_currencies.keys():
                user_currencies[user_id] = new_currency
                count += 1
            save_data()
            currency = CURRENCIES[new_currency]
            bot.answer_callback_query(call.id, f"✅ تم تغيير عملة {count} مستخدم إلى {currency['name']}")
            admin_panel(call.message)
        return
    
    # ===== إضافة منتج =====
    if data == "admin_add_product":
        bot.edit_message_text("📝 **إضافة منتج جديد**\n\nأرسل اسم ملف:", chat_id, call.message.message_id, reply_markup=back_kb(lang))
        bot.register_next_step_handler(call.message, add_product_step1)
    
    # ===== حذف منتج =====
    elif data == "admin_del_product":
        if not store_items:
            bot.edit_message_text("❌ لا توجد منتجات للحذف", chat_id, call.message.message_id, reply_markup=back_kb(lang))
            return
        
        kb = types.InlineKeyboardMarkup(row_width=2)
        for pid, item in store_items.items():
            kb.add(types.InlineKeyboardButton(f"🗑 {item['country']}", callback_data=f"del_{pid}"))
        kb.add(types.InlineKeyboardButton("رجوع", callback_data="back", style="danger"))
        bot.edit_message_text("🗑 اختر المنتج للحذف:", chat_id, call.message.message_id, reply_markup=kb)
    
    elif data.startswith("del_"):
        pid = data.replace("del_", "")
        if pid in store_items:
            del store_items[pid]
            save_data()
            bot.answer_callback_query(call.id, "✅ تم الحذف")
            bot.edit_message_text("✅ تم حذف المنتج", chat_id, call.message.message_id, reply_markup=back_kb(lang))
        else:
            bot.answer_callback_query(call.id, "❌ غير موجود")
    
    # ===== عرض المنتجات =====
    elif data == "admin_list_products":
        if not store_items:
            bot.edit_message_text("❌ لا توجد منتجات", chat_id, call.message.message_id, reply_markup=back_kb(lang))
            return
        
        text = "📋 **قائمة المنتجات:**\n\n"
        for pid, item in store_items.items():
            text += f"🆔 {pid}\n📂 {item['country']}\n⭐ {item['price']} نقطة\n📎 الملف: {item.get('file_path', 'لا يوجد')}\n━━━━━━━━━━━━\n"
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=back_kb(lang))
    
    # ===== إدارة النقاط =====
    elif data == "admin_points":
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb.add(
            types.InlineKeyboardButton("➕ إضافة نقاط", callback_data="admin_add_points", style="success"),
            types.InlineKeyboardButton("➖ خصم نقاط", callback_data="admin_remove_points", style="success")
        )
        kb.add(
            types.InlineKeyboardButton("📊 عرض رصيد", callback_data="admin_show_points", style="danger"),
            types.InlineKeyboardButton("رجوع", callback_data="admin", style="primary")
        )
        bot.edit_message_text("💰 **إدارة النقاط**", chat_id, call.message.message_id, reply_markup=kb)
    
    elif data == "admin_add_points":
        bot.edit_message_text("➕ **إضافة نقاط**\n\nأرسل ID المستخدم:", chat_id, call.message.message_id, reply_markup=back_kb(lang))
        pending_points[chat_id] = {"action": "add"}
        bot.register_next_step_handler(call.message, process_points)
    
    elif data == "admin_remove_points":
        bot.edit_message_text("➖ **خصم نقاط**\n\nأرسل ID المستخدم:", chat_id, call.message.message_id, reply_markup=back_kb(lang))
        pending_points[chat_id] = {"action": "remove"}
        bot.register_next_step_handler(call.message, process_points)
    
    elif data == "admin_show_points":
        bot.edit_message_text("📊 **عرض رصيد**\n\nأرسل ID المستخدم:", chat_id, call.message.message_id, reply_markup=back_kb(lang))
        pending_points[chat_id] = {"action": "show"}
        bot.register_next_step_handler(call.message, process_points)
    
    # ===== إنشاء كود =====
    elif data == "admin_create_code":
        bot.edit_message_text("🎫 **إنشاء كود خصم**\n\nأرسل عدد النقاط للكود:", chat_id, call.message.message_id, reply_markup=back_kb(lang))
        bot.register_next_step_handler(call.message, create_code_step1)
    
    # ===== عرض الكودات =====
    elif data == "admin_list_codes":
        if not promo_codes:
            bot.edit_message_text("❌ لا توجد كودات", chat_id, call.message.message_id, reply_markup=back_kb(lang))
            return
        
        text = "📊 **قائمة الكودات:**\n\n"
        for code, code_data in promo_codes.items():
            if isinstance(code_data, dict):
                text += f"🔑 {code}\n⭐ {code_data['points']} نقطة\n👥 متبقي: {code_data['uses_left']}\n━━━━━━━━━━━━\n"
            else:
                text += f"🔑 {code}\n⭐ {code_data} نقطة\n━━━━━━━━━━━━\n"
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=back_kb(lang))
    
    # ===== إرسال جماعي =====
    elif data == "admin_broadcast":
        bot.edit_message_text("📢 **إرسال جماعي**\n\nأرسل الرسالة التي تريد إرسالها للجميع:", chat_id, call.message.message_id, reply_markup=back_kb(lang))
        bot.register_next_step_handler(call.message, broadcast_message)
    
    # ===== الإعدادات (تم إزالة زر force_subscribe) =====
    elif data == "admin_settings":
        settings_text = f"""
⚙️ **الإعدادات الحالية:**

🛒 العروض: {'✅' if bot_settings['buy_numbers'] else '❌'}
🎁 هدية يومية: {'✅' if bot_settings['daily_gift'] else '❌'} (القيمة: {settings['daily_gift_amount']} نقطة)
💰 شحن رصيد: {'✅' if bot_settings['recharge'] else '❌'}
💸 تحويل رصيد: {'✅' if bot_settings['transfer'] else '❌'} (الرسوم: {settings['transfer_fee_percent']}%)
🤝 دعوة: {'✅' if bot_settings['invite'] else '❌'}
🔒 اشتراك إجباري: ✅ (مفعل دائماً - @TATYCODEX)
🔄 استبدال كود: {'✅' if bot_settings['redeem_code'] else '❌'}
"""
        kb = types.InlineKeyboardMarkup(row_width=2)
        # ✅ إنشاء الأزرار مع تخطي force_subscribe لمنع التعديل
        for key in bot_settings:
            if key == "force_subscribe":
                continue  # لا نضيف زر لهذا الخيار
            status = "✅" if bot_settings[key] else "❌"
            kb.add(types.InlineKeyboardButton(f"{status} {key}", callback_data=f"toggle_{key}"))
        kb.add(types.InlineKeyboardButton("رجوع", callback_data="admin", style="danger"))
        bot.edit_message_text(settings_text, chat_id, call.message.message_id, reply_markup=kb)
    
    elif data.startswith("toggle_"):
        key = data.replace("toggle_", "")
        # ✅ منع تعديل force_subscribe حتى لو حاول أحد اختراق الكيبورد
        if key == "force_subscribe":
            bot.answer_callback_query(call.id, "⛔ هذا الإعداد ثابت ولا يمكن تغييره!", show_alert=True)
            return
        if key in bot_settings:
            bot_settings[key] = not bot_settings[key]
            save_data()
            bot.answer_callback_query(call.id, f"✅ تم تغيير {key}")
            admin_panel(call.message)
    
    # ===== تعديل الهدية اليومية =====
    elif data == "admin_daily_gift":
        kb = types.InlineKeyboardMarkup(row_width=3)
        for val in [1, 2, 3, 5, 10, 15, 20, 25, 50]:
            kb.add(types.InlineKeyboardButton(f"{val} نقطة", callback_data=f"set_gift_{val}"))
        kb.add(types.InlineKeyboardButton("رجوع", callback_data="admin", style="danger"))
        bot.edit_message_text(f"🎁 **تعديل الهدية اليومية**\n\nالقيمة الحالية: {settings['daily_gift_amount']} نقطة\n\nاختر القيمة الجديدة:", chat_id, call.message.message_id, reply_markup=kb)
    
    elif data.startswith("set_gift_"):
        settings['daily_gift_amount'] = int(data.replace("set_gift_", ""))
        save_data()
        bot.answer_callback_query(call.id, f"✅ تم تعديل الهدية إلى {settings['daily_gift_amount']} نقطة")
        admin_panel(call.message)
    
    # ===== تعديل رسوم التحويل =====
    elif data == "admin_transfer_fee":
        kb = types.InlineKeyboardMarkup(row_width=3)
        for val in [0, 1, 2, 3, 5, 7, 10, 15, 20]:
            kb.add(types.InlineKeyboardButton(f"{val}%", callback_data=f"set_fee_{val}"))
        kb.add(types.InlineKeyboardButton("رجوع", callback_data="admin", style="danger"))
        bot.edit_message_text(f"💸 **تعديل رسوم التحويل**\n\nالقيمة الحالية: {settings['transfer_fee_percent']}%\n\nاختر النسبة الجديدة:", chat_id, call.message.message_id, reply_markup=kb)
    
    elif data.startswith("set_fee_"):
        settings['transfer_fee_percent'] = int(data.replace("set_fee_", ""))
        save_data()
        bot.answer_callback_query(call.id, f"✅ تم تعديل رسوم التحويل إلى {settings['transfer_fee_percent']}%")
        admin_panel(call.message)

# ===== دوال إنشاء الكود =====
def create_code_step1(message):
    chat_id = str(message.chat.id)
    try:
        points = int(message.text.strip())
        admin_create_code[chat_id] = {"points": points}
        bot.send_message(chat_id, "📝 أرسل **عدد المستخدمين** الذين يمكنهم استخدام هذا الكود:", reply_markup=back_kb(user_languages.get(chat_id, 'ar')))
        bot.register_next_step_handler(message, create_code_step2)
    except:
        bot.send_message(chat_id, "❌ أرسل رقم صحيح!", reply_markup=back_kb(user_languages.get(chat_id, 'ar')))
        bot.register_next_step_handler(message, create_code_step1)

def create_code_step2(message):
    chat_id = str(message.chat.id)
    try:
        users_count = int(message.text.strip())
        points = admin_create_code[chat_id]["points"]
        
        code = generate_code()
        promo_codes[code] = {
            "points": points,
            "uses_left": users_count,
            "total_uses": users_count
        }
        save_data()
        del admin_create_code[chat_id]
        
        bot.send_message(chat_id, f"""
✅ **تم إنشاء الكود بنجاح!**

🔑 **الكود:** `{code}`
⭐ **النقاط:** {points}
👥 **عدد المستخدمين:** {users_count}

📌 يمكن استخدام الكود {users_count} مرة.
""", reply_markup=main_kb(chat_id, user_languages.get(chat_id, 'ar')))
    except:
        bot.send_message(chat_id, "❌ أرسل رقم صحيح!", reply_markup=back_kb(user_languages.get(chat_id, 'ar')))
        bot.register_next_step_handler(message, create_code_step2)

# ===== دوال إضافة المنتج =====
def add_product_step1(message):
    chat_id = str(message.chat.id)
    country = message.text.strip()
    admin_create_product[chat_id] = {"country": country}
    bot.send_message(chat_id, "💰 أرسل **السعر** (بالنقاط):", reply_markup=back_kb(user_languages.get(chat_id, 'ar')))
    bot.register_next_step_handler(message, add_product_step2)

def add_product_step2(message):
    chat_id = str(message.chat.id)
    try:
        price = int(message.text.strip())
        admin_create_product[chat_id]["price"] = price
        admin_create_product[chat_id]["step"] = "file"
        bot.send_message(chat_id, "📤 **أرسل ملف المنتج** (ارفع ملف وليس نص):", reply_markup=back_kb(user_languages.get(chat_id, 'ar')))
        bot.register_next_step_handler(message, add_product_step3)
        return
    except:
        bot.send_message(chat_id, "❌ السعر غير صحيح! أرسل رقم فقط.", reply_markup=back_kb(user_languages.get(chat_id, 'ar')))
        bot.register_next_step_handler(message, add_product_step2)

def add_product_step3(message):
    chat_id = str(message.chat.id)
    
    # ===== التأكد إن المستخدم رفع ملف =====
    if not message.document:
        bot.send_message(chat_id, "❌ **يرجى رفع ملف، وليس كتابة نص!**\nأعد رفع الملف:", reply_markup=back_kb(user_languages.get(chat_id, 'ar')))
        bot.register_next_step_handler(message, add_product_step3)
        return
    
    try:
        # ===== تحميل الملف =====
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = message.document.file_name
        
        # ===== حفظ الملف في مجلد المنتجات =====
        product_dir = os.path.join("products", str(chat_id))
        os.makedirs(product_dir, exist_ok=True)
        file_path = os.path.join(product_dir, file_name)
        with open(file_path, 'wb') as f:
            f.write(downloaded_file)
        
        # ===== حفظ مسار الملف في المنتج =====
        admin_create_product[chat_id]["file_path"] = file_path
        
        # ===== إضافة المنتج =====
        product_id = str(len(store_items) + 1)
        store_items[product_id] = admin_create_product[chat_id]
        save_data()
        del admin_create_product[chat_id]
        
        bot.send_message(
            chat_id,
            f"✅ **تم إضافة المنتج بنجاح!**\n\n"
            f"📂 ملف: {store_items[product_id]['country']}\n"
            f"⭐ السعر: {store_items[product_id]['price']} نقطة\n"
            f"📎 الملف: `{file_name}`",
            reply_markup=main_kb(chat_id, user_languages.get(chat_id, 'ar'))
        )
    except Exception as e:
        bot.send_message(chat_id, f"❌ حدث خطأ: {e}\nحاول مرة أخرى.", reply_markup=back_kb(user_languages.get(chat_id, 'ar')))
        bot.register_next_step_handler(message, add_product_step3)

# ===== دوال النقاط =====
def process_points(message):
    chat_id = str(message.chat.id)
    target_id = message.text.strip()
    
    if target_id not in user_points:
        bot.send_message(chat_id, "❌ المستخدم غير موجود!", reply_markup=main_kb(chat_id, user_languages.get(chat_id, 'ar')))
        return
    
    action = pending_points[chat_id]["action"]
    
    if action == "show":
        currency = CURRENCIES.get(get_user_currency(target_id), CURRENCIES["usd"])
        bot.send_message(chat_id, f"👤 **المستخدم:** `{target_id}`\n⭐ **النقاط:** {user_points[target_id]} {currency['symbol']}", reply_markup=main_kb(chat_id, user_languages.get(chat_id, 'ar')))
        del pending_points[chat_id]
        return
    
    bot.send_message(chat_id, f"📝 أرسل عدد النقاط لـ {action == 'add' and 'إضافة' or 'خصم'}:")
    bot.register_next_step_handler(message, process_points_amount, target_id, action)

def process_points_amount(message, target_id, action):
    chat_id = str(message.chat.id)
    try:
        amount = int(message.text.strip())
        currency = CURRENCIES.get(get_user_currency(target_id), CURRENCIES["usd"])
        
        if action == "add":
            user_points[target_id] = user_points.get(target_id, 0) + amount
            bot.send_message(chat_id, f"✅ تم إضافة {amount} {currency['symbol']} للمستخدم `{target_id}`\n⭐ الرصيد الحالي: {user_points[target_id]} {currency['symbol']}", reply_markup=main_kb(chat_id, user_languages.get(chat_id, 'ar')))
        else:
            if user_points.get(target_id, 0) < amount:
                bot.send_message(chat_id, f"❌ رصيد المستخدم غير كافي! عنده {user_points.get(target_id, 0)} {currency['symbol']} فقط.", reply_markup=main_kb(chat_id, user_languages.get(chat_id, 'ar')))
                return
            user_points[target_id] = user_points.get(target_id, 0) - amount
            bot.send_message(chat_id, f"✅ تم خصم {amount} {currency['symbol']} من المستخدم `{target_id}`\n⭐ الرصيد المتبقي: {user_points[target_id]} {currency['symbol']}", reply_markup=main_kb(chat_id, user_languages.get(chat_id, 'ar')))
        
        save_data()
        del pending_points[chat_id]
    except:
        bot.send_message(chat_id, "❌ أرسل رقم صحيح!", reply_markup=back_kb(user_languages.get(chat_id, 'ar')))
        bot.register_next_step_handler(message, process_points_amount, target_id, action)

# ===== دوال التحويل =====
@bot.message_handler(func=lambda message: str(message.chat.id) in transfer_data and transfer_data[str(message.chat.id)]["step"] == "waiting_id")
def transfer_step_id(message):
    chat_id = str(message.chat.id)
    target_id = message.text.strip()
    
    if target_id == chat_id:
        bot.send_message(chat_id, "❌ لا يمكنك التحويل لنفسك!", reply_markup=main_kb(chat_id, user_languages.get(chat_id, 'ar')))
        del transfer_data[chat_id]
        return
    
    if target_id not in user_points:
        bot.send_message(chat_id, "❌ المستخدم غير موجود!", reply_markup=main_kb(chat_id, user_languages.get(chat_id, 'ar')))
        del transfer_data[chat_id]
        return
    
    transfer_data[chat_id]["target"] = target_id
    transfer_data[chat_id]["step"] = "waiting_amount"
    bot.send_message(chat_id, f"📝 أرسل **عدد النقاط** التي تريد تحويلها للمستخدم `{target_id}`:\n\n📌 سيتم خصم {settings['transfer_fee_percent']}% رسوم تحويل.", reply_markup=back_kb(user_languages.get(chat_id, 'ar')))

@bot.message_handler(func=lambda message: str(message.chat.id) in transfer_data and transfer_data[str(message.chat.id)]["step"] == "waiting_amount")
def transfer_step_amount(message):
    chat_id = str(message.chat.id)
    try:
        amount = int(message.text.strip())
        target_id = transfer_data[chat_id]["target"]
        
        fee = int(amount * settings['transfer_fee_percent'] / 100)
        total_deduction = amount + fee
        
        if user_points.get(chat_id, 0) < total_deduction:
            bot.send_message(chat_id, f"❌ رصيدك غير كافي! تحتاج {total_deduction} نقطة (الرسوم: {fee})", reply_markup=main_kb(chat_id, user_languages.get(chat_id, 'ar')))
            del transfer_data[chat_id]
            return
        
        user_points[chat_id] = user_points.get(chat_id, 0) - total_deduction
        user_points[target_id] = user_points.get(target_id, 0) + amount
        save_data()
        
        currency = CURRENCIES.get(get_user_currency(chat_id), CURRENCIES["usd"])
        target_currency = CURRENCIES.get(get_user_currency(target_id), CURRENCIES["usd"])
        
        bot.send_message(chat_id, f"""
✅ **تم التحويل بنجاح!**

💸 **المبلغ:** {amount} {currency['symbol']}
📊 **الرسوم:** {fee} {currency['symbol']} ({settings['transfer_fee_percent']}%)
💰 **المبلغ المخصوم:** {total_deduction} {currency['symbol']}
👤 **إلى:** `{target_id}`
⭐ **رصيدك المتبقي:** {user_points[chat_id]} {currency['symbol']}
""", reply_markup=main_kb(chat_id, user_languages.get(chat_id, 'ar')))
        
        try:
            bot.send_message(target_id, f"""
💸 **استلام تحويل!**

👤 **من:** `{chat_id}`
💰 **المبلغ:** {amount} {target_currency['symbol']}
⭐ **رصيدك الجديد:** {user_points[target_id]} {target_currency['symbol']}
""", parse_mode='Markdown')
        except:
            pass
        
        del transfer_data[chat_id]
    except:
        bot.send_message(chat_id, "❌ أرسل رقم صحيح!", reply_markup=back_kb(user_languages.get(chat_id, 'ar')))
        bot.register_next_step_handler(message, transfer_step_amount)

# ===== دوال استبدال الكود =====
def redeem_code(message):
    chat_id = str(message.chat.id)
    code = message.text.strip()
    lang = user_languages.get(chat_id, 'ar')
    
    if code in promo_codes:
        code_data = promo_codes[code]
        
        if isinstance(code_data, dict):
            if code_data["uses_left"] <= 0:
                bot.send_message(chat_id, "❌ هذا الكود انتهت صلاحيته!", reply_markup=main_kb(chat_id, lang))
                return
            points = code_data["points"]
            code_data["uses_left"] -= 1
            if code_data["uses_left"] <= 0:
                del promo_codes[code]
            else:
                promo_codes[code] = code_data
        else:
            points = code_data
            del promo_codes[code]
        
        user_points[chat_id] = user_points.get(chat_id, 0) + points
        save_data()
        
        currency = CURRENCIES.get(get_user_currency(chat_id), CURRENCIES["usd"])
        bot.send_message(chat_id, f"✅ **تم استبدال الكود بنجاح!**\n\n⭐ حصلت على {points} {currency['symbol']}\n💰 رصيدك الحالي: {user_points[chat_id]} {currency['symbol']}", reply_markup=main_kb(chat_id, lang))
    else:
        bot.send_message(chat_id, "❌ كود غير صحيح!", reply_markup=main_kb(chat_id, lang))

# ===== دوال البث =====
def broadcast_message(message):
    chat_id = str(message.chat.id)
    msg = message.text
    
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("✅ تأكيد الإرسال", callback_data="broadcast_confirm", style="success"),
        types.InlineKeyboardButton("❌ إلغاء", callback_data="back", style="success")
    )
    
    pending_broadcast[chat_id] = msg
    bot.send_message(chat_id, f"📢 **تأكيد الإرسال الجماعي**\n\nالرسالة:\n━━━━━━━━━━━━━━\n{msg}\n━━━━━━━━━━━━━━\n\nهل أنت متأكد من إرسالها للجميع؟", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data == "broadcast_confirm")
def broadcast_confirm(call):
    chat_id = str(call.message.chat.id)
    if chat_id != ADMIN_ID:
        return
    
    msg = pending_broadcast.get(chat_id)
    if not msg:
        bot.answer_callback_query(call.id, "❌ لا توجد رسالة")
        return
    
    bot.edit_message_text("📤 **جاري الإرسال...**", chat_id, call.message.message_id)
    
    sent = 0
    failed = 0
    for user_id in list(user_points.keys()):
        try:
            bot.send_message(user_id, msg)
            sent += 1
            time.sleep(0.1)
        except:
            failed += 1
    
    bot.edit_message_text(f"✅ **تم الإرسال بنجاح!**\n\n✅ تم الإرسال: {sent}\n❌ فشل: {failed}", chat_id, call.message.message_id, reply_markup=back_kb(user_languages.get(chat_id, 'ar')))
    del pending_broadcast[chat_id]

# ============ تشغيل البوت ============
print("🤖 البوت شغال... (الاشتراك الإجباري مفعل دائماً لقناة @TATYCODEX)")
bot.infinity_polling()
