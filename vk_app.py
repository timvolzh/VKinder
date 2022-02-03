


class App():


    def __init__(self):
        pass


    def get_pair_2 (id, city=None, sex=None, age=None):
        if sex == 1:
            sex = 2
        elif sex == 2:
            sex = 1
        users = (app.method('users.search', {'city': city, 'sex': sex, 'age_from': age-1, 'age_to': age+1}))['items']
        for user in users:
            exist_pair_list = db.get_pairs_list()
            if user['id'] in exist_pair_list:
                pass
            else:
                db.add_pair(id, user['id'])

        pass