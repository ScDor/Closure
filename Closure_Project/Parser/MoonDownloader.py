import os
from multiprocessing import Pool
from time import sleep
from functools import partial
from os import path

import requests


def download_course(override_existing_files: bool, i: int):
    html_path = f'course_details_html/{i}.html'
    if not override_existing_files and path.exists(html_path):
        print(i)
        return

    url = f'http://moon.cc.huji.ac.il/nano/pages/wfrCourse.aspx?' \
          f'faculty=2&' \
          f'year=2021&' \
          f'courseId={i}'

    with open(html_path, 'wb') as f:
        f.write(requests.get(url).content)
    print(i)


def download_track(override_existing_files: bool, i: int):
    html_path = f'tracks_html/{i}.html'
    if not override_existing_files and path.exists(html_path):
        print(i)
        return

    url = f'http://moon.cc.huji.ac.il/nano/pages/wfrMaslulDetails.aspx' \
          f'?year=2021&' \
          f'faculty=2&' \
          f'maslulId=2{i}'

    text = None
    get = None

    while text is None or 'timeout' in text:  # todo use requests retry instead
        get = requests.get(url)
        text = get.text
        if 'timeout' in text:
            print(f'({i})')
            sleep(5)

    with open(html_path, 'wb') as f:
        f.write(get.content)
    print(i)


def download_all_courses(override_existing_files=False):
    folder = 'course_details_html'
    if not os.path.exists(folder):
        os.mkdir(folder)

    with Pool() as pool:
        func = partial(download_course, override_existing_files)
        pool.map(func, (i for i in range(1_000, 100_000)))


def download_all_tracks(override_existing_files=False):
    folder = 'tracks_html'
    if not os.path.exists(folder):
        os.mkdir(folder)

    with Pool() as pool:
        func = partial(download_track, override_existing_files)
        pool.map(func, (i for i in range(1_000, 10_000)))


def download_all():
    # download_all_courses()
    download_all_tracks()


if __name__ == '__main__':
    download_all()
