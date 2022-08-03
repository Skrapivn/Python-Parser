import logging
import re
import requests_cache

from bs4 import BeautifulSoup
from collections import defaultdict
from tqdm import tqdm
from urllib.parse import urljoin

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, EXPECTED_STATUS, LATEST_VERSIONS_RESULT,
                       MAIN_DOC_URL, PEP_RESULT, PEP_URL, WHATS_NEW_RESULT)
from outputs import control_output
from utils import get_response, find_tag


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    soup = BeautifulSoup(response.text, features='lxml')
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all('li',
                                              attrs={'class': 'toctree-l1'})
    results = WHATS_NEW_RESULT

    for section in tqdm(sections_by_python, desc='Загружаю последние новости'):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)

        response = get_response(session, version_link)
        if response is None:
            continue

        soup = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup, 'h1')
        h1_text = h1.text.replace('¶', '')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1_text, dl_text))

    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Не найден список c версиями Python')

    results = LATEST_VERSIONS_RESULT
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'

    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))

    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    soup = BeautifulSoup(response.text, 'lxml')
    main_tag = find_tag(soup, 'div', {'role': 'main'})
    table_tag = find_tag(main_tag, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]

    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename

    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    response = get_response(session, PEP_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    section_tag = find_tag(soup, 'section', {'id': 'numerical-index'})
    tbody_tag = find_tag(section_tag, 'tbody')
    tr_tags = tbody_tag.find_all('tr')

    results = PEP_RESULT
    all_pep_statuses = []
    page_pep_status = defaultdict()

    for pages in tqdm(tr_tags, desc='Загружаю PEP статусы'):
        pep_status = find_tag(pages, 'td')
        all_pep_statuses.append(pep_status.text[1:])

        a_tags = find_tag(pages, 'a', {'class': 'pep reference internal'})
        href = a_tags['href']
        link = urljoin(PEP_URL, href)

        response = get_response(session, link)
        if response is None:
            continue

        soup = BeautifulSoup(response.text, 'lxml')
        dl = find_tag(soup, 'dl')
        page_status = dl.find_next(string='Status').find_next('dd').text
        page_pep_status[page_status] = page_pep_status.get(page_status, 0) + 1

        all_pep_statuse = EXPECTED_STATUS.get(all_pep_statuses[-1], None)
        if page_status not in all_pep_statuse:
            log_message = (
                f'Несовпадающие статусы: {link}'
                f' Статус в карточке: {page_status}'
                f' Ожидаемые статусы: {all_pep_statuse}')
            logging.info(log_message)

    results.extend(page_pep_status.items())
    results.append(('Total', sum(page_pep_status.values())))
    logging.info('Загрузка статусов PEP завершена')
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')

    session = requests_cache.CachedSession()
    if args.clear_cache:
        logging.info('Чистим кэш')
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
