// Tab functionality
function openTab(tabId) {
    // Hide all tab contents with fade out
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.opacity = '0';
        setTimeout(() => {
            tab.classList.remove('active');
            if (tab.id === tabId) {
                // Show selected tab with fade in
                tab.classList.add('active');
                setTimeout(() => {
                    tab.style.opacity = '1';
                }, 50);
            }
        }, 300);
    });
    
    // Update tab buttons
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });
    event.currentTarget.classList.add('active');
}

// Modal functionality
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = "block";
    document.body.classList.add('modal-open');
    
    // Center modal content vertically
    const modalContent = modal.querySelector('.modal-content');
    const windowHeight = window.innerHeight;
    const modalHeight = modalContent.offsetHeight;
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (modalHeight < windowHeight) {
        modalContent.style.marginTop = Math.max(20, (windowHeight - modalHeight) / 2) + 'px';
    } else {
        modalContent.style.marginTop = '20px';
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = "none";
    document.body.classList.remove('modal-open');
}

// CRUD Operations
function deleteMataKuliah(id) {
    if (confirm('Apakah Anda yakin ingin menghapus mata kuliah ini? Semua kelas terkait juga akan dihapus.')) {
        window.location.href = `/admin/mata-kuliah/${id}/delete`;
    }
}

function deleteDosen(id) {
    if (confirm('Apakah Anda yakin ingin menghapus dosen ini? Semua kelas yang diampu dosen ini juga akan dihapus.')) {
        window.location.href = `/admin/dosen/${id}/delete`;
    }
}

function editMataKuliah(id) {
    const row = document.querySelector(`tr[data-mk-id="${id}"]`);
    const kode = row.cells[0].textContent;
    const nama = row.cells[1].textContent;
    const sks = row.cells[2].textContent;
    
    document.getElementById('edit_kode').value = kode;
    document.getElementById('edit_nama').value = nama;
    document.getElementById('edit_sks').value = sks;
    
    document.getElementById('formEditMataKuliah').action = `/admin/mata-kuliah/${id}/edit`;
    
    showModal('modalEditMataKuliah');
}

function viewDosen(id) {
    // Fetch lecturer details from the server
    fetch(`/admin/dosen/${id}/detail_json`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            // Update values
            document.getElementById('view_nip').innerHTML = `<span>${data.nip}</span>`;
            document.getElementById('view_nama').innerHTML = `<span>${data.nama}</span>`;
            document.getElementById('view_username').innerHTML = `<span>${data.username}</span>`;
            document.getElementById('view_email').innerHTML = `<span>${data.email}</span>`;
            document.getElementById('view_telepon').innerHTML = `<span>${data.telepon}</span>`;
            document.getElementById('view_alamat').innerHTML = `<span>${data.alamat}</span>`;
            
            // Update status badge
            const statusElement = document.getElementById('view_status');
            statusElement.textContent = data.status;
            statusElement.className = 'status-badge ' + (data.status === 'Aktif' ? 'active' : 'inactive');
            
            showModal('modalViewDosen');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Terjadi kesalahan saat mengambil data dosen');
        });
}

function editDosen(id) {
    const row = document.querySelector(`tr[data-dosen-id="${id}"]`);
    const nip = row.cells[0].textContent;
    const nama = row.cells[1].textContent;
    const email = row.cells[3].textContent !== '-' ? row.cells[3].textContent : '';
    const telepon = row.cells[4].textContent !== '-' ? row.cells[4].textContent : '';
    const status = row.querySelector('.status-badge').classList.contains('active') ? '1' : '0';
    
    document.getElementById('edit_nip').value = nip;
    document.getElementById('edit_nama_dosen').value = nama;
    document.getElementById('edit_email').value = email;
    document.getElementById('edit_telepon').value = telepon;
    document.getElementById('edit_status').value = status;
    
    document.getElementById('formEditDosen').action = `/admin/dosen/${id}/edit`;
    
    showModal('modalEditDosen');
}

function editMahasiswa(id) {
    const row = document.querySelector(`tr[data-mahasiswa-id="${id}"]`);
    const nama = row.cells[1].textContent;
    const program_studi = row.cells[2].textContent;
    const semester = row.cells[3].textContent;
    
    document.getElementById('edit_nama').value = nama;
    document.getElementById('edit_program_studi').value = program_studi;
    document.getElementById('edit_semester').value = semester;
    
    document.getElementById('formEditMahasiswa').action = `/admin/mahasiswa/${id}/edit`;
    
    showModal('modalEditMahasiswa');
}

function editKelas(id) {
    const row = document.querySelector(`tr[data-kelas-id="${id}"]`);
    const [kode, nama] = row.cells[0].textContent.split(' - ');
    const dosen = row.cells[1].textContent;
    const semester = row.cells[2].textContent;
    const [hari, waktu] = row.cells[3].textContent.split(', ');
    const ruangan = row.cells[4].textContent;
    
    // Set mata kuliah
    const mataKuliahSelect = document.getElementById('edit_mata_kuliah_id');
    Array.from(mataKuliahSelect.options).forEach(option => {
        if (option.text.includes(kode)) {
            option.selected = true;
        }
    });
    
    // Set dosen
    const dosenSelect = document.getElementById('edit_dosen_id');
    Array.from(dosenSelect.options).forEach(option => {
        if (option.text === dosen) {
            option.selected = true;
        }
    });
    
    document.getElementById('edit_semester').value = semester;
    document.getElementById('edit_hari').value = hari;
    document.getElementById('edit_waktu').value = waktu;
    document.getElementById('edit_ruangan').value = ruangan;
    
    document.getElementById('formEditKelas').action = `/admin/kelas/${id}/edit`;
    
    showModal('modalEditKelas');
}

function deleteMahasiswa(id) {
    if (confirm('Apakah Anda yakin ingin menghapus mahasiswa ini? Semua data terkait mahasiswa ini juga akan dihapus.')) {
        window.location.href = `/admin/mahasiswa/${id}/delete`;
    }
}

function deleteKelas(id) {
    if (confirm('Apakah Anda yakin ingin menghapus kelas ini? Semua data terkait kelas ini juga akan dihapus.')) {
        window.location.href = `/admin/kelas/${id}/delete`;
    }
}

function viewKelasDetail(id) {
    fetch(`/admin/kelas/${id}/detail`)
        .then(response => response.json())
        .then(data => {
            // Tampilkan informasi kelas
            const kelasInfo = document.getElementById('kelasInfo');
            kelasInfo.innerHTML = `
                <div class="detail-grid">
                    <div class="detail-item">
                        <div class="detail-label">Mata Kuliah</div>
                        <div class="detail-value-container">
                            <div class="detail-value">${data.mata_kuliah.kode} - ${data.mata_kuliah.nama}</div>
                        </div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">SKS:</div>
                        <div class="detail-value-container">
                            <div class="detail-value">${data.mata_kuliah.sks}</div>
                        </div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Dosen:</div>
                        <div class="detail-value-container">
                            <div class="detail-value">${data.dosen.nama}</div>
                        </div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Semester:</div>
                        <div class="detail-value-container">
                            <div class="detail-value">${data.semester}</div>
                        </div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Jadwal:</div>
                        <div class="detail-value-container">
                            <div class="detail-value">${data.hari}, ${data.waktu}</div>
                        </div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Ruangan:</div>
                        <div class="detail-value-container">
                            <div class="detail-value">${data.ruangan}</div>
                        </div>
                    </div>
                </div>
            `;

            // Tampilkan daftar mahasiswa
            const tbody = document.querySelector('#kelasStudentList tbody');
            tbody.innerHTML = '';
            data.peserta.forEach(p => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${p.mahasiswa.nim}</td>
                    <td>${p.mahasiswa.nama}</td>
                    <td>${p.is_confirmed ? '<span class="badge badge-success">Terkonfirmasi</span>' : '<span class="badge badge-warning">Menunggu</span>'}</td>
                    <td>${p.nilai_huruf || '-'}</td>
                `;
                tbody.appendChild(row);
            });

            showModal('modalKelasDetail');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Gagal memuat detail kelas');
        });
}

// Event Listeners
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        hideModal(event.target.id);
    }
}

window.addEventListener('resize', function() {
    const openModal = document.querySelector('.modal[style*="display: block"]');
    if (openModal) {
        const modalContent = openModal.querySelector('.modal-content');
        const windowHeight = window.innerHeight;
        const modalHeight = modalContent.offsetHeight;
        
        if (modalHeight < windowHeight) {
            modalContent.style.marginTop = Math.max(20, (windowHeight - modalHeight) / 2) + 'px';
        } else {
            modalContent.style.marginTop = '20px';
        }
    }
});

// Prevent modal content click from closing modal
document.querySelectorAll('.modal-content').forEach(content => {
    content.addEventListener('click', function(e) {
        e.stopPropagation();
    });
}); 