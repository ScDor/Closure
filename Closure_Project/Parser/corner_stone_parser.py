"""
Parses CornerStone courses from HUJI's website
"""
import re
from typing import List

import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import NewConnectionError

import utils

utils.setup_django_pycharm()  # pylint: disable=no-member
from rest_api.models import Course  # pylint: disable=import-error,wrong-import-order


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


def _parse_corner_stone_page(base_url: str, page_num: int = 0) -> List[int]:
    """
    :param base_url: url of a page showing corner stone course details,
     excluding its (optional) postfix of the format "?page=(number)"
    :param page_num: the zero-indexed page postfix to be appended to the url. (unless it is 0)
    :return: list of integer course identifiers.
    """
    course_ids = []
    url = base_url if page_num == 0 else f'{base_url}?page={page_num}'
    try:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        for tag in soup.findAll('a'):
            # parsed format:
            # "67925 | NAND to Tetris Workshop", optionally followed by "| <Professor's name>"
            search = re.search(r'(\d{3,6})\s*[|:-]\s*([^|\n\r\t]+)', str(tag.text))
            if search:
                course_id, _ = search.groups()
                # ignoring the 2nd argument as sometimes it is the professor's name
                course_ids.append(int(course_id))

        if course_ids:
            # if any courses were parsed, go on and attempt to parse the next page
            next_step = _parse_corner_stone_page(base_url, page_num + 1)
            course_ids += next_step

    except NewConnectionError:
        # nonexistent page, will just return the empty list
        pass

    return course_ids


def _parse_corner_stones(in_url: str) -> List[int]:
    """
    :param url: url to a page representing corner stone courses given by some faculty
    :return: list of integer course identifiers
    """
    urls = _parse_side_menu_urls(in_url)
    result = []
    for url in urls:
        result += _parse_corner_stone_page(url)
    return result


def fetch_parse_corner_stones():
    """
    fetches courses from the website
    """
    spirit = r'https://ap.huji.ac.il/%D7%A7%D7%95%D7%A8%D7%A1%D7%99%D7%9D-%D7%A8%D7%95%D7%97-2'
    social = r'https://ap.huji.ac.il/%D7%A7%D7%95%D7%A8%D7%A1%D7%99%D7%9D-%D7%97%D7%91%D7%A8' \
             r'%D7%94'
    democracy = r'https://ap.huji.ac.il/%D7%A8%D7%A9%D7%99%D7%9E%D7%AA-%D7%A7%D7%95%D7%A8%D7' \
                r'%A1%D7%99%D7%9D-%D7%9E%D7%AA%D7%97%D7%95%D7%9D-%D7%93%D7%9E%D7%95%D7%A7%D7' \
                r'%A8%D7%98%D7%99%D7%94-%D7%95%D7%97%D7%91%D7%A8%D7%94-%D7%91%D7%99%D7%A9%D7' \
                r'%A8%D7%90%D7%9C-0'
    experimental = r'https://ap.huji.ac.il/%D7%94%D7%AA%D7%97%D7%95%D7%9D-%D7%94%D7%A0%D7%99' \
                   r'%D7%A1%D7%95%D7%99%D7%99'
    result = []

    result.extend(_parse_corner_stones(spirit))
    result.extend(_parse_corner_stones(social))
    result.extend(_parse_corner_stones(experimental))
    result.extend(_parse_corner_stones(democracy))

    return result


def fetch_insert_corner_stones_into_db() -> None:
    """
    fetches corner stones from the website, and sets `is_corner_stone=True` to relevant ones.
    """
    old_corner_stones = {c.course_id for c in Course.objects.filter(is_corner_stone=True)}
    print(f'before parsing, {len(Course.objects.filter(is_corner_stone=True))} '
          f'courses are marked as corner stone')

    parsed = fetch_parse_corner_stones()

    for course_id in parsed:
        course = Course.objects.get(course_id=course_id)
        course.is_corner_stone = True
        course.save(update_fields=['is_corner_stone'])

    new_corner_stones = {c.course_id for c in Course.objects.filter(is_corner_stone=True)
                         if c.course_id not in old_corner_stones}
    print(f'after parsing, {len(new_corner_stones)} new courses marked as corner stone: '
          f'{new_corner_stones}')


if __name__ == '__main__':
    fetch_insert_corner_stones_into_db()
