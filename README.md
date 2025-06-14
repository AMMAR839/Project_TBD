# Sistem Informasi Akademik Universitas

Aplikasi web untuk manajemen akademik universitas yang memudahkan pengelolaan mata kuliah, dosen, dan mahasiswa. Dibangun menggunakan Flask framework dengan antarmuka modern dan responsif.

##  Fitur Aplikasi

###  Admin
- Mengelola data mata kuliah (tambah, edit, hapus)
- Mengelola data dosen (tambah, edit, hapus)
- Mengatur kelas dan jadwal perkuliahan
- Melihat daftar mahasiswa terdaftar
- Memantau status akademik
- Mengelola pendaftaran kelas
- Melihat detail kelas dan peserta

###  Dosen
- Melihat daftar kelas yang diampu
- Menginput dan mengedit nilai mahasiswa
- Mengelola profil pribadi
- Melihat jadwal mengajar
- Melihat daftar mahasiswa per kelas
- Statistik kelas dan performa mahasiswa
- Dashboard informatif dengan ringkasan mengajar

###  Mahasiswa
- Melihat dan mendaftar mata kuliah
- Melihat nilai dan transkrip
- Melihat jadwal kuliah
- Mengelola profil pribadi
- Dashboard modern dengan:
  - Informasi IPK dan IPS
  - Grafik perkembangan nilai
  - Status pengambilan mata kuliah
  - Batas dan total SKS yang diambil
  - Filter dan pencarian mata kuliah
  - Konfirmasi pengambilan mata kuliah

###  Sistem SKS dan Penilaian
Batas pengambilan SKS berdasarkan IPK:
| IPK         | Maksimal SKS |
|-------------|--------------|
| > 3.00      | 24 SKS      |
| 2.50 - 3.00 | 21 SKS      |
| < 2.50      | 18 SKS      |

##  Fitur UI/UX
- Antarmuka modern dan responsif
- Tema warna yang konsisten
- Ikon berwarna untuk navigasi intuitif
- Animasi dan transisi halus
- Filter dan pencarian real-time
- Modal dialog untuk aksi penting
- Notifikasi dan pesan status
- Dashboard yang informatif

##  Cara Menggunakan

### 1. Persiapan Awal
#### a. Clone Repository
```bash
git clone https://github.com/AMMAR839/Tugas_TBD.git
cd Project_TBD
```

#### b. Buat virtual environment
```bash
python -m venv venv
```

#### c. Aktifkan virtual environment

##### Untuk Windows:
```bash
venv\Scripts\activate
```
##### Untuk Linux/Mac:
```bash
source venv/bin/activate
```

### 2. Instalasi
#### Install semua dependencies
```bash
pip install -r requirements.txt
```

### 3. Menjalankan Aplikasi
```bash
python app.py
```
Buka browser dan akses `http://127.0.0.1:5000`



## Reset dan Isi Database dengan Data (Opsional)
- Mereset Database

```bash
python reset_db.py
```

- Memasukkan data admin untuk login
```bash
python create_admin.py
```

- Memasukkan nilai Atribut secara manual (Data Default)
```bash
python init_db.py
```


## Akun Default

### Admin
```
Username: admin
Password: admin123
```

### Dosen
```
Username: dosen
Password: dosen123
```
Contoh:

Username: budi.santoso

Password: dosen123

### Mahasiswa
```
Username: mahasiswa
Password: mhs123
```
Contoh:

Username: rudi.hartono

Password: mhs123

## Teknologi yang Digunakan

- **Backend:** Python Flask
- **Database:** SQLite dengan SQLAlchemy
- **Frontend:** 
  - HTML5, CSS3, JavaScript
  - Desain responsif modern
  - Animasi dan transisi CSS
- **UI Framework:** Bootstrap 5
- **Icons:** Font Awesome 6
- **Charts:** Chart.js untuk visualisasi data
- **Security:** Werkzeug Security
- **AJAX:** Fetch API untuk interaksi dinamis


## 📄 Lisensi

MIT License - Silakan gunakan dan modifikasi sesuai kebutuhan. 
