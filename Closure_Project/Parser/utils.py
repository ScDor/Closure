import json
import os


def dump_json(o: object, filename: str) -> None:
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(o, f, ensure_ascii=False)



