# Generated by Django 3.0.3 on 2020-04-24 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_room_availablestatus'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='photos',
            new_name='photo',
        ),
    ]
