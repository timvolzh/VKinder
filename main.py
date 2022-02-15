import re
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
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

                if message == 'а':
                    user_exist = db.search_user(user_id)
                    if user_exist:
                        pass
                    else:
                        app.db_add_user(user_id)
                    user = db.get_user(user_id)
                    pair = app.get_pair(user_id, user['city'], user['sex'], user['age'])
                    attachment = self.photo_attachment(pair["id"], pair["photos"])
                    self.send_msg(user_id, f'{pair["first_name"]} {pair["last_name"]}\nvk.com/id{pair["id"]}', attachment)

    # Формирование вложений фото
    def photo_attachment(self,id, photos):
        attachment = ''
        for photo in photos:
            attachment += f'photo{id}_{photo},'
        return attachment


if __name__ == "__main__":
    Bot = VkBot()
    Bot.listen()
