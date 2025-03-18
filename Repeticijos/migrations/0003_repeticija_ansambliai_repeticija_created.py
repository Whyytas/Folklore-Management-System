# Generated by Django 5.0.12 on 2025-03-17 13:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ansambliai', '0001_initial'),
        ('Repeticijos', '0002_alter_repeticija_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='repeticija',
            name='ansambliai',
            field=models.ManyToManyField(blank=True, related_name='repeticijos', to='Ansambliai.ansamblis'),
        ),
        migrations.AddField(
            model_name='repeticija',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2025, 3, 17, 13, 47, 38, 296961, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
