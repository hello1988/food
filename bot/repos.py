from .models import Member, FoodLog

class MemberRepo(object):
    def get_or_create(self, line_id):
        member, created = Member.objects.get_or_create(line_id=line_id)
        return member

class FoodLogRepo(object):
    def create(self, member, image_url):
        return FoodLog.objects.create(member=member, image_url=image_url )

    def get_by_id(self, id):
        try:
            return FoodLog.objects.get(id=id)
        except FoodLog.DoesNotExist:
            return None


    def get_logs(self, member_id, start_time=None, end_time=None):
        logs = FoodLog.objects.filter(member_id=member_id)

        if start_time:
            logs = logs.filter(created_at__gte=start_time)

        if end_time:
            logs = logs.filter(created_at__lt=end_time)

        return logs