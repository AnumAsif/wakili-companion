from django.db import models

# Create your models here.

class lawyers(models.Model)
    name = models.CharField(max_length=20,default='')
    id = models.primarykey()
class courts(models.Model)
    Cname = models.CharField()
    Cno = models.Foreignkey()

class courthearings(models.Model):
    judge = models.TextField()
    start_time = models.DateTimeField()

class courtcasses(models.Model)
    position = models.()
    type = models.Charfield()
    hearing = models.Foreignkey(courthearings, related_name='cases')
    case = models.Foreignkey(casses)

class casses(models.Model)
    casenumber = models.Integerfield()
    pleintiff = models.TextField()
    defendant = models.TextField()
