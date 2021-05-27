import os
import re
from typing import List

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib3.exceptions import NewConnectionError

import utils

utils.setup_django_pycharm()

from rest_api.models import Course


def _parse_side_menu_urls(url: str):
    """
    Parses the side menu, that represent different campuses where the courses are given
    :param url: url of a page (say, page representing Experimental-field courses
    :return: urls of the pages including the course details (one for each campus/online)
    """
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    base_urls = []

    for title in soup.find_all('li'):
        if 'קמפוס' in title.text or 'קורס מקוון' in title.text:
            try:
                # possible addon: parse campus where each course takes place / online
                base_urls.append(title.contents[0]['href'])
            except KeyError:
                pass
    return base_urls


def _parse_corner_stone_ids(base_url, course_ids, page_num, url):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    for a in soup.findAll('a'):
        # parsed format:
        # "67925 | NAND to Tetris Workshop", optionally followed by "| <Professor's name>"
        search = re.search(r'(\d{3,6})\s*[|:-]\s*([^|\n\r\t]+)', str(a.text))
        if search:
            course_id, course = search.groups()
            # ignoring `course` as sometimes it is the professor's name (website mistake)
            course_ids.append(int(course_id))
    if course_ids:
        # if any courses were parsed, go on and attempt to parse the next page
        next_step = _parse_corner_stone_page(base_url, page_num + 1)
        course_ids += next_step
    return course_ids


def parse_corner_stone_folder(html_folder: str) -> List[int]:
    """
    :return: list of integer course identifiers, REGARDLESS OF CATEGORY
    """
    result = []
    for file_name in os.listdir(html_folder):
        with open(os.path.join(html_folder, file_name), 'r') as f:
            result.extend(_parse_corner_stone_page(f.read()))
    return result


FIRST_LEVEL_URLS = {
    'spirit':
        r'https://ap.huji.ac.il/%D7%A7%D7%95%D7%A8%D7%A1%D7%99%D7%9D-%D7%A8%D7%95%D7%97-2',
    'social':
        r'https://ap.huji.ac.il/%D7%A7%D7%95%D7%A8%D7%A1%D7%99%D7%9D-%D7%97%D7%91%D7%A8%D7%94',
    'democracy':
        r'https://ap.huji.ac.il/%D7%A8%D7%A9%D7%99%D7%9E%D7%AA-%D7%A7%D7%95%D7%A8%D7%A1%D7%99'
        r'%D7%9D-%D7%9E%D7%AA%D7%97%D7%95%D7%9D-%D7%93%D7%9E%D7%95%D7%A7%D7%A8%D7%98%D7%99%D7'
        r'%94-%D7%95%D7%97%D7%91%D7%A8%D7%94-%D7%91%D7%99%D7%A9%D7%A8%D7%90%D7%9C-0',
    # 'experimental':
    #     r'https://ap.huji.ac.il/%D7%94%D7%AA%D7%97%D7%95%D7%9D-%D7%94%D7%A0%D7%99%D7%A1%D7%95'
    #     r'%D7%99%D7%99'
}


def download_corner_stones():
    def download_third_level(base_url: str, faculty: str):
        """
        :param base_url: url of a page showing corner stone course details,
        :param faculty: faculty name
         excluding its (optional) postfix of the format "?page=(number)"
        :return: list of integer course identifiers.
        """
        page_num = 0

        while True:
            url = f'{base_url}?page={page_num}' if page_num != 0 else base_url
            try:
                utils.download_webpage(url, f'{faculty}_{page_num}')
                print(f'\tdownloaded third level {faculty}, page {page_num}')
                page_num += 1
            except NewConnectionError:  # nonexistent page
                break

    for path in ['corner_stones', 'corner_stones/base']:
        if not os.path.exists(path):
            os.mkdir(path)

    for faculty, url_1 in FIRST_LEVEL_URLS.items():
        second_level_urls = _parse_side_menu_urls(url_1)
        print(f'downloading {len(second_level_urls)} page(s) of {faculty} corner stones')

        for i, url_2 in enumerate(second_level_urls):
            utils.download_webpage(url_2, f'corner_stones/base/{faculty}_{i}')
            download_third_level(url_2, faculty)


def insert_corner_stones_to_db() -> None:
    """
    sets `is_corner_stone=True` to relevant courses.
    """
    print('fetching and parsing corner stone courses')
    for faculty, course_ids in FIRST_LEVEL_URLS.items():

        for course_id in tqdm(course_ids):
            course = Course.objects.get(course_id=course_id)
            course.is_corner_stone = True
            course.save(update_fields=['is_corner_stone'])


if __name__ == '__main__':
    # fetch_insert_corner_stones_to_db()
    download_corner_stones()
