# Generated by Django 3.2.18 on 2023-05-02 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_alter_transaction_transaction_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cartid', models.AutoField(primary_key=True, serialize=False)),
                ('item1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item1', to='accounts.menuitem')),
                ('item2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item2', to='accounts.menuitem')),
                ('item3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item3', to='accounts.menuitem')),
                ('item4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item4', to='accounts.menuitem')),
                ('item5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item5', to='accounts.menuitem')),
                ('studentid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
            options={
                'db_table': 'cart',
            },
        ),
    ]
