# Generated by Django 3.2.4 on 2021-08-24 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Testing', '0007_auto_20210817_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='testingsessionofautorizeduser',
            name='group',
            field=models.CharField(blank=True, default='', help_text='Вкажіть групу', max_length=20, verbose_name='Група'),
        ),
        migrations.AddField(
            model_name='testingsessionofunautorizeduser',
            name='group',
            field=models.CharField(blank=True, default='', help_text='Вкажіть групу', max_length=20, verbose_name='Група'),
        ),
        migrations.AlterField(
            model_name='testingsessionofunautorizeduser',
            name='information',
            field=models.CharField(help_text="Введіть прізвище, ім'я", max_length=100, verbose_name='ПІБ'),
        ),
    ]
