from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()



# class lawyers(models.Model)
#     name = models.CharField(max_length=20,default='')
#     id = models.primarykey()
# class courts(models.Model)
#     Cname = models.CharField()
#     Cno = models.Foreignkey()
#
# class courthearings(models.Model):
#     judge = models.TextField()
#     start_time = models.DateTimeField()
#
# class courtcasses(models.Model)
#     position = models.()
#     type = models.Charfield()
#     hearing = models.Foreignkey(courthearings, related_name='cases')
#     case = models.Foreignkey(casses)
#
# class casses(models.Model)
#     casenumber = models.Integerfield()
#     pleintiff = models.TextField()
#     defendant = models.TextField()
