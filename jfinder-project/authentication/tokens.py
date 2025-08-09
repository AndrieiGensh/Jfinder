from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AuthTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(user.is_email_confirmed) + str(timestamp)
    
token_generator = AuthTokenGenerator()