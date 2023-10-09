import datetime, pytz
# from rest_framework import permissions, exceptions
# from authentication.models import User


def validate_token(valid_from):
        utc = pytz.UTC
        now = utc.localize(datetime.datetime.now())
        if valid_from < now - datetime.timedelta(hours=24):
            return False
        return True
