from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ChangeDeclaration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (
                    'create',
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name='\u0412\u0440\u0435\u043c\u044f \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f',
                    ),
                ),
                (
                    'data',
                    models.TextField(
                        null=True,
                        verbose_name='\u0421\u043e\u0434\u0435\u0440\u0436\u0438\u043c\u043e\u0435 \u043e\u0431\u044a\u0435\u043a\u0442\u0430',
                    ),
                ),
                (
                    'state',
                    models.SmallIntegerField(
                        default=0,
                        verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0439',
                        choices=[
                            (
                                0,
                                '\u041e\u0436\u0438\u0434\u0430\u0435\u0442 \u0440\u0435\u0448\u0435\u043d\u0438\u044f',
                            ),
                            (1, '\u041e\u0442\u043a\u0430\u0437\u0430\u043d\u043e'),
                            (2, '\u0418\u0441\u043f\u043e\u043b\u043d\u0435\u043d\u043e'),
                        ],
                    ),
                ),
                (
                    'commentary',
                    models.CharField(
                        max_length=250,
                        null=True,
                        verbose_name='\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439',
                        blank=True,
                    ),
                ),
                (
                    'source',
                    models.SmallIntegerField(
                        default=0,
                        null=True,
                        verbose_name='\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0439',
                        blank=True,
                        choices=[
                            (
                                0,
                                '\u041e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435 \u0434\u0430\u043d\u043d\u044b\u0445 \u0437\u0430\u044f\u0432\u043a\u0438',
                            ),
                            (
                                1,
                                '\u0421\u043e\u0437\u0434\u0430\u043d\u0438\u0435 \u043d\u043e\u0432\u043e\u0439 \u0437\u0430\u044f\u0432\u043a\u0438',
                            ),
                        ],
                    ),
                ),
                (
                    'case_number',
                    models.PositiveIntegerField(
                        null=True,
                        verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0437\u0430\u044f\u0432\u043a\u0438',
                        blank=True,
                    ),
                ),
            ],
            options={
                'verbose_name': '\u0421\u043f\u0438\u0441\u043e\u043a \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0439 \u0437\u0430\u044f\u0432\u043a\u0438 \u0441 \u0415\u041f\u0413\u0423',
            },
        ),
        migrations.CreateModel(
            name='DelegatePerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (
                    'doc_type',
                    models.PositiveSmallIntegerField(
                        verbose_name='\u0422\u0438\u043f \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430',
                        choices=[
                            (
                                1,
                                '\u041f\u0430\u0441\u043f\u043e\u0440\u0442 \u0433\u0440\u0430\u0436\u0434\u0430\u043d\u0438\u043d\u0430 \u0421\u0421\u0421\u0420',
                            ),
                            (
                                2,
                                '\u0417\u0430\u0433\u0440\u0430\u043d\u043f\u0430\u0441\u043f\u043e\u0440\u0442 \u0433\u0440\u0430\u0436\u0434\u0430\u043d\u0438\u043d\u0430 \u0421\u0421\u0421\u0420',
                            ),
                            (
                                4,
                                '\u0423\u0434\u043e\u0441\u0442\u043e\u0432\u0435\u0440\u0435\u043d\u0438\u0435 \u043b\u0438\u0447\u043d\u043e\u0441\u0442\u0438',
                            ),
                            (
                                5,
                                '\u0421\u043f\u0440\u0430\u0432\u043a\u0430 \u043e\u0431 \u043e\u0441\u0432\u043e\u0431\u043e\u0436\u0434\u0435\u043d\u0438\u0435',
                            ),
                            (
                                6,
                                '\u041f\u0430\u0441\u043f\u043e\u0440\u0442 \u041c\u0438\u043d\u043c\u043e\u0440\u0444\u043b\u043e\u0442\u0430',
                            ),
                            (7, '\u0412\u043e\u0435\u043d\u043d\u044b\u0439 \u0431\u0438\u043b\u0435\u0442'),
                            (
                                9,
                                '\u0414\u0438\u043f\u043b\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u043f\u0430\u0441\u043f\u043e\u0440\u0442 \u0433\u0440\u0430\u0436\u0434\u0430\u043d\u0438\u043d\u0430 \u0420\u0424',
                            ),
                            (
                                10,
                                '\u0418\u043d\u043e\u0441\u0442\u0440\u0430\u043d\u043d\u044b\u0439 \u043f\u0430\u0441\u043f\u043e\u0440\u0442',
                            ),
                            (
                                11,
                                '\u0421\u0432\u0438\u0434\u0435\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u043e \u043e \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438 \u0445\u043e\u0434\u0430\u0442\u0430\u0439\u0441\u0442\u0432\u0430 \u0438\u043c\u043c\u0438\u0433\u0440\u0430\u043d\u0442\u0430 \u043e \u043f\u0440\u0438\u0437\u043d\u0430\u043d\u0438\u0438 \u0435\u0433\u043e \u0431\u0435\u0436\u0435\u043d\u0446\u043e\u043c',
                            ),
                            (
                                12,
                                '\u0412\u0438\u0434 \u043d\u0430 \u0436\u0438\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u043e',
                            ),
                            (
                                13,
                                '\u0423\u0434\u043e\u0441\u0442\u043e\u0432\u0435\u0440\u0435\u043d\u0438\u0435 \u0431\u0435\u0436\u0435\u043d\u0446\u0430',
                            ),
                            (
                                14,
                                '\u0412\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0435 \u0443\u0434\u043e\u0441\u0442\u043e\u0432\u0435\u0440\u0435\u043d\u0438\u0435 \u043b\u0438\u0447\u043d\u043e\u0441\u0442\u0438 \u0433\u0440\u0430\u0436\u0434\u0430\u043d\u0438\u043d\u0430 \u0420\u0424',
                            ),
                            (
                                21,
                                '\u041f\u0430\u0441\u043f\u043e\u0440\u0442 \u0433\u0440\u0430\u0436\u0434\u0430\u043d\u0438\u043d\u0430 \u0420\u0424',
                            ),
                            (
                                22,
                                '\u0417\u0430\u0433\u0440\u0430\u043d\u043f\u0430\u0441\u043f\u043e\u0440\u0442 \u0433\u0440\u0430\u0436\u0434\u0430\u043d\u0438\u043d\u0430 \u0420\u0424',
                            ),
                            (26, '\u041f\u0430\u0441\u043f\u043e\u0440\u0442 \u043c\u043e\u0440\u044f\u043a\u0430'),
                            (
                                27,
                                '\u0412\u043e\u0435\u043d\u043d\u044b\u0439 \u0431\u0438\u043b\u0435\u0442 \u043e\u0444\u0438\u0446\u0435\u0440\u0430 \u0437\u0430\u043f\u0430\u0441\u0430',
                            ),
                        ],
                    ),
                ),
            ],
            options={
                'verbose_name': '\u0420\u0430\u0441\u0448\u0438\u0440\u0435\u043d\u0438\u0435 \u043c\u043e\u0434\u0435\u043b\u0438 \u041f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u0438\u0442\u0435\u043b\u044f',
            },
        ),
        migrations.CreateModel(
            name='DocExtraInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=350, verbose_name='\u041a\u043e\u0434')),
                ('name', models.CharField(max_length=350, null=True, verbose_name='\u0418\u043c\u044f', blank=True)),
                (
                    'description',
                    models.CharField(
                        max_length=350,
                        null=True,
                        verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435',
                        blank=True,
                    ),
                ),
            ],
            options={
                'verbose_name': '\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u0430\u044f \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043e \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430\u0445',
            },
        ),
        migrations.CreateModel(
            name='UpdateParams',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (
                    'model_name',
                    models.CharField(
                        max_length=250,
                        verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u043c\u043e\u0434\u0435\u043b\u0438',
                    ),
                ),
                (
                    'field_name',
                    models.CharField(
                        max_length=250,
                        verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u043f\u043e\u043b\u044f',
                    ),
                ),
            ],
            options={
                'verbose_name': '\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u0434\u043b\u044f \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f \u0434\u0430\u043d\u043d\u044b\u0445',
            },
        ),
        migrations.AlterUniqueTogether(
            name='updateparams',
            unique_together=set([('model_name', 'field_name')]),
        ),
    ]
