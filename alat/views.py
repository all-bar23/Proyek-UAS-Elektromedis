from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from datetime import datetime
from .models import AlatElektromedis

def daftar_alat(request):
    kata_kunci = request.GET.get('q', '')
    if kata_kunci:
        daftar = AlatElektromedis.objects.filter(
            Q(nama_alat__icontains=kata_kunci) | Q(kode_alat__icontains=kata_kunci)
        )
    else:
        daftar = AlatElektromedis.objects.all()

    jumlah_baik = 0
    jumlah_perawatan = 0
    jumlah_rusak = 0
    
    for alat in daftar:
        if alat.kondisi == "Baik":
            jumlah_baik += 1
        elif alat.kondisi == "Perlu Perawatan":
            jumlah_perawatan += 1
        else:
            jumlah_rusak += 1

    context = {
        'daftar_alat': daftar,
        'jumlah_baik': jumlah_baik,
        'jumlah_perawatan': jumlah_perawatan,
        'jumlah_rusak': jumlah_rusak,
        'kata_kunci': kata_kunci
    }
    return render(request, 'alat/daftar_alat.html', context)

def tambah_alat(request):
    if request.method == 'POST':
        kode_alat = request.POST.get('kode_alat')
        nama_alat = request.POST.get('nama_alat')
        jenis_alat = request.POST.get('jenis_alat')
        lokasi = request.POST.get('lokasi')
        tahun_pengadaan_str = request.POST.get('tahun_pengadaan')
        kondisi = request.POST.get('kondisi')
        
        errors = []
        if not kode_alat: errors.append("Kode alat tidak boleh kosong.")
        if not nama_alat: errors.append("Nama alat tidak boleh kosong.")
        
        try:
            tahun_pengadaan = int(tahun_pengadaan_str)
            if tahun_pengadaan > datetime.now().year:
                errors.append("Tahun pengadaan tidak boleh lebih besar dari tahun berjalan.")
        except ValueError:
            errors.append("Tahun pengadaan harus berupa angka.")
            
        if AlatElektromedis.objects.filter(kode_alat=kode_alat).exists():
            errors.append("Kode alat sudah digunakan.")

        if not errors:
            if kondisi == "Baik": status_kelayakan = "Layak Digunakan"
            elif kondisi == "Perlu Perawatan": status_kelayakan = "Layak dengan Catatan"
            else: status_kelayakan = "Tidak Layak Digunakan"

            AlatElektromedis.objects.create(
                kode_alat=kode_alat, nama_alat=nama_alat, jenis_alat=jenis_alat,
                lokasi=lokasi, tahun_pengadaan=tahun_pengadaan, kondisi=kondisi, status_kelayakan=status_kelayakan
            )
            return redirect('daftar_alat')
        return render(request, 'alat/tambah_alat.html', {'errors': errors})
    return render(request, 'alat/tambah_alat.html')


def detail_alat(request, pk):
    alat = get_object_or_404(AlatElektromedis, pk=pk)
    return render(request, 'alat/detail_alat.html', {'alat': alat})

def edit_alat(request, pk):
    alat = get_object_or_404(AlatElektromedis, pk=pk)
    if request.method == 'POST':
        kode_alat = request.POST.get('kode_alat')
        nama_alat = request.POST.get('nama_alat')
        jenis_alat = request.POST.get('jenis_alat')
        lokasi = request.POST.get('lokasi')
        tahun_pengadaan_str = request.POST.get('tahun_pengadaan')
        kondisi = request.POST.get('kondisi')
        
        errors = []
        if not kode_alat: errors.append("Kode alat tidak boleh kosong.")
        if not nama_alat: errors.append("Nama alat tidak boleh kosong.")
        try:
            tahun_pengadaan = int(tahun_pengadaan_str)
            if tahun_pengadaan > datetime.now().year:
                errors.append("Tahun pengadaan tidak boleh lebih besar dari tahun berjalan.")
        except ValueError:
            errors.append("Tahun pengadaan harus berupa angka.")
            
        # Menggunakan exclude(pk=pk) agar aman dari duplikasi nama
        if AlatElektromedis.objects.filter(kode_alat=kode_alat).exclude(pk=pk).exists():
            errors.append("Kode alat sudah digunakan alat lain.")

        if not errors:
            if kondisi == "Baik": status_kelayakan = "Layak Digunakan"
            elif kondisi == "Perlu Perawatan": status_kelayakan = "Layak dengan Catatan"
            else: status_kelayakan = "Tidak Layak Digunakan"

            alat.kode_alat = kode_alat
            alat.nama_alat = nama_alat
            alat.jenis_alat = jenis_alat
            alat.lokasi = lokasi
            alat.tahun_pengadaan = tahun_pengadaan
            alat.kondisi = kondisi
            alat.status_kelayakan = status_kelayakan
            alat.save()
            return redirect('daftar_alat')
        return render(request, 'alat/edit_alat.html', {'alat': alat, 'errors': errors})
    return render(request, 'alat/edit_alat.html', {'alat': alat})

def hapus_alat(request, pk):
    alat = get_object_or_404(AlatElektromedis, pk=pk)
    if request.method == 'POST':
        alat.delete()
        return redirect('daftar_alat')
    return render(request, 'alat/hapus_alat.html', {'alat': alat})