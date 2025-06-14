from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'dosen', 'mahasiswa'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Mahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nim = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    program_studi = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    ipk = db.Column(db.Float, default=0.0)
    user = db.relationship('User', backref='mahasiswa_profile', lazy=True)
    mata_kuliah = db.relationship('Enrollment', backref='mahasiswa', lazy=True,
                                cascade='all, delete-orphan')
    ips_history = db.relationship('IPSHistory', backref='mahasiswa', lazy=True,
                                cascade='all, delete-orphan')

class Dosen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nip = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    telepon = db.Column(db.String(20))
    alamat = db.Column(db.Text)
    status = db.Column(db.Boolean, default=True)
    user = db.relationship('User', backref='dosen_profile', lazy=True)
    mengajar = db.relationship('Kelas', backref='dosen', lazy=True,
                             cascade='all, delete-orphan')

class MataKuliah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(10), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    sks = db.Column(db.Integer, nullable=False)
    kelas = db.relationship('Kelas', backref='mata_kuliah', lazy=True,
                          cascade='all, delete-orphan')

class Kelas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mata_kuliah_id = db.Column(db.Integer, db.ForeignKey('mata_kuliah.id'), nullable=False)
    dosen_id = db.Column(db.Integer, db.ForeignKey('dosen.id'), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    hari = db.Column(db.String(20), nullable=False)
    waktu = db.Column(db.String(20), nullable=False)
    ruangan = db.Column(db.String(20), nullable=False)
    peserta = db.relationship('Enrollment', backref='kelas', lazy=True,
                            cascade='all, delete-orphan')

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mahasiswa_id = db.Column(db.Integer, db.ForeignKey('mahasiswa.id'), nullable=False)
    kelas_id = db.Column(db.Integer, db.ForeignKey('kelas.id'), nullable=False)
    nilai_angka = db.Column(db.Float, nullable=True)
    nilai_huruf = db.Column(db.String(2), nullable=True)
    is_confirmed = db.Column(db.Boolean, default=False)

class IPSHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mahasiswa_id = db.Column(db.Integer, db.ForeignKey('mahasiswa.id'), nullable=False)
    semester = db.Column(db.String(20), nullable=False)  # e.g., "2023/2024 Ganjil"
    ips = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 