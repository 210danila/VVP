import telebot
from telebot import types

token = "2127614087:AAFF3GR92torXn7GIEFb4KoI-F8jYwGm7Ho"

bot = telebot.TeleBot(token)

@bot.message_handler(content_types=["text"])
def any_msg(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Нажми меня", callback_data="test")
    keyboard.add(callback_button)
    msg = bot.send_message(message.chat.id, "Я – сообщение из обычного режима", reply_markup=keyboard)
    bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="Пыщь")


# В большинстве случаев целесообразно разбить этот хэндлер на несколько маленьких
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "test":
            bot.send_message(chat_id=call.message.chat.id, text='hhh')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")


if __name__ == '__main__':
    bot.infinity_polling()