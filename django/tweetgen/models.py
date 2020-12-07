from django.db import models
from account.models import User

class GeneratedModel(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    model = models.TextField()
    date = models.DateTimeField(auto_now=True)
