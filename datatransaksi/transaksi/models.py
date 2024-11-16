from django.db import models

# Create your models here.
anggota_choice = {
    ('Uti Nur Padila','Uti Nur Padila'),
    ('Nur Aini','Nur Aini'),
    ('Diah Linggawati','Diah Linggawati'),
    ('Muhammad Ilham','Muhammad Ilham'),
}



class Anggota(models.Model):
    nama = models.CharField(max_length=100, blank=True, null=True)
    alamat = models.TextField()
    no_hp = models.CharField(max_length=15)

    def __str__(self):
        return self.nama


class Transaksi(models.Model):
    JENIS_TRANSAKSI_CHOICES = [
        ('P', 'Pengeluaran'),
        ('M', 'Pemasukan'),
    ]
    
    id = models.AutoField(primary_key=True)
    tanggal = models.DateField(blank=True)
    jenis_transaksi = models.CharField(max_length=1, choices=JENIS_TRANSAKSI_CHOICES)
    anggota =  models.ForeignKey(Anggota, on_delete=models.CASCADE, blank=True) 
    jumlah = models.IntegerField()
    keterangan = models.TextField()
    bukti = models.FileField(upload_to='bukti_transaksi/', blank=True, null=True)
    

    def __str__(self):
        return self.keterangan









    