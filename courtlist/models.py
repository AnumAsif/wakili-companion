from django.db import models


class Lawyers(models.Model):
    name = models.CharField(max_length=255)


class Courts(models.Model):
    name = models.CharField(max_length=255)
    number = models.PositiveIntegerField()


class CourtHearings(models.Model):
    judge = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    court = models.ForeignKey(Courts, related_name='cause_list', null=True)


class Cases(models.Model):
    case_id = models.TextField()
    plaintiff = models.TextField()
    defendant = models.TextField()


class HearingCases(models.Model):
    position = models.PositiveIntegerField()
    hearing_type = models.CharField(max_length=64)
    hearing = models.ForeignKey(CourtHearings, related_name='cases')
    case = models.ForeignKey(Cases)
