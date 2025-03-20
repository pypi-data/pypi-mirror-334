import telebot
from luzigpt import LuziGPT  # luzigpt modülünü import ettik

# Telegram Bot Token
TOKEN = "TELEGRAM_BOT_TOKEN"
bot = telebot.TeleBot("6975616439:AAFKgeF7HC65Ho7RyjFcbvOU_6y4gL6-9a8")

# LuziGPT başlat
gpt = LuziGPT()

@bot.message_handler(commands=['soru'])
def handle_question(message):
    soru = message.text.replace("/soru", "").strip()  # Komuttan "/soru" kısmını çıkar
    
    if not soru:
        bot.reply_to(message, "Lütfen bir soru girin! Örnek: `/soru Merhaba`", parse_mode="Markdown")
        return

    # API'den cevabı al (LuziGPT modülünü kullanarak)
    cevap = gpt.cevap_ver(soru)
    
    # Cevap döndürme
    if cevap:
        bot.reply_to(message, cevap)
    else:
        bot.reply_to(message, "Üzgünüm, bu soruya yanıtım yok.")

print("Bot çalışıyor...")
bot.polling()
