// ===========================================
// JAVASCRIPT FRONTEND UNTUK INTERAKSI API
// ===========================================
// Mengapa JavaScript di frontend?
// - JavaScript adalah bahasa pemrograman web yang berjalan di browser.
// - Kita bisa membuat aplikasi interaktif tanpa reload halaman (SPA-like).
// - Fetch API untuk komunikasi dengan backend via HTTP requests.

// Konsep-konsep yang dipelajari:
// - DOM Manipulation: Mengubah HTML secara dinamis.
// - Asynchronous Programming: Menggunakan async/await untuk API calls.
// - Event Handling: Menangani klik tombol, submit form.
// - Error Handling: Menampilkan pesan error ke user.
// - CRUD Operations: Create, Read, Update, Delete via API.

// Konstanta untuk API endpoint
// Mengapa konstanta? Agar mudah diubah jika server berubah (misal production).
const API_BASE_URL = 'http://localhost:3000'; // Ganti dengan URL server jika deploy

// ===========================================
// FUNGSI UTAMA: LOAD USERS
// ===========================================
// Fungsi ini mengambil data users dari API dan menampilkan di tabel.
async function loadUsers() {
    const loading = document.getElementById('loading');
    const table = document.getElementById('usersTable');
    const tbody = document.getElementById('usersBody');

    // Tampilkan loading
    loading.style.display = 'block';
    table.style.display = 'none';

    try {
        // Fetch data dari API
        // Mengapa fetch? Modern way untuk HTTP requests di browser.
        const response = await fetch(`${API_BASE_URL}/users`);

        // Cek apakah response sukses (status 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse JSON response
        const users = await response.json();

        // Kosongkan tabel sebelum mengisi data baru
        tbody.innerHTML = '';

        // Loop melalui setiap user dan buat row tabel
        users.forEach(user => {
            const row = document.createElement('tr');

            // Format tanggal created_at agar mudah dibaca
            const createdDate = new Date(user.created_at).toLocaleDateString('id-ID');

            row.innerHTML = `
                <td>${user.id}</td>
                <td>${user.nama}</td>
                <td>${user.email}</td>
                <td>${user.umur}</td>
                <td>${createdDate}</td>
                <td class="actions">
                    <button class="btn btn-small" onclick="editUser(${user.id})">Edit</button>
                    <button class="btn btn-danger btn-small" onclick="deleteUser(${user.id})">Hapus</button>
                </td>
            `;

            tbody.appendChild(row);
        });

        // Sembunyikan loading, tampilkan tabel
        loading.style.display = 'none';
        table.style.display = 'table';

    } catch (error) {
        console.error('Error loading users:', error);
        loading.innerHTML = '❌ Gagal memuat data. Periksa koneksi server.';
        showMessage('Gagal memuat data users. Pastikan server backend berjalan.', 'error');
    }
}

// ===========================================
// FUNGSI CREATE/UPDATE USER
// ===========================================
// Fungsi ini menangani submit form untuk tambah atau edit user.
async function saveUser(event) {
    event.preventDefault(); // Mencegah reload halaman

    // Ambil data dari form
    const userId = document.getElementById('userId').value;
    const nama = document.getElementById('nama').value.trim();
    const email = document.getElementById('email').value.trim();
    const umur = document.getElementById('umur').value;

    // Validasi sederhana di frontend (sebagai tambahan backend validation)
    if (!nama || !email || !umur) {
        showMessage('Semua field harus diisi!', 'error');
        return;
    }

    // Siapkan data untuk dikirim
    const userData = { nama, email, umur: parseInt(umur) };

    try {
        let response;
        if (userId) {
            // UPDATE: Jika ada userId, lakukan PUT request
            response = await fetch(`${API_BASE_URL}/users/${userId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });
        } else {
            // CREATE: Jika tidak ada userId, lakukan POST request
            response = await fetch(`${API_BASE_URL}/users`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });
        }

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Gagal menyimpan user');
        }

        // Tampilkan pesan sukses
        showMessage(result.message || 'User berhasil disimpan!', 'success');

        // Reset form dan reload data
        resetForm();
        loadUsers();

    } catch (error) {
        console.error('Error saving user:', error);
        showMessage(error.message, 'error');
    }
}

// ===========================================
// FUNGSI EDIT USER
// ===========================================
// Fungsi ini mengisi form dengan data user yang akan diedit.
async function editUser(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/users`);
        const users = await response.json();

        // Cari user berdasarkan ID
        const user = users.find(u => u.id == id);
        if (!user) {
            showMessage('User tidak ditemukan!', 'error');
            return;
        }

        // Isi form dengan data user
        document.getElementById('userId').value = user.id;
        document.getElementById('nama').value = user.nama;
        document.getElementById('email').value = user.email;
        document.getElementById('umur').value = user.umur;

        // Ubah judul form dan tombol
        document.getElementById('form-title').textContent = '✏️ Edit User';
        document.getElementById('submitBtn').textContent = 'Update User';
        document.getElementById('cancelBtn').style.display = 'inline-block';

        // Scroll ke form
        document.querySelector('.form-section').scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        console.error('Error editing user:', error);
        showMessage('Gagal mengambil data user untuk edit.', 'error');
    }
}

// ===========================================
// FUNGSI DELETE USER
// ===========================================
// Fungsi ini menghapus user dengan konfirmasi.
async function deleteUser(id) {
    // Konfirmasi sebelum hapus
    if (!confirm('Apakah Anda yakin ingin menghapus user ini?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/users/${id}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Gagal menghapus user');
        }

        showMessage(result.message || 'User berhasil dihapus!', 'success');
        loadUsers();

    } catch (error) {
        console.error('Error deleting user:', error);
        showMessage(error.message, 'error');
    }
}

// ===========================================
// FUNGSI HELPER
// ===========================================

// Fungsi untuk menampilkan pesan (sukses/error)
function showMessage(message, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.innerHTML = `<div class="${type}">${message}</div>`;

    // Hilangkan pesan setelah 5 detik
    setTimeout(() => {
        messageDiv.innerHTML = '';
    }, 5000);
}

// Fungsi untuk reset form ke kondisi awal
function resetForm() {
    document.getElementById('userForm').reset();
    document.getElementById('userId').value = '';
    document.getElementById('form-title').textContent = '➕ Tambah User Baru';
    document.getElementById('submitBtn').textContent = 'Simpan User';
    document.getElementById('cancelBtn').style.display = 'none';
}

// ===========================================
// EVENT LISTENERS
// ===========================================
// Jalankan saat halaman selesai load
document.addEventListener('DOMContentLoaded', () => {
    // Load data users pertama kali
    loadUsers();

    // Event listener untuk form submit
    document.getElementById('userForm').addEventListener('submit', saveUser);

    // Event listener untuk tombol cancel
    document.getElementById('cancelBtn').addEventListener('click', resetForm);
});

// ===========================================
// BEST PRACTICES & KEAMANAN FRONTEND
// ===========================================
// 1. Input Validation: Selalu validasi input di frontend sebagai first line defense.
// 2. Error Handling: Tangani error dengan pesan user-friendly.
// 3. Loading States: Tampilkan loading untuk UX yang baik.
// 4. Confirmation Dialogs: Konfirmasi untuk actions destructive seperti delete.
// 5. Async/Await: Gunakan untuk kode asynchronous yang readable.
// 6. Template Literals: Untuk dynamic HTML generation.
// 7. Event Delegation: Lebih efisien untuk dynamic elements.
// 8. Security: Jangan pernah kirim password atau data sensitif tanpa HTTPS.
// 9. CORS: Pastikan backend mengizinkan requests dari frontend origin.
// 10. Testing: Test di berbagai browser dan device.

// Catatan untuk Production:
// - Gunakan HTTPS untuk semua komunikasi.
// - Implement authentication (JWT, sessions) untuk secure API.
// - Minify dan bundle JavaScript untuk performa.
// - Add service worker untuk offline capability.
// - Monitor errors dengan tools seperti Sentry.
