import logging 
import re 
from collections import Counter 
from urllib.parse import urljoin 
 
import requests_cache 
from tqdm import tqdm 
 
from configs import configure_argument_parser, configure_logging 
from constants import ( 
    BASE_DIR, MAIN_DOC_URL, PEP_DOC_URL, EXPECTED_STATUS, 
    CHECK_URL, CMD_ARGS, DOWNLOAD_RESULT, MESSAGE_ERRORS, 
    ERROR_PEP_STATUS 
) 
from outputs import control_output 
from utils import get_response, find_tag, get_soup 
 
 
def whats_new(session): 
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/') 
    soup = get_soup(session, whats_new_url) 
    sections_by_python = soup.select( 
        '#what-s-new-in-python div.toctree-wrapper li.toctree-l1' 
    ) 
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')] 
    for section in tqdm(sections_by_python): 
        version_a_tag = section.find('a')  # Избавились от повторного поиска тега
        href = version_a_tag['href'] 
        version_link = urljoin(whats_new_url, href) 
        soup = get_soup(session, version_link) 
        
        if soup is None: 
            message = CHECK_URL.format(url=version_link) 
            logging.exception(message, stack_info=True) 
        
        results.append(( 
            version_link, 
            find_tag(soup, 'h1').text, 
            find_tag(soup, 'dl').text.replace('\n', '') 
        )) 
    
    return results 
 
 
def latest_versions(session): 
    soup = get_soup(session, MAIN_DOC_URL) 
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'}) 
    ul_tags = sidebar.find_all('ul') 
    for ul in ul_tags: 
        if 'All versions' in ul.text: 
            a_tags = ul.find_all('a') 
            break 
    else: 
        raise ValueError('Ничего не нашлось')  # Заменили KeyError на ValueError
    
    results = [('Ссылка на документацию', 'Версия', 'Статус')] 
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)' 
    for a_tag in a_tags: 
        text_match = re.search(pattern, a_tag.text) 
        if text_match is None: 
            version, status = a_tag.text, '' 
        else: 
            version, status = text_match.groups() 
        
        results.append((a_tag['href'], version, status)) 
    
    return results
