from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Basket(models.Model):
    user = models.OneToOneField(User)
    count = models.IntegerField()

    def __str__(self):
        return self.user.username
