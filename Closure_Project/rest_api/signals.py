from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import User, Student

@receiver(post_save, sender=User, dispatch_uid='user.create_user_student')
def create_user_student(sender, instance, created, **kwargs):
    if created or not Student.objects.filter(user=instance).first():
        student = Student.objects.create(user=instance, track=None)
        student.save()