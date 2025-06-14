from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from models import db, User, Mahasiswa, Dosen, MataKuliah, Kelas, Enrollment, IPSHistory
from werkzeug.security import generate_password_hash
import random
import logging
from sqlalchemy.orm import session as sa_session # Import session from SQLAlchemy ORM

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db.init_app(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        logger.debug(f"Login attempt for username: {username}")
        
        user = User.query.filter_by(username=username).first()
        logger.debug(f"User found: {user is not None}")
        
        if user and user.check_password(password):
            logger.debug(f"Password check passed for user {username}")
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'dosen':
                logger.debug(f"Redirecting dosen {username} to dashboard")
                return redirect(url_for('dosen_dashboard'))
            else:
                return redirect(url_for('mahasiswa_dashboard'))
        else:
            if user:
                logger.debug(f"Password check failed for user {username}")
            flash('Username atau password salah')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('login'))
    
    try:
        mata_kuliah = MataKuliah.query.all()
        dosen = Dosen.query.all()
        kelas_list = Kelas.query.all()
        mahasiswa_list = Mahasiswa.query.all()
        
        return render_template('admin/dashboard.html',
                            mata_kuliah=mata_kuliah,
                            dosen=dosen,
                            kelas_list=kelas_list,
                            mahasiswa_list=mahasiswa_list)
    except Exception as e:
        logger.error(f"Error in admin_dashboard: {str(e)}", exc_info=True)
        flash('Terjadi kesalahan pada sistem saat memuat dashboard.', 'error')
        return redirect(url_for('login'))

@app.route('/admin/mata-kuliah', methods=['POST'])
@login_required
def tambah_mata_kuliah():
    if current_user.role != 'admin':
        flash('Anda tidak memiliki akses.', 'warning')
        return redirect(url_for('login'))
    
    try:
        kode = request.form.get('kode')
        nama = request.form.get('nama')
        sks = int(request.form.get('sks'))
        
        mata_kuliah = MataKuliah(kode=kode, nama=nama, sks=sks)
        db.session.add(mata_kuliah)
        db.session.commit()
        
        flash('Mata kuliah berhasil ditambahkan', 'success')
        logger.info(f"Course '{nama}' (Code: {kode}) added successfully.")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding course: {str(e)}", exc_info=True)
        flash(f'Gagal menambahkan mata kuliah: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/dosen', methods=['POST'])
@login_required
def tambah_dosen():
    if current_user.role != 'admin':
        flash('Anda tidak memiliki akses.', 'warning')
        return redirect(url_for('login'))
    
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        nama = request.form.get('nama')
        nip = request.form.get('nip')
        email = request.form.get('email')
        telepon = request.form.get('telepon')
        alamat = request.form.get('alamat')
        status_str = request.form.get('status')
        status = status_str == '1'
        
        logger.debug(f"Attempting to add dosen: Username={username}, NIP={nip}, Alamat={alamat}, Status={status}")

        # Cek apakah username sudah ada
        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan. Silakan pilih username lain.', 'error')
            logger.warning(f"Failed to add dosen: Username '{username}' already exists.")
            return redirect(url_for('admin_dashboard'))
        
        # Cek apakah NIP sudah ada
        if Dosen.query.filter_by(nip=nip).first():
            flash('NIP sudah terdaftar. Silakan masukkan NIP lain.', 'error')
            logger.warning(f"Failed to add dosen: NIP '{nip}' already registered.")
            return redirect(url_for('admin_dashboard'))
        
        user = User(username=username, role='dosen')
        user.set_password(password)
        db.session.add(user)
        
        # Lakukan commit di sini untuk mendapatkan user.id
        db.session.commit() 
        logger.debug(f"User '{username}' added with ID: {user.id}")
        
        dosen = Dosen(
            user_id=user.id, 
            nama=nama,
            nip=nip,
            email=email,
            telepon=telepon,
            alamat=alamat,
            status=status
        )
        db.session.add(dosen)
        db.session.commit()
        
        flash('Dosen berhasil ditambahkan', 'success')
        logger.info(f"Dosen '{nama}' (NIP: {nip}) added successfully.")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding dosen: {str(e)}", exc_info=True)
        flash(f'Gagal menambahkan dosen: {str(e)}. Periksa log server untuk detail.', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/dosen')
@login_required
def dosen_dashboard():
    if current_user.role != 'dosen':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('login'))
    
    try:
        dosen = Dosen.query.filter_by(user_id=current_user.id).first()
        if not dosen:
            flash('Profil dosen tidak ditemukan.', 'error')
            logout_user()
            return redirect(url_for('login'))
        kelas_diampu = Kelas.query.filter_by(dosen_id=dosen.id).all()
        
        return render_template('dosen/dashboard.html', 
                         dosen=dosen,
                         kelas_diampu=kelas_diampu)
    except Exception as e:
        logger.error(f"Error in dosen_dashboard: {str(e)}", exc_info=True)
        flash('Terjadi kesalahan pada sistem saat memuat dashboard dosen.', 'error')
        return redirect(url_for('login'))

@app.route('/mahasiswa')
@login_required
def mahasiswa_dashboard():
    if current_user.role != 'mahasiswa':
        flash('Anda tidak memiliki akses ke halaman ini.', 'warning')
        return redirect(url_for('login'))
    
    try:
        mahasiswa = Mahasiswa.query.filter_by(user_id=current_user.id).first()
        if not mahasiswa:
            flash('Profil mahasiswa tidak ditemukan.', 'error')
            logout_user()
            return redirect(url_for('login'))
        
        # Get IPS history and convert to serializable format
        ips_history_raw = IPSHistory.query.filter_by(mahasiswa_id=mahasiswa.id).order_by(IPSHistory.semester).all()
        ips_history = [{'semester': h.semester, 'ips': float(h.ips)} for h in ips_history_raw]
        ips_terakhir = ips_history[-1]['ips'] if ips_history else 0.0
        
        # Current active semester
        current_semester = '2023/2024 Ganjil'
        
        # Calculate max SKS based on IPK
        max_sks = 24 if mahasiswa.ipk >= 3.0 else (21 if mahasiswa.ipk >= 2.5 else 18)
        
        # Get enrolled courses
        mata_kuliah_diambil = Enrollment.query.filter_by(mahasiswa_id=mahasiswa.id).all()
        current_sks = sum(enroll.kelas.mata_kuliah.sks for enroll in mata_kuliah_diambil)
        
        # Get list of mata kuliah IDs that have been taken
        taken_mata_kuliah_ids = {enrollment.kelas.mata_kuliah_id for enrollment in mata_kuliah_diambil}
        
        # Get all available courses for the current semester
        available_kelas = Kelas.query.filter_by(semester=current_semester).all()
        
        # Check if any unconfirmed enrollments exist
        has_unconfirmed = any(not enroll.is_confirmed for enroll in mata_kuliah_diambil)
        
        # Get edit mode from session
        edit_mode = session.get('edit_mode', False)
        
        return render_template('mahasiswa/dashboard.html',
                             mahasiswa=mahasiswa,
                             max_sks=max_sks,
                             current_sks=current_sks,
                             mata_kuliah_diambil=mata_kuliah_diambil,
                             available_kelas=available_kelas,
                             taken_mata_kuliah_ids=taken_mata_kuliah_ids,
                             ips_history=ips_history,
                             ips_terakhir=ips_terakhir,
                             has_unconfirmed=has_unconfirmed,
                             edit_mode=edit_mode)
    except Exception as e:
        logger.error(f"Error in mahasiswa dashboard: {str(e)}", exc_info=True)
        flash('Terjadi kesalahan saat memuat dashboard', 'error')
        return redirect(url_for('login'))

def calculate_and_update_ips(mahasiswa_id, semester):
    """Calculate IPS for a student in a given semester and update the database"""
    # Get all confirmed enrollments with grades for the semester
    enrollments = Enrollment.query.join(Kelas).filter(
        Enrollment.mahasiswa_id == mahasiswa_id,
        Kelas.semester == semester,
        Enrollment.is_confirmed == True,
        Enrollment.nilai_angka != None
    ).all()
    
    if not enrollments:
        return None
    
    total_bobot = 0
    total_sks = 0
    
    # Calculate weighted average
    for enrollment in enrollments:
        # Convert numeric grade to letter grade if not already
        if not enrollment.nilai_huruf:
            if enrollment.nilai_angka >= 85:
                enrollment.nilai_huruf = 'A'
            elif enrollment.nilai_angka >= 80:
                enrollment.nilai_huruf = 'A-'
            elif enrollment.nilai_angka >= 75:
                enrollment.nilai_huruf = 'B+'
            elif enrollment.nilai_angka >= 70:
                enrollment.nilai_huruf = 'B'
            elif enrollment.nilai_angka >= 65:
                enrollment.nilai_huruf = 'B-'
            elif enrollment.nilai_angka >= 60:
                enrollment.nilai_huruf = 'C+'
            elif enrollment.nilai_angka >= 55:
                enrollment.nilai_huruf = 'C'
            elif enrollment.nilai_angka >= 40:
                enrollment.nilai_huruf = 'D'
            else:
                enrollment.nilai_huruf = 'E'
        
        # Convert letter grade to numeric value
        if enrollment.nilai_huruf == 'A':
            bobot = 4.0
        elif enrollment.nilai_huruf == 'A-':
            bobot = 3.75
        elif enrollment.nilai_huruf == 'B+':
            bobot = 3.5
        elif enrollment.nilai_huruf == 'B':
            bobot = 3.0
        elif enrollment.nilai_huruf == 'B-':
            bobot = 2.75
        elif enrollment.nilai_huruf == 'C+':
            bobot = 2.5
        elif enrollment.nilai_huruf == 'C':
            bobot = 2.0
        elif enrollment.nilai_huruf == 'D':
            bobot = 1.0
        else:  # E
            bobot = 0.0
        
        sks = enrollment.kelas.mata_kuliah.sks
        total_bobot += bobot * sks
        total_sks += sks
    
    if total_sks == 0:
        return None
    
    ips = round(total_bobot / total_sks, 2)
    
    # Update or create IPS history
    ips_history = IPSHistory.query.filter_by(
        mahasiswa_id=mahasiswa_id,
        semester=semester
    ).first()
    
    if ips_history:
        ips_history.ips = ips
    else:
        ips_history = IPSHistory(
            mahasiswa_id=mahasiswa_id,
            semester=semester,
            ips=ips
        )
        db.session.add(ips_history)
    
    # Calculate and update IPK
    mahasiswa = Mahasiswa.query.get(mahasiswa_id)
    all_ips = IPSHistory.query.filter_by(mahasiswa_id=mahasiswa_id).all()
    if all_ips:
        total_ips = sum(h.ips for h in all_ips)
        mahasiswa.ipk = round(total_ips / len(all_ips), 2)
    
    db.session.commit()
    return ips

@app.route('/dosen/update-nilai/<int:enrollment_id>', methods=['POST'])
@login_required
def update_nilai(enrollment_id):
    if current_user.role != 'dosen':
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    nilai_angka = float(data.get('nilai_angka'))
    
    # Validasi nilai
    if nilai_angka < 0 or nilai_angka > 100:
        return jsonify({'error': 'Nilai harus antara 0-100'}), 400
    
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    
    # Pastikan dosen hanya bisa memberi nilai untuk kelas yang dia ampu
    dosen = Dosen.query.filter_by(user_id=current_user.id).first()
    if enrollment.kelas.dosen_id != dosen.id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Pastikan mahasiswa sudah mengkonfirmasi mata kuliah
    if not enrollment.is_confirmed:
        return jsonify({'error': 'Mahasiswa belum mengkonfirmasi mata kuliah'}), 400
    
    enrollment.nilai_angka = nilai_angka
    
    # Konversi nilai angka ke huruf
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
    elif nilai_angka >= 55:
        enrollment.nilai_huruf = 'C'
    elif nilai_angka >= 40:
        enrollment.nilai_huruf = 'D'
    else:
        enrollment.nilai_huruf = 'E'
    
    db.session.commit()
    
    # Calculate and update IPS
    calculate_and_update_ips(enrollment.mahasiswa_id, enrollment.kelas.semester)
    
    return jsonify({
        'success': True,
        'nilai_angka': nilai_angka,
        'nilai_huruf': enrollment.nilai_huruf
    })

@app.route('/mahasiswa/ambil-kelas/<int:kelas_id>', methods=['POST'])
@login_required
def ambil_kelas(kelas_id):
    if current_user.role != 'mahasiswa':
        return redirect(url_for('login'))
    
    try:
        mahasiswa = Mahasiswa.query.filter_by(user_id=current_user.id).first()
        kelas = Kelas.query.get_or_404(kelas_id)
        
        # Check if student has already taken this course (confirmed, unconfirmed, or with grades)
        existing_enrollments = Enrollment.query.join(Kelas).filter(
            Enrollment.mahasiswa_id == mahasiswa.id,
            Kelas.mata_kuliah_id == kelas.mata_kuliah_id
        ).all()
        
        # If there are any enrollments at all for this course, prevent taking it
        if existing_enrollments:
            flash('Anda tidak dapat mengambil mata kuliah ini karena sudah terdaftar di kelas dengan mata kuliah yang sama.', 'warning')
            return redirect(url_for('mahasiswa_dashboard'))
        
        # Hitung total SKS yang sudah diambil
        current_sks = sum(enroll.kelas.mata_kuliah.sks for enroll in mahasiswa.mata_kuliah)
        max_sks = 24 if mahasiswa.ipk > 3.0 else (21 if mahasiswa.ipk > 2.5 else 18)

        if current_sks + kelas.mata_kuliah.sks <= max_sks:
            enrollment = Enrollment(mahasiswa_id=mahasiswa.id, kelas_id=kelas_id)
            db.session.add(enrollment)
            db.session.commit()
            flash('Mata kuliah berhasil ditambahkan', 'success')
            logger.info(f"Mahasiswa {mahasiswa.nim} enrolled in class {kelas.id}.")
        else:
            flash(f'Melebihi batas SKS yang diizinkan ({max_sks} SKS). Anda saat ini mengambil {current_sks} SKS.', 'error')
            logger.warning(f"Mahasiswa {mahasiswa.nim} failed to enroll in class {kelas.id}: SKS limit exceeded.")
        
        return redirect(url_for('mahasiswa_dashboard'))
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error enrolling mahasiswa in class {kelas_id}: {str(e)}", exc_info=True)
        flash(f'Gagal mengambil kelas: {str(e)}', 'error')
        return redirect(url_for('mahasiswa_dashboard'))

@app.route('/mahasiswa/batalkan-kelas/<int:enrollment_id>', methods=['POST'])
@login_required
def batalkan_kelas(enrollment_id):
    if current_user.role != 'mahasiswa':
        return redirect(url_for('login'))
    
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    if enrollment.nilai_huruf is None:  # Hanya bisa dibatalkan jika belum ada nilai
        db.session.delete(enrollment)
        db.session.commit()
        flash('Mata kuliah berhasil dibatalkan')
    else:
        flash('Tidak dapat membatalkan mata kuliah yang sudah dinilai')
    
    return redirect(url_for('mahasiswa_dashboard'))

@app.route('/admin/kelas', methods=['POST'])
@login_required
def tambah_kelas():
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    
    try:
        mata_kuliah_id = request.form.get('mata_kuliah_id')
        dosen_id = request.form.get('dosen_id')
        semester = request.form.get('semester')
        hari = request.form.get('hari')
        waktu = request.form.get('waktu')
        ruangan = request.form.get('ruangan')
        
        kelas = Kelas(
            mata_kuliah_id=mata_kuliah_id,
            dosen_id=dosen_id,
            semester=semester,
            hari=hari,
            waktu=waktu,
            ruangan=ruangan
        )
        db.session.add(kelas)
        db.session.commit()
        
        flash('Kelas berhasil ditambahkan', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menambahkan kelas: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/mata-kuliah/<int:mk_id>/delete', methods=['GET'])
@login_required
def hapus_mata_kuliah(mk_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        mata_kuliah = MataKuliah.query.get_or_404(mk_id)
        
        # Hapus semua kelas terkait
        kelas_list = Kelas.query.filter_by(mata_kuliah_id=mk_id).all()
        for kelas in kelas_list:
            # Hapus semua enrollment terkait kelas
            Enrollment.query.filter_by(kelas_id=kelas.id).delete()
            db.session.delete(kelas)
        
        db.session.delete(mata_kuliah)
        db.session.commit()
        
        flash('Mata kuliah berhasil dihapus', 'success')
        return redirect(url_for('admin_dashboard'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus mata kuliah: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/dosen/<int:dosen_id>/delete', methods=['GET'])
@login_required
def hapus_dosen(dosen_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        with db.session.no_autoflush:
            dosen = Dosen.query.get_or_404(dosen_id)
            
            # Hapus semua kelas yang diampu dosen
            kelas_list = Kelas.query.filter_by(dosen_id=dosen_id).all()
            for kelas in kelas_list:
                Enrollment.query.filter_by(kelas_id=kelas.id).delete()
                db.session.delete(kelas)
            
            # Hapus user terkait
            user = User.query.get(dosen.user_id)
            
            db.session.delete(dosen)
            
            if user:
                db.session.delete(user)
        
        db.session.commit() 
        
        flash('Dosen berhasil dihapus', 'success')
        return redirect(url_for('admin_dashboard'))
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting dosen {dosen_id}: {str(e)}", exc_info=True)
        flash(f'Gagal menghapus dosen: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/mata-kuliah/<int:mk_id>/edit', methods=['POST'])
@login_required
def edit_mata_kuliah(mk_id):
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    
    try:
        mata_kuliah = MataKuliah.query.get_or_404(mk_id)
        
        # Update data mata kuliah
        mata_kuliah.kode = request.form.get('kode')
        mata_kuliah.nama = request.form.get('nama')
        mata_kuliah.sks = int(request.form.get('sks'))
        
        db.session.commit()
        flash('Mata kuliah berhasil diperbarui', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal memperbarui mata kuliah: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/dosen/<int:dosen_id>/edit', methods=['POST'])
@login_required
def edit_dosen(dosen_id):
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    
    try:
        dosen = Dosen.query.get_or_404(dosen_id)
        
        # Update data dosen
        dosen.nip = request.form.get('nip')
        dosen.nama = request.form.get('nama')
        dosen.email = request.form.get('email')
        dosen.telepon = request.form.get('telepon')
        dosen.alamat = request.form.get('alamat')
        dosen.status = request.form.get('status') == '1'
        
        db.session.commit()
        flash('Data dosen berhasil diperbarui', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal memperbarui data dosen: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/dosen/<int:dosen_id>/detail_json', methods=['GET'])
@login_required
def detail_dosen_json(dosen_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        dosen = Dosen.query.get_or_404(dosen_id)
        return jsonify({
            'id': dosen.id,
            'nip': dosen.nip,
            'nama': dosen.nama,
            'username': dosen.user.username,
            'email': dosen.email if dosen.email else '-',
            'telepon': dosen.telepon if dosen.telepon else '-',
            'alamat': dosen.alamat if dosen.alamat else '-',
            'status': 'Aktif' if dosen.status else 'Tidak Aktif'
        })
    except Exception as e:
        logger.error(f"Error fetching dosen detail for ID {dosen_id}: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'message': 'Gagal memuat detail dosen'}), 500

@app.route('/mahasiswa/confirm-enrollment', methods=['POST'])
@login_required
def confirm_enrollment():
    if current_user.role != 'mahasiswa':
        return redirect(url_for('login'))
    
    mahasiswa = Mahasiswa.query.filter_by(user_id=current_user.id).first()
    
    try:
        # Confirm all unconfirmed enrollments
        enrollments = Enrollment.query.filter_by(mahasiswa_id=mahasiswa.id, is_confirmed=False).all()
        for enrollment in enrollments:
            enrollment.is_confirmed = True
        db.session.commit()
        flash('Pengambilan mata kuliah berhasil dikonfirmasi', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Terjadi kesalahan saat konfirmasi', 'error')
    
    return redirect(url_for('mahasiswa_dashboard'))

@app.route('/mahasiswa/toggle-edit-mode', methods=['POST'])
@login_required
def toggle_edit_mode():
    if current_user.role != 'mahasiswa':
        return redirect(url_for('login'))
    
    session['edit_mode'] = not session.get('edit_mode', False)
    return redirect(url_for('mahasiswa_dashboard'))

@app.route('/admin/kelas/<int:kelas_id>/detail')
@login_required
def detail_kelas(kelas_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        kelas = Kelas.query.get_or_404(kelas_id)
        return jsonify({
            'id': kelas.id,
            'mata_kuliah': {
                'id': kelas.mata_kuliah.id,
                'kode': kelas.mata_kuliah.kode,
                'nama': kelas.mata_kuliah.nama,
                'sks': kelas.mata_kuliah.sks
            },
            'dosen': {
                'id': kelas.dosen.id,
                'nama': kelas.dosen.nama
            },
            'semester': kelas.semester,
            'hari': kelas.hari,
            'waktu': kelas.waktu,
            'ruangan': kelas.ruangan,
            'peserta': [{
                'mahasiswa': {
                    'nim': enrollment.mahasiswa.nim,
                    'nama': enrollment.mahasiswa.nama
                },
                'is_confirmed': enrollment.is_confirmed,
                'nilai_huruf': enrollment.nilai_huruf
            } for enrollment in kelas.peserta]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/kelas/<int:kelas_id>/edit', methods=['POST'])
@login_required
def edit_kelas(kelas_id):
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    
    try:
        kelas = Kelas.query.get_or_404(kelas_id)
        kelas.mata_kuliah_id = request.form.get('mata_kuliah_id')
        kelas.dosen_id = request.form.get('dosen_id')
        kelas.semester = request.form.get('semester')
        kelas.hari = request.form.get('hari')
        kelas.waktu = request.form.get('waktu')
        kelas.ruangan = request.form.get('ruangan')
        
        db.session.commit()
        flash('Kelas berhasil diperbarui', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal memperbarui kelas: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/kelas/<int:kelas_id>/delete')
@login_required
def hapus_kelas(kelas_id):
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    
    try:
        kelas = Kelas.query.get_or_404(kelas_id)
        
        # Hapus semua enrollment terkait
        Enrollment.query.filter_by(kelas_id=kelas.id).delete()
        
        db.session.delete(kelas)
        db.session.commit()
        
        flash('Kelas berhasil dihapus', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus kelas: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/mahasiswa', methods=['POST'])
@login_required
def tambah_mahasiswa():
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        nama = request.form.get('nama')
        nim = request.form.get('nim')
        program_studi = request.form.get('program_studi')
        semester = int(request.form.get('semester'))
        
        # Cek apakah username sudah ada
        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan', 'error')
            return redirect(url_for('admin_dashboard'))
        
        # Cek apakah NIM sudah ada
        if Mahasiswa.query.filter_by(nim=nim).first():
            flash('NIM sudah terdaftar', 'error')
            return redirect(url_for('admin_dashboard'))
        
        user = User(username=username, role='mahasiswa')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        mahasiswa = Mahasiswa(
            user_id=user.id,
            nama=nama,
            nim=nim,
            program_studi=program_studi,
            semester=semester,
            ipk=0.0  # IPK awal 0
        )
        db.session.add(mahasiswa)
        db.session.commit()
        
        flash('Mahasiswa berhasil ditambahkan', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menambahkan mahasiswa: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/mahasiswa/<int:mahasiswa_id>/edit', methods=['POST'])
@login_required
def edit_mahasiswa(mahasiswa_id):
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    
    try:
        mahasiswa = Mahasiswa.query.get_or_404(mahasiswa_id)
        
        nama = request.form.get('nama')
        program_studi = request.form.get('program_studi')
        semester = int(request.form.get('semester'))
        
        # Update data mahasiswa
        mahasiswa.nama = nama
        mahasiswa.program_studi = program_studi
        mahasiswa.semester = semester
        
        db.session.commit()
        flash('Data mahasiswa berhasil diperbarui', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal memperbarui data mahasiswa: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/mahasiswa/<int:mahasiswa_id>/delete')
@login_required
def hapus_mahasiswa(mahasiswa_id):
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    
    try:
        mahasiswa = Mahasiswa.query.get_or_404(mahasiswa_id)
        user = User.query.get(mahasiswa.user_id)
        
        # Delete related records first
        Enrollment.query.filter_by(mahasiswa_id=mahasiswa.id).delete()
        IPSHistory.query.filter_by(mahasiswa_id=mahasiswa.id).delete()
        
        db.session.delete(mahasiswa)
        if user:
            db.session.delete(user)
        db.session.commit()
        
        flash('Mahasiswa berhasil dihapus', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus mahasiswa: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
