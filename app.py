import telebot
from const import keys, TOKEN
from extentions import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)



#@bot.message_handler()
#def echo_test(message: telebot.types.Message):
    #bot.send_message(message.chat.id, "Hello")

@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты цену которой он хочет узнать>\<имя валюты в которой надо узнать цену первой валюты>\<количество первой валюты>\nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) > 3:
            raise APIException("Слишком много параметров")

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")

    except Exception as e:
        bot.reply_to(message, f"не удалось обработать команду\n{e}")
    else:
        text = f"Цена{amount} {quote} в {base}-{total_base}"
        bot.send_message(message.chat.id, text)


bot.polling()