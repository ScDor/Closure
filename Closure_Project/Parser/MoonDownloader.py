import os
from multiprocessing import Pool
from time import sleep

import requests


def download_course(i: int):
    url = f'http://moon.cc.huji.ac.il/nano/pages/wfrCourse.aspx?' \
          f'faculty=2&' \
          f'year=2021&' \
          f'courseId={i}'

    with open(f'course_details/{i}.html', 'wb') as f:
        f.write(requests.get(url).content)
    print(i)


def download_track(i: int, skip_existing: bool = True):
    if skip_existing and os.path.exists(f'/tracks/{i}.html'):
        print(f'skipping {i}')
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

    with open(f'tracks/{i}.html', 'wb') as f:
        f.write(get.content)
    print(i)


def download_all_courses():
    with Pool() as pool:
        pool.map(download_course, (i for i in range(1_000, 100_000)))


def download_all_tracks():
    with Pool() as pool:
        pool.map(download_track, (i for i in range(1_000, 10_000)))


def download_all():
    for folder in ['tracks', 'course_details']:
        if not os.path.exists(folder):
            os.mkdir(folder)

    download_all_courses()
    download_all_tracks()


if __name__ == '__main__':
    download_all_tracks()
