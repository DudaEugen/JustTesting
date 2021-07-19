# Generated by Django 3.2.4 on 2021-07-19 07:25

from django.db import migrations, models
import uuid


def gen_uuid(apps, schema_editor):
    MultiplyChoiceTestAnswer = apps.get_model(
        'Task', 'multiplychoicetestanswer')
    for answer_option in MultiplyChoiceTestAnswer.objects.all():
        answer_option.identificator = uuid.uuid4()
        answer_option.save()


class Migration(migrations.Migration):

    dependencies = [
        ('Task', '0002_alter_multiplychoicetest_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='multiplychoicetestanswer',
            name='identificator',
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.RunPython(gen_uuid),
        migrations.AlterField(
            model_name='multiplychoicetestanswer',
            name='identificator',
            field=models.UUIDField(unique=True)
        )
    ]