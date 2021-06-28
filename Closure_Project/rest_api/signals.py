from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Student


from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_student(sender, instance: User, created, **kwargs):
    if created:
        Student.objects.create(user=instance)
