from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_report_notification(email_subject:str, email_body:str, recepient:str):
    send_mail(
            subject = email_subject,
            message=email_body, 
            from_email=settings.EMAIL_HOST_USER, 
            recipient_list=[recepient], 
            fail_silently=False
        )