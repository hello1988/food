from django.conf import settings
from linebot import LineBotApi

line_bot_api = LineBotApi(settings.LINE_BOT_ACCESS_TOKEN)
class BaseHandler(object):

    def __init__(self, *args, **kwargs):
        pass

    def handle(self, **kwargs):
        pass

    def push_template(self, line_id, template):
        line_bot_api.push_message(line_id, template)