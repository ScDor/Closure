import os

import jsonpickle

jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False)


def dump(o: object, filename: str, compact: bool = False) -> None:
    with open(filename, 'w', encoding='utf8') as f:
        f.write(jsonpickle.encode(o, indent=None if compact else 1))


def load(filename: str) -> object:
    with open(filename, 'r', encoding='utf8') as f:
        return jsonpickle.decode(f.read())


def setup_django_pycharm():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Closure_Project.Closure_Project.settings")
    import django
    django.setup()
