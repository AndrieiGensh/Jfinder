from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str



def check_uuid_and_token(request, uuidb64: str, token: str):
    from authentication.tokens import token_generator
    from authentication.models import User
    # decode the token and check if the user with such id exists
    user_id = force_str(urlsafe_base64_decode(uuidb64))
    user = get_object_or_404(User, id = user_id)

    # check the token and see if it is ok
    token_ok = token_generator.check_token(user=user, token=token)

    if token_ok:
        return True, user
    else:
        return False, None