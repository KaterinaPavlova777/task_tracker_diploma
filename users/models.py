from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    position = models.CharField(max_length=30, verbose_name='position')
    access_level = models.PositiveSmallIntegerField(default=0, verbose_name='access level')

    def __str__(self):
        return self.username
