# Generated by Django 5.1.1 on 2024-09-13 01:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaksi', '0004_anggota'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaksi',
            name='anggota',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='transaksi.anggota'),
            preserve_default=False,
        ),
    ]