from django.db import models
from account.models import User
from django.utils import timezone

class TextGenHistory(models.Model):
    target_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='target_user',
    )
    request_from = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='request_from',
    )
    gen_date = models.DateTimeField('generate date', default=timezone.now)
