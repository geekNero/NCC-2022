# Generated by Django 4.1.1 on 2022-09-22 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_question_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='question_status',
            name='penalty',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
