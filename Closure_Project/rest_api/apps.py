from django.apps import AppConfig
# from rest_api.signals import create_student, save_student
# from django.contrib.auth.models import User
#
# from django.db.models.signals import post_save


class RestApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rest_api'

    def ready(self):
        import rest_api.signals
