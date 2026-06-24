- [x] Парсинг файлов .py
- [x] Получение функций
- [x] Проверка на дандер методы
- [x] Вынести соответствующие проверки в класс DocstringChecker
    - [ ] Также отображения из main.py перенести в DocstringChecker, желательно отдельным интерфейсом
- [x] Проверка на декоратор
- [x] Покраска функций с символом через rich
- [ ] Сделать отображение в виде дерева
    - [x] Общий для функций в модуле
    - [ ] Включая классы
- [ ] Сделать отображение в панельке rich
- [ ] Подсчитывать количество и качество, выводить статистику в процентах в конце прогона
- [ ] Флаг вывода в файл

Добавить из примера в конфиг:
```
def connect_to_database(host, port=5432, user=None, password=None):
"""Establishes connection to PostgreSQL database.

:param host: Database server hostname or IP address.
:type host: str
:param port: Port number, defaults to 5432
:type port: int, optional
:param user: Username for authentication, if None uses system user
:type user: str, optional
:param password: Password for authentication
:type password: str, optional

:returns: Database connection object
:rtype: Connection

:raises ConnectionError: If connection cannot be established
"""
```


## Idea
- [ ] Флаг для анализа директории с проектами, и вывод статистики по проектам