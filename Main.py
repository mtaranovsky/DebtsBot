import config
import telebot
import re
from telebot import types


bot = telebot.TeleBot(config.token)
digits_pattern = re.compile(r'^[0-9]+$', re.MULTILINE)



@bot.message_handler(content_types=['text'])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    try:
        matches = re.match(digits_pattern, query.query)
    except AttributeError as ex:
        return
    num = matches.group()
    keybroad = types.InlineKeyboardMarkup()
    buttonAccept = types.InlineKeyboardButton(text='Прийняти', callback_data='accept')
    buttonCancel = types.InlineKeyboardButton(text='Відмінити', callback_data='cancel')
    keybroad.add(buttonAccept, buttonCancel)
    results = []
    msgLend = types.InlineQueryResultArticle(
        id='1', title='Дати в борг',
        input_message_content=types.InputTextMessageContent(message_text='Надано в борг '+num+' грн.'),
        reply_markup=keybroad
    )
    msgBorrow=types.InlineQueryResultArticle(
        id='2', title='Отримати в борг',
        input_message_content=types.InputTextMessageContent(message_text='Отримано в борг '+num+' грн.'),
        reply_markup=keybroad
    )
    msgReturn=types.InlineQueryResultArticle(
        id='3', title='Повернути борг',
        input_message_content=types.InputTextMessageContent(message_text='Повернено борг в сумі '+num+' грн.'),
        reply_markup=keybroad
    )

    results.append(msgLend)
    results.append(msgReturn)
    results.append(msgBorrow)
    bot.answer_inline_query(query.id, results)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.inline_message_id:
        if call.data == "accept":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text= '\nПрийнято')
    if call.inline_message_id:
        if call.data == "cancel":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text= '\nВідхилено')


if __name__ == '__main__':
     bot.polling(none_stop=True)