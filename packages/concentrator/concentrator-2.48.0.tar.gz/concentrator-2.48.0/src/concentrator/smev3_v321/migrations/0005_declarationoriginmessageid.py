import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    dependencies = [
        ('declaration', '0026_declaration_consent_full_time_group'),
        ('smev3_v321', '0004_load_classifiers_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeclarationOriginMessageID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'message_id',
                    models.CharField(
                        db_index=True, max_length=100, null=True, verbose_name='Уникальный идентификатор сообщения'
                    ),
                ),
                (
                    'declaration',
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='declaration.Declaration'),
                ),
            ],
        ),
    ]
