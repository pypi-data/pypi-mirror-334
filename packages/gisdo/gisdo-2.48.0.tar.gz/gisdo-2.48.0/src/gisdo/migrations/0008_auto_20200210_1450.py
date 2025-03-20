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
        ('gisdo', '0007_auto_20200207_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gisdounit',
            name='unit',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='gisdo',
                to='unit.Unit',
                verbose_name='Организация',
            ),
        ),
    ]
