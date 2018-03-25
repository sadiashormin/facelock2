from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid
@deconstructible
class RandomFileName(object):
    def __init__(self, path):
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _, filename):
        # @note It's up to the validators to check if it's the correct file type in name or if one even exist.
        extension = os.path.splitext(filename)[1]
        return self.path % (uuid.uuid4(), extension)

class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset().filter(city='London')

class UserProfile(models.Model):
    # user = models.OneToOneField(User)
    user=models.ForeignKey(User, unique=True)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile_image', blank=True)

    # london = UserProfileManager()

    def __str__(self):
        return self.user.username
class Face(models.Model):
    # user = models.ForeignKey(User,unique=True,default=uuid.uuid1)
    user = models.ForeignKey(User,unique=True)
    picture = models.ImageField(upload_to=RandomFileName('home/static/profile'))
    def __str__(self):
        return "%s the face" % self.user.name

def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile = UserProfile(user=kwargs['instance'])
        profile.save()
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
