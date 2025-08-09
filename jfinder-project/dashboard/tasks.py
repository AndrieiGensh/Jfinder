from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_confirmation_for_new_email(recepient : str):
    send_mail(
        subject="New Email Confirmation",
        message = "This email will later contain a unique link that ypu will have to click in order to activate the new email.\n " \
        "Only fter it is done will this new email be saved in the system",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recepient],
        fail_silently=True
    )