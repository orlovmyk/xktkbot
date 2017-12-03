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
        self.comment = ''
        self.mark = 0

    def add_comment(self, comment):
        self.comment = comment

    def add_mark(self, mark):
        self.mark = mark

    def show(self):
        res = """
Username: {0}
Имя: {1}
Фамилия: {2}

коммент: {3}
оцiночка: {4}
""".format(self.username, self.first_name, self.last_name,
           self.comment, self.mark)

        return res