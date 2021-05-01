import re
from typing import List

import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import NewConnectionError

from Types import Faculty


def _parse_side_menu_urls(url: str):
    soup = BeautifulSoup(requests.get(url).content)
    urls = []

    for title in soup.find_all('li'):
        if 'קמפוס' in title.text or 'קורס מקוון' in title.text:
            try:
                # possible addon: parse campus where each course takes place / online
                urls.append(title.contents[0]['href'])
            except KeyError:
                pass
    return urls


def _get_courses(base_url: str, page_num: int = 0) -> List[str]:
    course_ids = []
    url = base_url if page_num == 0 else f'{base_url}?page={page_num}'
    try:
        soup = BeautifulSoup(requests.get(url).text)
        for a in soup.findAll('a'):
            # parsed format:"67101 | Introduction to CS", sometimes followed by " | Prof. name"
            search = re.search(r'(\d{3,6})\s*[|:-]\s*([^|\n\r\t]+)', str(a.text))
            if search:
                course_id, course = search.groups()
                # ignoring `course` as sometimes it is the professor's name (website mistake)
                course_ids.append(course_id)

        if course_ids:
            next_step = _get_courses(base_url, page_num + 1)
            course_ids.extend(next_step)

    except NewConnectionError:
        # nonexistent page, will just return the empty list
        pass

    return course_ids


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
        Faculty.SPIRIT: _get_courses(spirit),
        Faculty.SOCIAL: _get_courses(social),
        Faculty.SCIENCE: _get_courses(experimental)
        # todo find a representation for the democracy ones, follow the url to see logic behind
    }
