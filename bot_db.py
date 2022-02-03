import psycopg2
import sqlalchemy
from bot_data import db


class BotDB:

    def __init__(self, db=None):
        db = 'postgresql://postgres:1111@localhost:5432/postgres'
        self.engine = sqlalchemy.create_engine(db)
        self.connection = self.engine.connect()

    def search_user(self, id):
        result = self.connection.execute(
            f"SELECT vk_id FROM vk_user WHERE vk_id = {id}").fetchmany(10)
        return result

    def add_user(self, id, city, sex, age):
        values = f'({id}, {city}, {sex}, {age})'
        request = f'INSERT INTO vk_user VALUES {values}'
        self.connection.execute(request)
        return 'user added'

    def get_user(self,id):
        result = (self.connection.execute(
            f"SELECT * FROM vk_user WHERE vk_id = {id}").fetchmany(10))[0]
        return {'id': result[0], 'city': result[1], 'sex': result[2], 'age': result[3]}

    def get_pairs_list(self,id):
        tuples_list = self.connection.execute(
            f"SELECT vk_pair_id FROM pairs WHERE vk_user_id = {id}").fetchmany(1000)
        result = []
        for tuple in tuples_list:
            result.append(tuple[0])
        return result

    def add_pair(self, vk_user_id, vk_pair_id):
        pair_id = (self.connection.execute("SELECT max(id) FROM pairs").fetchmany(1000))[0][0]
        result = self.connection.execute(
            f"INSERT INTO pairs VALUES ({pair_id + 1}, {vk_user_id}, {vk_pair_id})")
        return pair_id




###########Tests########################


# db  = BotDB()
# res = db.search_user('12783190')
# print(res)


# db  = BotDB()
# res = db.get_user(139122829)[0]
# print(res)


# db  = BotDB()
# res = db.get_pairs_list(12783190)
# print(res)

# db  = BotDB()
# res = db.add_pair(12783190, 54545555555555)
# print(res)

