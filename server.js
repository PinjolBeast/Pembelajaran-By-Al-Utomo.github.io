// ===========================================
// SERVER BACKEND DENGAN EXPRESS.JS
// ===========================================
// Mengapa menggunakan Express.js?
// - Framework minimal untuk Node.js yang memudahkan routing dan middleware.
// - Cepat setup, banyak middleware siap pakai untuk keamanan dan parsing.
// - Cocok untuk API RESTful yang akan kita buat untuk operasi CRUD.

// Mengapa struktur ini?
// - Import dependencies di atas.
// - Setup middleware (CORS, body-parser).
// - Definisi routes CRUD.
// - Jalankan server di port tertentu.

// Import dependencies
const express = require('express'); // Framework web untuk Node.js
const cors = require('cors');       // Middleware untuk Cross-Origin Resource Sharing
const bodyParser = require('body-parser'); // Middleware untuk parsing JSON dari request body
const db = require('./db');         // Koneksi database dari file db.js

// Inisialisasi aplikasi Express
const app = express();
const PORT = 3000; // Port server (bisa diganti, tapi pastikan tidak konflik)

// ===========================================
// MIDDLEWARE SETUP
// ===========================================
// Middleware adalah fungsi yang dijalankan sebelum request sampai ke route handler.
// Mereka memproses request secara otomatis.

// 1. CORS Middleware
// Mengapa CORS? Agar frontend (HTML/JS) bisa mengakses API dari domain berbeda.
// Tanpa ini, browser akan block request dari localhost ke localhost:3000.
app.use(cors());

// 2. Body Parser Middleware
// Mengapa? Untuk parsing JSON dari request body (POST/PUT data).
// extended: true untuk parsing nested objects.
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// ===========================================
// ROUTES CRUD UNTUK USERS
// ===========================================
// CRUD: Create, Read, Update, Delete
// Kita buat API endpoints yang bisa diakses frontend via fetch().

// 1. READ: GET /users - Mengambil semua users
app.get('/users', (req, res) => {
    // Query SQL untuk select semua data dari tabel users
    const query = 'SELECT * FROM users ORDER BY created_at DESC';

    // Menggunakan prepared statement (aman dari SQL injection)
    db.query(query, (err, results) => {
        if (err) {
            console.error('Error fetching users:', err);
            return res.status(500).json({ error: 'Gagal mengambil data users' });
        }
        // Kirim response JSON dengan data users
        res.json(results);
    });
});

// 2. CREATE: POST /users - Menambah user baru
app.post('/users', (req, res) => {
    // Ambil data dari request body
    const { nama, email, umur } = req.body;

    // Validasi input sederhana
    // Mengapa validasi? Mencegah data kosong atau invalid masuk database.
    if (!nama || !email || !umur) {
        return res.status(400).json({ error: 'Nama, email, dan umur harus diisi' });
    }

    // Validasi email sederhana (regex)
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        return res.status(400).json({ error: 'Format email tidak valid' });
    }

    // Validasi umur (harus angka positif)
    if (isNaN(umur) || umur < 1 || umur > 120) {
        return res.status(400).json({ error: 'Umur harus angka antara 1-120' });
    }

    // Query INSERT dengan prepared statement
    const query = 'INSERT INTO users (nama, email, umur) VALUES (?, ?, ?)';
    db.query(query, [nama, email, umur], (err, result) => {
        if (err) {
            console.error('Error creating user:', err);
            // Handle duplicate email
            if (err.code === 'ER_DUP_ENTRY') {
                return res.status(400).json({ error: 'Email sudah terdaftar' });
            }
            return res.status(500).json({ error: 'Gagal menambah user' });
        }
        // Kirim response sukses dengan ID user baru
        res.status(201).json({
            message: 'User berhasil ditambahkan',
            id: result.insertId
        });
    });
});

// 3. UPDATE: PUT /users/:id - Update user berdasarkan ID
app.put('/users/:id', (req, res) => {
    const { id } = req.params; // Ambil ID dari URL parameter
    const { nama, email, umur } = req.body;

    // Validasi ID (harus angka)
    if (isNaN(id)) {
        return res.status(400).json({ error: 'ID user tidak valid' });
    }

    // Validasi input sama seperti CREATE
    if (!nama || !email || !umur) {
        return res.status(400).json({ error: 'Nama, email, dan umur harus diisi' });
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        return res.status(400).json({ error: 'Format email tidak valid' });
    }

    if (isNaN(umur) || umur < 1 || umur > 120) {
        return res.status(400).json({ error: 'Umur harus angka antara 1-120' });
    }

    // Query UPDATE dengan prepared statement
    const query = 'UPDATE users SET nama = ?, email = ?, umur = ? WHERE id = ?';
    db.query(query, [nama, email, umur, id], (err, result) => {
        if (err) {
            console.error('Error updating user:', err);
            if (err.code === 'ER_DUP_ENTRY') {
                return res.status(400).json({ error: 'Email sudah digunakan user lain' });
            }
            return res.status(500).json({ error: 'Gagal update user' });
        }
        // Cek apakah ada row yang terupdate
        if (result.affectedRows === 0) {
            return res.status(404).json({ error: 'User tidak ditemukan' });
        }
        res.json({ message: 'User berhasil diupdate' });
    });
});

// 4. DELETE: DELETE /users/:id - Hapus user berdasarkan ID
app.delete('/users/:id', (req, res) => {
    const { id } = req.params;

    // Validasi ID
    if (isNaN(id)) {
        return res.status(400).json({ error: 'ID user tidak valid' });
    }

    // Query DELETE dengan prepared statement
    const query = 'DELETE FROM users WHERE id = ?';
    db.query(query, [id], (err, result) => {
        if (err) {
            console.error('Error deleting user:', err);
            return res.status(500).json({ error: 'Gagal hapus user' });
        }
        if (result.affectedRows === 0) {
            return res.status(404).json({ error: 'User tidak ditemukan' });
        }
        res.json({ message: 'User berhasil dihapus' });
    });
});

// ===========================================
// JALANKAN SERVER
// ===========================================
// Server akan listen di port yang ditentukan
app.listen(PORT, () => {
    console.log(`Server berjalan di http://localhost:${PORT}`);
    console.log('API endpoints:');
    console.log('GET    /users     - Ambil semua users');
    console.log('POST   /users     - Tambah user baru');
    console.log('PUT    /users/:id - Update user');
    console.log('DELETE /users/:id - Hapus user');
});

// ===========================================
// BEST PRACTICES & KEAMANAN
// ===========================================
// 1. Prepared Statements: Menggunakan ? placeholders untuk mencegah SQL injection.
// 2. Input Validation: Validasi semua input user sebelum proses.
// 3. Error Handling: Tangani error dengan response JSON yang informatif.
// 4. CORS: Diaktifkan untuk development, tapi di production sesuaikan origin.
// 5. Logging: Console.error untuk debugging error database.
// 6. Status Codes: Gunakan HTTP status codes yang tepat (200, 201, 400, 404, 500).
// 7. Security Headers: Di production, tambahkan helmet middleware untuk security headers.
// 8. Rate Limiting: Tambahkan express-rate-limit untuk mencegah abuse.
// 9. Environment Variables: Pindahkan konfigurasi sensitif (password, port) ke .env file.
// 10. Testing: Test semua endpoints dengan tools seperti Postman atau Thunder Client.
