// ===========================================
// KONFIGURASI KONEKSI DATABASE MYSQL
// ===========================================
// Mengapa perlu file terpisah untuk koneksi database?
// - Separation of Concerns: Memisahkan logika koneksi dari logika aplikasi utama.
// - Reusability: File ini bisa digunakan di berbagai bagian aplikasi.
// - Security: Konfigurasi database (password, dll) bisa diatur di satu tempat.
// - Best Practice: Menggunakan connection pool untuk performa dan stabilitas.

const mysql = require('mysql2');

// Mengapa mysql2? Karena mendukung prepared statements untuk keamanan SQL injection.
// Tidak menggunakan mysql biasa karena kurang aman untuk input user.

// Konfigurasi koneksi database
// Ganti nilai-nilai ini sesuai dengan setup MySQL Anda
const dbConfig = {
    host: 'localhost',        // Alamat server MySQL (biasanya localhost untuk lokal)
    user: 'root',             // Username MySQL (default root)
    password: '',             // Password MySQL (kosongkan jika default)
    database: 'pembelajaran_db', // Nama database yang dibuat di schema.sql
    waitForConnections: true, // Tunggu koneksi jika pool penuh
    connectionLimit: 10,      // Maksimal 10 koneksi simultan
    queueLimit: 0             // Tidak ada batas antrian
};

// Mengapa connection pool?
// - Performansi: Membuat koneksi baru mahal, pool reuse koneksi existing.
// - Scalability: Menangani banyak request tanpa membuat koneksi berlebihan.
// - Stabilitas: Otomatis manage koneksi rusak.

const pool = mysql.createPool(dbConfig);

// Export pool agar bisa digunakan di file lain (seperti server.js)
module.exports = pool;

// Cara menggunakan:
// const db = require('./db');
// db.query('SELECT * FROM users', (err, results) => { ... });

// Keamanan: Jangan commit password ke Git. Gunakan environment variables di production.
// Contoh: password: process.env.DB_PASSWORD
