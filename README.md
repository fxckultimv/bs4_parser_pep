# Проект парсинга pep
# Автор
Автор: veuxveuxveux

# Техно-стек
- Python 3.x
- Библиотеки: requests, BeautifulSoup, logging
- Формат данных: CSV

# Команды развертывания
1. Установите необходимые библиотеки:
   
   pip install requests beautifulsoup4
   
2. Загрузите репозиторий:
   
   git clone https://github.com/veuxveuxveux/parser.git
   
3. Перейдите в каталог проекта:
   
   cd parser
   

# Команды запуска
1. Запустите парсер для получения информации о последней версии Python:
   
   python main.py whats_new
   
2. Запустите парсер для получения информации о PEP документах:
   
   python main.py pep
   

# Доступ к справке
Для получения справки о доступных командах используйте флаг --help:
python main.py --help