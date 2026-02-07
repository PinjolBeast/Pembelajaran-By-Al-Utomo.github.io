# 🚀 Pembelajaran Full-Stack Web Development

Proyek pembelajaran komprehensif untuk belajar pengembangan web full-stack dari dasar hingga mahir. Dibuat dengan bahasa Indonesia untuk memudahkan pemula dalam memahami konsep-konsep programming.

## 👨‍💻 Pengembang

**Al Utomo**
- 📧 Email: [jendelapintugt@gmail.com](mailto:jendelapintugt@gmail.com)
- 📸 Instagram: [@alutomo1](https://instagram.com/alutomo1)

## 📋 Daftar Isi

- [Fitur Utama](#-fitur-utama)
- [Struktur Proyek](#-struktur-proyek)
- [Teknologi yang Digunakan](#-teknologi-yang-digunakan)
- [Instalasi dan Setup](#-instalasi-dan-setup)
- [Cara Penggunaan](#-cara-penggunaan)
- [AI Tutor System](#-ai-tutor-system)
- [Database Setup](#-database-setup)
- [API Endpoints](#-api-endpoints)
- [Kontribusi](#-kontribusi)
- [Lisensi](#-lisensi)

## 🎯 Fitur Utama

### 🌐 Frontend Components
- **Halaman Utama (index.html)**: Profil pribadi dengan foto dan link sosial media
- **Hub Pembelajaran (hub.html)**: Navigasi terpusat ke semua halaman pembelajaran
- **Aplikasi Manajemen User (app.html)**: Full-stack CRUD application
- **Pembelajaran Dasar (basic.html)**: Tutorial HTML, CSS, dan JavaScript
- **Panduan CSS Lengkap (css-guide.html)**: Referensi komprehensif CSS
- **AI Tutor Web (ai_tutor.html)**: Interface web untuk sistem quiz interaktif

### 🔧 Backend Services
- **Node.js Server (server.js)**: RESTful API untuk manajemen data
- **Database MySQL**: Penyimpanan data terstruktur
- **Flask Web App (ai_tutor_web.py)**: Web interface untuk AI Tutor

### 🤖 AI Tutor System
- **Python CLI Tutor (ai_tutor.py)**: Interactive terminal-based learning
- **Web-based Quiz System**: Browser-based testing dengan progress tracking
- **Multi-subject Coverage**: HTML, CSS, JavaScript, dan Python
- **Progress Persistence**: Menyimpan hasil belajar di localStorage

### 🔒 Keamanan Web
- **Security Learning (secuirty.html)**: Tutorial keamanan web
- **Input Validation**: Validasi data di frontend dan backend
- **SQL Injection Prevention**: Prepared statements
- **CORS Configuration**: Cross-origin resource sharing setup

## 📁 Struktur Proyek

```
pembelajaran/
├── 📄 index.html                 # Halaman utama/profil
├── 📄 hub.html                   # Hub navigasi
├── 📄 app.html                   # Aplikasi manajemen user
├── 📄 basic.html                 # Tutorial dasar
├── 📄 css-guide.html             # Panduan CSS lengkap
├── 📄 secuirty.html              # Tutorial keamanan
├── 📄 ai_tutor.html              # AI Tutor web interface
├── 📄 quiz.html                  # Sistem quiz (legacy)
├── 📄 contoh_html_ai_tutor.html  # Contoh file dari AI Tutor
├── 📄 contoh_css.css             # Contoh CSS dari AI Tutor
├── 📄 contoh_js.js               # Contoh JavaScript dari AI Tutor
│
├── 🐍 ai_tutor.py                # AI Tutor Python (CLI)
├── 🐍 ai_tutor_web.py            # AI Tutor Flask web app
├── 🐍 ai_tutor_commented.py      # Versi berkomentar AI Tutor
│
├── 📄 server.js                  # Backend Node.js
├── 📄 db.js                      # Konfigurasi database
├── 📄 package.json               # Dependencies Node.js
├── 📄 requirements.txt           # Dependencies Python
├── 📄 schema.sql                 # Schema database MySQL
│
├── 🎨 css/
│   └── 📄 style.css              # Global CSS styles
│
├── 📜 js/
│   ├── 📄 app.js                 # Frontend logic untuk app.html
│   ├── 📄 main.js                # Utility functions
│   ├── 📄 security.js            # Security utilities
│   ├── 📄 soal.js                # Quiz system (Node.js)
│   ├── 📄 tka.js                 # Tryout system
│   └── 📄 quiz.js                # Web quiz system (legacy)
│
├── 🖼️ img/
│   ├── 📄 aal.jpg                # Gambar profil
│   └── 📄 bomo.jpg               # Gambar tambahan
│
├── 📊 student_progress.json      # Progress belajar siswa
├── 📄 TODO.md                    # Task list proyek
├── 📄 Update.md                  # Changelog
├── 📄 PERBAIKAN_ERROR.md         # Log perbaikan
└── 📄 README.md                  # Dokumentasi ini
```

## 🛠️ Teknologi yang Digunakan

### Frontend
- **HTML5**: Semantic markup dan struktur halaman
- **CSS3**: Styling, animations, dan responsive design
- **JavaScript (ES6+)**: Interaktivitas dan DOM manipulation
- **Local Storage**: Persistent data storage

### Backend
- **Node.js**: Runtime JavaScript untuk server
- **Express.js**: Web framework untuk REST API
- **Python Flask**: Web framework untuk AI Tutor web
- **MySQL**: Relational database management

### Development Tools
- **VS Code**: Code editor utama
- **Git**: Version control
- **npm**: Package manager untuk Node.js
- **pip**: Package manager untuk Python

## 🚀 Instalasi dan Setup

### 1. Persiapan Environment

```bash
# Pastikan Node.js terinstall (versi 14+)
node --version

# Pastikan Python 3.x terinstall
python --version

# Pastikan MySQL terinstall dan running
mysql --version
```

### 2. Setup Backend (Node.js)

```bash
# Install dependencies
npm install

# Setup database MySQL
mysql -u root -p < schema.sql

# Jalankan server
npm start
# atau untuk development
npm run dev
```

### 3. Setup AI Tutor Python

```bash
# Install dependencies Python (jika diperlukan)
pip install flask

# Jalankan AI Tutor CLI
python ai_tutor.py

# Jalankan AI Tutor Web (opsional)
python ai_tutor_web.py
```

### 4. Akses Aplikasi

- **Frontend**: Buka `hub.html` di browser
- **API Backend**: `http://localhost:3000`
- **AI Tutor Web**: `http://localhost:5000`

## 📖 Cara Penggunaan

### Menggunakan Hub Pembelajaran

1. **Buka `hub.html`** di browser favorit Anda
2. **Pilih topik** yang ingin dipelajari dari grid menu
3. **Ikuti tutorial** dan contoh kode yang disediakan
4. **Praktik langsung** dengan mengedit file contoh

### Menggunakan AI Tutor

#### Versi Command Line:
```bash
python ai_tutor.py
```
- Pilih materi yang ingin dipelajari
- Ikuti quiz interaktif
- Lihat progress pembelajaran

#### Versi Web:
- Buka `ai_tutor.html` di browser
- Pilih kategori quiz (HTML/CSS/JavaScript)
- Jawab pertanyaan dan lihat penjelasan

### Menggunakan Aplikasi CRUD

1. **Buka `app.html`** di browser
2. **Connect ke API** backend yang sedang running
3. **Tambah/Edit/Hapus** data user
4. **Lihat hasil** di tabel real-time

## 🤖 AI Tutor System

### Fitur AI Tutor Python
- **Interactive Learning**: Pembelajaran step-by-step dengan bahasa Indonesia
- **Quiz System**: 10 soal per materi dengan penjelasan detail
- **Progress Tracking**: Simpan progress belajar ke file JSON
- **File Generation**: Buat file contoh HTML/CSS/JS otomatis
- **Multi-subject**: HTML, CSS, JavaScript, dan Python

### Fitur AI Tutor Web
- **Browser-based**: Tidak perlu install Python
- **Visual Interface**: UI modern dengan animasi
- **Progress Persistence**: Simpan hasil ke localStorage
- **Responsive Design**: Compatible dengan mobile

### Materi Pembelajaran
- **HTML**: Tags, attributes, semantic elements, forms
- **CSS**: Properties, selectors, Flexbox, Grid, animations
- **JavaScript**: Variables, functions, DOM, events, ES6+
- **Python**: Basic syntax, data structures, OOP, file handling

## 🗄️ Database Setup

### MySQL Database Schema

```sql
-- Buat database
CREATE DATABASE pembelajaran;

-- Gunakan database
USE pembelajaran;

-- Tabel users untuk aplikasi CRUD
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert data contoh
INSERT INTO users (name, email, age) VALUES
('John Doe', 'john@example.com', 25),
('Jane Smith', 'jane@example.com', 30);
```

### Konfigurasi Database Connection

**File `db.js`:**
```javascript
const mysql = require('mysql');

const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '', // Sesuaikan dengan password MySQL Anda
    database: 'pembelajaran'
});

module.exports = connection;
```

## 🔗 API Endpoints

### User Management API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | Ambil semua users |
| GET | `/api/users/:id` | Ambil user by ID |
| POST | `/api/users` | Tambah user baru |
| PUT | `/api/users/:id` | Update user |
| DELETE | `/api/users/:id` | Hapus user |

### AI Tutor API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Halaman home AI Tutor |
| GET | `/quiz` | Halaman kategori quiz |
| GET | `/quiz/<category>` | Quiz spesifik kategori |
| POST | `/update_progress/<lesson>` | Update progress belajar |

## 🤝 Kontribusi

Proyek ini dibuat untuk tujuan pembelajaran. Jika Anda ingin berkontribusi:

1. **Fork** repositori ini
2. **Buat branch** untuk fitur baru (`git checkout -b feature/AmazingFeature`)
3. **Commit** perubahan Anda (`git commit -m 'Add some AmazingFeature'`)
4. **Push** ke branch (`git push origin feature/AmazingFeature`)
5. **Buka Pull Request**

### Cara Berkontribusi:
- Tambah materi pembelajaran baru
- Perbaiki bug atau error
- Improve UI/UX
- Tambah fitur keamanan
- Buat dokumentasi lebih detail

## 📄 Lisensi

Proyek ini dibuat untuk tujuan pembelajaran dan pendidikan. Bebas digunakan untuk:

- ✅ Pembelajaran pribadi
- ✅ Tutorial dan workshop
- ✅ Portofolio development
- ✅ Referensi coding

**Dilarang untuk:**
- ❌ Commercial use tanpa izin
- ❌ Menghapus attribution/copyright
- ❌ Redistribusi sebagai karya sendiri

## 📞 Kontak

**Al Utomo**
- 📧 Email: [jendelapintugt@gmail.com](mailto:jendelapintugt@gmail.com)
- 📸 Instagram: [@alutomo1](https://instagram.com/alutomo1)

---

**⭐ Jika proyek ini membantu Anda belajar, berikan star di repository dan bagikan ke teman-teman Anda!**

*#WebDevelopment #FullStack #Pembelajaran #JavaScript #Python #MySQL #HTML #CSS*
