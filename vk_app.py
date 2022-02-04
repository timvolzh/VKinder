import bot_data
from bot_db import BotDB
import vk_api

class App():


    def __init__(self):
        self.vk = vk_api.VkApi(token=bot_data.app_token)
        self.vk.get_api()
        self.db = BotDB()
        pass

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

