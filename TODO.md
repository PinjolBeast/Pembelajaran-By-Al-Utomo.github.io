# TODO: Pembelajaran Full-Stack Aplikasi Sederhana

## ✅ COMPLETED: Setup Database
- [x] Buat file schema.sql untuk membuat tabel users
- [x] Jalankan schema.sql di MySQL untuk membuat database

## ✅ COMPLETED: Setup Backend (Node.js)
- [x] Buat package.json dengan dependencies
- [x] Buat db.js untuk koneksi database
- [x] Buat server.js dengan Express server dan routes CRUD
- [x] Install dependencies dengan npm install

## ✅ COMPLETED: Setup Frontend
- [x] Buat app.html sebagai halaman utama aplikasi
- [x] Buat js/app.js untuk JavaScript frontend yang berinteraksi dengan API

## ✅ COMPLETED: Keamanan dan Best Practices
- [x] Tambahkan validasi input
- [x] Gunakan prepared statements untuk mencegah SQL injection
- [x] Tambahkan CORS dan error handling

## NEXT STEPS: Jalankan dan Test Aplikasi

### 1. Setup Database MySQL
```bash
# Jalankan MySQL command line atau tool seperti phpMyAdmin
mysql -u root -p < schema.sql
# Atau copy-paste isi schema.sql ke MySQL client
```

### 2. Install Dependencies Backend
```bash
npm install
```

### 3. Jalankan Server
```bash
npm start
# Atau untuk development dengan auto-reload:
npm run dev
```

### 4. Buka Aplikasi
- Buka `app.html` di browser (bisa dengan Live Server extension VS Code)
- Server backend berjalan di http://localhost:3000
- Frontend akan connect ke API backend

### 5. Test CRUD Operations
- Tambah user baru
- Edit user existing
- Hapus user
- Lihat semua data di tabel

## DEPLOYMENT: Menjalankan di Server Lain

### Opsi 1: Deploy ke VPS/Cloud Server (Backend + Database)
1. **Setup Server Baru:**
   - Buat VPS di DigitalOcean, AWS, atau GCP
   - Install Node.js dan MySQL di server

2. **Upload Files:**
   ```bash
   # Upload semua file kecuali node_modules
   scp -r . user@server-ip:/path/to/app
   ```

3. **Setup Database di Server:**
   ```bash
   # SSH ke server
   ssh user@server-ip
   # Install MySQL jika belum ada
   sudo apt update && sudo apt install mysql-server
   # Jalankan schema
   mysql -u root -p < schema.sql
   ```

4. **Install Dependencies & Jalankan:**
   ```bash
   cd /path/to/app
   npm install
   npm start
   ```

5. **Update Frontend:**
   - Ganti `API_BASE_URL` di `js/app.js` ke IP/domain server baru
   - Contoh: `const API_BASE_URL = 'http://your-server-ip:3000';`

### Opsi 2: Netlify untuk Frontend (Static)
1. **Persiapan:**
   - Pastikan backend sudah deploy di server dengan domain/IP public
   - Update `API_BASE_URL` di `js/app.js` ke URL backend

2. **Deploy ke Netlify:**
   - Buat akun di netlify.com
   - Drag & drop file `app.html` ke dashboard Netlify
   - Atau connect GitHub repo jika menggunakan Git

3. **Konfigurasi Build (jika perlu):**
   - Build command: (kosong, karena static HTML)
   - Publish directory: ./ (root folder)

4. **Environment Variables (opsional):**
   - Jika perlu, set env vars untuk API keys, dll.

### Keamanan untuk Production:
- Gunakan HTTPS (SSL certificate)
- Setup firewall (ufw/iptables)
- Gunakan environment variables untuk konfigurasi sensitif
- Implement authentication (JWT)
- Backup database regularly
- Monitor logs dan errors

## BELAJAR LEBIH LANJUT:
- Authentication dengan JWT
- File upload handling
- Real-time dengan WebSockets
- Testing dengan Jest/Mocha
- Docker untuk containerization
