import datetime

from django.conf import (
    settings,
)
from sqlalchemy import (
    and_,
    or_,
)
from sqlalchemy.orm import (
    load_only,
)

from kinder.core.declaration_status.models import (
    DSS,
)

from gisdo.alchemy_models import (
    AlchemyChildren,
    AlchemyDeclaration,
    AlchemyDeclarationStatus,
    AlchemyWorkType,
)
from gisdo.algorithm.base import (
    BaseApplicationAlgorithm,
)
from gisdo.algorithm.constants import (
    get_short_day_types,
)


class ApplicationCountByAge(BaseApplicationAlgorithm):
    def get_result_set(self, **kwargs):
        """Количество заявлений по возрастам"""

        return self._get_base_query(**kwargs)


class ApplicationCountByDelivery(BaseApplicationAlgorithm):
    def _get_base_query(self, **kwargs):
        # Фильтрация по отчетному периоду.
        begin_report_period, end_report_period = self.get_report_period()

        _base_query = (
            self.session.query(AlchemyDeclaration, 'ord', 'unit_id')
            .filter(
                AlchemyDeclaration.date >= begin_report_period,
                AlchemyDeclaration.date <= datetime.datetime.combine(end_report_period, datetime.datetime.max.time()),
            )
            .join(self._dou_units())
            .join(self._kids(**kwargs))
            .options(load_only('portal', 'status_id', 'work_type_id', 'id', 'children_id', 'defer_demand'))
            .subquery()
        )

        return _base_query

    def get_result_set(self, **kwargs):
        """По типу подачи: с портала или при личном обращении"""

        portal = kwargs.get('portal', 0)
        base = self._get_base_query(**kwargs)

        base_query = (
            self.session.query(base)
            .join(AlchemyDeclarationStatus)
            .filter(base.c.portal == portal, AlchemyDeclarationStatus.code != DSS.NOT_ATTENDED)
        )

        # Для Тюмени не выполняет фильтрацию по чек-боксу "Отложенный запрос".
        if settings.PARTNER_QUIRKS != 'TUMEN':
            base_query = base_query.filter(base.c.defer_demand == False)

        return base_query.subquery()


class ApplicationCountByGroupType(BaseApplicationAlgorithm):
    def get_result_set(self, **kwargs):
        """Группы кратковременного пребывания"""
        base = self._get_base_query(**kwargs)
        return (
            self.session.query(base)
            .join(AlchemyWorkType)
            .join(AlchemyDeclarationStatus)
            .filter(
                and_(AlchemyWorkType.code.in_(get_short_day_types()), AlchemyDeclarationStatus.code != DSS.NOT_ATTENDED)
            )
            .subquery()
        )


class ApplicationCountByDenied(BaseApplicationAlgorithm):
    def get_result_set(self, **kwargs):
        """Количество отказов"""

        base = self._get_base_query(**kwargs)
        return (
            self.session.query(base)
            .join(AlchemyDeclarationStatus)
            .filter(or_(AlchemyDeclarationStatus.code == DSS.DIDNT_COME, AlchemyDeclarationStatus.code == DSS.REFUSED))
            .subquery()
        )


class ApplicationWantChangeDou(BaseApplicationAlgorithm):
    @staticmethod
    def get_report_period():
        down_border = datetime.datetime.combine(datetime.date.min, datetime.datetime.min.time())
        up_border = datetime.datetime.combine(datetime.date.max, datetime.datetime.max.time())

        return down_border, up_border

    def get_result_set(self, **kwargs):
        """В статусе желает изменить ДОУ"""

        base = self._get_base_query(**kwargs)
        return (
            self.session.query(base)
            .join(AlchemyDeclarationStatus)
            .filter(AlchemyDeclarationStatus.code == DSS.WANT_CHANGE_DOU)
            .subquery()
        )


class ApplicationWantChangeDouWithHN(ApplicationWantChangeDou):
    def get_result_set(self, **kwargs):
        """В статусе желает изменить ДОУ и потребностью по здоровью"""

        base = super(ApplicationWantChangeDouWithHN, self).get_result_set(**kwargs)
        return (
            self.session.query(base)
            .join(AlchemyChildren, AlchemyChildren.id == base.c.children_id)
            .filter(AlchemyChildren.health_need_id != None)
            .subquery()
        )
