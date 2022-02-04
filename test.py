from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime

# token = input('Token: ')
# vk = vk_api.VkApi(token=token)
# longpoll = VkLongPoll(vk)

vkbdate = '1.11.1995'
bdate = vkbdate.split('.')
bdate.reverse()
age = datetime.timedelta
print(bdate)


def get_pair(city=1, sex=1, age=None):  # Ищем пользователя с указанными параметрами и получаем 3 фото
    pair = search_user(city, sex)
    pair_photos = _get_photos(pair['id'])
    pair['photos'] = pair_photos
    return pair
