from pathlib import Path

# Пути и директории
BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'
DOWNLOAD_DIR = 'downloads'
RESULTS_DIR = 'results'
PATH_NAME_WHATS_NEW = 'whatsnew/'
PAGE_NAME_DOWNLOAD = 'download.html'

# Форматы и настройки логирования
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
CODE_PAGES = 'utf-8'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
FILE_FORMAT = 'csv'

# Режимы работы и открытия файлов
PRETTY_OUTPUT_MODE = 'pretty'
FILE_OUTPUT_MODE = 'file'
MODE_DOWNLOAD = 'wb'
MODE_OPEN_FILE = 'w'

# Сообщения и тексты
CHECK_URL = 'При загрузке {url} возникла ошибка!'
DOWNLOAD_RESULT = 'Архив был сохранён тут: {path}'
CMD_ARGS = 'Аргументы для команды: {args}'
MESSAGE_ERRORS = 'Ошибка: {error}'
PARSER_START = 'Парсер запущен!'
PARSER_END = 'Парсер завершил работу!'
NO_RESULTS = 'Ничего не нашлось'
ERROR_PAGE = 'При загузке {url} возникла ошибка.'
ERROR_TAG = 'Тег {tag} {attrs} не найден.'

# Заголовки таблиц
HEADER_WHATS_NEW = ('Ссылка на статью', 'Заголовок', 'Редактор, Автор')
HEADER_LATEST_VERSION = ('Ссылка на документацию', 'Версия', 'Статус')
HEADER_PEP = ('Статус', 'Количество')

# URL адреса
MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_DOC_URL = 'https://peps.python.org/'

# Ожидаемые статусы PEP
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}

# Сообщение об ошибке для PEP статусов
ERROR_PEP_STATUS = (
    '\nСтатусы не совпадают:'
    '\n{pep_url}'
    '\nСтатус в ответе:'
    '\n{status}'
    '\nОжидаемые статусы:'
    '\n{expected_status}'
)
