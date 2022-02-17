from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime
import re
import bot_data

res = r'изменить'

string = 'Изменить ' \
         'ьмльмле' \
         'иьеиьелдиь'
element = 7


vk = vk_api.VkApi(token=bot_data.app_token)
vk.get_api()
a = (vk.method('database.getCities', {'country_id': 1, 'q': 'смоленск'}))['items'][0]['id']
print(a)
