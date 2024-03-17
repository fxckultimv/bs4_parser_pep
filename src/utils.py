from bs4 import BeautifulSoup
from requests import RequestException

from constants import CODE_PAGES
from exceptions import ParserFindTagException

ERROR_PAGE = 'При загузке {url} возникла ошибка.'
ERROR_TAG = 'Тег {tag} {attrs} не найден.'


def get_soup(session, url):
    try:
        response = session.get(url)
        response.encoding = CODE_PAGES
        if response is None:
            return
        soup = BeautifulSoup(response.text, 'lxml')
        return soup
    except RequestException:
        raise ConnectionError(ERROR_PAGE.format(url=url))


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = CODE_PAGES
        return response
    except RequestException:
        raise ConnectionError(ERROR_PAGE.format(url=url))

def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        raise ParserFindTagException(ERROR_TAG.format(tag=tag, attrs=attrs))
    return searched_tag
