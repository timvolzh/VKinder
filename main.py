import re
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import bot_data
from bot_db import BotDB
from vk_app import App


class VkBot:

    def __init__(self):
        self.keyboard = '{"buttons":[[{"action":{"type":"text","label":"Найти пару","payload":""},"color":"positive"}],[{"action":{"type":"text","label":"Список команд","payload":""},"color":"secondary"}]]} '
        self.Vk_bot = vk_api.VkApi(token=bot_data.bot_token)
        give = self.Vk_bot.get_api()
        self.vk = vk_api.VkApi(token=bot_data.app_token)
        self.vk.get_api()
        self.db = BotDB()
        self.app = App()

    # Функция для ответа на сообщения в лс группы
    def send_msg(self, id, text=None, keyboard=None, attachment=None):
        self.Vk_bot.method('messages.send', {'user_id': id, 'message': text, 'attachment': attachment, 'random_id': 0})

    # Слушаем longpoll(Сообщения)
    def listen(self):
        longpoll = VkLongPoll(self.Vk_bot)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:  # Чтобы наш бот не слышал и не отвечал на самого себя
                message = event.text.lower()  # Для того чтобы бот читал все с маленьких букв
                user_id = event.user_id  # Получаем id пользователя

                if message == 'начать':  # Проверяем есть ли пользователь в БД  и Найти пару
                    user_exist = self.db.search_user(user_id)  #
                    if user_exist:
                        pass
                    else:
                        self.app.db_add_user(user_id)
                    user = self.db.get_user(user_id)
                    pair = self.app.get_pair(user_id, user['city'], user['sex'], user['age'])
                    attachment = self.photo_attachment(pair["id"], pair["photos"])
                    self.send_msg(id=user_id, text=f'{pair["first_name"]} {pair["last_name"]}\nvk.com/id{pair["id"]}',
                                  keyboard=self.keyboard, attachment=attachment)

                if message == 'найти пару':
                    user = self.db.get_user(user_id)
                    pair = self.app.get_pair(user_id, user['city'], user['sex'], user['age'])
                    attachment = self.photo_attachment(pair["id"], pair["photos"])
                    self.send_msg(id=user_id, text=f'{pair["first_name"]} {pair["last_name"]}\nvk.com/id{pair["id"]}',
                                  keyboard=self.keyboard, attachment=attachment)

                if message == 'параметры':  # показать параметры поиска
                    db_user = self.db.search_user(user_id)[0]
                    user = {'city': db_user[1], 'sex': db_user[2], 'age': db_user[3]}
                    print(user)
                    if user['city'] == None: user['city'] = 'не указан'
                    if user['sex'] == 0: user['sex'] = 'не указан'
                    if user['age'] == None: user['age'] = 'не указан'
                    self.send_msg(user_id,
                                  text=f'Город - {user["city"]}\nВозраст - {user["age"]}\nВаш пол - {user["sex"]}')

                if message.startswith('изменить'):
                    try:
                        city_name = re.sub(r'([гГ]ород)+(:*)( *)(\w*)', r'\4',
                                           re.search(r'([гГ]ород)+(:*)( *)(\w*)', message).group(0))
                        city = (self.vk.method('database.getCities', {'country_id': 1, 'q': city_name}))['items'][0]['id']
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
                    self.db.update_user(user_id, city, sex, age)

                if message == 'список команд':
                    text = 'Команды:\n' \
                           'Начать - начать пользоваться ботом\n' \
                           'Найти пару - найти пару)))\n' \
                           'Параметры - показать текущие параметры поиска\n ' \
                           'Изменить - изменить город/пол/возраст а указанный\n' \
                           '(Например: изменить город: Саратов)'
                    self.send_msg(id=user_id, text=text,
                                  keyboard=self.keyboard, attachment=None)

    # Формирование вложений фото
    def photo_attachment(self, id, photos):
        attachment = ''
        for photo in photos:
            attachment += f'photo{id}_{photo},'
        return attachment


if __name__ == "__main__":
    Bot = VkBot()
    Bot.listen()
