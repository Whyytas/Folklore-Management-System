# Generated by Django 5.0.12 on 2025-04-21 18:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Departments', '0001_initial'),
        ('Ensembles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ensemble',
            name='unit',
        ),
        migrations.AddField(
            model_name='ensemble',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ensembles', to='Departments.department'),
        ),
    ]
