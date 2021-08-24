# Generated by Django 3.2.4 on 2021-08-24 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Testing', '0009_rename_information_testingsessionofunautorizeduser_display_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='testingsessionofunautorizeduser',
            name='ip_begin',
            field=models.GenericIPAddressField(blank=True, help_text='IP, з якого була сьворена сесія тестування', null=True, verbose_name='IP'),
        ),
    ]