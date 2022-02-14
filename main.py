import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import bot_data
from bot_db import BotDB
from datetime import datetime
from vk_app import App

# Подключаем токен и longpoll
Vk_bot = vk_api.VkApi(token=bot_data.bot_token)
give = Vk_bot.get_api()
vk = vk_api.VkApi(token=bot_data.app_token)
vk.get_api()
db = BotDB()


# Создадим функцию для ответа на сообщения в лс группы
def send_msg(id, text=None, attachment=None):
    Vk_bot.method('messages.send', {'user_id': id, 'message': text, 'attachment': attachment, 'random_id': 0})


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
                    App.db_add_user(user_id)
                user = db.get_user(user_id)
                pair = get_pair(user_id, user['city'], user['sex'], user['age'])
                attachment = photo_attachment(pair["id"], pair["photos"])
                send_msg(user_id, f'{pair["first_name"]} {pair["last_name"]}\nvk.com/id{pair["id"]}', attachment)


def search_user(city=1, sex=1):  # Поиск пользователя по параметрам
    pairs = (vk.method('users.search', {'city': city, 'sex': sex}))['items']
    for pair in pairs[:2]:
        return pair


def get_pair(id, city=None, sex=None, age=None):
    if sex == 1:
        sex = 2
    elif sex == 2:
        sex = 1
    users = \
    (vk.method('users.search', {'count': 100, 'city': city, 'sex': sex, 'age_from': age - 1, 'age_to': age + 1}))[
        'items']
    exist_pair_list = db.get_pairs_list(id)
    for user in users:
        if user['id'] in exist_pair_list:
            pass
        else:
            db.add_pair(id, user['id'])
            pair = (vk.method('users.get', {'user_ids': user['id'], 'fields': 'city, sex, relation'}))[0]
            if pair[
                'is_closed'] == False:  # добавить RELATION!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                pair['photos'] = _get_photos(user['id'])
                return pair


def _get_photos(user_id):  # Получаем список фото из VK
    params = {
        'owner_id': user_id,
        'album_id': -6,
        'extended': 1
    }
    photos = (vk.method('photos.get', params))['items']
    photos_result = []
    while len(photos_result) < 3:  # Формируем список id 3-х самых залайканных
        for photo in photos:
            max_likes = 0
            photo_id = None
            if photo['likes']['count'] > max_likes:
                max_likes = photo['likes']['count']
                photo_id = photo['id']
        try:
            photos_result.append(photo_id)
        except:
            break
        try:
            photos.remove(photo)
        except:
            pass
    return photos_result


def photo_attachment(id, photos):
    attachment = ''
    for photo in photos:
        attachment += f'photo{id}_{photo},'
    print(photos)
    print(attachment)
    return attachment


if __name__ == "__main__":
    listen()
    # pprint(search_pair())
