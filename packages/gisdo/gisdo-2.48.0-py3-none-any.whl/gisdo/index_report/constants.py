from m3.db import (
    BaseEnumerate,
)


INDEX_1 = '1'
INDEX_1_1 = '1.1'
INDEX_2 = '2'
INDEX_3 = '3'
INDEX_4 = '4'
INDEX_4_1 = '4.1'
INDEX_4_2 = '4.2'
INDEX_5 = '5'
INDEX_6 = '6'
INDEX_7 = '7'
INDEX_7_1 = '7.1'
INDEX_7_2 = '7.2'
INDEX_7_3 = '7.3'
INDEX_7_4 = '7.4'
INDEX_7_5 = '7.5'
INDEX_7_6 = '7.6'
INDEX_7_7 = '7.7'
INDEX_8 = '8'
INDEX_8_1 = '8.1'
INDEX_8_2 = '8.2'
INDEX_8_3 = '8.3'
INDEX_9 = '9'
INDEX_9_1 = '9.1'
INDEX_10 = '10'
INDEX_10_1 = '10.1'
INDEX_11 = '11'
INDEX_12 = '12'
INDEX_12_1 = '12.1'
INDEX_13 = '13'
INDEX_13_1 = '13.1'
INDEX_14 = '14'
INDEX_15 = '15'
INDEX_16 = '16'
INDEX_17 = '17'
INDEX_17_1 = '17.1'
INDEX_18 = '18'
INDEX_18_1 = '18.1'
INDEX_18_2 = '18.2'
INDEX_18_3 = '18.3'
INDEX_18_4 = '18.4'
INDEX_18_5 = '18.5'
INDEX_19 = '19'
INDEX_19_1 = '19.1'
INDEX_19_2 = '19.2'
INDEX_19_3 = '19.3'
INDEX_20 = '20'
INDEX_20_1 = '20.1'
INDEX_20_2 = '20.2'
INDEX_20_3 = '20.3'
INDEX_20_4 = '20.4'
INDEX_20_5 = '20.5'
INDEX_20_6 = '20.6'
INDEX_20_7 = '20.7'
INDEX_20_8 = '20.8'
INDEX_21 = '21'
INDEX_22 = '22'
INDEX_22_1 = '22.1'
INDEX_22_1_1 = '22.1.1'
INDEX_22_1_2 = '22.1.2'
INDEX_22_2 = '22.2'
INDEX_22_3 = '22.3'
INDEX_22_3_1 = '22.3.1'
INDEX_22_3_2 = '22.3.2'
INDEX_22_4 = '22.4'
INDEX_22_5 = '22.5'
INDEX_22_5_1 = '22.5.1'
INDEX_22_5_2 = '22.5.2'
INDEX_22_6 = '22.6'
INDEX_22_7 = '22.7'
INDEX_22_8 = '22.8'
INDEX_22_8_1 = '22.8.1'
INDEX_22_8_2 = '22.8.2'
INDEX_23 = '23'
INDEX_24 = '24'
INDEX_25 = '25'
INDEX_26 = '26'
INDEX_27 = '27'
INDEX_28 = '28'
INDEX_29 = '29'
INDEX_29_1 = '29.1'
INDEX_29_2 = '29.2'
INDEX_29_3 = '29.3'
INDEX_30 = '30'
INDEX_30_1 = '30.1'
INDEX_30_2 = '30.2'
INDEX_31 = '31'
INDEX_31_1 = '31.1'
INDEX_31_2 = '31.2'
INDEX_31_3 = '31.3'
INDEX_31_4 = '31.4'
INDEX_32 = '32'
INDEX_32_1 = '32.1'
INDEX_32_2 = '32.2'
INDEX_33 = '33'

INDEX_CAPACITY = 'capacity'
INDEX_CAPACITY_GKP = 'capacity_gkp'
INDEX_ENROLLED = 'enrolled'
INDEX_FREE_SPACE = 'free_space'
INDEX_PROGRAM = 'program'
INDEX_PROGRAM_OVZ = 'program_ovz'
INDEX_LEKOTEKA = 'lekoteka'
INDEX_PASSPORT = 'passport'

INDEX_ENROLLED_GKP = 'enrolled_gkp'
INDEX_OVZ_DETI = 'ovz_deti'
INDEX_ADD_CONT = 'add_cont'
INDEX_ADD_CONT_GKP = 'add_cont_gkp'
INDEX_ADD_CONT_OVZ = 'add_cont_ovz'
INDEX_REDUCTION_SCHOOL = 'reduction_school'
INDEX_REDUCTION_OTHER = 'reduction_other'

# Теги для консультационного центра
INDEX_ADVISORY_CENTR_FACT = 'advisory_centr_fact'
INDEX_ADVISORY_CENTR_NUM_HITS_PERSONALLY = 'advisory_centr_num_hits_personally'
INDEX_ADVISORY_CENTR_NUM_HITS_DISTANT = 'advisory_centr_num_hits_distant'
INDEX_NUM_STAFF_MEMBER = 'num_staff_member'
INDEX_NUM_FREELANCER = 'num_freelancer'
INDEX_ADVISORY_CENTR_FORMA_1 = 'advisory_centr_forma_1'
INDEX_ADVISORY_CENTR_FORMA_2 = 'advisory_centr_forma_2'
INDEX_ADVISORY_CENTR_FORMA_3 = 'advisory_centr_forma_3'
INDEX_ADVISORY_CENTR_FORMA_4 = 'advisory_centr_forma_4'
# Теги для услуг ранней помощи
INDEX_EARLY_ASSISTANT_FACT = 'early_assistant_fact'
INDEX_EARLY_ASSISTANT_NUM_HITS_PERSONALLY = 'early_assistant_num_hits_personally'
INDEX_EARLY_ASSISTANT_NUM_HITS_DISTANT = 'early_assistant_num_hits_distant'
INDEX_EARLY_ASSISTANT_FORMA_1 = 'early_assistant_forma_1'
INDEX_EARLY_ASSISTANT_FORMA_2 = 'early_assistant_forma_2'
INDEX_EARLY_ASSISTANT_FORMA_3 = 'early_assistant_forma_3'
INDEX_EARLY_ASSISTANT_FORMA_4 = 'early_assistant_forma_4'


# Вспомогательные строки
ADVISORY_CENTR = 'Консультационный центр'
EARLY_ASSISTANT = 'Услуги ранней помощи'


INDEXES = [
    (INDEX_1, 'Показатель 1'),
    (INDEX_1_1, 'Показатель 1.1'),
    (INDEX_2, 'Показатель 2'),
    (INDEX_3, 'Показатель 3'),
    (INDEX_4, 'Показатель 4'),
    (INDEX_4_1, 'Показатель 4.1'),
    (INDEX_4_2, 'Показатель 4.2'),
    (INDEX_5, 'Показатель 5'),
    (INDEX_6, 'Показатель 6'),
    (INDEX_7, 'Показатель 7'),
    (INDEX_7_1, 'Показатель 7.1'),
    (INDEX_7_2, 'Показатель 7.2'),
    (INDEX_7_3, 'Показатель 7.3'),
    (INDEX_7_4, 'Показатель 7.4'),
    (INDEX_7_5, 'Показатель 7.5'),
    (INDEX_7_6, 'Показатель 7.6'),
    (INDEX_7_7, 'Показатель 7.7'),
    (INDEX_8, 'Показатель 8'),
    (INDEX_8_1, 'Показатель 8.1'),
    (INDEX_8_2, 'Показатель 8.2'),
    (INDEX_8_3, 'Показатель 8.3'),
    (INDEX_9, 'Показатель 9'),
    (INDEX_9_1, 'Показатель 9.1'),
    (INDEX_10, 'Показатель 10'),
    (INDEX_10_1, 'Показатель 10.1'),
    (INDEX_11, 'Показатель 11'),
    (INDEX_12, 'Показатель 12'),
    (INDEX_12_1, 'Показатель 12.1'),
    (INDEX_13, 'Показатель 13'),
    (INDEX_13_1, 'Показатель 13.1'),
    (INDEX_14, 'Показатель 14'),
    (INDEX_15, 'Показатель 15'),
    (INDEX_16, 'Показатель 16'),
    (INDEX_17, 'Показатель 17'),
    (INDEX_17_1, 'Показатель 17.1'),
    (INDEX_18, 'Показатель 18'),
    (INDEX_18_1, 'Показатель 18.1'),
    (INDEX_18_2, 'Показатель 18.2'),
    (INDEX_18_3, 'Показатель 18.3'),
    (INDEX_18_4, 'Показатель 18.4'),
    (INDEX_18_5, 'Показатель 18.5'),
    (INDEX_19, 'Показатель 19'),
    (INDEX_19_1, 'Показатель 19.1'),
    (INDEX_19_2, 'Показатель 19.2'),
    (INDEX_19_3, 'Показатель 19.3'),
    (INDEX_20, 'Показатель 20'),
    (INDEX_20_1, 'Показатель 20.1'),
    (INDEX_20_2, 'Показатель 20.2'),
    (INDEX_20_3, 'Показатель 20.3'),
    (INDEX_20_4, 'Показатель 20.4'),
    (INDEX_20_5, 'Показатель 20.5'),
    (INDEX_20_6, 'Показатель 20.6'),
    (INDEX_20_7, 'Показатель 20.7'),
    (INDEX_20_8, 'Показатель 20.8'),
    (INDEX_21, 'Показатель 21'),
    (INDEX_22, 'Показатель 22'),
    (INDEX_22_1, 'Показатель 22.1'),
    (INDEX_22_1_1, 'Показатель 22.1.1'),
    (INDEX_22_1_2, 'Показатель 22.1.2'),
    (INDEX_22_2, 'Показатель 22.2'),
    (INDEX_22_3, 'Показатель 22.3'),
    (INDEX_22_3_1, 'Показатель 22.3.1'),
    (INDEX_22_3_2, 'Показатель 22.3.2'),
    (INDEX_22_4, 'Показатель 22.4'),
    (INDEX_22_5, 'Показатель 22.5'),
    (INDEX_22_5_1, 'Показатель 22.5.1'),
    (INDEX_22_5_2, 'Показатель 22.5.2'),
    (INDEX_22_6, 'Показатель 22.6'),
    (INDEX_22_7, 'Показатель 22.7'),
    (INDEX_22_8, 'Показатель 22.8'),
    (INDEX_22_8_1, 'Показатель 22.8.1'),
    (INDEX_22_8_2, 'Показатель 22.8.2'),
    (INDEX_23, 'Показатель 23'),
    (INDEX_24, 'Показатель 24'),
    (INDEX_25, 'Показатель 25'),
    (INDEX_26, 'Показатель 26'),
    (INDEX_27, 'Показатель 27'),
    (INDEX_28, 'Показатель 28'),
    (INDEX_29, 'Показатель 29'),
    (INDEX_29_1, 'Показатель 29.1'),
    (INDEX_29_2, 'Показатель 29.2'),
    (INDEX_29_3, 'Показатель 29.3'),
    (INDEX_30, 'Показатель 30'),
    (INDEX_30_1, 'Показатель 30.1'),
    (INDEX_30_2, 'Показатель 30.2'),
    (INDEX_31, 'Показатель 31'),
    (INDEX_31_1, 'Показатель 31.1'),
    (INDEX_31_2, 'Показатель 31.2'),
    (INDEX_31_3, 'Показатель 31.3'),
    (INDEX_31_4, 'Показатель 31.4'),
    (INDEX_32, 'Показатель 32'),
    (INDEX_32_1, 'Показатель 32.1'),
    (INDEX_32_2, 'Показатель 32.2'),
    (INDEX_33, 'Показатель 33'),
    (INDEX_CAPACITY, 'Тег "capacity"'),
    (INDEX_CAPACITY_GKP, 'Тег "capacity_gkp"'),
    (INDEX_ENROLLED, 'Тег "enrolled"'),
    (INDEX_FREE_SPACE, 'Тег "free_space"'),
    (INDEX_PROGRAM, 'Тег "program"'),
    (INDEX_PROGRAM_OVZ, 'Тег "program_ovz"'),
    (INDEX_LEKOTEKA, 'Тег "lekoteka"'),
    (INDEX_PASSPORT, 'Тег "passport"'),
    (INDEX_ENROLLED_GKP, 'Тег "enrolled_gkp"'),
    (INDEX_OVZ_DETI, 'Тег "ovz_deti"'),
    (INDEX_ADD_CONT, 'Тег "add_cont"'),
    (INDEX_ADD_CONT_GKP, 'Тег "add_cont_gkp"'),
    (INDEX_ADD_CONT_OVZ, 'Тег "add_cont_ovz"'),
    (INDEX_REDUCTION_SCHOOL, 'Тег "reduction_school"'),
    (INDEX_REDUCTION_OTHER, 'Тег "reduction_other"'),
    # Теги для консультационного центра
    (INDEX_ADVISORY_CENTR_FACT, f'Тег "fact" ({ADVISORY_CENTR})'),
    (INDEX_ADVISORY_CENTR_NUM_HITS_PERSONALLY, f'Тег "num_hits_personally" ({ADVISORY_CENTR})'),
    (INDEX_ADVISORY_CENTR_NUM_HITS_DISTANT, f'Тег "num_hits_distant" ({ADVISORY_CENTR})'),
    (INDEX_NUM_STAFF_MEMBER, f'Тег "num_staff_member" ({ADVISORY_CENTR})'),
    (INDEX_NUM_FREELANCER, f'Тег "num_freelancer" ({ADVISORY_CENTR})'),
    (INDEX_ADVISORY_CENTR_FORMA_1, f'Тег "forma_1" ({ADVISORY_CENTR})'),
    (INDEX_ADVISORY_CENTR_FORMA_2, f'Тег "forma_2" ({ADVISORY_CENTR})'),
    (INDEX_ADVISORY_CENTR_FORMA_3, f'Тег "forma_3" ({ADVISORY_CENTR})'),
    (INDEX_ADVISORY_CENTR_FORMA_4, f'Тег "forma_4" ({ADVISORY_CENTR})'),
    # Теги для услуг ранней помощи
    (INDEX_EARLY_ASSISTANT_FACT, f'Тег "fact" ({EARLY_ASSISTANT})'),
    (INDEX_EARLY_ASSISTANT_NUM_HITS_PERSONALLY, f'Тег "num_hits_personally" ({EARLY_ASSISTANT})'),
    (INDEX_EARLY_ASSISTANT_NUM_HITS_DISTANT, f'Тег "num_hits_distant" ({EARLY_ASSISTANT})'),
    (INDEX_EARLY_ASSISTANT_FORMA_1, f'Тег "forma_1" ({EARLY_ASSISTANT})'),
    (INDEX_EARLY_ASSISTANT_FORMA_2, f'Тег "forma_2" ({EARLY_ASSISTANT})'),
    (INDEX_EARLY_ASSISTANT_FORMA_3, f'Тег "forma_3" ({EARLY_ASSISTANT})'),
    (INDEX_EARLY_ASSISTANT_FORMA_4, f'Тег "forma_4" ({EARLY_ASSISTANT})'),
]


REPORT_FIELDS = ('id', 'children__date_of_birth', 'desired_date', 'children_id', 'children__fullname')


QUEUE_INDEXES = (
    INDEX_7,
    INDEX_7_1,
    INDEX_7_2,
    INDEX_7_3,
    INDEX_7_4,
    INDEX_7_5,
    INDEX_7_6,
    INDEX_7_7,
    INDEX_12,
    INDEX_12_1,
    INDEX_13,
    INDEX_13_1,
    INDEX_14,
    INDEX_15,
    INDEX_16,
    INDEX_17,
    INDEX_17_1,
    INDEX_18,
    INDEX_18_1,
    INDEX_18_2,
    INDEX_18_3,
    INDEX_18_4,
    INDEX_18_5,
    INDEX_20,
    INDEX_20_1,
    INDEX_20_2,
    INDEX_20_3,
    INDEX_20_4,
    INDEX_20_5,
    INDEX_20_6,
    INDEX_20_7,
    INDEX_20_8,
)

INDEXES_31_x = (INDEX_31, INDEX_31_1, INDEX_31_2, INDEX_31_3, INDEX_31_4)

QUEUE_INDEXES_PARAMS = {
    INDEX_18_4: dict(distinct_children=True),
    INDEX_20_1: dict(check_unit=False, distinct_children=True),
    INDEX_20_5: dict(check_unit=False),
    INDEX_20_6: dict(check_unit=False),
    INDEX_20_7: dict(check_unit=False),
    INDEX_20_8: dict(check_unit=False),
}

QUEUE_INDEXES_ONLY_VALUES = (INDEX_8, INDEX_8_1, INDEX_8_2, INDEX_8_3)

# Теги из xml
XML_TAGS_BY_GROUP = (
    INDEX_ENROLLED_GKP,
    INDEX_OVZ_DETI,
    INDEX_ADD_CONT,
    INDEX_ADD_CONT_GKP,
    INDEX_ADD_CONT_OVZ,
    INDEX_REDUCTION_SCHOOL,
    INDEX_REDUCTION_OTHER,
)

XML_TAGS_BY_GROUP_ONLY_VALUES = (
    INDEX_FREE_SPACE,
    INDEX_CAPACITY,
    INDEX_CAPACITY_GKP,
    INDEX_PROGRAM,
    INDEX_PROGRAM_OVZ,
)

# Теги, у которых не нужно прописывать возрастную категорию(оставлять пустым)
EXCLUDE_AGE_CATEGORY = (
    INDEX_ENROLLED_GKP,
    INDEX_OVZ_DETI,
    INDEX_ADD_CONT,
    INDEX_ADD_CONT_GKP,
    INDEX_ADD_CONT_OVZ,
    INDEX_REDUCTION_SCHOOL,
    INDEX_REDUCTION_OTHER,
)

XML_TAGS = (
    INDEX_LEKOTEKA,
    INDEX_PASSPORT,
    INDEX_ADVISORY_CENTR_FACT,
    INDEX_ADVISORY_CENTR_NUM_HITS_PERSONALLY,
    INDEX_ADVISORY_CENTR_NUM_HITS_DISTANT,
    INDEX_ADVISORY_CENTR_NUM_HITS_DISTANT,
    INDEX_NUM_STAFF_MEMBER,
    INDEX_NUM_FREELANCER,
    INDEX_ADVISORY_CENTR_FORMA_1,
    INDEX_ADVISORY_CENTR_FORMA_2,
    INDEX_ADVISORY_CENTR_FORMA_3,
    INDEX_ADVISORY_CENTR_FORMA_4,
    INDEX_EARLY_ASSISTANT_FACT,
    INDEX_EARLY_ASSISTANT_NUM_HITS_PERSONALLY,
    INDEX_EARLY_ASSISTANT_NUM_HITS_DISTANT,
    INDEX_EARLY_ASSISTANT_FORMA_1,
    INDEX_EARLY_ASSISTANT_FORMA_2,
    INDEX_EARLY_ASSISTANT_FORMA_3,
    INDEX_EARLY_ASSISTANT_FORMA_4,
    *XML_TAGS_BY_GROUP,
    *XML_TAGS_BY_GROUP_ONLY_VALUES,
)


class DataTypes(BaseEnumerate):
    """Описание типов данных, используемых в запросах."""

    DIRECT = 'direct'
    DECLARATION = 'declaration'
    CHILD = 'child'
    PUPIL = 'pupil'
    DEDUCT = 'deduct'
    GROUP = 'group'

    values = {
        DIRECT: 'Направление',
        DECLARATION: 'Заявление',
        CHILD: 'Ребенок',
        PUPIL: 'Зачисление',
        DEDUCT: 'Отчисление',
        GROUP: 'Группа',
    }


# Маппинг тегов в выгружаемом xml файле (ключ - название словаря с данными,
# значение - кортежи (название тега; параметр, по которому берется значение
# из словаря)
XML_TAGS_MAPPING = {
    'organization': (
        (INDEX_LEKOTEKA, 'lekoteka'),
        (INDEX_PASSPORT, 'passport'),
        (INDEX_ADVISORY_CENTR_FACT, 'fact'),
    ),
    'data_advisory_centr': (
        (INDEX_ADVISORY_CENTR_NUM_HITS_PERSONALLY, 'num_hits_personally'),
        (INDEX_ADVISORY_CENTR_NUM_HITS_DISTANT, 'num_hits_distant'),
        (INDEX_NUM_STAFF_MEMBER, 'num_staff_member'),
        (INDEX_NUM_FREELANCER, 'num_freelancer'),
        (INDEX_ADVISORY_CENTR_FORMA_1, 'forma_1'),
        (INDEX_ADVISORY_CENTR_FORMA_2, 'forma_2'),
        (INDEX_ADVISORY_CENTR_FORMA_3, 'forma_3'),
        (INDEX_ADVISORY_CENTR_FORMA_4, 'forma_4'),
    ),
    'early_assistant_data': (
        (INDEX_EARLY_ASSISTANT_FACT, 'fact'),
        (INDEX_EARLY_ASSISTANT_NUM_HITS_PERSONALLY, 'num_hits_personally'),
        (INDEX_EARLY_ASSISTANT_NUM_HITS_DISTANT, 'num_hits_distant'),
        (INDEX_EARLY_ASSISTANT_FORMA_1, 'forma_1'),
        (INDEX_EARLY_ASSISTANT_FORMA_2, 'forma_2'),
        (INDEX_EARLY_ASSISTANT_FORMA_3, 'forma_3'),
        (INDEX_EARLY_ASSISTANT_FORMA_4, 'forma_4'),
    ),
}

XML_GROUP_TAGS_MAP = (
    (INDEX_ENROLLED_GKP, 'enrolled_gkp_children'),
    (INDEX_OVZ_DETI, 'ovz_deti_children'),
    (INDEX_ADD_CONT, 'add_cont_children'),
    (INDEX_ADD_CONT_GKP, 'add_cont_gkp_children'),
    (INDEX_ADD_CONT_OVZ, 'add_cont_ovz_children'),
    (INDEX_REDUCTION_SCHOOL, 'reduction_school_children'),
    (INDEX_REDUCTION_OTHER, 'reduction_other_children'),
)

XML_GROUP_TAGS_ONLY_VALUES_MAP = (
    (INDEX_FREE_SPACE, 'free_space'),
    (INDEX_CAPACITY, 'capacity'),
    (INDEX_CAPACITY_GKP, 'capacity_gkp'),
    (INDEX_PROGRAM, 'program'),
    (INDEX_PROGRAM_OVZ, 'program_ovz'),
)
