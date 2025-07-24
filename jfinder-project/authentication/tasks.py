from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_greeting_email(email: str):
    send_mail(
            subject = "Welcome at my website",
            message="Greetings, human! This is the testing email.", 
            from_email=settings.EMAIL_HOST_USER, 
            recipient_list=[email], 
            fail_silently=False
        )