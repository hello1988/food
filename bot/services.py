from .repos import MemberRepo, FoodLogRepo

member_repo = MemberRepo()
food_log_repo = FoodLogRepo()

class MemberService(object):
    def get_or_create(self, line_id):
        return member_repo.get_or_create(line_id)

    def set_active(self, line_id, active):
        member = self.get_or_create(line_id)
        member.active = active
        member.save()

    def update_profile(self, line_id, profile):
        if 'displayName' not in profile:
            return

        member = self.get_or_create(line_id)
        member.name = profile['displayName']
        member.photo = profile.get('pictureUrl')
        member.email = profile.get('email')
        member.active = True
        member.save()

    def set_action(self, line_id, action):
        member = self.get_or_create(line_id)
        member.last_action = action
        member.save()

class FoodLogService(object):
    def create(self, member, image_url):
        return food_log_repo.create(member, image_url)

    def get_logs(self, member_id, start_time=None, end_time=None):
        return food_log_repo.get_logs(member_id, start_time, end_time)

    def get_log_by_id(self, id):
        return food_log_repo.get_by_id(id)