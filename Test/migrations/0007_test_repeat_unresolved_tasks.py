# Generated by Django 3.2.4 on 2021-08-29 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0006_test_show_right_solution_after_mistake'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='repeat_unresolved_tasks',
            field=models.BooleanField(default=False, help_text='Задавати в кінці тестування завдання, в яких були допущені помилки?', verbose_name='Повернути помилку'),
        ),
    ]
