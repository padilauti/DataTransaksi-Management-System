# Generated by Django 5.1.1 on 2024-09-12 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaksi', '0003_alter_transaksi_anggota_alter_transaksi_bukti'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anggota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(blank=True, max_length=100, null=True)),
                ('alamat', models.TextField()),
                ('no_hp', models.CharField(max_length=15)),
            ],
        ),
    ]