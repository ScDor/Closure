import os
from multiprocessing import Pool
from time import sleep
from functools import partial
from os import path

import requests


def get_data_with_retry(url: str, max_retries: int = 10):
    for i in range(max_retries):
        get = requests.get(url)
        text = get.text
        if text is not None \
                and ('timeout' not in text) \
                and ("אירעה שגיאה באתר" not in text):
            return get
        print(f"retry #{i}", url[-20:])
        sleep(1)
    raise RuntimeError(f"timed out after {max_retries} retries while trying to get {url}")


def download_course(data_year: int, override_existing_files: bool, i: int):
    folder = f'{data_year}_courses'
    html_path = f'{folder}/{i}.html'

    if path.exists(html_path) and not override_existing_files:
        print(data_year, "course", i, "exists")
        return

    url = f'http://moon.cc.huji.ac.il/nano/pages/wfrCourse.aspx?' \
          f'faculty=2&' \
          f'year={data_year}&' \
          f'courseId={i}'

    content = get_data_with_retry(url).content

    if "=\"lblCourseName\"><" in str(content):  # course name tag is empty
        print(data_year, "course", i, "empty")

    else:
        with open(html_path, 'wb') as f:
            f.write(content)
        print(data_year, "course", i, "saved")


def download_track(data_year: int, override_existing_files: bool, i: int):
    html_path = f'{data_year}_tracks/{i}.html'

    if (not override_existing_files) and path.exists(html_path):
        print(data_year, "track", i, "exists")
        return

    url = f'http://moon.cc.huji.ac.il/nano/pages/wfrMaslulDetails.aspx' \
          f'?year={data_year}&' \
          f'faculty=2&' \
          f'maslulId=2{i}'

    content = get_data_with_retry(url).content
    if "lblError" in str(content):  # empty:
        print(data_year, "track", i, "empty")

    else:
        with open(html_path, 'wb') as f:
            f.write(content)
        print(data_year, "track", i, "saved")


def download_all_courses(data_year: int, override_existing_files=False):
    folder = f'{data_year}_courses'
    if not os.path.exists(folder):
        os.mkdir(folder)

    with Pool() as pool:
        func = partial(download_course, data_year, override_existing_files)
        pool.map(func, (i for i in range(1_000, 100_000)))


def download_all_tracks(data_year: int, override_existing_files=False):
    folder = f'{data_year}_tracks'
    if not os.path.exists(folder):
        os.mkdir(folder)

    with Pool() as pool:
        func = partial(download_track, data_year, override_existing_files)
        pool.map(func, (i for i in range(1_000, 10_000)))


def download_all(data_year: int):
    download_all_courses(data_year)
    download_all_tracks(data_year)


if __name__ == '__main__':
    data_year = 2022
    download_all(data_year)
