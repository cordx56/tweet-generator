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

class MarkovChainState3(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state0 = models.TextField(db_index=True)
    state1 = models.TextField(db_index=True)
    state2 = models.TextField(db_index=True)
    next = models.TextField()
    value = models.IntegerField()
