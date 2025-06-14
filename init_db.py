from app import app, db
from models import User, Dosen, MataKuliah, Mahasiswa, Kelas, IPSHistory, Enrollment
import random
from datetime import datetime, timedelta

def create_initial_data():
    try:
        

        # Create dummy dosen with more detailed data
        dosen_data = [
            {
                'nip': '198501012010011001',
                'nama': 'Dr. Ahmad Suryadi, M.Kom',
                'username': 'ahmad.suryadi',
                'password': 'dosen123',
                'email': 'ahmad.suryadi@university.ac.id',
                'telepon': '081234567890',
                'alamat': 'Jl. Profesor No. 123, Jakarta'
            },
            {
                'nip': '198607152011012002',
                'nama': 'Dr. Siti Aminah, M.Sc',
                'username': 'siti.aminah',
                'password': 'dosen123',
                'email': 'siti.aminah@university.ac.id',
                'telepon': '081345678901',
                'alamat': 'Jl. Pendidikan No. 45, Bandung'
            },
            {
                'nip': '199003242012011003',
                'nama': 'Dr. Budi Santoso, M.T',
                'username': 'budi.santoso',
                'password': 'dosen123',
                'email': 'budi.santoso@university.ac.id',
                'telepon': '081456789012',
                'alamat': 'Jl. Teknologi No. 67, Surabaya'
            },
            {
                'nip': '198709182013011004',
                'nama': 'Dr. Dewi Lestari, M.Sc',
                'username': 'dewi.lestari',
                'password': 'dosen123',
                'email': 'dewi.lestari@university.ac.id',
                'telepon': '081567890123',
                'alamat': 'Jl. Ilmu No. 89, Yogyakarta'
            },
            {
                'nip': '198812252014011005',
                'nama': 'Dr. Rudi Hermawan, M.Kom',
                'username': 'rudi.hermawan',
                'password': 'dosen123',
                'email': 'rudi.hermawan@university.ac.id',
                'telepon': '081678901234',
                'alamat': 'Jl. Komputer No. 12, Malang'
            }
        ]

        for data in dosen_data:
            user = User(username=data['username'], role='dosen')
            user.set_password(data['password'])
            db.session.add(user)
            db.session.commit()

            dosen = Dosen(
                user_id=user.id,
                nip=data['nip'],
                nama=data['nama'],
                email=data['email'],
                telepon=data['telepon'],
                alamat=data['alamat'],
                status=True
            )
            db.session.add(dosen)
            db.session.commit()

        # Create dummy mata kuliah with more variety
        mata_kuliah_data = [
            {'kode': 'IF101', 'nama': 'Pemrograman Dasar', 'sks': 3},
            {'kode': 'IF102', 'nama': 'Algoritma dan Struktur Data', 'sks': 3},
            {'kode': 'IF201', 'nama': 'Basis Data', 'sks': 3},
            {'kode': 'IF202', 'nama': 'Pemrograman Web', 'sks': 3},
            {'kode': 'IF301', 'nama': 'Kecerdasan Buatan', 'sks': 3},
            {'kode': 'IF302', 'nama': 'Jaringan Komputer', 'sks': 3},
            {'kode': 'IF303', 'nama': 'Sistem Operasi', 'sks': 3},
            {'kode': 'IF304', 'nama': 'Pemrograman Mobile', 'sks': 3},
            {'kode': 'IF401', 'nama': 'Keamanan Informasi', 'sks': 3},
            {'kode': 'IF402', 'nama': 'Cloud Computing', 'sks': 3},
            {'kode': 'IF403', 'nama': 'Data Mining', 'sks': 3},
            {'kode': 'IF404', 'nama': 'Machine Learning', 'sks': 3}
        ]

        for data in mata_kuliah_data:
            mk = MataKuliah(**data)
            db.session.add(mk)
            db.session.commit()

        # Create dummy mahasiswa with more variety
        mahasiswa_data = [
            {
                'nim': '2021001', 'nama': 'Andi Wijaya',
                'username': 'andi.wijaya', 'password': 'mhs123',
                'program_studi': 'Teknik Informatika', 'semester': 4,
                'ipk': 3.75
            },
            {
                'nim': '2021002', 'nama': 'Dewi Putri',
                'username': 'dewi.putri', 'password': 'mhs123',
                'program_studi': 'Teknik Informatika', 'semester': 4,
                'ipk': 3.85
            },
            {
                'nim': '2021003', 'nama': 'Rudi Hartono',
                'username': 'rudi.hartono', 'password': 'mhs123',
                'program_studi': 'Teknik Informatika', 'semester': 4,
                'ipk': 3.50
            },
            {
                'nim': '2021004', 'nama': 'Siti Fatimah',
                'username': 'siti.fatimah', 'password': 'mhs123',
                'program_studi': 'Teknik Informatika', 'semester': 4,
                'ipk': 3.90
            },
            {
                'nim': '2021005', 'nama': 'Budi Prakoso',
                'username': 'budi.prakoso', 'password': 'mhs123',
                'program_studi': 'Teknik Informatika', 'semester': 4,
                'ipk': 3.65
            }
        ]

        semester_list = ['2021/2022 Ganjil', '2021/2022 Genap', '2022/2023 Ganjil', '2022/2023 Genap', '2023/2024 Ganjil']
        
        for data in mahasiswa_data:
            user = User(username=data['username'], role='mahasiswa')
            user.set_password(data['password'])
            db.session.add(user)
            db.session.commit()

            mahasiswa = Mahasiswa(
                user_id=user.id,
                nim=data['nim'],
                nama=data['nama'],
                program_studi=data['program_studi'],
                semester=data['semester'],
                ipk=data['ipk']
            )
            db.session.add(mahasiswa)
            db.session.commit()

            # Add IPS history for each mahasiswa with realistic progression
            base_ips = round(random.uniform(2.8, 3.2), 2)
            for i, semester in enumerate(semester_list):
                # Gradually improve IPS
                improvement = round(random.uniform(0.1, 0.3), 2)
                ips = min(4.0, base_ips + (improvement * i))
                history = IPSHistory(
                    mahasiswa_id=mahasiswa.id,
                    semester=semester,
                    ips=ips,
                    created_at=datetime.now() - timedelta(days=(len(semester_list)-i)*180)
                )
                db.session.add(history)
            db.session.commit()

        # Create dummy kelas with more realistic schedules
        dosen_list = Dosen.query.all()
        mata_kuliah_list = MataKuliah.query.all()
        hari_list = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
        waktu_list = [
            '08:00-09:40', '10:00-11:40', '13:00-14:40', '15:00-16:40',
            '08:00-10:30', '10:30-13:00', '13:00-15:30', '15:30-18:00'
        ]
        ruangan_list = ['R101', 'R102', 'R103', 'R104', 'R105', 'Lab 1', 'Lab 2', 'Lab 3']

        # Create classes for current semester
        current_semester = '2023/2024 Ganjil'
        for mk in mata_kuliah_list:
            # Create 1-2 classes per course
            for _ in range(random.randint(1, 2)):
                kelas = Kelas(
                    mata_kuliah_id=mk.id,
                    dosen_id=random.choice(dosen_list).id,
                    semester=current_semester,
                    hari=random.choice(hari_list),
                    waktu=random.choice(waktu_list),
                    ruangan=random.choice(ruangan_list)
                )
                db.session.add(kelas)
                db.session.commit()

        # Enroll students in classes with some having grades
        kelas_list = Kelas.query.filter_by(semester=current_semester).all()
        mahasiswa_list = Mahasiswa.query.all()
        
        for mahasiswa in mahasiswa_list:
            # Enroll in 4-6 classes
            selected_kelas = random.sample(kelas_list, random.randint(4, 6))
            
            # Tentukan apakah mahasiswa ini sudah konfirmasi semua mata kuliah
            is_all_confirmed = random.choice([True, True, False])  # 66% chance of all confirmed
            
            for kelas in selected_kelas:
                enrollment = Enrollment(
                    mahasiswa_id=mahasiswa.id,
                    kelas_id=kelas.id,
                    is_confirmed=is_all_confirmed or random.random() > 0.3  # Higher chance of confirmation
                )
                
                # Add grades only for confirmed enrollments
                if enrollment.is_confirmed:
                    # 70% chance of having grades if confirmed
                    if random.random() < 0.7:
                        nilai_angka = round(random.uniform(60, 95))
                        enrollment.nilai_angka = nilai_angka
                        
                        # Convert numerical grade to letter grade
                        if nilai_angka >= 85:
                            enrollment.nilai_huruf = 'A'
                        elif nilai_angka >= 80:
                            enrollment.nilai_huruf = 'A-'
                        elif nilai_angka >= 75:
                            enrollment.nilai_huruf = 'B+'
                        elif nilai_angka >= 70:
                            enrollment.nilai_huruf = 'B'
                        elif nilai_angka >= 65:
                            enrollment.nilai_huruf = 'B-'
                        elif nilai_angka >= 60:
                            enrollment.nilai_huruf = 'C+'
                        else:
                            enrollment.nilai_huruf = 'C'
                
                db.session.add(enrollment)
                db.session.commit()

        print("Data awal berhasil dibuat!")
        return True

    except Exception as e:
        print("Error creating initial data:", str(e))
        db.session.rollback()
        return False

if __name__ == '__main__':
    with app.app_context():
        print("Membuat database baru...")
        db.create_all()
        print("Database berhasil dibuat!")
        
        print("Menambahkan data awal...")
        if create_initial_data():
            print("Data awal berhasil ditambahkan!")
        else:
            print("Gagal menambahkan data awal.") 