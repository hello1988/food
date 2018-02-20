from pytz import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import random

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import status

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage,
    PostbackEvent, FollowEvent,
    ImageMessage, UnfollowEvent,
    TextSendMessage,
)

from .line_api import get_line_user_profile
from .services import MemberService, FoodLogService
from .utils import save_file, remove_file
from food.firebase import Firebase

from .handlers.log_handler import LogHandler
from .handlers.action_handle import ActionHandler
from .constants import *

HASH_CODE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
firebase = Firebase()
line_bot_api = LineBotApi(settings.LINE_BOT_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_BOT_SECRET)

member_service = MemberService()
food_log_service = FoodLogService()

@csrf_exempt
@require_POST
def webhook(request):

    # get X-Line-Signature header value
    signature = request.META.get('HTTP_X_LINE_SIGNATURE')
    # get request body as text
    body = request.body.decode('utf-8')
    # print request.body
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        HttpResponse(status=status.HTTP_404_NOT_FOUND)

    return HttpResponse(status=status.HTTP_200_OK)

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):

    # init
    line_id = event.source.sender_id
    reply_token = event.reply_token
    source_type = event.source.type
    text_from_user = event.message.text
    if source_type != 'user':
        return

    member = member_service.get_or_create(line_id)
    if check_action(member):
        handler = ActionHandler(member)
        handler.handle(text_from_user)
        return

    dt = try_parse_datetime(text_from_user)
    if dt is not None:
        handler = LogHandler(member)
        handler.handle(datetime=dt)

    elif text_from_user == '今天':
        handler = LogHandler(member)
        handler.handle(type=TODAY)
    elif text_from_user == '昨天':
        handler = LogHandler(member)
        handler.handle(type=YESTERDAY)

    elif text_from_user == '本週':
        handler = LogHandler(member)
        handler.handle(type=THIS_WEEK)

    elif text_from_user == '上週':
        handler = LogHandler(member)
        handler.handle(type=LAST_WEEK)

def check_action(member):
    if not member.last_action:
        return False

    action_time = member.updated_at.astimezone(tz=timezone(settings.TIME_ZONE))
    now = datetime.now().astimezone(tz=timezone(settings.TIME_ZONE))
    if ( action_time + relativedelta(minutes=5) ) < now:
        return False

    return True

def try_parse_datetime(text):
    try:
        tz = timezone(settings.TIME_ZONE)
        return parse(text).replace(tzinfo=tz)
    except:
        return None


@handler.add(MessageEvent, message=(ImageMessage,))
def handle_content_message(event):

    if not isinstance(event.message, ImageMessage):
        return

    line_id = event.source.sender_id
    message_content = line_bot_api.get_message_content(event.message.id)
    tempfile_path = save_file(message_content)

    member = member_service.get_or_create(line_id)
    now_time = datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M')
    seed = ''.join(random.sample(HASH_CODE, 5))
    image_name = '{name}_{time}_{seed}'.format(name=member.name, time=now_time, seed=seed)
    image_url = firebase.uploadImg(event, tempfile_path, image_name)
    remove_file(tempfile_path)

    food_log_service.create(member, image_url)

@handler.add(PostbackEvent)
def postback_text(event):
    line_id = event.source.sender_id
    reply_token = event.reply_token
    data = event.postback.data

    if data.startswith('EDIT_NUTRIENTS'):
        member_service.set_action(line_id, data)
        line_bot_api.reply_message(reply_token, TextSendMessage(text='請輸入營養素\n以空白隔開'))


@handler.add(FollowEvent)
def on_followed(event):
    line_id = event.source.sender_id
    profile = get_line_user_profile(line_id)
    member_service.update_profile(line_id, profile)

@handler.add(UnfollowEvent)
def unfollowed(event):
    line_id = event.source.sender_id
