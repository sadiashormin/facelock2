from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid


class Face(models.Model):
    user = models.ForeignKey(User, unique=True)
    picture = models.ImageField()

    def __str__(self):
        return "%s the face" % self.user.name
