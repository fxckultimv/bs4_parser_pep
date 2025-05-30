from bs4 import BeautifulSoup
from requests import RequestException

from constants import CODE_PAGES, ERROR_PAGE, ERROR_TAG
from exceptions import ParserFindTagException


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        raise ParserFindTagException(ERROR_TAG.format(tag=tag, attrs=attrs))
    return searched_tag


def get_response(session, url, encode=CODE_PAGES):
    try:
        response = session.get(url)
        response.encoding = encode
        return response
    except RequestException as error:
        raise ConnectionError(ERROR_PAGE.format(url=url, error=error))


def get_soup(session, url, feature='lxml'):
    return BeautifulSoup(get_response(session, url).text, feature)
