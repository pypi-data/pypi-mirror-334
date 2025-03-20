from __future__ import (
    unicode_literals,
)

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    dependencies = [
        ('unit', '0001_initial'),
        ('users', '0002_notifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='GisdoUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(db_index=True, max_length=32, null=True, blank=True)),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(db_index=True, auto_now=True, null=True)),
                (
                    'unit',
                    models.OneToOneField(
                        parent_link=True, related_name='gisdo', to='unit.Unit', on_delete=models.CASCADE
                    ),
                ),
                (
                    'not_on_federal_report',
                    models.BooleanField(
                        default=False,
                        verbose_name='\u041d\u0435 \u043e\u0442\u043f\u0440\u0430\u0432\u043b\u044f\u0442\u044c \u0444\u0435\u0434.\u043e\u0442\u0447\u0435\u0442\u043d\u043e\u0441\u0442\u044c',
                    ),
                ),
                (
                    'doo_identity',
                    models.CharField(
                        max_length=20,
                        null=True,
                        verbose_name='\u0418\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 \u0414\u041e\u041e \u0434\u043b\u044f \u0448\u0438\u043d\u044b',
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReportForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(db_index=True, max_length=32, null=True, blank=True)),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(db_index=True, auto_now=True, null=True)),
                (
                    'date',
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f',
                    ),
                ),
                (
                    'sent_time',
                    models.DateTimeField(
                        null=True,
                        verbose_name='\u0412\u0440\u0435\u043c\u044f \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438',
                    ),
                ),
                (
                    'xml',
                    models.TextField(
                        null=True,
                        verbose_name='\u0421\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0430\u044f XML',
                    ),
                ),
                (
                    'in_progress',
                    models.BooleanField(
                        default=False, verbose_name='\u0421\u0431\u043e\u0440 \u043e\u0442\u0447\u0435\u0442\u0430'
                    ),
                ),
                (
                    'unit',
                    models.ForeignKey(
                        verbose_name='\u0423\u0447\u0440\u0435\u0436\u0434\u0435\u043d\u0438\u0435',
                        to='unit.Unit',
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c',
                        to='users.UserProfile',
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                'verbose_name': "\u0424\u043e\u0440\u043c\u0430 '\u0424\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u0442\u0447\u0435\u0442\u043d\u043e\u0441\u0442\u044c'",
                'verbose_name_plural': "\u0424\u043e\u0440\u043c\u044b '\u0424\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u0442\u0447\u0435\u0442\u043d\u043e\u0441\u0442\u044c'",
            },
        ),
        migrations.CreateModel(
            name='ReportFormRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(db_index=True, max_length=32, null=True, blank=True)),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(db_index=True, auto_now=True, null=True)),
                (
                    'applications',
                    models.TextField(
                        null=True,
                        verbose_name='\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043f\u043e \u0437\u0430\u044f\u0432\u043b\u0435\u043d\u0438\u044f\u043c',
                    ),
                ),
                (
                    'queues',
                    models.TextField(
                        null=True,
                        verbose_name='\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043f\u043e \u043e\u0447\u0435\u0440\u0435\u0434\u044f\u043c',
                    ),
                ),
                (
                    'enrolled',
                    models.TextField(
                        null=True,
                        verbose_name='\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043e \u0437\u0430\u0447\u0438\u0441\u043b\u0435\u043d\u043d\u044b\u0445 \u0434\u0435\u0442\u044f\u0445',
                    ),
                ),
                (
                    'capacities',
                    models.TextField(
                        null=True,
                        verbose_name='\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043e \u0441\u0432\u043e\u0431\u043e\u0434\u043d\u044b\u0445 \u043c\u0435\u0441\u0442\u0430\u0445',
                    ),
                ),
                (
                    'report',
                    models.ForeignKey(
                        verbose_name='\u0424\u043e\u0440\u043c\u0430 \u043e\u0442\u0447\u0435\u0442\u043d\u043e\u0441\u0442\u0438',
                        to='gisdo.ReportForm',
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    'unit',
                    models.ForeignKey(
                        verbose_name='\u0423\u0447\u0440\u0435\u0436\u0434\u0435\u043d\u0438\u0435',
                        to='unit.Unit',
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                'verbose_name': '\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043f\u043e \u0443\u0447\u0440\u0435\u0436\u0434\u0435\u043d\u0438\u044e',
                'verbose_name_plural': '\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0438 \u043f\u043e \u0443\u0447\u0440\u0435\u0436\u0434\u0435\u043d\u0438\u044e',
            },
        ),
        migrations.CreateModel(
            name='ScheduleSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (
                    'push_login',
                    models.CharField(
                        max_length=30,
                        null=True,
                        verbose_name='\u041b\u043e\u0433\u0438\u043d \u0434\u043b\u044f \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438',
                    ),
                ),
                (
                    'push_password',
                    models.CharField(
                        max_length=30,
                        null=True,
                        verbose_name='\u041f\u0430\u0440\u043e\u043b\u044c \u0434\u043b\u044f \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438',
                    ),
                ),
                (
                    'time',
                    models.TimeField(
                        null=True, verbose_name='\u0412\u0440\u0435\u043c\u044f \u043d\u0430\u0447\u0430\u043b\u0430'
                    ),
                ),
                (
                    'is_active',
                    models.BooleanField(
                        default=False,
                        verbose_name='\u0412\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435 \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e \u0441\u0431\u043e\u0440\u0430',
                    ),
                ),
                (
                    'resend_count',
                    models.PositiveSmallIntegerField(
                        default=3,
                        verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u043e\u0432\u0442\u043e\u0440\u043d\u044b\u0445 \u043e\u0442\u043f\u0440\u0430\u0432\u043e\u043a \u043f\u0440\u0438 \u043d\u0435\u0443\u0434\u0430\u0447\u0435',
                    ),
                ),
                (
                    'resend_after_time',
                    models.PositiveSmallIntegerField(
                        default=0,
                        verbose_name='\u0417\u0430\u043f\u0443\u0441\u043a\u0430\u0442\u044c \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0443\u044e \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0443 \u043f\u043e\u0441\u043b\u0435 \u043d\u0435\u0443\u0434\u0430\u0447\u043d\u043e\u0439 \u043f\u043e\u043f\u044b\u0442\u043a\u0438 \u0447\u0435\u0440\u0435\u0437',
                    ),
                ),
                (
                    'zip_xml',
                    models.BooleanField(
                        default=False,
                        verbose_name='\u041a\u043e\u0434\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0434\u0430\u043d\u043d\u044b\u0435 \u043f\u0440\u0438 \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0435 \u0432 ZIP',
                    ),
                ),
                (
                    'async_send',
                    models.BooleanField(
                        default=False,
                        verbose_name='\u0410\u0441\u0438\u043d\u0445\u0440\u043e\u043d\u043d\u0430\u044f \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0430 \u043e\u0442\u0447\u0435\u0442\u0430',
                    ),
                ),
                (
                    'system_name',
                    models.CharField(
                        max_length=250,
                        null=True,
                        verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0441\u0438\u0441\u0442\u0435\u043c\u044b',
                    ),
                ),
                (
                    'email',
                    models.EmailField(
                        max_length=30,
                        null=True,
                        verbose_name='E-mail \u043a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u043e\u0433\u043e \u043b\u0438\u0446\u0430',
                    ),
                ),
                (
                    'installation_type',
                    models.SmallIntegerField(
                        null=True,
                        choices=[
                            (1, '\u0420\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u0430\u044f'),
                            (2, '\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u0430\u044f'),
                        ],
                    ),
                ),
            ],
        ),
    ]
