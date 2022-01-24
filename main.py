import vk_api
import json
# Достаём из неё longpoll
from vk_api.longpoll import VkLongPoll, VkEventType

import bot_data

token = bot_data.bot_token

# Подключаем токен и longpoll
Vk_bot = vk_api.VkApi(token=token)
give = Vk_bot.get_api()
longpoll = VkLongPoll(Vk_bot)


# Создадим функцию для ответа на сообщения в лс группы
def send_msg(id, text):
    Vk_bot.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})


# Слушаем longpoll(Сообщения)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        # Чтобы наш бот не слышал и не отвечал на самого себя
        if event.to_me:

            # Для того чтобы бот читал все с маленьких букв
            message = event.text.lower()
            # Получаем id пользователя
            id = event.user_id


            if message == 'привет':
                send_msg(id, 'Привет, я бот Артема!')
                print(event)
            elif message == 'как дела?':
                send_msg(id, 'Хорошо, а твои как?')

            else:
                send_msg(id, 'Я вас не понимаю! :(')

    if event.type == VkEventType.MESSAGE_EVENT:
        if event.to_me:
            if message == 'привет':
                send_msg(id, 'Привет, я бот Артема!')
