import json
import os


def dump(o: object, filename: str) -> None:
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(o, f, ensure_ascii=False)


def load(filename: str):
    with open(filename, 'r', encoding='utf8') as f:
        return json.load(f)


def setup_django_pycharm():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Closure_Project.Closure_Project.settings")
    import django
    django.setup()
