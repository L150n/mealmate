# Generated by Django 2.2.9 on 2023-04-04 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20230404_0531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='dob',
            field=models.DateField(default='0000-00-00'),
        ),
    ]
