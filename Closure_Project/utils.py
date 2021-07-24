import json
import os
from typing import Dict


def dump_json(o: object, filename: str, extend: bool) -> None:
    if extend:
        try:
            previous = load_json(filename)
            if isinstance(previous, list):
                previous.extend(o)
            elif isinstance(previous, Dict):
                previous.update(o)
            else:
                raise ValueError(f"unexpected type {type(o)}")

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(previous, f, ensure_ascii=False)
                return

        except (FileNotFoundError, json.decoder.JSONDecodeError):
            pass  # called with extend=true on a file that had not existed before

    with open(filename, 'w', encoding='utf8') as f:
        json.dump(o, f, ensure_ascii=False)


def load_json(filename: str) -> Dict:
    """ deserializes from json """
    with open(filename, 'r', encoding='utf8') as f:
        return json.load(f)


def setup_django_pycharm() -> None:
    """ sets a Django environment up """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_settings.settings")
    import django
    django.setup()
