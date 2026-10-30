from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import base36_to_int


class OneHourResetTokenGenerator(PasswordResetTokenGenerator):
    def check_token(self, user, token):
        if not super().check_token(user, token):
            return False
        timestamp = base36_to_int(token.split("-", 1)[0])
        age = self._num_seconds(self._now()) - timestamp
        return 0 <= age < 3600
