from collections import (
    OrderedDict,
)

from kinder.core.dict.models import (
    DouType,
)
from kinder.core.unit.models import (
    UnitStatus,
)


# Сдвиг текущей даты для проверки даты по приказу
DATE_SHIFT_IN_ORDER = 2

# Список статусов организаций, которые не учитываются в запросах.
# Организации, которые больше не функционируют.
# ("Ликвидировано", "Закрыто", "Присоединена к другой организации")
STATUSES_UNIT_EXCLUDE = (UnitStatus.CLOSED, UnitStatus.LIQUIDATED, UnitStatus.JOINED_OTHER)

# ---------------------------------------
# Перечисления для формирования запроса
# ---------------------------------------
AGE_CATEGORIES_FULL = OrderedDict(
    [
        ('2-6-MONTHS', 'от 2 месяцев до 6 месяцев'),
        ('0.5-1-YEARS', 'от 6 месяцев до 1 года'),
        ('1-1.5-YEARS', 'от 1 года до 1,5 года'),
        ('1.5-2-YEARS', 'от 1,5 до 2 лет'),
        ('2-2.5-YEARS', 'от 2 до 2,5 лет'),
        ('2.5-3-YEARS', 'от 2,5 до 3 лет'),
        ('3-3.5-YEARS', 'от 3 до 3,5 лет'),
        ('3.5-4-YEARS', 'от 3,5 до 4 лет'),
        ('4-4.5-YEARS', 'от 4 до 4,5 лет'),
        ('4.5-5-YEARS', 'от 4,5 до 5 лет'),
        ('5-5.5-YEARS', 'от 5 до 5,5 лет'),
        ('5.5-6-YEARS', 'от 5,5 до 6 лет'),
        ('6-6.5-YEARS', 'от 6 до 6,5 лет'),
        ('6.5-7-YEARS', 'от 6,5 до 7 лет'),
        ('7-7.5-YEARS', 'от 7 до 7,5 лет'),
        ('7.5-99-YEARS', 'от 7,5 лет и старше'),
    ]
)


AGE_CATEGORIES_EIGHT = OrderedDict(
    [
        ('2-1-YEARS', 'от 2 месяцев до 1 года'),
        ('1-2-YEARS', 'от 1 года до 2 лет'),
        ('2-3-YEARS', 'от 2 до 3 лет'),
        ('3-4-YEARS', 'от 3 до 4 лет'),
        ('4-5-YEARS', 'от 4 до 5 лет'),
        ('5-6-YEARS', 'от 5 до 6 лет'),
        ('6-7-YEARS', 'от 6 до 7 лет'),
        ('7-7.5-YEARS', 'от 7 лет и старше'),
    ]
)


# При расчете показателей по очереди было сделано неправильное решение.
# формируется словарик
# queue_cache[ИД_УЧРЕЖДЕНИЯ][ключ возрастной категории][тип_Учреждения]
# При расчете на 10 сентября и текущюю дату необходимо,
# чтобы ключи AGE_CATEGORIES_FULL и AGE_CATEGORIES_FULL_CURRENT
# как-то различались.
# НЕ СУДИТЕ МЕНЯ СТРОГО.
AGE_CATEGORIES_FULL_CURRENT = {
    'C2-6-MONTHS': 'от 2 месяцев до 6 месяцев (на текущую дату)',
    'C0.5-1-YEARS': 'от 6 месяцев до 1 года (на текущую дату)',
    'C1-1.5-YEARS': 'от 1 года до 1,5 года (на текущую дату)',
    'C1.5-2-YEARS': 'от 1,5 до 2 лет (на текущую дату)',
    'C2-2.5-YEARS': 'от 2 до 2,5 лет (на текущую дату)',
    'C2.5-3-YEARS': 'от 2,5 до 3 лет (на текущую дату)',
    'C3-3.5-YEARS': 'от 3 до 3,5 лет (на текущую дату)',
    'C3.5-4-YEARS': 'от 3,5 до 4 лет (на текущую дату)',
    'C4-4.5-YEARS': 'от 4 до 4,5 лет (на текущую дату)',
    'C4.5-5-YEARS': 'от 4,5 до 5 лет (на текущую дату)',
    'C5-5.5-YEARS': 'от 5 до 5,5 лет (на текущую дату)',
    'C5.5-6-YEARS': 'от 5,5 до 6 лет (на текущую дату)',
    'C6-6.5-YEARS': 'от 6 до 6,5 лет (на текущую дату)',
    'C6.5-7-YEARS': 'от 6,5 до 7 лет (на текущую дату)',
    'C7-7.5-YEARS': 'от 7 до 7,5 лет (на текущую дату)',
    'C7.5-99-YEARS': 'от 7,5 лет и старше (на текущую дату)',
}
AGE_CATEGORIES_FULL_MAP = {
    'от 2 месяцев до 6 месяцев (на текущую дату)': 'от 2 месяцев до 6 месяцев',
    'от 6 месяцев до 1 года (на текущую дату)': 'от 6 месяцев до 1 года',
    'от 1 года до 1,5 года (на текущую дату)': 'от 1 года до 1,5 года',
    'от 1,5 до 2 лет (на текущую дату)': 'от 1,5 до 2 лет',
    'от 2 до 2,5 лет (на текущую дату)': 'от 2 до 2,5 лет',
    'от 2,5 до 3 лет (на текущую дату)': 'от 2,5 до 3 лет',
    'от 3 до 3,5 лет (на текущую дату)': 'от 3 до 3,5 лет',
    'от 3,5 до 4 лет (на текущую дату)': 'от 3,5 до 4 лет',
    'от 4 до 4,5 лет (на текущую дату)': 'от 4 до 4,5 лет',
    'от 4,5 до 5 лет (на текущую дату)': 'от 4,5 до 5 лет',
    'от 5 до 5,5 лет (на текущую дату)': 'от 5 до 5,5 лет',
    'от 5,5 до 6 лет (на текущую дату)': 'от 5,5 до 6 лет',
    'от 6 до 6,5 лет (на текущую дату)': 'от 6 до 6,5 лет',
    'от 6,5 до 7 лет (на текущую дату)': 'от 6,5 до 7 лет',
    'от 7 до 7,5 лет (на текущую дату)': 'от 7 до 7,5 лет',
    'от 7,5 лет и старше (на текущую дату)': 'от 7,5 лет и старше',
}

# Важен порядок
AGE_CATEGORIES_FULL_LIST = [
    '2-6-MONTHS',
    '0.5-1-YEARS',
    '1-1.5-YEARS',
    '1.5-2-YEARS',
    '2-2.5-YEARS',
    '2.5-3-YEARS',
    '3-3.5-YEARS',
    '3.5-4-YEARS',
    '4-4.5-YEARS',
    '4.5-5-YEARS',
    '5-5.5-YEARS',
    '5.5-6-YEARS',
    '6-6.5-YEARS',
    '6.5-7-YEARS',
    '7-7.5-YEARS',
    '7.5-99-YEARS',
]
AGE_CATEGORIES_CUT = OrderedDict(
    [('2M-3YEARS', 'от 2 месяцев до 3 лет'), ('3-5-YEARS', 'от 3 до 5 лет'), ('5-7.5-YEARS', 'от 5 до 7,5 лет')]
)


AGE_CATEGORIES_CUT_LIST = [
    '2M-3YEARS',
    '3-5-YEARS',
    '5-7.5-YEARS',
]

ALL = 'Все'

AGE_CATEGORIES_ALL = {'ALL': ALL}

GOVERNMENT = 'gov_dou'
NOT_GOVERNMENT = 'not_gov_dou'
IP = 'ip_dou'
ALL_UNIT_TYPES = 'ALL_TYPES'

# Переопределяем типы ДОУ т.к. в ЭДС DEPARTMENTAL и OTHER - не государственные
REDEFINED_TYPES = (DouType.DEPARTMENTAL, DouType.OTHER)

# Добавляем типы DEPARTMENTAL и OTHER к государственным
GOVERNMENT_TYPES = DouType.GOVERNMENT_TYPES + REDEFINED_TYPES

# Убираем типы DEPARTMENTAL и OTHER из не государственных
NOT_GOVERNMENT_TYPES = [e for e in DouType.NOT_GOVERNMENT_TYPES if e not in REDEFINED_TYPES]

DOU_TYPE_MAP = {GOVERNMENT: GOVERNMENT_TYPES, NOT_GOVERNMENT: NOT_GOVERNMENT_TYPES, IP: DouType.IP_TYPES}

CURRENT_ALL = 'Все (на текущую дату)'
NO = 'Нет'

#: Вид подачи заявления
DELIVERY_TYPES = {'IN_PERSON': 'При личном обращении', 'PORTAL': 'С портала'}
#: Виды ДОО
DOO_TYPES = {'NON_STATE': 'Негосударственные', 'BUSINESS': 'ИП'}
AGE_CATEGORIES_CALC = {
    # key: (age1, age2, age1_month, age2_month)
    ALL: (0, 7, 0, 6),  # (#90444)
    AGE_CATEGORIES_FULL['2-6-MONTHS']: (0, 0, 0, 6),  # (#90444)
    AGE_CATEGORIES_FULL['0.5-1-YEARS']: (0, 1, 6, 0),
    AGE_CATEGORIES_FULL['1-1.5-YEARS']: (1, 1, 0, 6),
    AGE_CATEGORIES_FULL['1.5-2-YEARS']: (1, 2, 6, 0),
    AGE_CATEGORIES_FULL['2-2.5-YEARS']: (2, 2, 0, 6),
    AGE_CATEGORIES_FULL['2.5-3-YEARS']: (2, 3, 6, 0),
    AGE_CATEGORIES_FULL['3-3.5-YEARS']: (3, 3, 0, 6),
    AGE_CATEGORIES_FULL['3.5-4-YEARS']: (3, 4, 6, 0),
    AGE_CATEGORIES_FULL['4-4.5-YEARS']: (4, 4, 0, 6),
    AGE_CATEGORIES_FULL['4.5-5-YEARS']: (4, 5, 6, 0),
    AGE_CATEGORIES_FULL['5-5.5-YEARS']: (5, 5, 0, 6),
    AGE_CATEGORIES_FULL['5.5-6-YEARS']: (5, 6, 6, 0),
    AGE_CATEGORIES_FULL['6-6.5-YEARS']: (6, 6, 0, 6),
    AGE_CATEGORIES_FULL['6.5-7-YEARS']: (6, 7, 6, 0),
    AGE_CATEGORIES_FULL['7-7.5-YEARS']: (7, 7, 0, 6),
    AGE_CATEGORIES_FULL['7.5-99-YEARS']: (7, 99, 6, 0),
    AGE_CATEGORIES_EIGHT['2-1-YEARS']: (0, 1, 2, 0),
    AGE_CATEGORIES_EIGHT['1-2-YEARS']: (1, 2, 0, 0),
    AGE_CATEGORIES_EIGHT['2-3-YEARS']: (2, 3, 0, 0),
    AGE_CATEGORIES_EIGHT['3-4-YEARS']: (3, 4, 0, 0),
    AGE_CATEGORIES_EIGHT['4-5-YEARS']: (4, 5, 0, 0),
    AGE_CATEGORIES_EIGHT['5-6-YEARS']: (5, 6, 0, 0),
    AGE_CATEGORIES_EIGHT['6-7-YEARS']: (6, 7, 0, 0),
    AGE_CATEGORIES_CUT['2M-3YEARS']: (0, 3, 2, 0),
    AGE_CATEGORIES_CUT['3-5-YEARS']: (3, 5, 0, 0),
    AGE_CATEGORIES_CUT['5-7.5-YEARS']: (5, 7, 0, 6),
    '0-7.5-YEARS': (0, 7, 0, 6),
    '3-7.5-YEARS': (3, 7, 0, 6),
}

#: Статусы заявления
APPLICATION_STATUSES = {
    'IN_LINE': 'В очереди',
    'IN_LINE_DEFERRED': 'В очереди (отложенный спрос)',
    'ENROLLED': 'Зачислены',
    'WANT_CHANGE_DOO': 'Желающие сменить ДОО',
    'IN_LINE_ENROLLED': 'В очереди и зачислены',
    'IN_LINE_WANT_CHANGE_DOO': 'В очереди и желающие сменить ДОО',
    'DENIED': 'Отказано в услуге',
}
#: Виды льгот
BENEFIT_TYPES = {
    'HAVE_BENEFITS': 'Имеются льготы',
    'FEDERAL': 'Федеральная льгота',
    'REGIONAL': 'Региональная льгота',
    'MUNICIPAL': 'Муниципальная льгота',
}
#: Потребности по здоровью
HEALTH_NEEDS = {
    'DISABLED': 'Ограниченные возможности здоровья',
    'HEALTH': 'Нуждающиеся в оздоровительных группах',
    'CORRECT': 'Нуждающиеся в компенсирующих группах',
}
#: Виды групп
GROUP_TYPES = {
    'FAMILY': 'Семейные дошкольные группы',
    'SHORT_STAY': 'Группы кратковременного пребывания',
    'DISABLED': 'Группы для детей с ограниченными возможностями здоровья',
    'CORRECT': 'Компенсирующие группы',
    'HEALTH': 'Оздоровительные группы',
    'CARE': 'Группы по присмотру и уходу',
}
#: Федеральные объекты
FEDERAL_DISTRICTS = {
    'CENTRAL_REGION': 'Центральный федеральный округ',
    'SOUTH_REGION': 'Южный федеральный округ',
    'NORTHWEST_REGION': 'Северо-Западный федеральный округ',
    'FAR_EASTERN_REGION': 'Дальневосточный федеральный округ',
    'SIBERIAN_REGION': 'Сибирский федеральный округ',
    'URALIAN_REGION': 'Уральский федеральный округ',
    'VOLGA_REGION': 'Приволжский федеральный округ',
    'NORTH_CAUCASUS_REGION': 'Северо-Кавказский федеральный округ',
}

# Карта соотношений возрастных подкатегорий
# системы и возрастных категорий ФО
AGE_CUT_SUBCATEGORY_MAP = {
    AGE_CATEGORIES_CUT['2M-3YEARS']: ['0-1', '1-2', '2-3', '1-3', '1-4'],
    AGE_CATEGORIES_CUT['3-5-YEARS']: [
        '3-4',
        '4-5',
        '3-5',
        '4-6',
        '3-6',
        '3-7',
        '1-5',
        '2-5',
        '1-6',
        '2-4',
        '2-6',
        '1-7',
    ],
    AGE_CATEGORIES_CUT['5-7.5-YEARS']: ['5-6', '6-7', '5-7', '4-7', '2-7'],
}
# Карта соотношений возрастных категорий
# системы и возрастных категорий ФО
AGE_CUT_CATEGORY_MAP = {
    AGE_CATEGORIES_CUT['2M-3YEARS']: ['0-1', '1-3'],
    AGE_CATEGORIES_CUT['3-5-YEARS']: ['3-7', '1-7'],
    AGE_CATEGORIES_CUT['5-7.5-YEARS']: [],
}

AGE_CUT_DEFAULT_CATEGORY = '3-5-YEARS'

AGE_EIGHT_SUBCATEGORY_MAP = {
    AGE_CATEGORIES_EIGHT['2-1-YEARS']: [0, 1],
    AGE_CATEGORIES_EIGHT['1-2-YEARS']: [2],
    AGE_CATEGORIES_EIGHT['2-3-YEARS']: [3],
    AGE_CATEGORIES_EIGHT['3-4-YEARS']: [4],
    AGE_CATEGORIES_EIGHT['4-5-YEARS']: [5],
    AGE_CATEGORIES_EIGHT['5-6-YEARS']: [6],
    AGE_CATEGORIES_EIGHT['6-7-YEARS']: [7],
    AGE_CATEGORIES_EIGHT['7-7.5-YEARS']: [8],
}

AGE_EIGHT_CATEGORY_MAP = {
    AGE_CATEGORIES_EIGHT['2-1-YEARS']: ['0-1'],
    AGE_CATEGORIES_EIGHT['1-2-YEARS']: [],
    AGE_CATEGORIES_EIGHT['2-3-YEARS']: ['1-3'],
    AGE_CATEGORIES_EIGHT['3-4-YEARS']: [],
    AGE_CATEGORIES_EIGHT['4-5-YEARS']: ['1-7', '3-7'],
    AGE_CATEGORIES_EIGHT['5-6-YEARS']: [],
    AGE_CATEGORIES_EIGHT['6-7-YEARS']: [],
    AGE_CATEGORIES_EIGHT['7-7.5-YEARS']: [],
}

AGE_EIGHT_DEFAULT_CATEGORY = '4-5-YEARS'

CUT_TO_FULL_CATEGORY_MAP = {
    AGE_CATEGORIES_CUT['2M-3YEARS']: [
        AGE_CATEGORIES_FULL['2-6-MONTHS'],
        AGE_CATEGORIES_FULL['0.5-1-YEARS'],
        AGE_CATEGORIES_FULL['1-1.5-YEARS'],
        AGE_CATEGORIES_FULL['1.5-2-YEARS'],
        AGE_CATEGORIES_FULL['2-2.5-YEARS'],
        AGE_CATEGORIES_FULL['2.5-3-YEARS'],
    ],
    AGE_CATEGORIES_CUT['3-5-YEARS']: [
        AGE_CATEGORIES_FULL['3-3.5-YEARS'],
        AGE_CATEGORIES_FULL['3.5-4-YEARS'],
        AGE_CATEGORIES_FULL['4-4.5-YEARS'],
        AGE_CATEGORIES_FULL['4.5-5-YEARS'],
    ],
    AGE_CATEGORIES_CUT['5-7.5-YEARS']: [
        AGE_CATEGORIES_FULL['5-5.5-YEARS'],
        AGE_CATEGORIES_FULL['5.5-6-YEARS'],
        AGE_CATEGORIES_FULL['6-6.5-YEARS'],
        AGE_CATEGORIES_FULL['6.5-7-YEARS'],
        AGE_CATEGORIES_FULL['7-7.5-YEARS'],
    ],
}

CUT_TO_EIGHT_CATEGORY_MAP = {
    AGE_CATEGORIES_CUT['2M-3YEARS']: [
        AGE_CATEGORIES_EIGHT['2-1-YEARS'],
        AGE_CATEGORIES_EIGHT['1-2-YEARS'],
        AGE_CATEGORIES_EIGHT['2-3-YEARS'],
    ],
    AGE_CATEGORIES_CUT['3-5-YEARS']: [AGE_CATEGORIES_EIGHT['3-4-YEARS'], AGE_CATEGORIES_EIGHT['4-5-YEARS']],
    AGE_CATEGORIES_CUT['5-7.5-YEARS']: [
        AGE_CATEGORIES_EIGHT['5-6-YEARS'],
        AGE_CATEGORIES_EIGHT['6-7-YEARS'],
        AGE_CATEGORIES_EIGHT['7-7.5-YEARS'],
    ],
}

FEDERAL = 1
MUNICIPAL = 2
REGIONAL = 3

# Доступные значения выпадающего поля,
# расположенного в окне "Настройки",
# которое задает интервал повторной отправки
RESEND_AFTER_TIMES_LIST = [
    (0, 'Нет'),
    (5, '5 минут'),
    (15, '15 минут'),
    (30, '30 минут'),
    (60, '1 час'),
    (120, '2 часа'),
    (240, '4 часа'),
]

# Показатели, которые обнуляются при динамическом подсчете
RESET_METRICS = ('8', '8.1', '8.2', '8.3')

ATTENDANCE_TRANSFER_TYPES = ((1, 'По табелю'), (2, 'По полю "Количество дето-дней"'))

# Тексты ошибок, при которых нужно производить переотправку ФО
RESEND_FEDERAL_REPORT_ERRORS = [
    'Проблема при авторизации:',
]

# Номера простых индексов для показателей 22.х
SIMPLE_INDEXES_22 = (
    '22',
    '22.1.1',
    '22.1.2',
    '22.2',
    '22.3.1',
    '22.3.2',
    '22.4',
    '22.5.1',
    '22.5.2',
    '22.6',
    '22.7',
    '22.8.1',
    '22.8.2',
)
# Маппинг для сложных показателей 22 {показатель: суммируемые показатели}
SUM_INDEXES_22 = {
    '22.1': ('22.1.1', '22.1.2'),
    '22.3': ('22.3.1', '22.3.2'),
    '22.5': ('22.5.1', '22.5.2'),
    '22.8': ('22.8.1', '22.8.2'),
}

# Название права "Поле "Относится к МО""
PERM_RELATED_TO_MO = 'field_related_to_mo'
