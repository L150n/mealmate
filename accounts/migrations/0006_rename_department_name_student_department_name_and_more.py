# Generated by Django 4.2 on 2023-04-06 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20230404_0535'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='Department_name',
            new_name='department_name',
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1),
        ),
    ]
