
from .base import BaseHandler

from bot.services import MemberService, FoodLogService

member_service = MemberService()
food_log_service = FoodLogService()

class ActionHandler(BaseHandler):

    def __init__(self, member, *args, **kwargs):
        self.member = member
        super(ActionHandler, self).__init__(*args, **kwargs)

    def handle(self, text_from_user):
        if self.member.last_action.startswith('EDIT_NUTRIENTS'):
            log_id = self.member.last_action.replace('EDIT_NUTRIENTS_', '')
            log = food_log_service.get_log_by_id(log_id)

            data = text_from_user.split(' ')
            attrs = ['starch', 'protein', 'fruit', 'vegetables']
            for index in range( min( len(data), len(attrs) ) ):
                value = data[index]
                attr = attrs[index]
                setattr(log, attr, value)

            log.save()
            member_service.set_action(self.member.line_id, None)