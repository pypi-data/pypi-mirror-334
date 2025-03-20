from __future__ import (
    absolute_import,
    division,
)

import datetime
import json

from django.core.serializers.json import (
    DjangoJSONEncoder,
)
from django.db import (
    models,
)
from django.db.models.signals import (
    pre_delete,
)
from django.dispatch import (
    receiver,
)
from django_celery_beat.models import (
    CrontabSchedule,
    PeriodicTask,
)
from future.builtins import (
    object,
    str,
)
from past.utils import (
    old_div,
)

from m3.actions import (
    ApplicationLogicException,
)
from m3.db import (
    BaseEnumerate,
)

from kinder.core.audit_log_kndg.managers import (
    AuditLog,
)
from kinder.core.models import (
    BaseReplicatedModel,
    DateAwareModel,
    ModificationDateAwareModel,
)
from kinder.core.unit.models import (
    Unit,
    UnitKind,
)

from . import (
    settings as gs_settings,
)
from .constants import (
    AGE_CATEGORIES_CUT,
    AGE_CATEGORIES_CUT_LIST,
    AGE_CATEGORIES_FULL,
    AGE_CATEGORIES_FULL_CURRENT,
    AGE_CATEGORIES_FULL_LIST,
    AGE_CATEGORIES_FULL_MAP,
    APPLICATION_STATUSES,
    BENEFIT_TYPES,
    DELIVERY_TYPES,
    DOO_TYPES,
    GROUP_TYPES,
    HEALTH_NEEDS,
    NO,
)
from .utils import (
    ViewList,
)


@receiver(pre_delete, sender=Unit)
def delete_unit(instance, **kwargs):
    GisdoUnit.objects.filter(unit=instance).delete()


class InstallationType(BaseEnumerate):
    REGIONAL = 1
    MUNICIPAL = 2

    values = {REGIONAL: 'Региональная', MUNICIPAL: 'Муниципальная'}


class ServerLocType(BaseEnumerate):
    STRUCT = 1
    SUB = 2
    MUN = 3
    COMM = 4

    values = {
        STRUCT: 'На серверах в структуре органов власти субъекта РФ',
        SUB: 'На серверах организаций, подведомственных органам власти субъекта РФ',
        MUN: 'На серверах органов местного самоуправления',
        COMM: 'На серверах коммерческих организаций',
    }


class AttendanceTransferType(BaseEnumerate):
    """
    Способы передачи посещаемости
    """

    ATTENDANCE_SHEET = 1
    CHILD_DAYS = 2

    values = {ATTENDANCE_SHEET: 'По табелю', CHILD_DAYS: 'По полю "Количество дето-дней"'}


class GisdoUnit(BaseReplicatedModel):
    """
    Модель, для расширения организаций
    """

    unit = models.OneToOneField(Unit, verbose_name='Организация', related_name='gisdo', on_delete=models.CASCADE)
    not_on_federal_report = models.BooleanField(verbose_name='Не отправлять фед.отчетность', default=False)
    doo_identity = models.CharField(max_length=20, verbose_name='Идентификатор ДОО для шины', null=True)
    related_to_mo = models.ForeignKey(Unit, verbose_name='Относится к МО', null=True, on_delete=models.SET_NULL)

    audit_log = AuditLog(['modified'])

    # идентификатор ДОО
    def create_doo_identity(self):
        """композитный идентификатор ДОО, заполняется следующим образом:
        xxyyyyyyyyyyyyzzzz,
        xx - код региона (2 знака) из настроек проекта
        yyyyyyyyyyyy - цифры кода ОКТМО (11 знаков)
        zzzz - номер ДОО (поле doo_number)
        """
        octmo_max_length = 11
        doo_number_max_length = 4
        region_max_length = 2

        if self.unit.kind.id != UnitKind.DOU:
            return
        if not gs_settings.REGION_CODE:
            raise ApplicationLogicException('Не задан код региона')
        if len(str(gs_settings.REGION_CODE)) > region_max_length:
            raise ApplicationLogicException('Длина кода региона превышает максимальное значение')

        identity = str(gs_settings.REGION_CODE).rjust(region_max_length, '0')

        oktmo_unit = self.unit.get_parent_by_kind('mo') or self.unit.get_parent_by_kind('region')

        if oktmo_unit is None:
            raise ApplicationLogicException('У ДОО не найден родительский МО/Регион.')
        elif not oktmo_unit.octmo:
            raise ApplicationLogicException(
                'В родительском МО/Регионе "{}" не задан код ОКТМО.'.format(oktmo_unit.display())
            )
        else:
            identity += oktmo_unit.octmo.rjust(octmo_max_length, '0')

        identity += str(self.unit.doo_number).rjust(doo_number_max_length, '0')

        # Так сделано потому, что теперь не изменяем идентификатор,
        # если он начинается с тринадцати нулей.
        if not identity.startswith('0' * (region_max_length + octmo_max_length)):
            self.doo_identity = identity

    class Meta:
        verbose_name = 'Поля организации для ФО'


class ReportForm(BaseReplicatedModel):
    """
    Форма отчетности "Федеральная отчетность"
    """

    date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    sent_time = models.DateTimeField(verbose_name='Время отправки', null=True)
    user = models.ForeignKey('users.UserProfile', verbose_name='Пользователь', null=True, on_delete=models.SET_NULL)
    unit = models.ForeignKey('unit.Unit', verbose_name='Организация', null=True, on_delete=models.SET_NULL)
    xml = models.TextField(verbose_name='Сформированная XML', null=True)
    in_progress = models.BooleanField(default=False, verbose_name='Сбор отчета')

    class Meta:
        verbose_name = "Форма 'Федеральная отчетность'"
        verbose_name_plural = "Формы 'Федеральная отчетность'"

    def __unicode__(self):
        return '%s от %s' % (self._meta.verbose_name, self.date)

    @property
    def presentation(self):
        date = self.date.strftime('%d.%m.%Y')

        return '{date}, {unit}'.format(date=date, unit=self.unit)

    @property
    def progress(self):
        return 'В процессе сборки' if self.in_progress else 'Собран'

    @property
    def sent(self):
        return 'Отправлен' if self.sent_time else 'Не отправлен'


class ReportFormRow(BaseReplicatedModel):
    """
    Строка отчета для конкретной организации
    """

    report = models.ForeignKey(ReportForm, verbose_name='Форма отчетности', on_delete=models.CASCADE)
    unit = models.ForeignKey('unit.Unit', verbose_name='Организация', on_delete=models.CASCADE)

    applications = models.TextField(verbose_name='Информация по заявлениям', null=True)
    queues = models.TextField(verbose_name='Информация по очередям', null=True)
    enrolled = models.TextField(verbose_name='Информация о зачисленных детях', null=True)
    capacities = models.TextField(verbose_name='Информация о свободных местах', null=True)

    class Meta(object):
        verbose_name = 'Показатель по организации'
        verbose_name_plural = 'Показатели по организации'

    def __unicode__(self):
        return '%s %s на %s' % (self._meta.verbose_name, self.unit.display(), self.report.date if self.report else '-')


class GroupData(DateAwareModel):
    """
    Данные групп для передачи в отчёте
    """

    report = models.ForeignKey(ReportForm, verbose_name='Форма отчетности', on_delete=models.CASCADE)

    unit = models.ForeignKey('unit.Unit', verbose_name='Организация', on_delete=models.CASCADE)

    data = models.JSONField(verbose_name='Данные группы', encoder=DjangoJSONEncoder)

    class Meta:
        verbose_name = 'Данные групп для передачи в отчёте'


class ScheduleSettings(models.Model):
    """
    Модель настроек celery beat
    """

    PK = 1
    push_login = models.CharField('Логин для отправки', max_length=30, null=True)
    push_password = models.CharField('Пароль для отправки', max_length=30, null=True)

    time = models.TimeField(verbose_name='Время начала', null=True)
    is_active = models.BooleanField(verbose_name='Включение автоматического сбора', default=False)
    resend_count = models.PositiveSmallIntegerField(verbose_name='Количество повторных отправок при неудаче', default=3)
    resend_after_time = models.PositiveSmallIntegerField(
        verbose_name='Запускать автоматическую отправку после неудачной попытки через', default=0
    )  # число минут
    attendance_transfer_type = models.SmallIntegerField(
        'Способ передачи посещаемости',
        choices=AttendanceTransferType.get_choices(),
        default=AttendanceTransferType.ATTENDANCE_SHEET,
    )
    zip_xml = models.BooleanField(verbose_name='Кодировать данные при отправке в ZIP', default=False)
    async_send = models.BooleanField(verbose_name='Асинхронная отправка отчета', default=False)
    system_name = models.CharField('Наименование системы', max_length=250, null=True)
    email = models.EmailField('E-mail контактного лица', max_length=30, null=True)
    installation_type = models.SmallIntegerField('Тип установки', choices=InstallationType.get_choices(), null=True)
    server_location = models.SmallIntegerField(
        'Место расположения серверов', choices=ServerLocType.get_choices(), default=ServerLocType.STRUCT
    )

    audit_log = AuditLog()

    class Meta(object):
        verbose_name = 'Фед. отчетность - настройки'

    def save(self, force_insert=False, force_update=False, using=None):
        self.pk = self.PK
        super(ScheduleSettings, self).save(force_update, force_update, using)

    @staticmethod
    def get_settings():
        ss, created = ScheduleSettings.objects.get_or_create(
            id=ScheduleSettings.PK, defaults={'id': ScheduleSettings.PK}
        )
        return ss

    @classmethod
    def get_interval_and_count_retries(cls):
        settings = cls.get_settings()

        interval = settings.resend_after_time
        now = datetime.datetime.now()
        tomorrow = datetime.datetime(now.year, now.month, now.day, 0, 0, 0) + datetime.timedelta(days=1)
        # вычисляем сколько раз имеет смысл совершить
        # повторных попыток до конца сегодняшнего дня
        if interval:
            max_count_retries_before_tomorrow = old_div((tomorrow - now).seconds, (60 * interval))
        else:
            # если interval = 0 (значение "Нет" на форме), то сохраняем
            # старую реализацию, то есть не переотправляем
            max_count_retries_before_tomorrow = 0

        return interval, max_count_retries_before_tomorrow


class TaskScheduler(models.Model):
    """
    Планировщик для сбора данных
    """

    periodic_task = models.ForeignKey(PeriodicTask, on_delete=models.CASCADE)

    @staticmethod
    def schedule_every(task_name, hour, minute, args='[]', kwargs='{}'):
        """
        schedules a task by name
        """
        ptask_name = '%s_%s' % (task_name, datetime.datetime.now())
        crontab_schedules = CrontabSchedule.objects.filter(
            hour=hour, minute=minute, day_of_week='*', day_of_month='*', month_of_year='*'
        )
        crontab_schedule = (
            crontab_schedules[0]
            if crontab_schedules.exists()
            else CrontabSchedule.objects.create(hour=hour, minute=minute)
        )
        ptask = PeriodicTask.objects.create(
            name=ptask_name,
            task=task_name,
            crontab=crontab_schedule,
            args=args,
            kwargs=kwargs,
            queue=gs_settings.CELERY_WORKER_TASK_QUEUE,
        )
        return TaskScheduler.objects.create(periodic_task=ptask)

    def stop(self):
        self.periodic_task.enabled = False
        self.periodic_task.save()

    def start(self):
        self.periodic_task.enabled = True
        self.periodic_task.save()

    def terminate(self):
        self.stop()
        self.delete()
        self.periodic_task.delete()

    class Meta:
        verbose_name = 'Планировщик для сбора данных'


class MOErrorResponse(ModificationDateAwareModel):
    """Модель для хранения ошибок, которые вернулись при отправке"""

    mo = models.OneToOneField(Unit, verbose_name='МО', on_delete=models.CASCADE)

    error = models.CharField(verbose_name='Ошибка, которая пришла в ответе на запрос', max_length=255, null=True)

    class Meta:
        verbose_name = 'Ошибка, при отправке ФО'
        verbose_name_plural = 'Ошибки, при отправке ФО'
