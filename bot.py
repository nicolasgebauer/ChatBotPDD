import telebot

bot = telebot.TeleBot("5670463206:AAEoQE14qn2_TqV0qmyyRK5kgDv-BJmDxto")
@bot.message_handler(commands=["help","start"])


def numeros(message):
    bot.reply_to(message, "Hola,como estas?")
    for i in range(10):
        bot.reply_to(message, i)

bot.polling()