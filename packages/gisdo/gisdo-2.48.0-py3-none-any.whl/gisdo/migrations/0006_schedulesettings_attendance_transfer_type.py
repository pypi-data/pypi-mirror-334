from __future__ import (
    unicode_literals,
)

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    dependencies = [
        ('gisdo', '0005_gisdounit_related_to_mo'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedulesettings',
            name='attendance_transfer_type',
            field=models.SmallIntegerField(
                choices=[(1, 'По табелю'), (2, 'По полю "Количество дето-дней"')],
                default=1,
                verbose_name='Способ передачи посещаемости',
            ),
        ),
    ]
