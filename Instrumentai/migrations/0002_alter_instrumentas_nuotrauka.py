# Generated by Django 5.0.12 on 2025-03-12 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Instrumentai', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrumentas',
            name='nuotrauka',
            field=models.ImageField(blank=True, null=True, upload_to='instrument_photos/'),
        ),
    ]
