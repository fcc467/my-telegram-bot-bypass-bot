import telebot
import requests

# توكن بوت تلغرام (من BotFather)
BOT_TOKEN = "8916848099:AAEEDlUw-4cGRXnYWS8o6BT8fItPxMJ3_xw"

# مفتاح API الخاص بك
API_KEY = "ccsk_MR20ANFzTQDOVJprZdyoAI1Gk0kmg4lkvnz8usQ6vHQ"

# رابط API الموقع
BASE_URL = "https://api.ccraftspace.dpdns.org/api/v1/scripts"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك في بوت نياج عباس ارسلي رابط حته انيجه.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text.strip()
    msg = bot.reply_to(message, "⏳ جاري نكح رابط المفتاح.")

    headers = {
        "X-API-Key": API_KEY
    }

    try:
        url = f"{BASE_URL}/{user_input}" if user_input else BASE_URL
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            script_code = data.get("script", {}).get("code") or data.get("code") or str(data)
            
            if len(script_code) > 3500:
                script_code = script_code[:3500] + "\n... (تم اقتطاع النص لطوله)"

            bot.edit_message_text(f"✅ **تم جلب البيانات بنجاح:**\n\n```\n{script_code}\n```", 
                                  chat_id=message.chat.id, 
                                  message_id=msg.message_id, 
                                  parse_mode="Markdown")
        else:
            bot.edit_message_text(f"❌ حدث خطأ من الموقع ({response.status_code}):\n{response.text}", 
                                  chat_id=message.chat.id, 
                                  message_id=msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ أثناء الاتصال بالسيرفر: {str(e)}", 
                              chat_id=message.chat.id, 
                              message_id=msg.message_id)

bot.infinity_polling()
