import telebot

bot = telebot.TeleBot("5670463206:AAEoQE14qn2_TqV0qmyyRK5kgDv-BJmDxto")
@bot.message_handler(commands=["help","start"])


def enviar(message):
    bot.reply_to(message, "Hola,como estas?")


bot.polling()