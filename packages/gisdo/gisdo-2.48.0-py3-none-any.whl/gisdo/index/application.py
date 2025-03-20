from sqlalchemy import (
    and_,
)
from sqlalchemy.sql.functions import (
    min,
)

from gisdo.algorithm.application import (
    ApplicationCountByAge,
    ApplicationCountByDelivery,
    ApplicationCountByDenied,
    ApplicationCountByGroupType,
    ApplicationWantChangeDou,
    ApplicationWantChangeDouWithHN,
)
from gisdo.constants import (
    ALL_UNIT_TYPES,
    DOU_TYPE_MAP,
    GOVERNMENT,
)
from gisdo.index.base import (
    BaseIndex,
)


class ApplicationIndex(BaseIndex):
    """
    Запросы группы "Общее количество поданных заявлений"
    """

    COUNT_BY_AGE = 1
    COUNT_BY_DELIVERY = 2
    COUNT_BY_GROUP_TYPE = 3
    COUNT_DENIED = 4
    WANT_CHANGE_DOU = 5
    WANT_CHANGE_DOU_WITH_HN = 6

    ALGORITHM_MAP = {
        COUNT_BY_AGE: ApplicationCountByAge,
        COUNT_BY_DELIVERY: ApplicationCountByDelivery,
        COUNT_BY_GROUP_TYPE: ApplicationCountByGroupType,
        COUNT_DENIED: ApplicationCountByDenied,
        WANT_CHANGE_DOU: ApplicationWantChangeDou,
        WANT_CHANGE_DOU_WITH_HN: ApplicationWantChangeDouWithHN,
    }

    def get_count(self, dou_type=ALL_UNIT_TYPES, index_type=COUNT_BY_AGE, **kwargs):
        """
        Для всех показателей есть общий тип запроса.
        В конкретных показателях навешиваются дополнительные фильтры.
        В зависимости от параметра index_type управление
        пробрасывается конкретной функции для добавления специфичных
        для показателя фильтров.
        """

        # Если необходимо посчитать количество заявлений в
        # негосударственное или частное ДОУ для государственного сада,
        # то сразу возвращаем 0.
        if dou_type != ALL_UNIT_TYPES:
            if (not self.dou_type and dou_type != GOVERNMENT) or (
                self.dou_type and self.dou_type.code not in DOU_TYPE_MAP[dou_type]
            ):
                return 0

        result_set = ApplicationIndex.get_algorithm(index_type)(session=self.session, unit=self.unit).get_result_set(
            **kwargs
        )

        # base - это таблица с тремя столбцами
        # id | unit_id | ord
        # Нам необходимо для каждой заявки отобрать
        # самую приоритетную организацию Unit.
        # SELECT * FROM base
        # JOIN (SELECT id, min(ord) as min_ord FROM base) as T
        # ON T.id = base.id AND T.min_ord = base.ord
        result_set_min_ord = (
            self.session.query(result_set.c.id, min(result_set.c.ord).label('min_ord'))
            .group_by(result_set.c.id)
            .subquery()
        )
        return (
            self.session.query(result_set)
            .join(
                result_set_min_ord,
                and_(result_set.c.id == result_set_min_ord.c.id, result_set.c.ord == result_set_min_ord.c.min_ord),
            )
            .filter(result_set.c.unit_id == self.unit.id)
            .count()
        )
