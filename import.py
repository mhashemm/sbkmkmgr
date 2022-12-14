import os
import json
import re

BOOKMARK_PATH = f"{os.environ['XDG_CONFIG_HOME']}/chromium/Default/Bookmarks"
bookmarks: dict = {}
dest = "/mnt/ssd/scripts/sbkmkmgr/testbk/"
with open(BOOKMARK_PATH, 'r') as file:
    bookmarks = json.load(file)['roots']['bookmark_bar']


def sanitize_name(name):
    return re.sub(r"[^a-zA-Z0-9]+", '-', name.split("?")[0].split("%")[0].split('&')[0].lower()).strip('-')


def generate_name_from_url(url):
    return sanitize_name(url.replace('https://', '').replace('http://', ''))


def create(bkmks, path=''):
    for i, bk in enumerate(bkmks):
        if bk['type'] == 'folder':
            new_path = f"{path}{sanitize_name(bk['name'])}/"
            os.makedirs(f"{dest}{new_path}")
            create(bk['children'], new_path)
        elif bk['type'] == 'url':
            name = sanitize_name(bk['name'])
            name = generate_name_from_url(bk['url']) if name == '' else name
            if os.path.exists(f'{dest}{path}{name}'):
                name += str(i)
            with open(f'{dest}{path}{name}', 'w') as f:
                f.write(bk['url'])


create(bookmarks['children'])
