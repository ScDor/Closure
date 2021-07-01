import os
from typing import Optional

from django.contrib.auth.models import User
from django.db import migrations
from django.db.backends.postgresql.schema import DatabaseSchemaEditor
from django.db.migrations.state import StateApps

import google.auth
from google.cloud import secretmanager
import warnings

def try_get_password_from_secret_manager() -> Optional[str]:
    try:
        # Get project value for identifying current context
        _, project = google.auth.default()
    except google.auth.exceptions.DefaultCredentialsError:
        # We are not in a GCP environment
        return None

    print(f"Determined we're in GCP project '{project}', fetching password from secret manager")
    client = secretmanager.SecretManagerServiceClient()
    # Retrieve the previously stored admin password
    PASSWORD_NAME = os.environ.get("PASSWORD_NAME", "superuser_password")
    name = f"projects/{project}/secrets/{PASSWORD_NAME}/versions/latest"
    admin_password = client.access_secret_version(name=name).payload.data.decode(
        "UTF-8"
    )
    return admin_password.strip()

PASSWORD_ENV = "SUPERUSER_PASSWORD"

def try_get_password_from_env() -> Optional[str]:
    name = os.environ.get(PASSWORD_ENV, None)
    if name:
        print(f"Creating superuser via password stored in env var {PASSWORD_ENV}")
        return name.strip()
    return None

def try_get_password_for_ci() -> Optional[str]:
    if os.getenv("TRAMPOLINE_CI", None) or os.getenv("CI", False):
        print(f"Detected we're in CI, using placeholder password")
        return "test"
    return None

def createsuperuser(apps: StateApps, schema_editor: DatabaseSchemaEditor) -> None:
    """
    Dynamically create an admin user as part of a migration
    Password is pulled from Secret Manger (previously created as part of tutorial)
    """
    admin_password = try_get_password_from_env()
    admin_password = try_get_password_for_ci() if not admin_password else admin_password
    admin_password = try_get_password_from_secret_manager() if not admin_password else admin_password
    if not admin_password:
        print
        warnings.warn("Couldn't find superuser password." \
                      f"If running this migration locally, make sure to set the environment variable {PASSWORD_ENV}")
        return
    

    # Create a new user using acquired password, stripping any accidentally stored newline characters
    User.objects.create_superuser("admin", password=admin_password)


class Migration(migrations.Migration):
    dependencies = [
        ('rest_api', '0001_initial'),
    ]
    operations = [migrations.RunPython(createsuperuser)]

