# Generated by Django 5.0.12 on 2025-04-02 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Kuriniai', '0014_kurinys_paruosimas_alter_kurinys_tipas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kurinys',
            name='sudetingumas',
        ),
        migrations.AddField(
            model_name='kurinys',
            name='greitumas',
            field=models.CharField(blank=True, choices=[('Lėtas', 'Lėtas'), ('Vidutinis', 'Vidutinis'), ('Greitas', 'Greitas')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='kurinys',
            name='paruosimas',
            field=models.CharField(blank=True, choices=[('Naujas', 'Naujas'), ('Ruošiamas', 'Ruošiamas'), ('Paruoštas', 'Paruoštas'), ('Archyvas', 'Archyvas')], max_length=20, null=True),
        ),
    ]
