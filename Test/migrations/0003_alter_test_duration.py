# Generated by Django 3.2.4 on 2021-07-21 09:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0002_alter_m2mtasklistintest_task_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='duration',
            field=models.PositiveIntegerField(help_text='Максимально дозволена тривалість тестування у хвилинах', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Тривалість, хв'),
        ),
    ]
