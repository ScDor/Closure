import re
from typing import List

import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import NewConnectionError

from rest_api.models import Faculty


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

    except NewConnectionError:
        # nonexistent page, will just return the empty list
        pass

    return course_ids


def _parse_corner_stones(url: str) -> List[int]:
    """
    :param url: url to a page representing corner stone courses given by some faculty
    :return: list of integer course identifiers
    """
    urls = _parse_side_menu_urls(url)
    result = []
    for url in urls:
        result += _parse_corner_stone_page(url)
    return result


def get_corner_stones():
    spirit = r'https://ap.huji.ac.il/%D7%A7%D7%95%D7%A8%D7%A1%D7%99%D7%9D-%D7%A8%D7%95%D7%97-2'
    social = r'https://ap.huji.ac.il/%D7%A7%D7%95%D7%A8%D7%A1%D7%99%D7%9D-%D7%97%D7%91%D7%A8' \
             r'%D7%94'
    democracy = r'https://ap.huji.ac.il/%D7%A8%D7%A9%D7%99%D7%9E%D7%AA-%D7%A7%D7%95%D7%A8%D7' \
                r'%A1%D7%99%D7%9D-%D7%9E%D7%AA%D7%97%D7%95%D7%9D-%D7%93%D7%9E%D7%95%D7%A7%D7' \
                r'%A8%D7%98%D7%99%D7%94-%D7%95%D7%97%D7%91%D7%A8%D7%94-%D7%91%D7%99%D7%A9%D7' \
                r'%A8%D7%90%D7%9C-0'
    experimental = r'https://ap.huji.ac.il/%D7%94%D7%AA%D7%97%D7%95%D7%9D-%D7%94%D7%A0%D7%99' \
                   r'%D7%A1%D7%95%D7%99%D7%99'

    return {
        Faculty.SPIRIT: _parse_corner_stones(spirit),
        Faculty.SOCIAL: _parse_corner_stones(social),
        Faculty.SCIENCE: _parse_corner_stones(experimental)
        # todo find a representation for the democracy ones, follow the url to see logic behind
    }
