// Initialize IPS Chart
function initializeIPSChart(ipsData) {
    const ctx = document.getElementById('ipsChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ipsData.map(d => d.semester),
            datasets: [{
                label: 'IPS',
                data: ipsData.map(d => d.ips),
                borderColor: '#007bff',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 4
                }
            }
        }
    });
}

// Filter mata kuliah
function filterMataKuliah() {
    // Get filter values for available courses
    const searchTersedia = document.getElementById('searchMatkul')?.value.toLowerCase() || '';
    const hariTersedia = document.getElementById('filterHari')?.value || '';
    
    // Get filter values for enrolled courses
    const searchDiambil = document.getElementById('searchMatkulDiambil')?.value.toLowerCase() || '';
    const hariDiambil = document.getElementById('filterHariDiambil')?.value || '';
    
    // Filter available courses
    const availableCards = document.querySelectorAll('.available-courses .course-card');
    availableCards.forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        const cardHari = card.dataset.hari;
        
        const matchSearch = !searchTersedia || title.includes(searchTersedia);
        const matchHari = !hariTersedia || cardHari === hariTersedia;
        
        card.style.display = matchSearch && matchHari ? 'block' : 'none';
    });

    // Filter enrolled courses
    const enrolledCards = document.querySelectorAll('.enrolled-courses .course-card');
    enrolledCards.forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        const cardHari = card.dataset.hari;
        
        const matchSearch = !searchDiambil || title.includes(searchDiambil);
        const matchHari = !hariDiambil || cardHari === hariDiambil;
        
        card.style.display = matchSearch && matchHari ? 'block' : 'none';
    });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Initialize search and filter functionality
    const searchMatkul = document.getElementById('searchMatkul');
    const searchMatkulDiambil = document.getElementById('searchMatkulDiambil');
    const filterHari = document.getElementById('filterHari');
    const filterHariDiambil = document.getElementById('filterHariDiambil');
    
    // Add event listeners for available courses filters
    if (searchMatkul) {
        searchMatkul.addEventListener('input', filterMataKuliah);
        searchMatkul.addEventListener('change', filterMataKuliah);
    }
    
    if (filterHari) {
        filterHari.addEventListener('change', filterMataKuliah);
    }
    
    // Add event listeners for enrolled courses filters
    if (searchMatkulDiambil) {
        searchMatkulDiambil.addEventListener('input', filterMataKuliah);
        searchMatkulDiambil.addEventListener('change', filterMataKuliah);
    }

    if (filterHariDiambil) {
        filterHariDiambil.addEventListener('change', filterMataKuliah);
    }

    // Run initial filter
    filterMataKuliah();

    // Initialize IPS Chart if data exists
    try {
        const ipsData = JSON.parse(document.getElementById('ips-data').textContent);
        if (ipsData && Array.isArray(ipsData) && ipsData.length > 0) {
            initializeIPSChart(ipsData);
        }
    } catch (error) {
        console.error('Error initializing IPS chart:', error);
    }
}); 