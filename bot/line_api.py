import json
import requests

from django.conf import settings

headers = {'Authorization':'Bearer %s'%(settings.LINE_BOT_ACCESS_TOKEN),}

class Area(object):
    # area objects    https://developers.line.me/en/docs/messaging-api/reference/#area-object
    def __init__(self, x, y, width, height, action):
        self.bounds ={
            "x": x,
            "y": y,
            "width": width,
            "height": height
        }

        self.action = action

    def get_dict(self):
        return self.__dict__

def get_rich_menu_list():
    url = 'https://api.line.me/v2/bot/richmenu/list'
    resp = requests.get(url, headers=headers)
    return json.dumps(resp.text)

def create_rich_menu(name, chat_bar_text, areas):
    if not isinstance(areas, (list, tuple)):
        return

    area_list = []
    for area in areas:
        if not isinstance(area, Area):
            return
        area_list.append(area.get_dict())

    url = 'https://api.line.me/v2/bot/richmenu'
    data = {
        "size": {
            "width": 2500,
            "height": 1686
        },
        "selected": False,
        "name": name,
        "chatBarText": chat_bar_text,
        "areas": area_list,
    }

    create_headers = {'Content-Type':'application/json'}
    create_headers.update( headers )
    resp = requests.post(url, data=json.dumps(data), headers=create_headers)
    return json.loads(resp.text)

def upload_rich_menu_image(rich_menu_id, image_path):
    url = 'https://api.line.me/v2/bot/richmenu/%s/content'%(rich_menu_id)

    upload_headers = {'Content-Type':'image/png'}
    upload_headers.update( headers )

    data = open(image_path, 'rb')
    resp = requests.post(url, headers=upload_headers, data=data)
    return json.loads(resp.text)

def delete_rich_menu(rich_menu_id):
    url = 'https://api.line.me/v2/bot/richmenu/%s'%(rich_menu_id)

    resp = requests.delete(url, headers=headers)
    return json.loads(resp.text)

def link_user(rich_menu_id, line_id):
    url = 'https://api.line.me/v2/bot/user/%s/richmenu/%s'%(line_id, rich_menu_id,)
    resp = requests.post(url, headers=headers)
    return json.loads(resp.text)

def unlink_user(line_id):
    url = 'https://api.line.me/v2/bot/user/%s/richmenu'%(line_id,)
    resp = requests.delete(url, headers=headers)
    return json.loads(resp.text)

def get_user_richmenu(line_id):
    url = 'https://api.line.me/v2/bot/user/%s/richmenu'%(line_id,)
    resp = requests.get(url, headers=headers)
    return json.loads(resp.text)

def get_line_user_profile(line_id):
    url = 'https://api.line.me/v2/bot/profile/%s' % (line_id,)
    resp = requests.get(url, headers=headers)
    return json.loads(resp.text)