# Generated by Django 4.2 on 2023-04-06 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_student_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='dob',
            field=models.DateField(default='2000-01-01'),
        ),
    ]
