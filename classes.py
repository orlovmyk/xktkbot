"""
Just sketches load and write
"""
import json
from random import choice


class Sketches():
    def __init__(self):
        self.photos = {}

    def load(self):
        with open('sketches.json', 'r') as f:
            try:
                self.photos = json.loads(f.read())
            except json.JSONDecodeError:
                self.photos = {}

    def write(self, photo_id):
        res = {str(len(self.photos)): photo_id}

        self.photos.update(res)
        with open('sketches.json', 'w') as f:
            f.write(json.dumps(self.photos))

    def get_random(self):
        key = choice(list(self.photos.keys()))
        return (key, self.photos[key])


class User():
    def __init__(self, first_name, last_name, username):
        if not first_name: first_name = ''
        if not last_name: last_name = ''
        if not username: username = ''
        self.first_name = first_name
        self.last_name = last_name
        self.username = '@' + username
        self.time = None
        self.info = None
        self.phone = None

    def add_time(self, time):
        self.time = time

    def add_info(self, info):
        self.info = info

    def add_phone(self, phone):
        self.phone = phone

    def get(self):
        res = """
Username: {0}
Имя: {1}
Фамилия: {2}

время: {3}
пожелания: {4}
контактная информация: {5}
""".format(self.username, self.first_name, self.last_name,
           self.time, self.info, self.phone)
        return res