# Generated by Django 3.2.4 on 2021-08-25 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0004_test_is_allow_help'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='is_allow_skip_task',
            field=models.BooleanField(default=False, help_text="Чи дозволено пропускати завдання? (В кінці тестування пропущені завдання знов з'являться)", verbose_name='Пропуск завдання'),
        ),
    ]
