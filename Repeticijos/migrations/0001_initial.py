# Generated by Django 5.0.12 on 2025-03-19 21:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Ansambliai', '0001_initial'),
        ('Kuriniai', '0011_kurinys_natos_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repeticija',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pavadinimas', models.CharField(max_length=255)),
                ('data', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ansamblis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repeticijos', to='Ansambliai.ansamblis')),
            ],
        ),
        migrations.CreateModel(
            name='RepeticijaKurinys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('kurinys', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Kuriniai.kurinys')),
                ('repeticija', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Repeticijos.repeticija')),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('repeticija', 'kurinys')},
            },
        ),
        migrations.AddField(
            model_name='repeticija',
            name='kuriniai',
            field=models.ManyToManyField(through='Repeticijos.RepeticijaKurinys', to='Kuriniai.kurinys'),
        ),
    ]
