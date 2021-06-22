from django.db import models


class PrerequisiteList(models.Model):
    take_one_of = models.ManyToManyField("Course")
