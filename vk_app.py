import bot_data
from bot_db import BotDB
import vk_api
from datetime import datetime


class App:

    def __init__(self):
        self.vk = vk_api.VkApi(token=bot_data.app_token)
        self.vk.get_api()
        self.db = BotDB()
        pass

    def get_pair(self, id, city=None, sex=None, age=None):
        if sex == 1:
            sex = 2
        elif sex == 2:
            sex = 1
        users = \
        (self.vk.method('users.search', {'count': 100, 'city': city, 'sex': sex, 'age_from': age - 1, 'age_to': age + 1}))[
            'items']
        exist_pair_list = self.db.get_pairs_list(id)
        for user in users:
            if user['id'] in exist_pair_list:
                pass
            else:
                self.db.add_pair(id, user['id'])
                pair = (self.vk.method('users.get', {'user_ids': user['id'], 'fields': 'city, sex, relation'}))[0]
                if pair[
                    'is_closed'] == False:  # добавить RELATION!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    pair['photos'] = self._get_photos(user['id'])
                    return pair

    def _get_photos(self, user_id):  # Получаем список фото из VK
        params = {
            'owner_id': user_id,
            'album_id': -6,
            'extended': 1
        }
        photos = (self.vk.method('photos.get', params))['items']
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

    def get_user(self, user_id):
        user = (self.vk.method('users.get', {'user_ids': user_id, 'fields': 'city, sex, bdate'}))[0]
        user['age'] = (datetime.now() - datetime.strptime(user['bdate'], "%d.%m.%Y")).days // 365
        return user

    def db_add_user(self, user_id):
        user = self.get_user(user_id)
        self.db.add_user(user_id, f"'{user['city']['id']}'", user['sex'], user['age'])

    def search_user(self, city=1, sex=1):  # Поиск пользователя по параметрам
        pairs = (self.vk.method('users.search', {'city': city, 'sex': sex}))['items']
        for pair in pairs[:2]:
            return pair
