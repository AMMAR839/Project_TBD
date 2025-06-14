// Add event listeners when the document is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Handle form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields');
            }
        });
    });
});

function showAddMataKuliahForm() {
    document.getElementById('addMataKuliahForm').style.display = 'block';
}

function showAddDosenForm() {
    document.getElementById('addDosenForm').style.display = 'block';
}

function editMataKuliah(id) {
    // Implementasi edit mata kuliah
    console.log('Edit mata kuliah:', id);
}

function deleteMataKuliah(id) {
    if (confirm('Apakah Anda yakin ingin menghapus mata kuliah ini?')) {
        // Implementasi delete mata kuliah
        console.log('Delete mata kuliah:', id);
    }
}

function editDosen(id) {
    // Implementasi edit dosen
    console.log('Edit dosen:', id);
}

function deleteDosen(id) {
    if (confirm('Apakah Anda yakin ingin menghapus dosen ini?')) {
        // Implementasi delete dosen
        console.log('Delete dosen:', id);
    }
}

function updateGrade(enrollmentId) {
    const newGrade = prompt('Masukkan nilai baru (0-4):');
    if (newGrade !== null) {
        fetch(`/teacher/update-grade/${enrollmentId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ grade: newGrade })
        }).then(() => {
            document.getElementById(`grade-${enrollmentId}`).textContent = newGrade;
        });
    }
}

function updateNilai(enrollmentId) {
    const nilaiAngka = prompt('Masukkan nilai angka (0-100):');
    if (nilaiAngka !== null) {
        fetch(`/dosen/update-nilai/${enrollmentId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nilai_angka: nilaiAngka })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById(`nilai-angka-${enrollmentId}`).textContent = data.nilai_angka;
                document.getElementById(`nilai-huruf-${enrollmentId}`).textContent = data.nilai_huruf;
            }
        });
    }
} 