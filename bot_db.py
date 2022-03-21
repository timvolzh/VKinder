import sqlalchemy


class BotDB:

    def __init__(self, db=None):
        db = 'postgresql://postgres:1111@localhost:5432/postgres'
        self.engine = sqlalchemy.create_engine(db)
        self.connection = self.engine.connect()

    def search_user(self, id):
        result = self.connection.execute(
            f"SELECT * FROM vk_user WHERE vk_id = {id}").fetchmany(10)
        return result

    def add_user(self, id, city, sex, age):
        values = f"({id}, {city}, {sex}, {age})"
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
        if pair_id:
            result = self.connection.execute(
                f"INSERT INTO pairs VALUES ({pair_id + 1}, {vk_user_id}, {vk_pair_id})")
        else:
            result = self.connection.execute(
                f"INSERT INTO pairs VALUES (1, {vk_user_id}, {vk_pair_id})")
        return pair_id

    def update_user(self, user_id, city=None, sex=None, age=None):
        new_values = ''
        if city:
            new_values += f'vk_city={city},'
        if sex == 'м' :
            new_values += f'vk_sex=2,'
        elif sex == 'ж':
            new_values += f'vk_sex=1,'
        if age:
            new_values += f'vk_age={age},'
        new_values = new_values[:-1]
        requests = self.connection.execute(f'UPDATE vk_user SET {new_values} WHERE vk_id={user_id}')
