# Generated by Django 4.1.1 on 2022-09-27 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('JSGame_api', '0008_asset_frames'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='Frames',
            new_name='frames',
        ),
    ]
