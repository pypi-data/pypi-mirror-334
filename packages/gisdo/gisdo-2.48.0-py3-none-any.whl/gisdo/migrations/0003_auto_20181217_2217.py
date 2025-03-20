from __future__ import (
    unicode_literals,
)

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    dependencies = [
        ('gisdo', '0002_auto_20181017_0903'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedulesettings',
            name='server_location',
            field=models.SmallIntegerField(
                choices=[
                    (1, 'На серверах в структуре органов власти субъекта РФ'),
                    (2, 'На серверах организаций, подведомственных органам власти субъекта РФ'),
                    (3, 'На серверах органов местного самоуправления'),
                    (4, 'На серверах коммерческих организаций'),
                ],
                default=1,
                verbose_name='Место расположения серверов',
            ),
        ),
        migrations.AlterField(
            model_name='schedulesettings',
            name='installation_type',
            field=models.SmallIntegerField(
                choices=[(1, 'Региональная'), (2, 'Муниципальная')], null=True, verbose_name='Тип установки'
            ),
        ),
    ]
