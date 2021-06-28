
from django.db import migrations


from rest_api.huji_loader import load_from_zip


def import_parsed_data(apps, schema_editor):
    load_from_zip()


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0001_initial'),
        ('rest_api', '0002_create_superuser')
    ]

    operations = [
        migrations.RunPython(import_parsed_data)
    ]
