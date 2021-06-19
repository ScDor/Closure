""" downloads data from teh HUJI moon website"""
import os
from multiprocessing import Pool
from time import sleep

import requests


def download_course(i: int):
    """ downloads a single course data """
    url = f'http://moon.cc.huji.ac.il/nano/pages/wfrCourse.aspx?' \
          f'faculty=2&' \
          f'year=2021&' \
          f'courseId={i}'

    with open(f'course_details_html/{i}.html', 'wb') as open_file:
        open_file.write(requests.get(url).content)
    print(i)


def download_track(i: int):
    """ downloads a track """
    url = f'http://moon.cc.huji.ac.il/nano/pages/wfrMaslulDetails.aspx' \
          f'?year=2021&' \
          f'faculty=2&' \
          f'maslulId=2{i}'

    body = ''
    get = None

    while body == '' or 'timeout' in body:
        get = requests.get(url)
        body = get.text
        if 'timeout' in body:
            print(f'({i})')
            sleep(5)

    with open(f'tracks_html/{i}.html', 'wb') as track_file:
        track_file.write(get.content)
    print(i)


def download_all_courses():
    """ downloads all possible courses. may take a long time"""
    folder = 'course_details_html'
    if not os.path.exists(folder):
        os.mkdir(folder)

    with Pool() as pool:
        pool.map(download_course, (i for i in range(1_000, 100_000)))


def download_all_tracks():
    """ downloads all possible tracks. may take time"""
    folder = 'tracks_html'
    if not os.path.exists(folder):
        os.mkdir(folder)

    with Pool() as pool:
        pool.map(download_track, (i for i in range(1_000, 10_000)))


def download_all():
    """ downloads all courses and tracks. may take time"""
    download_all_courses()
    download_all_tracks()


if __name__ == '__main__':
    download_all()
