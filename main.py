import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import bot_data
from pprint import pprint
import requests
from bot_db import BotDB
from datetime import datetime

# Подключаем токен и longpoll
Vk_bot = vk_api.VkApi(token=bot_data.bot_token)
give = Vk_bot.get_api()
app = vk_api.VkApi(token=bot_data.app_token)
app.get_api()
db = BotDB()


# Создадим функцию для ответа на сообщения в лс группы
def send_msg(id, text=None, attachment=None):
    Vk_bot.method('messages.send', {'user_id': id, 'message': text,'attachment': attachment, 'random_id': 0})


# Слушаем longpoll(Сообщения)
def listen():
    longpoll = VkLongPoll(Vk_bot)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:  # Чтобы наш бот не слышал и не отвечал на самого себя
            message = event.text.lower()  # Для того чтобы бот читал все с маленьких букв
            user_id = event.user_id  # Получаем id пользователя

            if message == 'а':
                user_exist = db.search_user(user_id)
                if user_exist:
                    pass
                else:
                    user = (Vk_bot.method('users.get', {'user_ids': user_id, 'fields': 'city, sex, bdate'}))[0]
                    user['age'] = (datetime.now() - datetime.strptime(user['bdate'], "%d.%m.%Y")).days // 365
                    db.add_user(user_id, f"'{user['city']['id']}'", user['sex'], user['age'])
                user = db.get_user(user_id)
                pair = get_pair(user['city'], user['sex'], user['age'])
                attachment = f'photo{pair["id"]}_{pair["photos"][0]},photo{pair["id"]}_{pair["photos"][1]},photo{pair["id"]}_{pair["photos"][2]}'
                send_msg(user_id, f'{pair["first_name"]} {pair["last_name"]}\nvk.com/{pair["id"]}', attachment)
                # print(user)

def get_pair(city=1, sex=1, age=None):  # Ищем пользователя с указанными параметрами и получаем 3 фото
    pair = search_user(city, sex)
    pair_photos = _get_photos(pair['id'])
    pair['photos'] = pair_photos
    return pair


def search_user(city=1, sex=1):  # Поиск пользователя по параметрам
    pairs = (app.method('users.search', {'city': city, 'sex': sex}))['items']
    for pair in pairs[:2]:
        return pair

def get_pair_2 (id, city=None, sex=None, age=None):
    if sex == 1:
        sex = 2
    elif sex == 2:
        sex = 1
    users = (app.method('users.search', {'city': city, 'sex': sex, 'age_from': age-1, 'age_to': age+1}))['items']
    for user in users:
        exist_pair_list = db.get_pairs_list()
        if user['id'] in exist_pair_list:
            pass
        else:
            db.add_pair(id, user['id'])

    pass

def _get_photos(user_id):  # Получаем список фото из VK
    params = {
        'owner_id': user_id,
        'album_id': -6,
        'extended': 1
    }
    photos = (app.method('photos.get', params))['items']
    photos_result = []
    while len(photos_result) < 3: # Формируем список id 3-х самых залайканных
        for photo in photos:
            max_likes = 0
            photo_id = None
            if photo['likes']['count'] > max_likes:
                max_likes = photo['likes']['count']
                photo_id = photo['id']
        photos_result.append(photo_id)
        photos.remove(photo)
    return photos_result


if __name__ == "__main__":
    listen()
    # pprint(search_pair())
