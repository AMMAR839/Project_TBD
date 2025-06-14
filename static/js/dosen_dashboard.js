// Modal functionality
const modal = document.getElementById("modalInputNilai");
const span = document.getElementsByClassName("close")[0];

function inputNilai(enrollmentId) {
    document.getElementById('enrollment_id').value = enrollmentId;
    modal.style.display = "block";
    
    // Get existing grade if any
    const nilaiAngka = document.getElementById(`nilai-angka-${enrollmentId}`).textContent.trim();
    if (nilaiAngka !== '-') {
        document.getElementById('nilai_angka').value = nilaiAngka;
    } else {
        document.getElementById('nilai_angka').value = '';
    }
}

function closeModal() {
    modal.style.display = "none";
}

// Event Listeners
span.onclick = closeModal;

window.onclick = function(event) {
    if (event.target == modal) {
        closeModal();
    }
}

// Form submission
function submitNilai(event) {
    event.preventDefault();
    const enrollmentId = document.getElementById('enrollment_id').value;
    const nilaiAngka = document.getElementById('nilai_angka').value;

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
            closeModal();
            showNotification('Nilai berhasil disimpan', 'success');
        } else {
            showNotification(data.error || 'Terjadi kesalahan', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Terjadi kesalahan', 'error');
    });
}

// Notification system
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }, 100);
}

// Initialize event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Form submission handler
    const formNilai = document.getElementById('formNilai');
    if (formNilai) {
        formNilai.addEventListener('submit', submitNilai);
    }
}); 