# Generated by Django 4.2.4 on 2024-06-19 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foldermaster', '0003_alter_file_file_alter_file_folder'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]