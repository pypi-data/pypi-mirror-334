from future.builtins import (
    object,
)
from yadic import (
    Container,
)


class GisdoContainer(object):
    """Специализация контейнера для пакета Gisdo

    cont = GisdoContainer()
    builder = cont.get("7.3")
    qs = builder.build(ctx)
    qs.count() # Значение показателя 7.3
    """

    # Словарь Номер показателя -> Путь до фильтра
    # Специфичный для каждого из показателей фильтр
    index_filters = {
        'p1': 'gisdo.queue_index.config_filters.get_1_filter',
        'p4': 'gisdo.queue_index.config_filters.get_4_filter',
        'p4_1': 'gisdo.queue_index.config_filters.get_41_filter',
        'p4_2': 'gisdo.queue_index.config_filters.get_42_filter',
        'p5': 'gisdo.queue_index.config_filters.get_5_filter',
        'p7': 'gisdo.queue_index.config_filters.get_7_filter',
        'p7_1': 'gisdo.queue_index.config_filters.get_71_filter',
        'p7_2': 'gisdo.queue_index.config_filters.get_72_filter',
        'p7_3': 'gisdo.queue_index.config_filters.get_73_filter',
        'p7_4': 'gisdo.queue_index.config_filters.get_74_filter',
        'p7_5': 'gisdo.queue_index.config_filters.get_75_filter',
        'p7_7': 'gisdo.queue_index.config_filters.get_77_filter',
        'p8': 'gisdo.queue_index.config_filters.get_8_filter',
        'p8_1': 'gisdo.queue_index.config_filters.get_81_filter',
        'p8_2': 'gisdo.queue_index.config_filters.get_82_filter',
        'p8_3': 'gisdo.queue_index.config_filters.get_83_filter',
        'p9': 'gisdo.queue_index.config_filters.get_9_filter',
        'p10': 'gisdo.queue_index.config_filters.get_10_filter',
        'p10_1': 'gisdo.queue_index.config_filters.get_101_filter',
        'p11': 'gisdo.queue_index.config_filters.get_11_filter',
        'p12': 'gisdo.queue_index.config_filters.get_12_filter',
        'p12_1': 'gisdo.queue_index.config_filters.get_121_filter',
        'p13': 'gisdo.queue_index.config_filters.get_13_filter',
        'p13_1': 'gisdo.queue_index.config_filters.get_131_filter',
        'p14': 'gisdo.queue_index.config_filters.get_14_filter',
        'p15': 'gisdo.queue_index.config_filters.get_15_filter',
        'p16': 'gisdo.queue_index.config_filters.get_16_filter',
        'p17': 'gisdo.queue_index.config_filters.get_17_filter',
        'p17_1': 'gisdo.queue_index.config_filters.get_171_filter',
        'p18': 'gisdo.queue_index.config_filters.get_18_filter',
        'p18_1': 'gisdo.queue_index.config_filters.get_181_filter',
        'p18_2': 'gisdo.queue_index.config_filters.get_182_filter',
        'p18_3': 'gisdo.queue_index.config_filters.get_183_filter',
        'p18_4': 'gisdo.queue_index.config_filters.get_184_filter',
        'p18_5': 'gisdo.queue_index.config_filters.get_185_filter',
        'p20': 'gisdo.queue_index.config_filters.get_20_filter',
        'p20_1': 'gisdo.queue_index.config_filters.get_201_filter',
        'p20_2': 'gisdo.queue_index.config_filters.get_202_filter',
        'p20_3': 'gisdo.queue_index.config_filters.get_203_filter',
        'p20_4': 'gisdo.queue_index.config_filters.get_204_filter',
        'p20_5': 'gisdo.queue_index.config_filters.get_205_filter',
        'p20_6': 'gisdo.queue_index.config_filters.get_206_filter',
        'p20_7': 'gisdo.queue_index.config_filters.get_207_filter',
        'p20_8': 'gisdo.queue_index.config_filters.get_208_filter',
        'p30': 'gisdo.queue_index.config_filters.get_30_filter',
        'p30_2': 'gisdo.queue_index.config_filters.get_302_filter',
        'p33': 'gisdo.queue_index.config_filters.get_33_filter',
    }

    def __init__(self):
        config = {
            'model': {
                '__default__': {'__type__': 'static'},
                'Declaration': {
                    '__realization__': 'kinder.core.declaration.models.Declaration',
                },
            },
            'queue': {'__default__': {'__realization__': 'kinder.core.queue_api.builder.Builder'}},
        }

        for index, filter_path in self.index_filters.items():
            config['queue'][index] = {
                '$filter': filter_path,
                '$sorting': [],
                '$selectfields': ['id', 'children__date_of_birth', 'desired_date', 'children_id', 'children__fullname'],
                'model': 'Declaration',
            }
        self._container = Container(config)

    def get_builder(self, name):
        """Yadic падает, если имя параметра начинаеся не с буквы
        :param group:
        :param name:
        :return:
        """
        if name != 'Declaration':
            name = 'p{0}'.format(name.replace('.', '_'))
        return self._container.get('queue', name)
