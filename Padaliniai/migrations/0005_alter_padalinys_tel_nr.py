# Generated by Django 5.0.12 on 2025-04-04 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Padaliniai', '0004_padalinys_ansambliai'),
    ]

    operations = [
        migrations.AlterField(
            model_name='padalinys',
            name='tel_nr',
            field=models.CharField(default='-', max_length=20),
        ),
    ]
