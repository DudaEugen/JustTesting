# Generated by Django 3.2.4 on 2021-08-24 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Task', '0008_auto_20210815_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='help_text',
            field=models.TextField(blank=True, default='', help_text='Введіть текст підказки до завдання', null=True, verbose_name='Підказка'),
        ),
    ]
