# Generated by Django 5.0.12 on 2025-03-05 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ansambliai', '0001_initial'),
        ('Initial', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ansambliai',
            field=models.ManyToManyField(blank=True, related_name='members', to='Ansambliai.ansamblis'),
        ),
    ]
