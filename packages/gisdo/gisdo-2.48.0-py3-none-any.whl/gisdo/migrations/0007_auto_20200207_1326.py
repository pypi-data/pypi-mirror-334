from __future__ import (
    unicode_literals,
)

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    dependencies = [
        ('gisdo', '0006_schedulesettings_attendance_transfer_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gisdounit',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name='Создан'),
        ),
        migrations.AlterField(
            model_name='gisdounit',
            name='modified',
            field=models.DateTimeField(auto_now=True, db_index=True, null=True, verbose_name='Изменен'),
        ),
        migrations.AlterField(
            model_name='reportform',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name='Создан'),
        ),
        migrations.AlterField(
            model_name='reportform',
            name='modified',
            field=models.DateTimeField(auto_now=True, db_index=True, null=True, verbose_name='Изменен'),
        ),
        migrations.AlterField(
            model_name='reportformrow',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name='Создан'),
        ),
        migrations.AlterField(
            model_name='reportformrow',
            name='modified',
            field=models.DateTimeField(auto_now=True, db_index=True, null=True, verbose_name='Изменен'),
        ),
    ]
