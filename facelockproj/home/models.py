from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    post = models.CharField(max_length=500)
    status=models.IntegerField(default=0)
    picture = models.ImageField()
    bluredPicture = models.ImageField(null=True)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    labels = models.TextField(null=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True)

class Tag(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    status=models.IntegerField(default=0)
    top=models.IntegerField(null=True)
    right=models.IntegerField(null=True)
    bottom=models.IntegerField(null=True)
    left=models.IntegerField(null=True)
    
class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)
