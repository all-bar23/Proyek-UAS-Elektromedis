from django.db import models

class AlatElektromedis(models.Model):
    KONDISI_CHOICES = (
        ('Baik', 'Baik'),
        ('Perlu Perawatan', 'Perlu Perawatan'),
        ('Rusak', 'Rusak'),
    )

    kode_alat = models.CharField(max_length=20, unique=True)
    nama_alat = models.CharField(max_length=100)
    jenis_alat = models.CharField(max_length=100)
    lokasi = models.CharField(max_length=100)
    tahun_pengadaan = models.IntegerField()
    kondisi = models.CharField(max_length=30, choices=KONDISI_CHOICES)
    status_kelayakan = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.kode_alat} - {self.nama_alat}"