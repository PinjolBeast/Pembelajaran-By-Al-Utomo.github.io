-- ===========================================
-- SCHEMA DATABASE UNTUK APLIKASI PEMBELAJARAN FULL-STACK
-- ===========================================
-- Mengapa menggunakan MySQL? Karena MySQL adalah database relasional yang populer,
-- stabil, dan cocok untuk aplikasi web sederhana. Kita akan membuat tabel 'users'
-- untuk menyimpan data pengguna dengan operasi CRUD (Create, Read, Update, Delete).

-- Langkah 1: Membuat Database
-- Database adalah wadah untuk menyimpan tabel-tabel. Kita beri nama 'pembelajaran_db'.
CREATE DATABASE IF NOT EXISTS pembelajaran_db;

-- Menggunakan database yang baru dibuat
USE pembelajaran_db;

-- Langkah 2: Membuat Tabel Users
-- Tabel ini akan menyimpan informasi pengguna.
-- Kolom-kolom:
-- - id: Primary key, auto-increment untuk ID unik
-- - nama: Nama pengguna (VARCHAR untuk teks pendek)
-- - email: Email pengguna (UNIQUE untuk mencegah duplikasi)
-- - umur: Umur pengguna (INT untuk angka)
-- - created_at: Timestamp pembuatan record (TIMESTAMP untuk waktu)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    umur INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mengapa struktur ini?
-- - AUTO_INCREMENT: Agar ID otomatis bertambah tanpa manual input.
-- - NOT NULL: Memastikan kolom tidak kosong.
-- - UNIQUE pada email: Mencegah email duplikat.
-- - TIMESTAMP: Untuk tracking kapan data dibuat.

-- Langkah 3: Insert Data Awal (Opsional untuk Testing)
-- Kita masukkan beberapa data dummy agar aplikasi bisa langsung ditest.
INSERT INTO users (nama, email, umur) VALUES
('Bimo Prayogo', 'bimo@example.com', 25),
('Naufal Rahman', 'naufal@example.com', 22),
('Siti Aminah', 'siti@example.com', 28);

-- Mengapa insert data awal? Untuk memudahkan testing tanpa harus input manual pertama kali.
