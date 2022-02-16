import re
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import bot_data
from bot_db import BotDB
from vk_app import App

# Подключаем базу данных, приложение и модуль vk
Vk_bot = vk_api.VkApi(token=bot_data.bot_token)
give = Vk_bot.get_api()
vk = vk_api.VkApi(token=bot_data.app_token)
vk.get_api()
db = BotDB()
app = App()

#


class VkBot:
    # Функция для ответа на сообщения в лс группы
    def send_msg(self, id, text=None, attachment=None):
        Vk_bot.method('messages.send', {'user_id': id, 'message': text, 'attachment': attachment, 'random_id': 0})

    # Слушаем longpoll(Сообщения)
    def listen(self):
        longpoll = VkLongPoll(Vk_bot)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:  # Чтобы наш бот не слышал и не отвечал на самого себя
                message = event.text.lower()  # Для того чтобы бот читал все с маленьких букв
                user_id = event.user_id  # Получаем id пользователя

                self.send_msg(user_id, )

                if message == 'начать':  # Найти пару
                    user_exist = db.search_user(user_id)  # проверяем есть ли пользователь в БД
                    if user_exist:
                        pass
                    else:
                        app.db_add_user(user_id)
                    user = db.get_user(user_id)
                    pair = app.get_pair(user_id, user['city'], user['sex'], user['age'])
                    attachment = self.photo_attachment(pair["id"], pair["photos"])
                    self.send_msg(user_id, f'{pair["first_name"]} {pair["last_name"]}\nvk.com/id{pair["id"]}',
                                  attachment)

                if message == 'и':  # показать параметры поиска
                    db_user = db.search_user(user_id)[0]
                    user = {'city': db_user[1], 'sex': db_user[2], 'age': db_user[3]}
                    print(user)
                    if user['city'] == None: user['city'] = 'не указан'
                    if user['sex'] == 0: user['sex'] = 'не указан'
                    if user['age'] == None: user['age'] = 'не указан'
                    self.send_msg(user_id, f'Город - {user["city"]}\nВозраст - {user["age"]}\nВаш пол - {user["sex"]}')

                if message.startswith('с'):
                    try:
                        city_name = re.sub(r'([гГ]ород)+(:*)( *)(\w*)', r'\4',
                                           re.search(r'([гГ]ород)+(:*)( *)(\w*)', message).group(0))
                        city = (vk.method('database.getCities', {'country_id': 1, 'q': city_name}))['items'][0]['id']
                    except:
                        city = None
                    try:
                        sex = re.sub(r'([пП]ол)+(:*)( *)(\w*)', r'\4',
                                     re.search(r'([пП]ол)+(:*)( *)(\w*)', message).group(0))
                    except:
                        sex = None
                    try:
                        age = re.sub(r'([вВ]озраст)+(:*)( *)(\w*)', r'\4',
                                     re.search(r'([вВ]озраст)+(:*)( *)(\w*)', message).group(0))
                    except:
                        age = None
                    db.update_user(user_id, city, sex, age)

    # Формирование вложений фото
    def photo_attachment(self, id, photos):
        attachment = ''
        for photo in photos:
            attachment += f'photo{id}_{photo},'
        return attachment


if __name__ == "__main__":
    Bot = VkBot()
    Bot.listen()
