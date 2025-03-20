"""Модуль содержит определение таблиц SQLA."""

from sqlalchemy.ext.declarative import (
    declarative_base,
)
from sqlalchemy.schema import (
    Table,
)

from gisdo.settings import (
    engine,
)


Base = declarative_base()


class AlchemyDeclaration(Base):
    """Заявления."""

    __table__ = Table('declaration', Base.metadata, autoload=True, autoload_with=engine)


class AlchemyDeclarationUnit(Base):
    """Желаемые организации."""

    __table__ = Table('declaration_unit', Base.metadata, autoload=True, autoload_with=engine)


class AlchemyUnit(Base):
    """Учреждения."""

    __table__ = Table('unit', Base.metadata, autoload=True, autoload_with=engine)


class AlchemyChildren(Base):
    """Дети."""

    __table__ = Table('children', Base.metadata, autoload=True, autoload_with=engine)


class AlchemyWorkType(Base):
    """Режимы работы."""

    __table__ = Table('work_type', Base.metadata, autoload=True, autoload_with=engine)


class AlchemyDeclarationStatus(Base):
    """Статус заявления."""

    __table__ = Table('declaration_status', Base.metadata, autoload=True, autoload_with=engine)


class AlchemyGroup(Base):
    """Группы."""

    __table__ = Table('group', Base.metadata, autoload=True, autoload_with=engine)


class AlchemyPupil(Base):
    """Ученики."""

    __table__ = Table('pupil', Base.metadata, autoload=True, autoload_with=engine)


class AlchemyGroupType(Base):
    """Типы групп."""

    __table__ = Table('group_type', Base.metadata, autoload=True, autoload_with=engine)


class AlchemyGroupWorkType(Base):
    """Режимы работы групп."""

    __table__ = Table('work_type', Base.metadata, autoload=True, autoload_with=engine)
