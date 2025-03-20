from __future__ import (
    unicode_literals,
)

from django.db import (
    migrations,
)


class Migration(migrations.Migration):
    dependencies = [
        ('gisdo', '0003_auto_20181217_2217'),
    ]

    operations = [migrations.RunSQL('DROP TABLE IF EXISTS public.group_work_days_groupworkdays')]
