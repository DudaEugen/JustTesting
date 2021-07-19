# Generated by Django 3.2.4 on 2021-07-19 07:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Task', '0004_alter_multiplychoicetestanswer_identificator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='multiplychoicetestanswer',
            name='id',
        ),
        migrations.AlterField(
            model_name='multiplychoicetestanswer',
            name='identificator',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
