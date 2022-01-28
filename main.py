import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import bot_data
from pprint import pprint
import requests

# Подключаем токен и longpoll
Vk_bot = vk_api.VkApi(token=bot_data.bot_token)
give = Vk_bot.get_api()
app = vk_api.VkApi(token=bot_data.app_token)
app.get_api()


# Создадим функцию для ответа на сообщения в лс группы
def send_msg(id=None, text=None, attachment=None):
    Vk_bot.method('messages.send', {'user_id': id, 'message': text,'attachment': attachment, 'random_id': 0})


# Слушаем longpoll(Сообщения)
def listen():
    longpoll = VkLongPoll(Vk_bot)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:  # Чтобы наш бот не слышал и не отвечал на самого себя
                message = event.text.lower()  # Для того чтобы бот читал все с маленьких букв
                user_id = event.user_id  # Получаем id пользователя

                if message == 'а':
                    user = (Vk_bot.method('users.get',{'user_ids':user_id,'fields':'city, sex'}))[0]
                    pair = get_pair(user['city']['id'], user['sex'])
                    attachment = f'photo{pair["id"]}_{pair["photos"][0]},photo{pair["id"]}_{pair["photos"][1]},photo{pair["id"]}_{pair["photos"][2]}'
                    send_msg(user_id, f'{pair["first_name"]} {pair["last_name"]}\nvk.com/{pair["id"]}', attachment)
                    pprint(pair)


def get_pair(city=1, sex=1, age=None): # Ищем пользователя с указанными параметрами и получаем 3 фото
    pair = search_user(city, sex)
    pair_photos = _get_photos(pair['id'])
    pair['photos'] = pair_photos
    return pair


def search_user(city=1, sex=1): # Поиск пользователя по параметрам
    pairs = (app.method('users.search', {'city': city, 'sex': sex}))['items']
    for pair in pairs[:2]:
        return pair


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
