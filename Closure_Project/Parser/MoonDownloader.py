import os
from multiprocessing import Pool
from time import sleep
from functools import partial
from os import path

import requests


def get_data_with_retry(url, max_retries=5):
    for i in range(max_retries):
        get = requests.get(url)
        text = get.text
        if text is not None and 'timeout' not in text:
            return get
        sleep(1)


def download_course(override_existing_files: bool, i: int):
    html_path = f'course_details_html/{i}.html'
    if path.exists(html_path) and not override_existing_files:
        print(i, "exists")
        return

    url = f'http://moon.cc.huji.ac.il/nano/pages/wfrCourse.aspx?' \
          f'faculty=2&' \
          f'year=2021&' \
          f'courseId={i}'

    content = get_data_with_retry(url, 5).content

    if len(content) in [29_443, 29_440]:  # empty
        print(i, "skipped")

    else:
        with open(html_path, 'wb') as f:
            f.write(content)
            print(i, "saved")


def download_track(override_existing_files: bool, i: int):
    html_path = f'tracks_html/{i}.html'
    if path.exists(html_path) and not override_existing_files:
        print(i, "exists")
        return

    url = f'http://moon.cc.huji.ac.il/nano/pages/wfrMaslulDetails.aspx' \
          f'?year=2021&' \
          f'faculty=2&' \
          f'maslulId=2{i}'

    content = get_data_with_retry(url, max_retries=5).content
    if len(content) == 6561:  # empty:
        print(i, "empty")
    else:
        with open(html_path, 'wb') as f:
            f.write(content)
        print(i, "saved")


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
    download_all_courses()
    download_all_tracks()


if __name__ == '__main__':
    download_all()
