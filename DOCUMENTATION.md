# Dokumentasi Teknis Sistem Informasi Akademik

## Struktur Database

### 1. User (Pengguna)
```sql
Table: users
- id: Integer (Primary Key)
- username: String (Unique)
- password: String (Hashed)
- role: String (admin/dosen/mahasiswa)
- is_active: Boolean
- last_login: DateTime
```
- Menyimpan data autentikasi semua pengguna
- Password di-hash menggunakan Werkzeug Security
- Terhubung one-to-one dengan tabel Dosen/Mahasiswa
- Mencatat waktu login terakhir untuk keamanan

### 2. Dosen
```sql
Table: dosen
- id: Integer (Primary Key)
- user_id: Integer (Foreign Key ke users)
- nip: String (Unique)
- nama: String
- email: String
- telepon: String
- alamat: Text
- status: Boolean
- created_at: DateTime
- updated_at: DateTime
```
- Menyimpan informasi detail dosen
- Terhubung one-to-many dengan tabel Kelas
- Status menunjukkan aktif/tidak aktif
- Mencatat waktu pembuatan dan update data

### 3. Mahasiswa
```sql
Table: mahasiswa
- id: Integer (Primary Key)
- user_id: Integer (Foreign Key ke users)
- nim: String (Unique)
- nama: String
- program_studi: String
- angkatan: Integer
- semester: Integer
- ipk: Float
- total_sks: Integer
- created_at: DateTime
- updated_at: DateTime
```
- Menyimpan informasi detail mahasiswa
- IPK dihitung otomatis dari nilai
- Total SKS diupdate saat enrollment berubah
- Mencatat progress semester mahasiswa

### 4. Mata Kuliah
```sql
Table: mata_kuliah
- id: Integer (Primary Key)
- kode: String (Unique)
- nama: String
- sks: Integer
- deskripsi: Text
- created_at: DateTime
- updated_at: DateTime
```
- Informasi dasar mata kuliah
- SKS digunakan untuk perhitungan IPK
- Terhubung one-to-many dengan Kelas

### 5. Kelas
```sql
Table: kelas
- id: Integer (Primary Key)
- mata_kuliah_id: Integer (Foreign Key)
- dosen_id: Integer (Foreign Key)
- semester: String
- hari: String
- waktu: String
- ruangan: String
- kapasitas: Integer
- created_at: DateTime
- updated_at: DateTime
```
- Menghubungkan Dosen dengan Mata Kuliah
- Satu mata kuliah bisa memiliki beberapa kelas
- Mencatat jadwal dan lokasi perkuliahan

### 6. Enrollment (Pendaftaran)
```sql
Table: enrollment
- id: Integer (Primary Key)
- mahasiswa_id: Integer (Foreign Key)
- kelas_id: Integer (Foreign Key)
- nilai_angka: Float
- nilai_huruf: String
- is_confirmed: Boolean
- created_at: DateTime
- updated_at: DateTime
```
- Mencatat pendaftaran mata kuliah
- Menyimpan nilai mahasiswa
- Status konfirmasi pengambilan mata kuliah

### 7. IPS History
```sql
Table: ips_history
- id: Integer (Primary Key)
- mahasiswa_id: Integer (Foreign Key)
- semester: String
- ips: Float
- created_at: DateTime
```
- Menyimpan riwayat IPS per semester
- Digunakan untuk grafik perkembangan nilai
- Data untuk analisis performa mahasiswa

##  Alur Sistem

### 1. Autentikasi & Otorisasi
```python
@login_required
@role_required('admin')
def admin_dashboard():
    # Kode untuk admin dashboard
```
- Menggunakan Flask-Login untuk manajemen sesi
- Dekorator @role_required untuk kontrol akses
- Session timeout setelah 1 jam tidak aktif
- Pencatatan waktu login terakhir

### 2. Perhitungan IPK & IPS
```python
def hitung_ipk(nilai_list):
    total_bobot = 0
    total_sks = 0
    for nilai in nilai_list:
        bobot = konversi_nilai(nilai.nilai_angka)
        total_bobot += bobot * nilai.kelas.mata_kuliah.sks
        total_sks += nilai.kelas.mata_kuliah.sks
    return total_bobot / total_sks if total_sks > 0 else 0

def hitung_ips(nilai_semester):
    # Perhitungan IPS per semester
    # Kode perhitungan
```
- Dihitung otomatis saat nilai diupdate
- Menggunakan sistem 4.0
- Bobot nilai: A=4, B=3, C=2, D=1, E=0
- Update otomatis ke IPS History

### 3. Validasi SKS
```python
def validasi_sks(mahasiswa, sks_baru):
    batas_sks = {
        3.0: 24,  # IPK > 3.0
        2.5: 21,  # IPK 2.5 - 3.0
        0.0: 18   # IPK < 2.5
    }
    # Kode validasi
```
- Cek batas SKS berdasarkan IPK
- Validasi dilakukan saat enrollment
- Mencegah pengambilan SKS berlebih
- Notifikasi jika melebihi batas

### 4. Manajemen Kelas
```python
def konfirmasi_enrollment():
    # Konfirmasi pengambilan mata kuliah
    # Update status enrollment
    # Kirim notifikasi

def batalkan_enrollment():
    # Batalkan pengambilan mata kuliah
    # Update total SKS
    # Kirim notifikasi
```
- Proses pendaftaran dan pembatalan kelas
- Update status konfirmasi
- Manajemen kuota kelas
- Notifikasi perubahan status

##  Komponen UI

### 1. Dashboard Cards
```html
<div class="info-card">
    <div class="card-header">
        <h2>Informasi Mahasiswa</h2>
    </div>
    <div class="card-body">
        <!-- Konten card -->
    </div>
</div>
```
- Desain responsif
- Animasi hover
- Shadow effect
- Tema warna konsisten

### 2. Ikon dan Badge
```css
.info-row i {
    width: 18px;
    height: 18px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    color: #specific-color;
}
```
- Ikon Font Awesome
- Warna tematik
- Ukuran konsisten
- Tooltip informatif

### 3. Tabel Data
```html
<table class="data-table">
    <thead>
        <!-- Header tabel -->
    </thead>
    <tbody>
        <!-- Data rows -->
    </tbody>
</table>
```
- Sorting kolom
- Pagination
- Filter dan pencarian
- Responsif pada mobile

### 4. Modal Dialog
```html
<div class="modal">
    <div class="modal-content">
        <div class="modal-header">
            <!-- Header modal -->
        </div>
        <div class="modal-body">
            <!-- Konten modal -->
        </div>
    </div>
</div>
```
- Animasi transisi
- Backdrop blur
- Form validation
- Responsive design

##  Keamanan

### 1. Autentikasi
- Password di-hash dengan salt
- Proteksi terhadap brute force
- Session management yang aman
- CSRF protection

### 2. Validasi Input
- Sanitasi input form
- Validasi tipe data
- Pencegahan SQL injection
- XSS protection

### 3. Database
- Foreign key constraints
- Transaction management
- Regular backup
- Data encryption

## 🔧 Panduan Pengembangan

### Menambah Fitur
1. Buat branch baru
2. Update models.py
3. Buat/update routes
4. Tambah/update templates
5. Test fitur
6. Merge ke main

### Debug Mode
```python
if __name__ == '__main__':
    app.run(debug=True)
```
- Error stack trace lengkap
- Auto-reload saat development
- Debug toolbar aktif
- SQL query logging

### Logging
```python
app.logger.info('Info message')
app.logger.error('Error message')
```
- Log rotasi harian
- Level: DEBUG, INFO, WARNING, ERROR
- Format: timestamp, level, message
- Separate error logs

##  Maintenance

### Backup Database
```bash
# Backup otomatis setiap hari
0 0 * * * /path/to/backup.sh
```

### Update Sistem
1. Pull kode terbaru
2. Aktifkan maintenance mode
3. Backup database
4. Update dependencies
5. Jalankan migrasi
6. Test sistem
7. Nonaktifkan maintenance mode 
