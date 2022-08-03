from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_URL = 'https://peps.python.org/'
BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
LOG_DT_FORMAT = '%d.%m.%Y %H:%M:%S'
LOG_DIR = BASE_DIR / 'logs'

WHATS_NEW_RESULT = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
LATEST_VERSIONS_RESULT = [('Ссылка на документацию', 'Версия', 'Статус')]
PEP_RESULT = [('Статус', 'Количество')]

EXPECTED_STATUS = {
    'A': ['Active', 'Accepted'],
    'D': ['Deferred'],
    'F': ['Final'],
    'P': ['Provisional'],
    'R': ['Rejected'],
    'S': ['Superseded'],
    'W': ['Withdrawn'],
    '': ['Draft', 'Active'],
}
