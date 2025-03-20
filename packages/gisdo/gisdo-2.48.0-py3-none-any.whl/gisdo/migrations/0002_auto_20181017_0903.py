from __future__ import (
    unicode_literals,
)

import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    dependencies = [
        ('gisdo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reportformrow',
            options={'verbose_name': 'Показатель по организации', 'verbose_name_plural': 'Показатели по организации'},
        ),
        migrations.AlterModelOptions(
            name='schedulesettings',
            options={'verbose_name': 'Фед. отчетность - настройки'},
        ),
        migrations.AlterField(
            model_name='gisdounit',
            name='unit',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, related_name='gisdo', to='unit.Unit'
            ),
        ),
        migrations.AlterField(
            model_name='reportform',
            name='unit',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to='unit.Unit', verbose_name='Организация'
            ),
        ),
        migrations.AlterField(
            model_name='reportformrow',
            name='unit',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='unit.Unit', verbose_name='Организация'
            ),
        ),
    ]
