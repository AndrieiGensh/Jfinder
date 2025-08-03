from django.db import models
from django.utils import timezone
# Create your models here.

MESSAGE_TYPES = {
    'ST': 'STATUS_UPDATE',
    'DI': 'DECISION_ISSUED',
    'RR': 'RESPONSE_REQUEST'
}


class Message(models.Model):

    sender = models.ForeignKey(
        'authentication.User', on_delete=models.DO_NOTHING, related_name="message_sender")
    recipient = models.ForeignKey(
        'authentication.User', on_delete=models.DO_NOTHING, related_name="message_recipient")

    related_offer = models.ForeignKey(
        'jobs.Offer', on_delete=models.DO_NOTHING, related_name="related_offer")
    date_sent = models.DateTimeField(auto_now_add=True)

    message_type = models.TextField(choices=MESSAGE_TYPES)
    header = models.TextField(
        max_length=100, default='Learn what is new', null=False)
    content = models.TextField(
        blank=False, null=False, default='There is a new message')

    is_read = models.BooleanField(default=False)
    no_reply = models.BooleanField(default=True)


class Bookmark(models.Model):

    bookmarked_offer = models.ForeignKey(
        'jobs.Offer', on_delete=models.CASCADE)
    bookmarked_by = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE)
    bookmark_date = models.DateField(auto_now_add=True)
    comment = models.TextField(max_length=100, default='Offer comment')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['bookmarked_offer', 'bookmarked_by'], name='unique_user_bookmark'
            )
        ]
