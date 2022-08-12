# Pep Python Parser

## Парсер выполняет четыре функции:

- ```whats-new``` Собирает ссылки на статьи о нововведениях в Python, переходит по ним и забирает информацию об авторах и редакторах статей - ```https://docs.python.org/3/``` (Cсылка на документацию, Версия и Статус)

- ```latest-version```Собирает информацию о статусах версий Python - ```https://docs.python.org/3/``` (сканирует карточку каждой версии Python и выводит информацию: Ссылка на статью, Заголовок, Редактор, Автор.)

- ```download``` Скачивает архив с актуальной документацией в формате zip. Папка src/downloads - ```https://docs.python.org/3/download.html```

- ```pep``` Собирает статусы всех PEP, ссылки на каждый PEP и подсчитывает общее количество PEP - ```https://peps.python.org/```

- В проекте информация пишется в логах на уровне INFO - ```.../src/logs/```

## Параматры парсера:
```
positional arguments:
  {whats-new,latest-versions,download,pep}  Режимы работы парсера

optional arguments:
  -h, --help  show this help message and exit
  -c, --clear-cache  Очистка кеша
  -o {pretty,file}, --output {pretty,file}  Дополнительные способы вывода данных
```
Режимы работы парсера:
- whats-new
- latest-version
- download
- pep

Очистка кеша:
- ```-с ``` - делает очистку 

Дополнительные способы вывода данных:
- ```-o pretty``` - вывод результатов в консоль в виде таблицы;
- ```-o file``` - вывод результатов в виде .csv файла, который сохраняется в директорию ../src/results;
- если не указывать команды по выводу, то итоги выводятся в консоль.

## Как запустить проект:
1. Клонировать репозиторий:
```
git clone https://github.com/Skrapivn/bs4_parser_pep.git
```

2. Создать виртуальное окружение:
```
python -m venv venv
```

3. Активировать виртуальное окружение, обновить версию ```pip``` и установить зависимости из ```requirements.txt```:
```
source venv/bin/activate
```
```
python -m pip install -–upgrade pip.
```
```
pip install -r requirements.txt
```

4. Запустить ```main.py``` с нужным режимом работы. Можно вызвать ```python main.py``` с параметром ```-h``` для просмотра параметров:
```
python main.py
```
Пример:
```
python main.py latest-versions -o pretty
```
[Sergey K.](https://github.com/skrapivn/)
