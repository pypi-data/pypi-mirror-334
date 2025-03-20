import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    dependencies = [
        ('unit', '0024_remove_unit_days_for_confirm_proposed_doo'),
        ('gisdo', '0008_auto_20200210_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='MOErrorResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified', models.DateTimeField(auto_now=True, db_index=True, null=True, verbose_name='Изменен')),
                (
                    'error',
                    models.CharField(
                        max_length=255, null=True, verbose_name='Ошибка, которая пришла в ответе на запрос'
                    ),
                ),
                (
                    'mo',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to='unit.Unit', verbose_name='МО'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Ошибка, при отправке ФО',
                'verbose_name_plural': 'Ошибки, при отправке ФО',
            },
        ),
    ]
