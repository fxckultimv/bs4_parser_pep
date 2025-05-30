import logging
import re
from collections import Counter
from urllib.parse import urljoin
from exceptions import ParserFindTagException

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging


from constants import (
    BASE_DIR,
    MAIN_DOC_URL,
    PEP_DOC_URL,
    EXPECTED_STATUS,
    CHECK_URL,
    CMD_ARGS,
    DOWNLOAD_RESULT,
    MESSAGE_ERRORS,
    ERROR_PEP_STATUS,
    PATH_NAME_WHATS_NEW,
    PARSER_END,
    PARSER_START,
    NO_RESULTS,
    HEADER_WHATS_NEW,
    HEADER_LATEST_VERSION,
    PAGE_NAME_DOWNLOAD,
    DOWNLOAD_DIR,
    MODE_DOWNLOAD,
)
from outputs import control_output
from utils import get_response, find_tag, get_soup


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, PATH_NAME_WHATS_NEW)
    soup = get_soup(session, whats_new_url)
    a_tags = soup.select(
        "#what-s-new-in-python div.toctree-wrapper "
        'li.toctree-l1 a[href$=".html"]'
    )
    results = [HEADER_WHATS_NEW]
    messages_error = []

    for a_tag in tqdm(a_tags):
        version_link = urljoin(whats_new_url, a_tag["href"])
        try:
            soup = get_soup(session, version_link)
        except ConnectionError as error:
            messages_error.append(CHECK_URL.format(error=error))
            continue
        results.append(
            (
                version_link,
                find_tag(soup, "h1").text,
                find_tag(soup, "dl").text.replace("\n", ""),
            )
        )

    list(map(logging.error, messages_error))

    return results


def latest_versions(session):
    soup = get_soup(session, MAIN_DOC_URL)
    ul_tags = soup.select("div.sphinxsidebarwrapper ul")

    for ul in ul_tags:
        if "All versions" in ul.text:
            a_tags = ul.find_all("a")
            break
    else:
        raise ParserFindTagException(NO_RESULTS)

    results = [HEADER_LATEST_VERSION]
    pattern = r"Python (?P<version>\d\.\d+) \((?P<status>.*)\)"

    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match is None:
            version, status = a_tag.text, ""
        else:
            version, status = text_match.groups()
        results.append((a_tag["href"], version, status))

    return results


def pep(session):
    soup = get_soup(session, PEP_DOC_URL)
    a_tags = soup.select("#numerical-index a.pep.reference.internal")
    statuses = []
    messages = []
    messages_error = []
    for a_tag in tqdm(a_tags):
        link = a_tag["href"]
        pep_url = urljoin(PEP_DOC_URL, link)
        try:
            soup = get_soup(session, pep_url)
        except ConnectionError as error:
            messages_error.append(CHECK_URL.format(error=error))
            continue
        abbr_tags = find_tag(soup, "abbr")
        status = abbr_tags.text
        abbreviation_status = status[0]
        statuses.append(status)
        if status not in EXPECTED_STATUS[abbreviation_status]:
            messages.append(
                ERROR_PEP_STATUS.format(
                    pep_url=pep_url,
                    status=status,
                    expected_status=EXPECTED_STATUS[abbreviation_status],
                )
            )
    list(map(logging.error, messages_error))
    list(map(logging.error, messages))
    counter = Counter(statuses)
    return [
        ('Статус', 'Количество'),
        *counter.items(),
        ('Всего', sum(counter.values())),
    ]


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, PAGE_NAME_DOWNLOAD)
    response = get_response(session, downloads_url)
    soup = get_soup(session, downloads_url)
    pdf_a4_link = soup.select_one(
        'div table.docutils a[href$="a4.zip"]')["href"]
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split("/")[-1]
    download_dir = BASE_DIR / DOWNLOAD_DIR
    download_dir.mkdir(exist_ok=True)
    archive_path = download_dir / filename
    with open(archive_path, MODE_DOWNLOAD) as file:
        file.write(response.content)
    message = DOWNLOAD_RESULT.format(path=archive_path)
    logging.info(message)


MODE_TO_FUNCTION = {
    "whats-new": whats_new,
    "latest-versions": latest_versions,
    "download": download,
    "pep": pep,
}


def main():
    try:
        configure_logging()
        logging.info(PARSER_START)
        arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
        args = arg_parser.parse_args()
        message = CMD_ARGS.format(args=args)
        logging.info(message)
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
        logging.info(PARSER_END)
    except Exception as error:
        logging.exception(MESSAGE_ERRORS.format(error=error))


if __name__ == "__main__":
    main()
