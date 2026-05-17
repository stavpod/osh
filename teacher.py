import telebot

TOKEN = "8637896450:AAGsB7u2dEfM_k8yAl-mUqZhIbNMM_Zbx4A"
bot = telebot.TeleBot(TOKEN)


last_meet_url = ""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Бот-сигнализация запущен. Ожидаю ссылку от учителя.")

@bot.message_handler(func=lambda message: "meet.google.com" in message.text)
def handle_link(message):
    global last_meet_url
    last_meet_url = message.text
    bot.reply_to(message, f"✅ Ссылка принята! Ученики получили сигнал.")


bot.polling(none_stop=True)