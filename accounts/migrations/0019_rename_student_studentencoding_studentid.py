# Generated by Django 4.2 on 2023-04-07 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_studentencoding'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentencoding',
            old_name='student',
            new_name='studentid',
        ),
    ]
