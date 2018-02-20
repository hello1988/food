from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from pytz import timezone

from bot.constants import *
from bot.services import FoodLogService
from .base import BaseHandler

from django.conf import settings

from linebot.models import (
    TemplateSendMessage, CarouselTemplate, CarouselColumn,
    PostbackTemplateAction, TextSendMessage, URITemplateAction,
)

import math
from django.forms.models import model_to_dict

food_log_service = FoodLogService()

class LogHandler(BaseHandler):

    def __init__(self, member, *args, **kwargs):
        self.member = member
        super(LogHandler, self).__init__(*args, **kwargs)

    def handle(self, **kwargs):
        type = kwargs.get('type', None)
        date_str = kwargs.get('date',None)
        start_time = end_time = None
        if type is not None:
            start_time, end_time = self.__get_duration_by_type(type)
        elif date_str is not None:
            start_time, end_time = self.__get_duration_by_date_string(date_str)
        else:
            return

        logs = food_log_service.get_logs(self.member.id, start_time, end_time)
        # logs = self.food_log_service.get_logs(self.member.id)
        if logs.count() > 0 :
            template = self.__generate_templates(logs)
            self.push_template(self.member.line_id, template)
        else:
            self.push_template(self.member.line_id, TextSendMessage(text='目前沒有相關紀錄喔'))


    def __get_duration_by_type(self, type):
        start_time = end_time = None
        now = datetime.now().astimezone(tz=timezone(settings.TIME_ZONE))
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if type == TODAY:
            start_time = today
            end_time = today + relativedelta(days=1)
        elif type == YESTERDAY:
            start_time = today + relativedelta(days=-1)
            end_time = today
        elif type == THIS_WEEK:
            week_day = today.weekday()
            start_time = today + relativedelta(days=-week_day)
            end_time = start_time + relativedelta(days=7)
        elif type == LAST_WEEK:
            week_day = today.weekday()
            end_time = today + relativedelta(days=-week_day)
            start_time = end_time + relativedelta(days=-7)

        return start_time, end_time

    def __get_duration_by_date_string(self, date_str):
        tz = timezone(settings.TIME_ZONE)
        start_time = parse(date_str).replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=tz)
        end_time = start_time + relativedelta(days=1)

        return start_time, end_time

    def __generate_templates(self, logs):
        templates = []
        tz = timezone(settings.TIME_ZONE)
        row_count = int(math.ceil( len(logs)/10.0 ))
        nutrients = {'starch':0, 'protein':0, 'fruit':0, 'vegetables':0}
        for row in range(row_count):
            num = min( 10, len(logs[row*10:]) )
            columns = []
            for count in range(num):
                index = row*10 + count
                log = logs[index]
                data = model_to_dict(log, fields=['starch', 'protein', 'fruit', 'vegetables'])
                nutrients['starch'] += data['starch']
                nutrients['protein'] += data['protein']
                nutrients['fruit'] += data['fruit']
                nutrients['vegetables'] += data['vegetables']

                dt = datetime.strftime(log.created_at.astimezone(tz=tz), '%Y-%m-%d %H:%M')
                text = '{starch}主 {protein}肉 {fruit}果 {vegetables}菜'.format(**data)
                actions = []
                actions.append( PostbackTemplateAction(label='修改', data='EDIT_NUTRIENTS_{id}'.format(id=log.id)) )
                actions.append( URITemplateAction(label='檢視原圖', uri=log.image_url) )
                column = CarouselColumn(title=dt, text=text, thumbnail_image_url=log.image_url, actions=actions)
                columns.append(column)

            template = TemplateSendMessage(alt_text='飲食紀錄', template=CarouselTemplate(columns=columns))
            templates.append(template)


        text = '營養素總計\n{starch}主\n{protein}肉\n{fruit}果\n{vegetables}菜'.format(**nutrients)
        templates.append( TextSendMessage(text=text) )
        return templates