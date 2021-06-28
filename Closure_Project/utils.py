import json
import os
from typing import Dict


def dump_json(to_dump: object, filename: str) -> None:
    """ serializes a (serializable) object to json """
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(to_dump, f, ensure_ascii=False)


def load_json(filename: str) -> Dict:
    """ deserializes from json """
    with open(filename, 'r', encoding='utf8') as f:
        return json.load(f)


def setup_django_pycharm() -> None:
    """ sets a Django environment up """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_settings.settings")
    import django
    django.setup()
