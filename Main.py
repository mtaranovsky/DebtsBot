# import config
# import db
# import telebot
# import re
#
#
# bot = telebot.TeleBot(config.token)
# digits_pattern = re.compile(r'^[0-9]+$', re.MULTILINE)
#
#
# # @bot.message_handler(content_telebot.types=['text'])
# # def repeat_all_messages(message):  # Название функции не играет никакой роли, в принципе
# #     bot.send_message(message.chat.id, message.text)
#
# @bot.message_handler(commands=['myWallet'])
# def send_wallet(message):
#     bot.reply_to(message, db.feedback(message.from_user.username))
#
#
# @bot.inline_handler(func=lambda query: len(query.query) > 0)
# def query_text(query):
#     try:
#         matches = re.match(digits_pattern, query.query)
#     except AttributeError as ex:
#         return
#     num = matches.group()
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     button_accept = telebot.types.InlineKeyboardButton(text='Прийняти', callback_data='accept')
#     button_cancel = telebot.types.InlineKeyboardButton(text='Відмінити', callback_data='cancel')
#     keyboard.add(button_accept, button_cancel)
#     results = []
#
#     msg_lend = telebot.types.InlineQueryResultArticle(
#         id='1', title='Дати в борг',
#         input_message_content=telebot.types.InputTextMessageContent(
#             message_text='Надано в борг ' + num + ' грн.\n' + str(query.from_user.username)),
#         reply_markup=keyboard
#     )
#     msg_borrow = telebot.types.InlineQueryResultArticle(
#         id='2', title='Отримати в борг',
#         input_message_content=telebot.types.InputTextMessageContent(
#             message_text='Отримано в борг ' + num + ' грн.\n' + str(query.from_user.username)),
#         reply_markup=keyboard
#     )
#     msg_return = telebot.types.InlineQueryResultArticle(
#         id='3', title='Повернути борг',
#         input_message_content=telebot.types.InputTextMessageContent(
#             message_text='Повернено борг в сумі ' + num + ' грн.\n' + str(query.from_user.username)),
#         reply_markup=keyboard
#     )
#
#     results.append(msg_lend)
#     results.append(msg_return)
#     results.append(msg_borrow)
#
#     bot.answer_inline_query(query.id, results)
#
#
# @bot.chosen_inline_handler(func=lambda chosen_inline_result: True)
# def chosen_msg(chosen_inline_result):
#     global num1, user_name
#     user_name = chosen_inline_result.from_user.username
#
#     if chosen_inline_result.result_id == '1' or chosen_inline_result.result_id == '3':
#         num1 = int(chosen_inline_result.query)
#     elif chosen_inline_result.result_id == '2':
#         num1 = - int(chosen_inline_result.query)
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#
#     if call.data == "accept":
#         bot.edit_message_text(inline_message_id=call.inline_message_id, text='\nПрийнято \n@' + call.from_user.username)
#         db.request(user_name, call.from_user.username,num1)
#     if call.data == "cancel":
#         bot.edit_message_text(inline_message_id=call.inline_message_id, text='\nВідхилено \n@' + call.from_user.username)
#
#
# @bot.inline_handler(func=lambda query: len(query.query) is 0)
# def query_empty(inline_query):
#
#     try:
#         msg_current_debs = telebot.types.InlineQueryResultArticle(
#             id='4',
#             title="Переглянути активні борги",
#             input_message_content=telebot.types.InputTextMessageContent(
#                 message_text=db.feedback(inline_query.from_user.username))
#         )
#         bot.answer_inline_query(inline_query.id, [msg_current_debs])
#     except Exception as e:
#         print(e)
#
#
# if __name__ == '__main__':
#     bot.polling(none_stop=True)
print("fm")