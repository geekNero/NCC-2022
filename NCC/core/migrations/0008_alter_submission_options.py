# Generated by Django 4.1.1 on 2022-10-29 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_container_cid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='submission',
            options={'ordering': ['time']},
        ),
    ]
