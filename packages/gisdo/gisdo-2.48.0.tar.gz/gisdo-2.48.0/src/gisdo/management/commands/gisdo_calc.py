import datetime

from django.core.management.base import (
    BaseCommand,
)

from kinder.core.children.models import (
    Children,
)
from kinder.core.unit.models import (
    Unit,
)

from gisdo.counter.filters import *
from gisdo.counter.provider import (
    DataProvider,
)
from gisdo.index.queue import (
    get_queue_index_collection,
)
from gisdo.queue_index.queue_conf import (
    GisdoContainer,
)
from gisdo.utils import (
    UnitHelper,
)


class Command(BaseCommand):
    """
    Вспомогательная команда, выведет список детей попадающих
    в показатель по старому и новому расчёту

    # TODO: После завершения разработки нового метода подсчёта можно удалить
    """

    # Сюда добавлять новые реализованные фильтры
    filters = {
        '1': filter_1,
        '1.1': filter_1,
        '2.1': filter_2,
        '3.1': filter_3,
        '4': filter_4,
        '4.1': filter_4_1,
        '4.2': filter_4_2,
        '5': filter_5,
        '6': filter_6,
        '7': filter_7,
        '7.2': filter_7_2,
        '7.3': filter_7_3,
        '7.4': filter_7_4,
        '7.5': filter_7_5,
        '7.7': filter_7_7,
        '9': filter_9,
        '10': filter_10,
        '10.1': filter_10_1,
        '11': filter_11,
    }

    def add_arguments(self, parser):
        parser.add_argument('mo', type=int, help='МО')
        parser.add_argument('index', help='Показатель')
        parser.add_argument('only', nargs='*', type=int, help='Считать только для указанных ДОО')

        date_format = '%Y-%m-%d'

        parser.add_argument(
            '--date',
            type=lambda s: datetime.strptime(s, date_format),
            required=False,
            default=datetime.datetime.today(),
            help='Дата на которую расчитывать показатель',
        )

    def handle(self, *a, **kw):
        mo_id = kw['mo']
        index = kw['index']
        only_units = set(kw['only'])
        date = kw['date']

        filter_fn = self.filters.get(index)

        mo = Unit.objects.get(pk=mo_id)
        unit_helper = UnitHelper(mo)
        units = unit_helper.get_mo_units(mo.id)

        has_old = 'p{0}'.format(index.replace('.', '_')) in GisdoContainer.index_filters

        for dou in units:
            if only_units and dou.id not in only_units:
                continue

            if has_old:
                # Старый подсчёт через GisdoContainer
                decls = get_queue_index_collection(index, dou, on_date=date)
                cnt = len(decls)
                print('-' * 10, f'[OLD] ID={dou.id}', dou.name, f'({cnt})', '-' * 10)
                for decl in decls.order_by('children_id'):
                    print(decl['children_id'], decl['children__fullname'])

            if filter_fn is not None:
                # Новый подсчёт
                provider = DataProvider(dou)
                decls = provider.get_rows()
                filtered_list = {}
                for child_row in decls:
                    n = filter_fn(child_row)
                    if n > 0:
                        filtered_list[child_row.id] = n
                cnt = sum(filtered_list.values())
                print('-' * 10, f'[NEW] ID={dou.id}', dou.name, f'({cnt})', '-' * 10)
                for child in Children.objects.filter(id__in=filtered_list.keys()).order_by('id'):
                    print(child.id, child.fullname, filtered_list[child.id])
