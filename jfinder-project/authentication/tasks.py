from celery import shared_task

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings

from .models import User

@shared_task
def send_greeting_email(email: str):
    send_mail(
            subject = "Welcome at my website",
            message="Greetings, human! This is the testing email.", 
            from_email=settings.EMAIL_HOST_USER, 
            recipient_list=[email], 
            fail_silently=False
        )

# replace the body of the message with a parameterized template
# that will be populated from context variable with token, date, user's name
@shared_task
def process_email_change_request(request_secure: bool, domain: str, user_id: int, new_email : str):
    from .tokens import token_generator
    from .models import UserEmailChangeRequestModel, User

    user = get_object_or_404(User, pk=user_id)
    print(user)

    # get the encoded user's pk fro the url
    u_uid = urlsafe_base64_encode(force_bytes(user.pk))

    # get the token for the user
    validation_token = token_generator.make_token(user=user)

    # clear the previous requests, so that only the most recent one is maintained
    qs = UserEmailChangeRequestModel.objects.filter(user=user)
    qs.delete()

    # create the new request, record the token and the new requested email 
    new_request = UserEmailChangeRequestModel.objects.create(user = user, new_email = new_email, validation_token = validation_token)
    new_request.save()

    protocol = 'https' if request_secure else 'http'

    # compose the email body with the link for the reset
    context = {
        'email': new_email,
        'name': user.name,
        'token': validation_token,
        'uuid': u_uid,
        'protocol': protocol,
        'domain': domain,
    }
    email_body = render_to_string('authentication/components/email_confirmation_email.html', context=context)

    send_mail(
        subject="New Email Confirmation",
        message = email_body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[new_email],
        fail_silently=True
    )