import requests
import bot_data
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from pprint import pprint

Vk_bot = vk_api.VkApi(token='9b1eb309d15d58b19d06f4808e0ab42bef5fa1bdec1032e442cc7e6979148aa9c444e043e856b75e389b3')
give = Vk_bot.get_api()
longpoll = VkLongPoll(Vk_bot)


# pair = Vk_bot.method('users.search',{'city': 1})
# print(pair)


def start():
    Vk_bot = vk_api.VkApi(token=bot_data.bot_token)
    give = Vk_bot.get_api()
    longpoll = VkLongPoll(Vk_bot)


def listen():
    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:  # Чтобы наш бот не слышал и не отвечал на самого себя
                message = event.text.lower()  # Для того чтобы бот читал все с маленьких букв
                user_id = event.user_id  # Получаем id пользователя

                if message == 'а':
                    user = (Vk_bot.method('users.get', {'user_ids': user_id, 'fields': 'city, nickname'}))[0]
                    pair = Vk_bot.method('users.search', {'city': 1})
                    send_msg(id, f'{user["first_name"]}\n{user["city"]["title"]}')
                    pprint(user)


def search_pair():
    pass


def send_msg(id, text):
    Vk_bot.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})


def get_user_info(self):
    info = Vk_bot.method('users.get',{'user_ids': 1111,'fields':'city, nickname'})
