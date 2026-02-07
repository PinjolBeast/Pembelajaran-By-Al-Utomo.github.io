#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI TUTOR PEMBELAJARAN CODING - VERSI WEB DENGAN FLASK
Skrip Python interaktif untuk belajar coding dengan interface web menggunakan Flask.
Dibuat untuk pemula yang ingin belajar programming dengan bahasa Indonesia.

Fitur Utama:
- Interface web menggunakan Flask
- Interaktif seperti AI tutor dengan efek mengetik
- Bahasa Indonesia penuh
- Generate contoh HTML, CSS, JS, dan Python
- Komentar detail untuk belajar
- Quiz interaktif dengan scoring
- Progress tracking
- File management (buat, edit, hapus file)
- Tidak perlu library tambahan kecuali Flask
- Error handling yang baik
- Cross-platform (Windows, Linux, Mac)

Cara menjalankan:
1. Install Flask: pip install flask
2. Pastikan Python 3.x terinstall (download dari python.org)
3. Jalankan: python ai_tutor_web.py
4. Buka browser ke: http://localhost:5000
5. Ikuti instruksi di layar
6. File contoh akan dibuat di folder yang sama

Requirements:
- Python 3.6+
- Flask (pip install flask)
- Tidak ada library eksternal lainnya diperlukan

Author: AI Assistant
Versi: 1.0 - Web Edition
Tanggal: 2024

CATATAN KEANEHAN DAN PERBAIKAN:
- Mengapa ada string panjang? Karena template HTML/CSS/JS yang kompleks untuk contoh interaktif.
- Mengapa os.system? Untuk clear screen cross-platform, tapi berpotensi tidak aman jika input tidak dikontrol.
- Mengapa banyak nested code? Untuk membuat contoh lengkap yang mudah dipahami pemula.
- Perbaikan: Tambahkan validasi input, gunakan subprocess lebih aman, bagi kode menjadi fungsi lebih kecil.
"""

# ===========================================
# IMPORT STATEMENTS - Mengimpor modul yang diperlukan
# ===========================================
import os  # Modul untuk interaksi dengan sistem operasi (file, direktori, command)
import sys  # Modul untuk interaksi dengan interpreter Python (exit, version)
import time  # Modul untuk operasi waktu (delay, datetime)
import random  # Modul untuk generate angka acak
import json  # Modul untuk bekerja dengan data JSON (load/save progress)
from datetime import datetime  # Modul untuk tanggal dan waktu
from flask import Flask, render_template_string, request, redirect, url_for, flash, session  # Flask untuk web

# Inisialisasi Flask app
app = Flask(__name__)
app.secret_key = 'ai_tutor_secret_key_2024'  # Secret key untuk session

# Mengapa import banyak? Karena program ini multifungsi: file I/O, random, JSON, Flask web framework.
# Keanehan: Tidak ada yang aneh di sini, standar untuk aplikasi web Python.

# ===========================================
# FUNGSI UTILITAS DASAR
# ===========================================

def clear_screen():
    """
    Membersihkan layar terminal untuk tampilan yang bersih.

    Mengapa os.system? Karena cross-platform (Windows 'cls', Unix 'clear').
    Keanehan: os.system bisa berbahaya jika command berasal dari input user (injection attack).
    Perbaikan yang disarankan: Gunakan subprocess.run() dengan argumen terpisah, atau library seperti colorama.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    # os.name == 'nt' mendeteksi Windows (nt = New Technology, nama internal Windows)
    # Jika bukan Windows, gunakan 'clear' (Unix/Linux/Mac)

def type_text(text, delay=0.03):
    """
    Menampilkan teks dengan efek mengetik untuk suasana AI.

    Parameter:
    - text: String yang akan ditampilkan
    - delay: Waktu jeda antar karakter (detik)

    Mengapa efek mengetik? Untuk membuat interaksi terasa seperti AI chatbot.
    Keanehan: Loop sederhana, tapi delay bisa membuat program lambat jika teks panjang.
    Perbaikan: Tambahkan opsi untuk skip efek jika user ingin cepat.
    """
    for char in text:  # Loop setiap karakter dalam teks
        print(char, end='', flush=True)  # Print tanpa newline, flush untuk langsung tampil
        time.sleep(delay)  # Jeda sesuai delay
    print()  # Newline di akhir

# ===========================================
# CLASS UNTUK PROGRESS SISWA
# ===========================================

class StudentProgress:
    """
    Class untuk tracking progress pembelajaran siswa.

    Mengapa class? Untuk mengelompokkan data dan method terkait progress.
    Keanehan: Menggunakan JSON untuk penyimpanan sederhana, tapi tidak aman untuk data sensitif.
    Perbaikan: Tambahkan enkripsi jika data pribadi, atau gunakan database.
    """

    def __init__(self):
        """
        Inisialisasi class StudentProgress.

        Mengapa __init__? Constructor Python, dipanggil saat objek dibuat.
        Keanehan: File path hardcoded, bisa bermasalah jika direktori tidak writable.
        """
        self.progress_file = "student_progress.json"  # Nama file untuk menyimpan progress
        self.progress = self.load_progress()  # Load progress saat inisialisasi

    def load_progress(self):
        """
        Memuat progress dari file JSON.

        Return: Dictionary progress atau default jika file tidak ada.

        Mengapa try-except? Untuk handle error jika file tidak ada atau corrupt.
        Keanehan: Default progress hardcoded, bisa diperbaiki dengan config file.
        """
        try:
            if os.path.exists(self.progress_file):  # Cek apakah file ada
                with open(self.progress_file, 'r', encoding='utf-8') as f:  # Buka file untuk baca
                    return json.load(f)  # Load JSON ke dictionary
            else:
                # Default progress jika file belum ada
                return {
                    "nama": "",
                    "pelajaran_selesai": [],  # List pelajaran yang selesai
                    "quiz_score": {},  # Dictionary score per pelajaran
                    "waktu_mulai": str(datetime.now()),  # Waktu mulai
                    "total_sesi": 0  # Total sesi belajar
                }
        except Exception as e:  # Catch semua exception (JSON error, file error, dll)
            print(f"Error loading progress: {e}")  # Print error untuk debugging
            return {"nama": "", "pelajaran_selesai": [], "quiz_score": {}, "waktu_mulai": str(datetime.now()), "total_sesi": 0}

    def save_progress(self):
        """
        Menyimpan progress ke file JSON.

        Mengapa indent=2? Untuk readability file JSON.
        Keanehan: Overwrite file tanpa backup, bisa hilang jika error saat write.
        Perbaikan: Simpan ke temp file dulu, lalu rename.
        """
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:  # Buka file untuk write
                json.dump(self.progress, f, indent=2, ensure_ascii=False)  # Dump dict ke JSON
        except Exception as e:
            print(f"Error saving progress: {e}")

    def update_progress(self, lesson, score=None):
        """
        Update progress pelajaran.

        Parameter:
        - lesson: Nama pelajaran
        - score: Score quiz (optional)

        Mengapa append dan update? Untuk track completion dan score.
        Keanehan: Tidak cek duplikasi lesson, bisa double count.
        """
        if lesson not in self.progress["pelajaran_selesai"]:  # Cek jika belum selesai
            self.progress["pelajaran_selesai"].append(lesson)  # Tambah ke list
        if score is not None:  # Jika score diberikan
            self.progress["quiz_score"][lesson] = score  # Simpan score
        self.progress["total_sesi"] += 1  # Increment total sesi
        self.save_progress()  # Simpan perubahan

    def show_progress(self):
        """
        Menampilkan progress siswa.

        Mengapa banyak print? Untuk tampilan user-friendly.
        Keanehan: Logic sederhana, tapi bisa diperbaiki dengan tabel atau chart.
        """
        clear_screen()  # Bersihkan layar
        type_text("📊 PROGRESS PEMBELAJARAN ANDA")  # Judul dengan efek
        type_text("=" * 40)

        if self.progress["nama"]:  # Jika nama sudah ada
            type_text(f"Nama: {self.progress['nama']}")  # Tampilkan nama
        else:
            nama = input("Siapa nama Anda? ")  # Input nama
            self.progress["nama"] = nama  # Simpan nama
            self.save_progress()  # Simpan

        type_text(f"Pelajaran selesai: {len(self.progress['pelajaran_selesai'])}")  # Jumlah pelajaran
        type_text(f"Total sesi belajar: {self.progress['total_sesi']}")  # Total sesi
        type_text(f"Waktu mulai: {self.progress['waktu_mulai'][:10]}")  # Tanggal mulai (slice untuk YYYY-MM-DD)

        if self.progress["pelajaran_selesai"]:  # Jika ada pelajaran selesai
            type_text("\n✅ Pelajaran yang sudah diselesaikan:")
            for lesson in self.progress["pelajaran_selesai"]:  # Loop setiap lesson
                score = self.progress["quiz_score"].get(lesson, "N/A")  # Ambil score atau N/A
                type_text(f"   • {lesson} (Score: {score})")  # Tampilkan

        if self.progress["quiz_score"]:  # Jika ada score
            total_score = sum(self.progress["quiz_score"].values())  # Jumlah semua score
            avg_score = total_score / len(self.progress["quiz_score"])  # Rata-rata
            type_text(f"Rata-rata score: {avg_score:.1f}")  # Tampilkan rata-rata

# ===========================================
# FUNGSI UNTUK MEMBUAT FILE CONTOH
# ===========================================

def create_file_example(file_type, filename, title, content):
    """
    Membuat file contoh berbagai jenis (HTML, CSS, JS, Python).

    Parameter:
    - file_type: Tipe file ('html', 'css', 'js', 'python')
    - filename: Nama file output
    - title: Judul untuk file
    - content: Konten tambahan

    Mengapa fungsi panjang? Karena template HTML/CSS/JS yang kompleks.
    Keanehan: String template sangat panjang, sulit dibaca dan maintain.
    Perbaikan: Pisah template ke file terpisah atau gunakan template engine seperti Jinja2.
    """
    if file_type == "html":
        # Template HTML dengan styling internal
        html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        /* CSS Internal untuk styling */
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}

        .container {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}

        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
        }}

        .code-example {{
            background: #2d3748;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            margin: 15px 0;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }}

        .highlight {{
            background: #3498db;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }}

        button {{
            background: #3498db;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px 5px;
            transition: background 0.3s;
        }}

        button:hover {{
            background: #2980b9;
        }}

        .demo-section {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #e74c3c;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 {title}</h1>
        {content}
        <div class="demo-section">
            <h3>💡 Tips untuk Pemula:</h3>
            <ul>
                <li>Buka file ini di browser untuk melihat hasilnya</li>
                <li>Coba edit kode dan lihat perubahannya</li>
                <li>Praktekkan dengan membuat file HTML sendiri</li>
            </ul>
        </div>
    </div>

    <script>
        // JavaScript sederhana untuk interaktivitas
        console.log('File {filename} berhasil dimuat!');
        console.log('Selamat belajar coding! 🚀');
    </script>
</body>
</html>"""
        with open(filename, 'w', encoding='utf-8') as f:  # Buka file untuk write
            f.write(html_content)  # Tulis konten

    elif file_type == "css":
        # Template CSS dengan komentar
        css_content = f"""/* {title} */
/* File CSS terpisah untuk styling yang lebih rapi */

/* Reset dan base styles */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* Body styling */
body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #74ebd5 0%, #acb6e5 100%);
    min-height: 100vh;
    padding: 20px;
}}

/* Container utama */
.container {{
    max-width: 800px;
    margin: 0 auto;
    background: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}}

/* Typography */
h1, h2, h3 {{
    color: #2c3e50;
    margin-bottom: 15px;
}}

h1 {{
    text-align: center;
    font-size: 2.5em;
    margin-bottom: 30px;
}}

p {{
    line-height: 1.6;
    margin-bottom: 15px;
    color: #555;
}}

/* Code examples */
.code-example {{
    background: #2d3748;
    color: #e2e8f0;
    padding: 20px;
    border-radius: 8px;
    font-family: 'Courier New', monospace;
    margin: 15px 0;
    overflow-x: auto;
    border-left: 4px solid #3498db;
}}

/* Buttons */
.btn {{
    display: inline-block;
    background: #3498db;
    color: white;
    padding: 12px 24px;
    text-decoration: none;
    border-radius: 6px;
    margin: 10px 5px;
    transition: all 0.3s;
    border: none;
    cursor: pointer;
    font-size: 16px;
}}

.btn:hover {{
    background: #2980b9;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}}

/* Demo sections */
.demo-section {{
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
    border-left: 4px solid #e74c3c;
}}

/* Animations */
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.fade-in {{
    animation: fadeIn 0.5s ease-in;
}}

/* Responsive design */
@media (max-width: 768px) {{
    body {{
        padding: 10px;
    }}

    .container {{
        padding: 20px;
        margin: 0;
        border-radius: 0;
    }}

    h1 {{
        font-size: 2em;
    }}

    .btn {{
        width: 100%;
        margin: 10px 0;
        padding: 15px;
        font-size: 16px;
    }}
}}

{content}
"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(css_content)

    elif file_type == "js":
        # Template JS dengan komentar detail
        js_content = f"""// {title}
// File JavaScript untuk logika interaktif

// ===========================================
// KOMENTAR DAN PENJELASAN
// ===========================================
// File ini berisi contoh JavaScript untuk pemula
// Setiap bagian memiliki komentar yang menjelaskan fungsinya

// ===========================================
// VARIABEL DAN TIPE DATA
// ===========================================

// String - teks
let nama = "Budi";
const pesan = "Selamat belajar JavaScript!";

// Number - angka
let umur = 25;
const pi = 3.14159;

// Boolean - true/false
let isStudent = true;
let isCompleted = false;

// Array - kumpulan data
let hobi = ["coding", "gaming", "reading"];
let angka = [1, 2, 3, 4, 5];

// Object - objek dengan properti
let orang = {{
    nama: "Budi",
    umur: 25,
    hobi: ["coding", "gaming"],
    alamat: {{
        kota: "Jakarta",
        negara: "Indonesia"
    }}
}};

// ===========================================
// FUNGSI (FUNCTIONS)
// ===========================================

/**
 * Fungsi untuk menyapa pengguna
 * @param {{string}} nama - Nama pengguna
 * @returns {{string}} Pesan sapaan
 */
function sapaPengguna(nama) {{
    return `Halo, ${{nama}}! Selamat datang di dunia JavaScript!`;
}}

/**
 * Fungsi untuk menghitung luas persegi panjang
 * @param {{number}} panjang - Panjang persegi panjang
 * @param {{number}} lebar - Lebar persegi panjang
 * @returns {{number}} Luas persegi panjang
 */
function hitungLuasPersegiPanjang(panjang, lebar) {{
    if (panjang <= 0 || lebar <= 0) {{
        return "Panjang dan lebar harus positif!";
    }}
    return panjang * lebar;
}}

/**
 * Fungsi untuk mengecek apakah angka genap
 * @param {{number}} angka - Angka yang akan dicek
 * @returns {{boolean}} True jika genap, false jika ganjil
 */
function isGenap(angka) {{
    return angka % 2 === 0;
}}

// ===========================================
// KONDISIONAL (IF/ELSE)
// ===========================================

function cekUsia(usia) {{
    if (usia < 13) {{
        return "Anak-anak";
    }} else if (usia < 20) {{
        return "Remaja";
    }} else if (usia < 60) {{
        return "Dewasa";
    }} else {{
        return "Lansia";
    }}
}}

// ===========================================
// LOOPING (PERULANGAN)
// ===========================================

/**
 * Fungsi untuk menampilkan angka 1 sampai n
 * @param {{number}} n - Batas akhir
 */
function tampilkanAngka(n) {{
    console.log("Menggunakan for loop:");
    for (let i = 1; i <= n; i++) {{
        console.log(i);
    }}

    console.log("Menggunakan while loop:");
    let j = 1;
    while (j <= n) {{
        console.log(j);
        j++;
    }}
}}

/**
 * Fungsi untuk menghitung jumlah array
 * @param {{Array}} arr - Array angka
 * @returns {{number}} Jumlah semua elemen
 */
function jumlahArray(arr) {{
    let total = 0;
    for (let num of arr) {{
        total += num;
    }}
    return total;
}}

// ===========================================
// EVENT HANDLING
// ===========================================

// Fungsi yang akan dipanggil saat tombol diklik
function handleClick() {{
    alert("Tombol diklik!");
    console.log("Event click terdeteksi");
}}

// Fungsi untuk validasi form
function validateForm(nama, email) {{
    if (!nama || nama.trim() === "") {{
        return "Nama tidak boleh kosong";
    }}

    if (!email || !email.includes("@")) {{
        return "Email tidak valid";
    }}

    return "Valid";
}}

// ===========================================
// ASYNCHRONOUS PROGRAMMING
// ===========================================

/**
 * Fungsi async untuk simulasi API call
 * @param {{string}} url - URL API
 * @returns {{Promise}} Promise dengan data
 */
async function fetchData(url) {{
    try {{
        console.log(`Mengambil data dari: ${{url}}`);
        // Simulasi delay seperti API call
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Simulasi response
        return {{
            status: "success",
            data: {{
                message: "Data berhasil diambil!",
                timestamp: new Date().toISOString()
            }}
        }};
    }} catch (error) {{
        console.error("Error:", error);
        return {{
            status: "error",
            message: "Gagal mengambil data"
        }};
    }}
}}

// ===========================================
// DOM MANIPULATION (JIKA ADA HTML)
// ===========================================

// Fungsi untuk mengubah teks elemen
function ubahTeks(selector, teksBaru) {{
    const element = document.querySelector(selector);
    if (element) {{
        element.textContent = teksBaru;
    }}
}}

// Fungsi untuk menambah class CSS
function tambahClass(selector, className) {{
    const element = document.querySelector(selector);
    if (element) {{
        element.classList.add(className);
    }}
}}

// ===========================================
// CONTOH PENGGUNAAN
// ===========================================

// Jalankan contoh saat file dimuat
console.log("=== CONTOH PENGGUNAAN JAVASCRIPT ===");

// Contoh variabel dan fungsi
console.log("Sapaan:", sapaPengguna("Budi"));
console.log("Luas persegi panjang 5x3:", hitungLuasPersegiPanjang(5, 3));
console.log("Apakah 4 genap?", isGenap(4));
console.log("Kategori usia 25 tahun:", cekUsia(25));

// Contoh array
console.log("Jumlah array [1,2,3,4,5]:", jumlahArray([1, 2, 3, 4, 5]));

// Contoh async
fetchData("https://api.example.com/data").then(result => {{
    console.log("Hasil fetch:", result);
}});

// Export untuk digunakan di file lain (jika menggunakan module)
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = {{
        sapaPengguna,
        hitungLuasPersegiPanjang,
        isGenap,
        cekUsia,
        tampilkanAngka,
        jumlahArray,
        validateForm,
        fetchData
    }};
}}

{content}

// ===========================================
// TIPS UNTUK PEMULA
// ===========================================
/*
1. Selalu gunakan let/const, hindari var
2. Beri nama variabel/fungsi yang deskriptif
3. Gunakan komentar untuk menjelaskan kode
4. Test kode Anda di browser console
5. Pelajari error messages dengan baik
6. Praktekkan setiap hari untuk mahir
7. Baca dokumentasi MDN Web Docs
8. Bergabung dengan komunitas programmer

Selamat belajar JavaScript! 🚀
*/
"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(js_content)

    elif file_type == "python":
        # Template Python dengan komentar
        py_content = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
{title}
Contoh program Python untuk pemula
\"\"\"

{content}

# ===========================================
# CONTOH PROGRAM PYTHON LENGKAP
# ===========================================

import os
import sys
import random
from datetime import datetime

def main():
    \"\"\"Fungsi utama program\"\"\"
    print("🎯 Selamat datang di program Python!")
    print("=" * 40)

    # Contoh input dari user
    nama = input("Siapa nama Anda? ")
    umur = int(input("Berapa umur Anda? "))

    print(f"\\nHalo, {{nama}}! Anda berusia {{umur}} tahun.")

    # Contoh conditional
    if umur < 18:
        print("Anda masih di bawah umur.")
    elif umur < 60:
        print("Anda sudah dewasa.")
    else:
        print("Anda sudah senior.")

    # Contoh loop
    print("\\nMari kita hitung sampai 5:")
    for i in range(1, 6):
        print(f"Angka: {{i}}")

    # Contoh list
    hobi = ["coding", "gaming", "reading", "sports"]
    print(f"\\nHobi Anda bisa: {{hobi}}")

    # Contoh random
    hobi_random = random.choice(hobi)
    print(f"Hobi acak hari ini: {{hobi_random}}")

    print("\\n✅ Program selesai! Selamat belajar Python! 🐍")

if __name__ == "__main__":
    main()

# ===========================================
# TIPS BELAJAR PYTHON
# ===========================================
# 1. Install Python dari python.org
# 2. Gunakan IDE seperti VS Code atau PyCharm
# 3. Pelajari dasar syntax dan tipe data
# 4. Praktekkan dengan membuat program sederhana
# 5. Baca dokumentasi resmi Python
# 6. Bergabung dengan komunitas Python Indonesia
# 7. Ikuti tutorial di YouTube atau freeCodeCamp
# 8. Buat project kecil setiap hari

# Selamat belajar Python! 🚀
"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(py_content)

    return filename  # Return nama file yang dibuat

# ===========================================
# FUNGSI PELAJARAN INTERAKTIF
# ===========================================

def pelajaran_html():
    """
    Pelajaran interaktif tentang HTML dasar.

    Mengapa fungsi ini? Untuk memberikan pengalaman belajar interaktif.
    Keanehan: Konten HTML sebagai string panjang, sulit maintain.
    Perbaikan: Gunakan file template terpisah.
    """
    clear_screen()
    type_text("🎯 PELAJARAN HTML DASAR")
    type_text("HTML adalah bahasa markup untuk membuat struktur halaman web.")
    type_text("Mari kita mulai dengan contoh sederhana!\n")

    # Buat contoh HTML
    content = """
        <h2>Apa itu HTML?</h2>
        <p>HTML (HyperText Markup Language) adalah bahasa untuk membuat halaman web.</p>

        <div class="code-example">
<!DOCTYPE html><br>
<html><br>
&nbsp;&nbsp;<head><br>
&nbsp;&nbsp;&nbsp;&nbsp;<title>Judul Halaman</title><br>
&nbsp;&nbsp;</head><br>
&nbsp;&nbsp;<body><br>
&nbsp;&nbsp;&nbsp;&nbsp;<h1>Hello World!</h1><br>
&nbsp;&nbsp;&nbsp;&nbsp;<p>Ini paragraf pertama.</p><br>
&nbsp;&nbsp;</body><br>
</html>
        </div>

        <h2>Elemen HTML Dasar:</h2>
        <ul>
            <li><h1> - <h6>: Heading (judul)</li>
            <li><p>: Paragraph (paragraf)</li>
            <li><a>: Link (tautan)</li>
            <li><img>: Gambar</li>
            <li><div>: Container</li>
        </ul>
    """

    filename = create_file_example("html", "contoh_html.html", "Pelajaran HTML Dasar", content)
    type_text(f"✅ File HTML contoh telah dibuat: {filename}")
    type_text("Buka file tersebut di browser untuk melihat hasilnya!\n")

    # Quiz interaktif
    type_text("🧠 QUIZ: Apa singkatan dari HTML?")
    type_text("A) HyperText Markup Language")
    type_text("B) High Tech Modern Language")
    type_text("C) Home Tool Markup Language")

    jawaban = input("Jawaban Anda (A/B/C): ").upper()
    if jawaban == "A":
        type_text("🎉 Benar! HTML adalah HyperText Markup Language.")
    else:
        type_text("❌ Salah. Jawaban yang benar adalah A) HyperText Markup Language.")

def pelajaran_css():
    """
    Pelajaran interaktif tentang CSS dasar.

    Mirip dengan HTML, tapi fokus pada styling.
    Keanehan: Konten sebagai string multiline, bisa error jika indent salah.
    """
    clear_screen()
    type_text("🎨 PELAJARAN CSS DASAR")
    type_text("CSS digunakan untuk mengatur tampilan dan layout halaman web.")
    type_text("Mari pelajari cara styling elemen HTML!\n")

    content = """
        <h2>Apa itu CSS?</h2>
        <p>CSS (Cascading Style Sheets) mengatur tampilan HTML.</p>

        <div class="code-example">
/* CSS untuk mengubah warna teks */
h1 {
    color: blue;
    font-size: 24px;
}

/* CSS untuk background */
body {
    background-color: lightgray;
}

/* CSS untuk layout */
.container {
    width: 80%;
    margin: 0 auto;
    padding: 20px;
}
        </div>

        <h2>Properti CSS Populer:</h2>
        <ul>
            <li><strong>color:</strong> Warna teks</li>
            <li><strong>background-color:</strong> Warna latar belakang</li>
            <li><strong>font-size:</strong> Ukuran font</li>
            <li><strong>margin:</strong> Ruang di luar elemen</li>
            <li><strong>padding:</strong> Ruang di dalam elemen</li>
            <li><strong>border:</strong> Garis tepi</li>
        </ul>

        <div style="background: linear-gradient(to right, red, blue); padding: 20px; color: white; margin: 20px 0;">
            Contoh gradient background dengan CSS!
        </div>
    """

    filename = create_file_example("html", "contoh_css.html", "Pelajaran CSS Dasar", content)
    type_text(f"✅ File HTML contoh telah dibuat: {filename}\n")

    # Quiz
    type_text("🧠 QUIZ: Properti CSS mana yang digunakan untuk mengubah warna teks?")
    type_text("A) background-color")
    type_text("B) color")
    type_text("C) font-color")

    jawaban = input("Jawaban Anda (A/B/C): ").upper()
    if jawaban == "B":
        type_text("🎉 Benar! Properti 'color' digunakan untuk mengubah warna teks.")
    else:
        type_text("❌ Salah. Jawaban yang benar adalah B) color.")

def pelajaran_javascript():
    """
    Pelajaran interaktif tentang JavaScript dasar.

    Keanehan: Konten JS sebagai string, tapi JS dalam HTML string.
    Perbaikan: Pisah JS ke file terpisah.
    """
    clear_screen()
    type_text("⚡ PELAJARAN JAVASCRIPT DASAR")
    type_text("JavaScript membuat halaman web menjadi interaktif.")
    type_text("Mari pelajari dasar-dasar programming dengan JS!\n")

    content = """
        <h2>Apa itu JavaScript?</h2>
        <p>JavaScript adalah bahasa programming untuk web yang membuat halaman interaktif.</p>

        <div class="code-example">
// Variabel untuk menyimpan data
let nama = "Budi";
let umur = 25;

// Fungsi untuk menampilkan pesan
function sapaPengguna() {
    alert("Halo, " + nama + "! Umur Anda " + umur + " tahun.");
}

// Event listener untuk tombol
document.getElementById("tombolSapa").addEventListener("click", sapaPengguna);
        </div>

        <button id="tombolSapa" onclick="sapaPengguna()">Klik untuk sapa!</button>

        <h2>Konsep Dasar JavaScript:</h2>
        <ul>
            <li><strong>Variabel:</strong> let, const, var</li>
            <li><strong>Fungsi:</strong> function namaFungsi() { ... }</li>
            <li><strong>Event:</strong> onclick, onload, dll</li>
            <li><strong>DOM:</strong> Document Object Model</li>
            <li><strong>Conditional:</strong> if, else, switch</li>
            <li><strong>Loop:</strong> for, while, do-while</li>
        </ul>

        <script>
        function sapaPengguna() {
            let nama = prompt("Siapa nama Anda?");
            if (nama) {
                alert("Halo, " + nama + "! Selamat belajar JavaScript!");
            }
        }
        </script>
    """

    filename = create_file_example("html", "contoh_js.html", "Pelajaran JavaScript Dasar", content)
    type_text(f"✅ File HTML contoh telah dibuat: {filename}\n")

    # Quiz
    type_text("🧠 QUIZ: Keyword mana yang digunakan untuk mendeklarasikan variabel yang bisa diubah?")
    type_text("A) const")
    type_text("B) let")
    type_text("C) function")

    jawaban = input("Jawaban Anda (A/B/C): ").upper()
    if jawaban == "B":
        type_text("🎉 Benar! 'let' digunakan untuk variabel yang bisa diubah nilainya.")
    else:
        type_text("❌ Salah. Jawaban yang benar adalah B) let.")

# ===========================================
# ROUTES FLASK - WEB INTERFACE
# ===========================================

@app.route('/')
def home():
    """
    Route utama - halaman home.

    Mengapa route ini? Entry point aplikasi web.
    Keanehan: Template sebagai string, bisa diperbaiki dengan file template terpisah.
    """
    progress = StudentProgress()
    nama = progress.progress.get("nama", "")

    html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🤖 AI Tutor Coding</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                color: #333;
            }}

            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}

            h1 {{
                color: #2c3e50;
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5em;
            }}

            .welcome {{
                text-align: center;
                margin-bottom: 30px;
                font-size: 1.2em;
                color: #555;
            }}

            .menu {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}

            .menu-item {{
                background: #f8f9fa;
                padding: 25px;
                border-radius: 10px;
                text-align: center;
                text-decoration: none;
                color: #333;
                transition: all 0.3s;
                border: 2px solid transparent;
            }}

            .menu-item:hover {{
                background: #3498db;
                color: white;
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            }}

            .menu-item h3 {{
                margin: 0 0 10px 0;
                font-size: 1.3em;
            }}

            .menu-item p {{
                margin: 0;
                font-size: 0.9em;
                opacity: 0.8;
            }}

            .progress {{
                background: #ecf0f1;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 30px;
            }}

            .progress h3 {{
                margin-top: 0;
                color: #2c3e50;
            }}

            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
                margin-top: 15px;
            }}

            .stat {{
                text-align: center;
                padding: 10px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}

            .stat-number {{
                font-size: 1.5em;
                font-weight: bold;
                color: #3498db;
            }}

            .stat-label {{
                font-size: 0.8em;
                color: #7f8c8d;
                margin-top: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 AI Tutor Coding</h1>
            <div class="welcome">
                {f"Halo, {nama}!" if nama else "Selamat datang di AI Tutor Coding!"}
                <br>
                Saya adalah tutor AI yang akan membantu Anda belajar programming dengan cara interaktif.
            </div>

            {f'''
            <div class="progress">
                <h3>📊 Progress Pembelajaran Anda</h3>
                <div class="stats">
                    <div class="stat">
                        <div class="stat-number">{len(progress.progress.get("pelajaran_selesai", []))}</div>
                        <div class="stat-label">Pelajaran Selesai</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">{progress.progress.get("total_sesi", 0)}</div>
                        <div class="stat-label">Total Sesi</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">{len(progress.progress.get("quiz_score", {}))}</div>
                        <div class="stat-label">Quiz Diselesaikan</div>
                    </div>
                </div>
            </div>
            ''' if nama else ''}

            <div class="menu">
                <a href="/html" class="menu-item">
                    <h3>🎯 HTML Dasar</h3>
                    <p>Pelajari struktur halaman web dengan HTML</p>
                </a>
                <a href="/css" class="menu-item">
                    <h3>🎨 CSS Dasar</h3>
                    <p>Styling dan layout dengan CSS</p>
                </a>
                <a href="/javascript" class="menu-item">
                    <h3>⚡ JavaScript Dasar</h3>
                    <p>Interaktivitas dengan JavaScript</p>
                </a>
                <a href="/python" class="menu-item">
                    <h3>🐍 Python Dasar</h3>
                    <p>Programming dasar dengan Python</p>
                </a>
                <a href="/chat" class="menu-item">
                    <h3>🤖 AI Chat</h3>
                    <p>Tanya apa saja tentang programming</p>
                </a>
                <a href="/progress" class="menu-item">
                    <h3>📊 Progress</h3>
                    <p>Lihat progress pembelajaran Anda</p>
                </a>
            </div>

            <div style="text-align: center; margin-top: 30px; color: #7f8c8d;">
                💡 Tips: Klik salah satu menu di atas untuk mulai belajar!
            </div>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/html')
def html_lesson():
    """Route untuk pelajaran HTML"""
    progress = StudentProgress()

    html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HTML Dasar - AI Tutor</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                color: #333;
            }}

            .container {{
                max-width: 900px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}

            h1 {{
                color: #2c3e50;
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5em;
            }}

            .content {{
                line-height: 1.6;
            }}

            .code-example {{
                background: #2d3748;
                color: #e2e8f0;
                padding: 20px;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                margin: 20px 0;
                overflow-x: auto;
                border-left: 4px solid #3498db;
            }}

            .quiz {{
                background: #f8f9fa;
                padding: 25px;
                border-radius: 10px;
                margin: 30px 0;
                border-left: 4px solid #e74c3c;
            }}

            .quiz h3 {{
                margin-top: 0;
                color: #2c3e50;
            }}

            .options {{
                margin: 15px 0;
            }}

            .option {{
                display: block;
                margin: 10px 0;
                padding: 12px;
                background: white;
                border: 2px solid #ddd;
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.3s;
            }}

            .option:hover {{
                border-color: #3498db;
                background: #f8f9fa;
            }}

            .btn {{
                background: #3498db;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
                margin: 10px 5px;
                text-decoration: none;
                display: inline-block;
                transition: background 0.3s;
            }}

            .btn:hover {{
                background: #2980b9;
            }}

            .btn-success {{
                background: #27ae60;
            }}

            .btn-success:hover {{
                background: #229954;
            }}

            .result {{
                margin-top: 20px;
                padding: 15px;
                border-radius: 6px;
                display: none;
            }}

            .correct {{
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }}

            .wrong {{
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 Pelajaran HTML Dasar</h1>

            <div class="content">
                <h2>Apa itu HTML?</h2>
                <p><strong>HTML (HyperText Markup Language)</strong> adalah bahasa markup yang digunakan untuk membuat struktur halaman web. HTML menggunakan tag-tag untuk menandai berbagai elemen pada halaman web.</p>

                <h2>Contoh Struktur HTML Dasar:</h2>
                <div class="code-example">
<!DOCTYPE html><br>
<html><br>
&nbsp;&nbsp;<head><br>
&nbsp;&nbsp;&nbsp;&nbsp;<title>Judul Halaman</title><br>
&nbsp;&nbsp;</head><br>
&nbsp;&nbsp;<body><br>
&nbsp;&nbsp;&nbsp;&nbsp;<h1>Hello World!</h1><br>
&nbsp;&nbsp;&nbsp;&nbsp;<p>Ini adalah paragraf.</p><br>
&nbsp;&nbsp;</body><br>
</html>
                </div>

                <h2>Elemen HTML Dasar:</h2>
                <ul>
                    <li><code><h1> - <h6></code>: Heading (judul) dengan berbagai tingkatan</li>
                    <li><code><p></code>: Paragraph (paragraf)</li>
                    <li><code><a></code>: Link (tautan)</li>
                    <li><code><img></code>: Gambar</li>
                    <li><code><div></code>: Container untuk mengelompokkan elemen</li>
                    <li><code><span></code>: Container inline</li>
                </ul>

                <div class="quiz">
                    <h3>🧠 Quiz: Apa singkatan dari HTML?</h3>
                    <div class="options">
                        <label class="option">
                            <input type="radio" name="html_quiz" value="A"> A) HyperText Markup Language
                        </label>
                        <label class="option">
                            <input type="radio" name="html_quiz" value="B"> B) High Tech Modern Language
                        </label>
                        <label class="option">
                            <input type="radio" name="html_quiz" value="C"> C) Home Tool Markup Language
                        </label>
                    </div>
                    <button class="btn" onclick="checkAnswer()">Periksa Jawaban</button>
                    <div id="result" class="result"></div>
                </div>

                <div style="text-align: center; margin-top: 30px;">
                    <a href="/create_html" class="btn">📝 Buat File HTML Contoh</a>
                    <a href="/" class="btn btn-success">🏠 Kembali ke Menu</a>
                </div>
            </div>
        </div>

        <script>
            function checkAnswer() {{
                const selected = document.querySelector('input[name="html_quiz"]:checked');
                const result = document.getElementById('result');

                if (!selected) {{
                    result.innerHTML = 'Silakan pilih jawaban terlebih dahulu!';
                    result.className = 'result wrong';
                    result.style.display = 'block';
                    return;
                }}

                if (selected.value === 'A') {{
                    result.innerHTML = '🎉 Benar! HTML adalah HyperText Markup Language.';
                    result.className = 'result correct';
                    // Update progress via AJAX
                    fetch('/update_progress/html', {{method: 'POST'}});
                }} else {{
                    result.innerHTML = '❌ Salah. Jawaban yang benar adalah A) HyperText Markup Language.';
                    result.className = 'result wrong';
                }}

                result.style.display = 'block';
            }}
        </script>
    </body>
    </html>
    """
    return html

@app.route('/create_html')
def create_html():
    """Route untuk membuat file HTML contoh"""
    content = '''
        <h2>Contoh Halaman HTML</h2>
        <p>Ini adalah contoh halaman HTML yang dibuat oleh AI Tutor.</p>

        <h3>Daftar Hobi:</h3>
        <ul>
            <li>Programming</li>
            <li>Gaming</li>
            <li>Reading</li>
            <li>Sports</li>
        </ul>

        <div style="background: #f0f0f0; padding: 20px; margin: 20px 0; border-radius: 8px;">
            <h3>Tips untuk Pemula:</h3>
            <p>Praktekkan dengan membuat halaman HTML sendiri!</p>
        </div>
    '''

    filename = create_file_example("html", "contoh_html_ai_tutor.html", "HTML dari AI Tutor", content)

    html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File HTML Dibuat - AI Tutor</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                color: #333;
                text-align: center;
            }}

            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}

            h1 {{
                color: #2c3e50;
                margin-bottom: 20px;
            }}

            .success {{
                background: #d4edda;
                color: #155724;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                border: 1px solid #c3e6cb;
            }}

            .btn {{
                background: #3498db;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
                margin: 10px;
                text-decoration: none;
                display: inline-block;
                transition: background 0.3s;
            }}

            .btn:hover {{
                background: #2980b9;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✅ File HTML Berhasil Dibuat!</h1>

            <div class="success">
                <h3>🎉 Berhasil!</h3>
                <p>File HTML contoh telah dibuat dengan nama: <strong>{filename}</strong></p>
                <p>Buka file tersebut di browser untuk melihat hasilnya!</p>
            </div>

            <a href="/html" class="btn">📖 Kembali ke Pelajaran HTML</a>
            <a href="/" class="btn">🏠 Kembali ke Menu Utama</a>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/update_progress/<lesson>', methods=['POST'])
def update_progress(lesson):
    """Route untuk update progress"""
    progress = StudentProgress()
    progress.update_progress(lesson, score=1)  # Score sederhana untuk demo
    return {'status': 'success'}

@app.route('/progress')
def show_progress():
    """Route untuk menampilkan progress"""
    progress = StudentProgress()

    html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Progress Pembelajaran - AI Tutor</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                color: #333;
            }}

            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}

            h1 {{
                color: #2c3e50;
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5em;
            }}

            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}

            .stat-card {{
                background: #f8f9fa;
                padding: 25px;
                border-radius: 10px;
                text-align: center;
                border-left: 4px solid #3498db;
            }}

            .stat-number {{
                font-size: 2.5em;
                font-weight: bold;
                color: #3498db;
                margin-bottom: 5px;
            }}

            .stat-label {{
                color: #7f8c8d;
                font-size: 0.9em;
            }}

            .lessons {{
                margin-top: 30px;
            }}

            .lesson-item {{
                background: #f8f9fa;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}

            .lesson-name {{
                font-weight: bold;
                color: #2c3e50;
            }}

            .lesson-score {{
                background: #27ae60;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 0.8em;
            }}

            .no-data {{
                text-align: center;
                color: #7f8c8d;
                font-style: italic;
                margin: 20px 0;
            }}

            .btn {{
                background: #3498db;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
                margin: 10px;
                text-decoration: none;
                display: inline-block;
                transition: background 0.3s;
            }}

            .btn:hover {{
                background: #2980b9;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Progress Pembelajaran</h1>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{len(progress.progress.get('pelajaran_selesai', []))}</div>
                    <div class="stat-label">Pelajaran Selesai</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{progress.progress.get('total_sesi', 0)}</div>
                    <div class="stat-label">Total Sesi Belajar</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(progress.progress.get('quiz_score', {}))}</div>
                    <div class="stat-label">Quiz Diselesaikan</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{progress.progress.get('waktu_mulai', '')[:10] if progress.progress.get('waktu_mulai') else 'N/A'}</div>
                    <div class="stat-label">Tanggal Mulai</div>
                </div>
            </div>

            <div class="lessons">
                <h2>📚 Pelajaran yang Telah Diselesaikan</h2>

                {'''
                <div class="no-data">Belum ada pelajaran yang diselesaikan. Mulai belajar sekarang!</div>
                ''' if not progress.progress.get('pelajaran_selesai') else ''}

                {'''
                '''.join([f'''
                <div class="lesson-item">
                    <span class="lesson-name">{lesson.title()}</span>
                    <span class="lesson-score">Score: {progress.progress.get('quiz_score', {}).get(lesson, 'N/A')}</span>
                </div>
                ''' for lesson in progress.progress.get('pelajaran_selesai', [])])}
            </div>

            <div style="text-align: center; margin-top: 40px;">
                <a href="/" class="btn">🏠 Kembali ke Menu Utama</a>
            </div>
        </div>
    </body>
    </html>
    """
    return html



@app.route('/python')
def python_lesson():
    """Route untuk pelajaran Python dengan 50+ soal"""
    progress = StudentProgress()

    html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🐍 Python Dasar - AI Tutor</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                color: #333;
            }}

            .container {{
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}

            h1 {{
                color: #2c3e50;
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5em;
            }}

            .content {{
                line-height: 1.6;
            }}

            .code-example {{
                background: #2d3748;
                color: #e2e8f0;
                padding: 20px;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                margin: 20px 0;
                overflow-x: auto;
                border-left: 4px solid #3498db;
            }}

            .quiz-section {{
                background: #f8f9fa;
                padding: 25px;
                border-radius: 10px;
                margin: 30px 0;
                border-left: 4px solid #e74c3c;
            }}

            .quiz-section h3 {{
                margin-top: 0;
                color: #2c3e50;
                margin-bottom: 20px;
            }}

            .question {{
                margin-bottom: 25px;
                padding: 15px;
                background: white;
                border-radius: 8px;
                border: 1px solid #ddd;
            }}

            .question p {{
                margin: 0 0 10px 0;
                font-weight: bold;
            }}

            .options {{
                margin: 10px 0;
            }}

            .option {{
                display: block;
                margin: 8px 0;
                padding: 10px;
                background: #f8f9fa;
                border: 2px solid #ddd;
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.3s;
            }}

            .option:hover {{
                border-color: #3498db;
                background: #e3f2fd;
            }}

            .btn {{
                background: #3498db;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
                margin: 10px 5px;
                text-decoration: none;
                display: inline-block;
                transition: background 0.3s;
            }}

            .btn:hover {{
                background: #2980b9;
            }}

            .btn-success {{
                background: #27ae60;
            }}

            .btn-success:hover {{
                background: #229954;
            }}

            .result {{
                margin-top: 15px;
                padding: 12px;
                border-radius: 6px;
                display: none;
            }}

            .correct {{
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }}

            .wrong {{
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }}

            .score-display {{
                text-align: center;
                font-size: 1.2em;
                font-weight: bold;
                margin: 20px 0;
                color: #2c3e50;
            }}

            .progress-bar {{
                width: 100%;
                height: 20px;
                background: #f0f0f0;
                border-radius: 10px;
                margin: 10px 0;
                overflow: hidden;
            }}

            .progress-fill {{
                height: 100%;
                background: linear-gradient(90deg, #3498db, #2980b9);
                width: 0%;
                transition: width 0.3s ease;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐍 Pelajaran Python Dasar</h1>

            <div class="content">
                <h2>Apa itu Python?</h2>
                <p><strong>Python</strong> adalah bahasa pemrograman yang mudah dipelajari dan powerful. Python digunakan untuk web development, data science, AI, dan banyak lagi.</p>

                <h2>Contoh Kode Python Dasar:</h2>
                <div class="code-example">
# Program Hello World<br>
print("Hello, World!")<br>
<br>
# Variabel dan tipe data<br>
nama = "Budi"<br>
umur = 25<br>
tinggi = 175.5<br>
is_student = True<br>
<br>
# Operasi matematika<br>
hasil = 10 + 5 * 2<br>
print(f"Hasil: {{hasil}}")
                </div>

                <h2>Konsep Dasar Python:</h2>
                <ul>
                    <li><strong>Variabel:</strong> Penyimpanan data (nama = "Budi")</li>
                    <li><strong>Tipe Data:</strong> String, Integer, Float, Boolean</li>
                    <li><strong>Operator:</strong> +, -, *, /, %, ==, !=</li>
                    <li><strong>Conditional:</strong> if, elif, else</li>
                    <li><strong>Loop:</strong> for, while</li>
                    <li><strong>Function:</strong> def nama_fungsi():</li>
                </ul>

                <div class="quiz-section">
                    <h3>🧠 Quiz Python - Bagian 1: Dasar-dasar (Soal 1-10)</h3>
                    <div id="quiz1">
                        <div class="question">
                            <p>1. Apa output dari print("Hello World!")?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q1" value="A"> A) Hello World!</label>
                                <label class="option"><input type="radio" name="q1" value="B"> B) "Hello World!"</label>
                                <label class="option"><input type="radio" name="q1" value="C"> C) Error</label>
                            </div>
                            <div id="result1" class="result"></div>
                        </div>

                        <div class="question">
                            <p>2. Mana yang benar untuk mendeklarasikan variabel string?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q2" value="A"> A) nama = Budi</label>
                                <label class="option"><input type="radio" name="q2" value="B"> B) nama = "Budi"</label>
                                <label class="option"><input type="radio" name="q2" value="C"> C) nama = 'Budi'</label>
                            </div>
                            <div id="result2" class="result"></div>
                        </div>

                        <div class="question">
                            <p>3. Apa tipe data dari 25.5?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q3" value="A"> A) Integer</label>
                                <label class="option"><input type="radio" name="q3" value="B"> B) Float</label>
                                <label class="option"><input type="radio" name="q3" value="C"> C) String</label>
                            </div>
                            <div id="result3" class="result"></div>
                        </div>

                        <div class="question">
                            <p>4. Operator apa yang digunakan untuk membandingkan kesamaan?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q4" value="A"> A) =</label>
                                <label class="option"><input type="radio" name="q4" value="B"> B) ==</label>
                                <label class="option"><input type="radio" name="q4" value="C"> C) ===</label>
                            </div>
                            <div id="result4" class="result"></div>
                        </div>

                        <div class="question">
                            <p>5. Apa output dari 10 % 3?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q5" value="A"> A) 3</label>
                                <label class="option"><input type="radio" name="q5" value="B"> B) 1</label>
                                <label class="option"><input type="radio" name="q5" value="C"> C) 0</label>
                            </div>
                            <div id="result5" class="result"></div>
                        </div>

                        <div class="question">
                            <p>6. Keyword apa yang digunakan untuk conditional?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q6" value="A"> A) when</label>
                                <label class="option"><input type="radio" name="q6" value="B"> B) if</label>
                                <label class="option"><input type="radio" name="q6" value="C"> C) check</label>
                            </div>
                            <div id="result6" class="result"></div>
                        </div>

                        <div class="question">
                            <p>7. Loop mana yang digunakan untuk range tertentu?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q7" value="A"> A) while</label>
                                <label class="option"><input type="radio" name="q7" value="B"> B) for</label>
                                <label class="option"><input type="radio" name="q7" value="C"> C) repeat</label>
                            </div>
                            <div id="result7" class="result"></div>
                        </div>

                        <div class="question">
                            <p>8. Bagaimana mendefinisikan function?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q8" value="A"> A) function nama():</label>
                                <label class="option"><input type="radio" name="q8" value="B"> B) def nama():</label>
                                <label class="option"><input type="radio" name="q8" value="C"> C) func nama():</label>
                            </div>
                            <div id="result8" class="result"></div>
                        </div>

                        <div class="question">
                            <p>9. Apa yang benar tentang indentation di Python?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q9" value="A"> A) Opsional</label>
                                <label class="option"><input type="radio" name="q9" value="B"> B) Wajib untuk struktur kode</label>
                                <label class="option"><input type="radio" name="q9" value="C"> C) Hanya untuk komentar</label>
                            </div>
                            <div id="result9" class="result"></div>
                        </div>

                        <div class="question">
                            <p>10. Comment di Python dimulai dengan?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q10" value="A"> A) //</label>
                                <label class="option"><input type="radio" name="q10" value="B"> B) #</label>
                                <label class="option"><input type="radio" name="q10" value="C"> C) /* */</label>
                            </div>
                            <div id="result10" class="result"></div>
                        </div>
                    </div>

                    <button class="btn" onclick="checkQuiz1()">Periksa Jawaban Quiz 1</button>
                    <div id="score1" class="score-display" style="display:none;"></div>
                </div>

                <div class="quiz-section">
                    <h3>🧠 Quiz Python - Bagian 2: Struktur Data (Soal 11-25)</h3>
                    <div id="quiz2">
                        <div class="question">
                            <p>11. Mana yang bukan tipe data built-in Python?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q11" value="A"> A) list</label>
                                <label class="option"><input type="radio" name="q11" value="B"> B) array</label>
                                <label class="option"><input type="radio" name="q11" value="C"> C) dict</label>
                            </div>
                            <div id="result11" class="result"></div>
                        </div>

                        <div class="question">
                            <p>12. Bagaimana membuat list kosong?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q12" value="A"> A) list = []</label>
                                <label class="option"><input type="radio" name="q12" value="B"> B) list = list()</label>
                                <label class="option"><input type="radio" name="q12" value="C"> C) Kedua-duanya benar</label>
                            </div>
                            <div id="result12" class="result"></div>
                        </div>

                        <div class="question">
                            <p>13. Method apa untuk menambah item ke list?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q13" value="A"> A) add()</label>
                                <label class="option"><input type="radio" name="q13" value="B"> B) append()</label>
                                <label class="option"><input type="radio" name="q13" value="C"> C) insert()</label>
                            </div>
                            <div id="result13" class="result"></div>
                        </div>

                        <div class="question">
                            <p>14. Bagaimana mengakses item pertama list?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q14" value="A"> A) list[0]</label>
                                <label class="option"><input type="radio" name="q14" value="B"> B) list[1]</label>
                                <label class="option"><input type="radio" name="q14" value="C"> C) list.first()</label>
                            </div>
                            <div id="result14" class="result"></div>
                        </div>

                        <div class="question">
                            <p>15. Apa perbedaan tuple dan list?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q15" value="A"> A) Tuple mutable, list immutable</label>
                                <label class="option"><input type="radio" name="q15" value="B"> B) List mutable, tuple immutable</label>
                                <label class="option"><input type="radio" name="q15" value="C"> C) Sama saja</label>
                            </div>
                            <div id="result15" class="result"></div>
                        </div>

                        <div class="question">
                            <p>16. Bagaimana membuat dictionary?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q16" value="A"> A) dict = {{}}</label>
                                <label class="option"><input type="radio" name="q16" value="B"> B) dict = dict()</label>
                                <label class="option"><input type="radio" name="q16" value="C"> C) Kedua-duanya benar</label>
                            </div>
                            <div id="result16" class="result"></div>
                        </div>

                        <div class="question">
                            <p>17. Bagaimana mengakses value dari key 'nama'?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q17" value="A"> A) dict.nama</label>
                                <label class="option"><input type="radio" name="q17" value="B"> B) dict['nama']</label>
                                <label class="option"><input type="radio" name="q17" value="C"> C) dict.get('nama')</label>
                            </div>
                            <div id="result17" class="result"></div>
                        </div>

                        <div class="question">
                            <p>18. Method apa untuk mendapatkan semua keys dict?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q18" value="A"> A) keys()</label>
                                <label class="option"><input type="radio" name="q18" value="B"> B) get_keys()</label>
                                <label class="option"><input type="radio" name="q18" value="C"> C) all_keys()</label>
                            </div>
                            <div id="result18" class="result"></div>
                        </div>

                        <div class="question">
                            <p>19. Apa itu set di Python?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q19" value="A"> A) Koleksi unordered unique items</label>
                                <label class="option"><input type="radio" name="q19" value="B"> B) Koleksi ordered items</label>
                                <label class="option"><input type="radio" name="q19" value="C"> C) Array dengan index</label>
                            </div>
                            <div id="result19" class="result"></div>
                        </div>

                        <div class="question">
                            <p>20. Operator apa untuk union set?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q20" value="A"> A) |</label>
                                <label class="option"><input type="radio" name="q20" value="B"> B) &</label>
                                <label class="option"><input type="radio" name="q20" value="C"> C) +</label>
                            </div>
                            <div id="result20" class="result"></div>
                        </div>

                        <div class="question">
                            <p>21. Method apa untuk sorting list?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q21" value="A"> A) sort()</label>
                                <label class="option"><input type="radio" name="q21" value="B"> B) order()</label>
                                <label class="option"><input type="radio" name="q21" value="C"> C) arrange()</label>
                            </div>
                            <div id="result21" class="result"></div>
                        </div>

                        <div class="question">
                            <p>22. Apa output len([1,2,3,4])?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q22" value="A"> A) 3</label>
                                <label class="option"><input type="radio" name="q22" value="B"> B) 4</label>
                                <label class="option"><input type="radio" name="q22" value="C"> C) 5</label>
                            </div>
                            <div id="result22" class="result"></div>
                        </div>

                        <div class="question">
                            <p>23. Method apa untuk reverse list?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q23" value="A"> A) reverse()</label>
                                <label class="option"><input type="radio" name="q23" value="B"> B) flip()</label>
                                <label class="option"><input type="radio" name="q23" value="C"> C) backward()</label>
                            </div>
                            <div id="result23" class="result"></div>
                        </div>

                        <div class="question">
                            <p>24. Apa itu list comprehension?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q24" value="A"> A) Cara singkat membuat list</label>
                                <label class="option"><input type="radio" name="q24" value="B"> B) Mengerti list</label>
                                <label class="option"><input type="radio" name="q24" value="C"> C) Menghapus list</label>
                            </div>
                            <div id="result24" class="result"></div>
                        </div>

                        <div class="question">
                            <p>25. Contoh list comprehension yang benar?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q25" value="A"> A) [x*2 for x in range(5)]</label>
                                <label class="option"><input type="radio" name="q25" value="B"> B) [x*2 in range(5)]</label>
                                <label class="option"><input type="radio" name="q25" value="C"> C) [for x in range(5): x*2]</label>
                            </div>
                            <div id="result25" class="result"></div>
                        </div>
                    </div>

                    <button class="btn" onclick="checkQuiz2()">Periksa Jawaban Quiz 2</button>
                    <div id="score2" class="score-display" style="display:none;"></div>
                </div>

                <div class="quiz-section">
                    <h3>🧠 Quiz Python - Bagian 3: Functions & OOP (Soal 26-40)</h3>
                    <div id="quiz3">
                        <div class="question">
                            <p>26. Bagaimana mendefinisikan function dengan parameter?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q26" value="A"> A) def func x:</label>
                                <label class="option"><input type="radio" name="q26" value="B"> B) def func(x):</label>
                                <label class="option"><input type="radio" name="q26" value="C"> C) function func(x):</label>
                            </div>
                            <div id="result26" class="result"></div>
                        </div>

                        <div class="question">
                            <p>27. Apa itu return statement?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q27" value="A"> A) Menghentikan function</label>
                                <label class="option"><input type="radio" name="q27" value="B"> B) Mengembalikan nilai dari function</label>
                                <label class="option"><input type="radio" name="q27" value="C"> C) Memulai function</label>
                            </div>
                            <div id="result27" class="result"></div>
                        </div>

                        <div class="question">
                            <p>28. Apa itu scope di Python?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q28" value="A"> A) Area dimana variabel dapat diakses</label>
                                <label class="option"><input type="radio" name="q28" value="B"> B) Ukuran function</label>
                                <label class="option"><input type="radio" name="q28" value="C"> C) Jumlah parameter</label>
                            </div>
                            <div id="result28" class="result"></div>
                        </div>

                        <div class="question">
                            <p>29. Keyword apa untuk global variable?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q29" value="A"> A) global</label>
                                <label class="option"><input type="radio" name="q29" value="B"> B) outside</label>
                                <label class="option"><input type="radio" name="q29" value="C"> C) world</label>
                            </div>
                            <div id="result29" class="result"></div>
                        </div>

                        <div class="question">
                            <p>30. Apa itu lambda function?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q30" value="A"> A) Function tanpa nama</label>
                                <label class="option"><input type="radio" name="q30" value="B"> B) Function dengan banyak parameter</label>
                                <label class="option"><input type="radio" name="q30" value="C"> C) Function recursive</label>
                            </div>
                            <div id="result30" class="result"></div>
                        </div>

                        <div class="question">
                            <p>31. Contoh lambda function yang benar?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q31" value="A"> A) lambda x: x*2</label>
                                <label class="option"><input type="radio" name="q31" value="B"> B) lambda x*2</label>
                                <label class="option"><input type="radio" name="q31" value="C"> C) lambda: x*2</label>
                            </div>
                            <div id="result31" class="result"></div>
                        </div>

                        <div class="question">
                            <p>32. Apa itu class di Python?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q32" value="A"> A) Template untuk membuat objek</label>
                                <label class="option"><input type="radio" name="q32" value="B"> B) Function khusus</label>
                                <label class="option"><input type="radio" name="q32" value="C"> C) Tipe data baru</label>
                            </div>
                            <div id="result32" class="result"></div>
                        </div>

                        <div class="question">
                            <p>33. Bagaimana mendefinisikan class?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q33" value="A"> A) class NamaClass:</label>
                                <label class="option"><input type="radio" name="q33" value="B"> B) def NamaClass:</label>
                                <label class="option"><input type="radio" name="q33" value="C"> C) function NamaClass:</label>
                            </div>
                            <div id="result33" class="result"></div>
                        </div>

                        <div class="question">
                            <p>34. Apa itu __init__ method?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q34" value="A"> A) Constructor class</label>
                                <label class="option"><input type="radio" name="q34" value="B"> B) Destructor class</label>
                                <label class="option"><input type="radio" name="q34" value="C"> C) Method biasa</label>
                            </div>
                            <div id="result34" class="result"></div>
                        </div>

                        <div class="question">
                            <p>35. Bagaimana membuat instance dari class?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q35" value="A"> A) obj = NamaClass()</label>
                                <label class="option"><input type="radio" name="q35" value="B"> B) obj = new NamaClass()</label>
                                <label class="option"><input type="radio" name="q35" value="C"> C) obj = create NamaClass()</label>
                            </div>
                            <div id="result35" class="result"></div>
                        </div>

                        <div class="question">
                            <p>36. Apa itu inheritance?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q36" value="A"> A) Class mewarisi properti dari parent class</label>
                                <label class="option"><input type="radio" name="q36" value="B"> B) Class membuat instance baru</label>
                                <label class="option"><input type="radio" name="q36" value="C"> C) Class menghapus method</label>
                            </div>
                            <div id="result36" class="result"></div>
                        </div>

                        <div class="question">
                            <p>37. Bagaimana inheritance di Python?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q37" value="A"> A) class Child(Parent):</label>
                                <label class="option"><input type="radio" name="q37" value="B"> B) class Child extends Parent:</label>
                                <label class="option"><input type="radio" name="q37" value="C"> C) class Child inherits Parent:</label>
                            </div>
                            <div id="result37" class="result"></div>
                        </div>

                        <div class="question">
                            <p>38. Apa itu method overriding?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q38" value="A"> A) Mengubah implementasi method parent</label>
                                <label class="option"><input type="radio" name="q38" value="B"> B) Menambah method baru</label>
                                <label class="option"><input type="radio" name="q38" value="C"> C) Menghapus method</label>
                            </div>
                            <div id="result38" class="result"></div>
                        </div>

                        <div class="question">
                            <p>39. Apa itu encapsulation?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q39" value="A"> A) Menyembunyikan detail implementasi</label>
                                <label class="option"><input type="radio" name="q39" value="B"> B) Menggabungkan class</label>
                                <label class="option"><input type="radio" name="q39" value="C"> C) Membuat instance</label>
                            </div>
                            <div id="result39" class="result"></div>
                        </div>

                        <div class="question">
                            <p>40. Convention untuk private attribute?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q40" value="A"> A) __attribute</label>
                                <label class="option"><input type="radio" name="q40" value="B"> B) _attribute</label>
                                <label class="option"><input type="radio" name="q40" value="C"> C) attribute_</label>
                            </div>
                            <div id="result40" class="result"></div>
                        </div>
                    </div>

                    <button class="btn" onclick="checkQuiz3()">Periksa Jawaban Quiz 3</button>
                    <div id="score3" class="score-display" style="display:none;"></div>
                </div>

                <div class="quiz-section">
                    <h3>🧠 Quiz Python - Bagian 4: Advanced Topics (Soal 41-55)</h3>
                    <div id="quiz4">
                        <div class="question">
                            <p>41. Apa itu exception handling?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q41" value="A"> A) Menangani error saat runtime</label>
                                <label class="option"><input type="radio" name="q41" value="B"> B) Mengoptimalkan kode</label>
                                <label class="option"><input type="radio" name="q41" value="C"> C) Mengkompilasi kode</label>
                            </div>
                            <div id="result41" class="result"></div>
                        </div>

                        <div class="question">
                            <p>42. Struktur try-except yang benar?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q42" value="A"> A) try: ... except:</label>
                                <label class="option"><input type="radio" name="q42" value="B"> B) try ... catch:</label>
                                <label class="option"><input type="radio" name="q42" value="C"> C) do: ... catch:</label>
                            </div>
                            <div id="result42" class="result"></div>
                        </div>

                        <div class="question">
                            <p>43. Apa itu file handling?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q43" value="A"> A) Membaca/menulis file</label>
                                <label class="option"><input type="radio" name="q43" value="B"> B) Mengelola memory</label>
                                <label class="option"><input type="radio" name="q43" value="C"> C) Mengatur thread</label>
                            </div>
                            <div id="result43" class="result"></div>
                        </div>

                        <div class="question">
                            <p>44. Mode apa untuk membaca file?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q44" value="A"> A) 'r'</label>
                                <label class="option"><input type="radio" name="q44" value="B"> B) 'w'</label>
                                <label class="option"><input type="radio" name="q44" value="C"> C) 'x'</label>
                            </div>
                            <div id="result44" class="result"></div>
                        </div>

                        <div class="question">
                            <p>45. Method apa untuk menulis ke file?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q45" value="A"> A) write()</label>
                                <label class="option"><input type="radio" name="q45" value="B"> B) put()</label>
                                <label class="option"><input type="radio" name="q45" value="C"> C) send()</label>
                            </div>
                            <div id="result45" class="result"></div>
                        </div>

                        <div class="question">
                            <p>46. Apa itu module di Python?</p>
                            <div class="options">
                                <label class="option"><input type="radio" name="q46" value="A"> A) File yang berisi kode Python</label>
                                <label class="option"><input type="radio" name="q46" value="B"> B) Fungsi built-in</label>
                                <label class="option"><input type="radio" name="q46" value="C"> C) Tipe data baru</label>
                            </div>
                            <div id="result46" class="result"></div>
                        </div>
                    </div>

                    <button class="btn" onclick="checkQuiz4()">Periksa Jawaban Quiz 4</button>
                    <div id="score4" class="score-display" style="display:none;"></div>
                </div>

                <div style="text-align: center; margin-top: 30px;">
                    <a href="/" class="btn btn-success">🏠 Kembali ke Menu Utama</a>
                </div>
            </div>
        </div>

        <script>
            function checkQuiz1() {{
                let score = 0;
                const answers = {{'q1': 'A', 'q2': 'B', 'q3': 'B', 'q4': 'B', 'q5': 'B', 'q6': 'B', 'q7': 'B', 'q8': 'B', 'q9': 'B', 'q10': 'B'}};
                for (let i = 1; i <= 10; i++) {{
                    const selected = document.querySelector(`input[name="q${{i}}"]:checked`);
                    const result = document.getElementById(`result${{i}}`);
                    if (selected && selected.value === answers[`q${{i}}`]) {{
                        score++;
                        result.innerHTML = '✅ Benar!';
                        result.className = 'result correct';
                    }} else {{
                        result.innerHTML = '❌ Salah!';
                        result.className = 'result wrong';
                    }}
                    result.style.display = 'block';
                }}
                document.getElementById('score1').innerHTML = `Score: ${{score}}/10`;
                document.getElementById('score1').style.display = 'block';
            }}

            function checkQuiz2() {{
                let score = 0;
                const answers = {{'q11': 'B', 'q12': 'C', 'q13': 'B', 'q14': 'A', 'q15': 'B', 'q16': 'C', 'q17': 'B', 'q18': 'A', 'q19': 'A', 'q20': 'A', 'q21': 'A', 'q22': 'B', 'q23': 'A', 'q24': 'A', 'q25': 'A'}};
                for (let i = 11; i <= 25; i++) {{
                    const selected = document.querySelector(`input[name="q${{i}}"]:checked`);
                    const result = document.getElementById(`result${{i}}`);
                    if (selected && selected.value === answers[`q${{i}}`]) {{
                        score++;
                        result.innerHTML = '✅ Benar!';
                        result.className = 'result correct';
                    }} else {{
                        result.innerHTML = '❌ Salah!';
                        result.className = 'result wrong';
                    }}
                    result.style.display = 'block';
                }}
                document.getElementById('score2').innerHTML = `Score: ${{score}}/15`;
                document.getElementById('score2').style.display = 'block';
            }}

            function checkQuiz3() {{
                let score = 0;
                const answers = {{'q26': 'B', 'q27': 'B', 'q28': 'A', 'q29': 'A', 'q30': 'A', 'q31': 'A', 'q32': 'A', 'q33': 'A', 'q34': 'A', 'q35': 'A', 'q36': 'A', 'q37': 'A', 'q38': 'A', 'q39': 'A', 'q40': 'A'}};
                for (let i = 26; i <= 40; i++) {{
                    const selected = document.querySelector(`input[name="q${{i}}"]:checked`);
                    const result = document.getElementById(`result${{i}}`);
                    if (selected && selected.value === answers[`q${{i}}`]) {{
                        score++;
                        result.innerHTML = '✅ Benar!';
                        result.className = 'result correct';
                    }} else {{
                        result.innerHTML = '❌ Salah!';
                        result.className = 'result wrong';
                    }}
                    result.style.display = 'block';
                }}
                document.getElementById('score3').innerHTML = `Score: ${{score}}/15`;
                document.getElementById('score3').style.display = 'block';
            }}

            function checkQuiz4() {{
                let score = 0;
                const answers = {{'q41': 'A', 'q42': 'A', 'q43': 'A', 'q44': 'A', 'q45': 'A', 'q46': 'A'}};
                for (let i = 41; i <= 46; i++) {{
                    const selected = document.querySelector(`input[name="q${{i}}"]:checked`);
                    const result = document.getElementById(`result${{i}}`);
                    if (selected && selected.value === answers[`q${{i}}`]) {{
                        score++;
                        result.innerHTML = '✅ Benar!';
                        result.className = 'result correct';
                    }} else {{
                        result.innerHTML = '❌ Salah!';
                        result.className = 'result wrong';
                    }}
                    result.style.display = 'block';
                }}
                document.getElementById('score4').innerHTML = `Score: ${{score}}/6`;
                document.getElementById('score4').style.display = 'block';
            }}
        </script>
    </body>
    </html>
    """
    return html

@app.route('/css')
def css_lesson():
    """Route untuk pelajaran CSS"""
    progress = StudentProgress()

    html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CSS Dasar - AI Tutor</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                color: #333;
            }}

            .container {{
                max-width: 900px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}

            h1 {{
                color: #2c3e50;
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5em;
            }}

            .content {{
                line-height: 1.6;
            }}

            .code-example {{
                background: #2d3748;
                color: #e2e8f0;
                padding: 20px;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                margin: 20px 0;
                overflow-x: auto;
                border-left: 4px solid #3498db;
            }}

            .quiz {{
                background: #f8f9fa;
                padding: 25px;
                border-radius: 10px;
                margin: 30px 0;
                border-left: 4px solid #e74c3c;
            }}

            .quiz h3 {{
                margin-top: 0;
                color: #2c3e50;
            }}

            .options {{
                margin: 15px 0;
            }}

            .option {{
                display: block;
                margin: 10px 0;
                padding: 12px;
                background: white;
                border: 2px solid #ddd;
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.3s;
            }}

            .option:hover {{
                border-color: #3498db;
                background: #f8f9fa;
            }}

            .btn {{
                background: #3498db;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
                margin: 10px 5px;
                text-decoration: none;
                display: inline-block;
                transition: background 0.3s;
            }}

            .btn:hover {{
                background: #2980b9;
            }}

            .btn-success {{
                background: #27ae60;
            }}

            .btn-success:hover {{
                background: #229954;
            }}

            .result {{
                margin-top: 20px;
                padding: 15px;
                border-radius: 6px;
                display: none;
            }}

            .correct {{
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }}

            .wrong {{
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }}

            .gradient-demo {{
                background: linear-gradient(to right, red, blue);
                padding: 20px;
                color: white;
                margin: 20px 0;
                border-radius: 8px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎨 Pelajaran CSS Dasar</h1>

            <div class="content">
                <h2>Apa itu CSS?</h2>
                <p><strong>CSS (Cascading Style Sheets)</strong> adalah bahasa yang digunakan untuk mengatur tampilan dan layout halaman web. CSS memungkinkan Anda mengubah warna, font, ukuran, dan posisi elemen HTML.</p>

                <h2>Contoh Kode CSS Dasar:</h2>
                <div class="code-example">
/* CSS untuk mengubah warna teks */<br>
h1 {{<br>
&nbsp;&nbsp;&nbsp;&nbsp;color: blue;<br>
&nbsp;&nbsp;&nbsp;&nbsp;font-size: 24px;<br>
}}<br>
<br>
/* CSS untuk background */<br>
body {{<br>
&nbsp;&nbsp;&nbsp;&nbsp;background-color: lightgray;<br>
}}<br>
<br>
/* CSS untuk layout */<br>
.container {{<br>
&nbsp;&nbsp;&nbsp;&nbsp;width: 80%;<br>
&nbsp;&nbsp;&nbsp;&nbsp;margin: 0 auto;<br>
&nbsp;&nbsp;&nbsp;&nbsp;padding: 20px;<br>
}}
                </div>

                <h2>Properti CSS Populer:</h2>
                <ul>
                    <li><code>color</code>: Mengubah warna teks</li>
                    <li><code>background-color</code>: Mengubah warna latar belakang</li>
                    <li><code>font-size</code>: Mengubah ukuran font</li>
                    <li><code>margin</code>: Mengatur ruang di luar elemen</li>
                    <li><code>padding</code>: Mengatur ruang di dalam elemen</li>
                    <li><code>border</code>: Menambahkan garis tepi</li>
                    <li><code>width</code> dan <code>height</code>: Mengatur ukuran elemen</li>
                </ul>

                <div class="gradient-demo">
                    Contoh gradient background dengan CSS!
                </div>

                <div class="quiz">
                    <h3>🧠 Quiz: Properti CSS mana yang digunakan untuk mengubah warna teks?</h3>
                    <div class="options">
                        <label class="option">
                            <input type="radio" name="css_quiz" value="A"> A) background-color
                        </label>
                        <label class="option">
                            <input type="radio" name="css_quiz" value="B"> B) color
                        </label>
                        <label class="option">
                            <input type="radio" name="css_quiz" value="C"> C) font-color
                        </label>
                    </div>
                    <button class="btn" onclick="checkAnswer()">Periksa Jawaban</button>
                    <div id="result" class="result"></div>
                </div>

                <div style="text-align: center; margin-top: 30px;">
                    <a href="/create_css" class="btn">📝 Buat File CSS Contoh</a>
                    <a href="/" class="btn btn-success">🏠 Kembali ke Menu</a>
                </div>
            </div>
        </div>

        <script>
            function checkAnswer() {{
                const selected = document.querySelector('input[name="css_quiz"]:checked');
                const result = document.getElementById('result');

                if (!selected) {{
                    result.innerHTML = 'Silakan pilih jawaban terlebih dahulu!';
                    result.className = 'result wrong';
                    result.style.display = 'block';
                    return;
                }}

                if (selected.value === 'B') {{
                    result.innerHTML = '🎉 Benar! Properti \'color\' digunakan untuk mengubah warna teks.';
                    result.className = 'result correct';
                    // Update progress via AJAX
                    fetch('/update_progress/css', {{method: 'POST'}});
                }} else {{
                    result.innerHTML = '❌ Salah. Jawaban yang benar adalah B) color.';
                    result.className = 'result wrong';
                }}

                result.style.display = 'block';
            }}
        </script>
    </body>
    </html>
    """
    return html

@app.route('/create_css')
def create_css():
    """Route untuk membuat file CSS contoh"""
    content = """
/* Contoh CSS untuk styling halaman web */

body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f0f0f0;
}

.header {
    background-color: #3498db;
    color: white;
    text-align: center;
    padding: 20px;
    border-radius: 8px;
}

.content {
    background-color: white;
    padding: 20px;
    margin: 20px 0;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.footer {
    text-align: center;
    color: #666;
    margin-top: 20px;
}
"""

    filename = create_file_example("css", "contoh_css.css", "CSS Contoh", content)

    html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File CSS Dibuat - AI Tutor</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                color: #333;
                text-align: center;
            }}

            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}

            h1 {{
                color: #2c3e50;
                margin-bottom: 20px;
            }}

            .success {{
                background: #d4edda;
                color: #155724;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                border: 1px solid #c3e6cb;
            }}

            .btn {{
                background: #3498db;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
                margin: 10px;
                text-decoration: none;
                display: inline-block;
                transition: background 0.3s;
            }}

            .btn:hover {{
                background: #2980b9;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✅ File CSS Berhasil Dibuat!</h1>

            <div class="success">
                <h3>🎉 Berhasil!</h3>
                <p>File CSS contoh telah dibuat dengan nama: <strong>{filename}</strong></p>
                <p>Buka file tersebut untuk melihat kode CSS yang telah dibuat!</p>
            </div>

            <a href="/css" class="btn">📖 Kembali ke Pelajaran CSS</a>
            <a href="/" class="btn">🏠 Kembali ke Menu Utama</a>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/javascript')
def js_lesson():
    """Route untuk pelajaran JavaScript"""
    progress = StudentProgress()

    html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>JavaScript Dasar - AI Tutor</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                color: #333;
            }}

            .container {{
                max-width: 900px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}

            h1 {{
                color: #2c3e50;
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5em;
            }}

            .content {{
                line-height: 1.6;
            }}

            .code-example {{
                background: #2d3748;
                color: #e2e8f0;
                padding: 20px;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                margin: 20px 0;
                overflow-x: auto;
                border-left: 4px solid #3498db;
            }}

            .quiz {{
                background: #f8f9fa;
                padding: 25px;
                border-radius: 10px;
                margin: 30px 0;
                border-left: 4px solid #e74c3c;
            }}

            .quiz h3 {{
                margin-top: 0;
                color: #2c3e50;
            }}

            .options {{
                margin: 15px 0;
            }}

            .option {{
                display: block;
                margin: 10px 0;
                padding: 12px;
                background: white;
                border: 2px solid #ddd;
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.3s;
            }}

            .option:hover {{
                border-color: #3498db;
                background: #f8f9fa;
            }}

            .btn {{
                background: #3498db;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
                margin: 10px 5px;
                text-decoration: none;
                display: inline-block;
                transition: background 0.3s;
            }}

            .btn:hover {{
                background: #2980b9;
            }}

            .btn-success {{
                background: #27ae60;
            }}

            .btn-success:hover {{
                background: #229954;
            }}

            .result {{
                margin-top: 20px;
                padding: 15px;
                border-radius: 6px;
                display: none;
            }}

            .correct {{
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }}

            .wrong {{
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }}

            .demo-button {{
                background: #3498db;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
                margin: 20px 0;
                transition: background 0.3s;
            }}

            .demo-button:hover {{
                background: #2980b9;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚡ Pelajaran JavaScript Dasar</h1>

            <div class="content">
                <h2>Apa itu JavaScript?</h2>
                <p><strong>JavaScript</strong> adalah bahasa pemrograman yang membuat halaman web menjadi interaktif. JavaScript dapat mengubah konten HTML, menangani event (seperti klik tombol), dan berkomunikasi dengan server.</p>

                <h2>Contoh Kode JavaScript Dasar:</h2>
                <div class="code-example">
// Variabel untuk menyimpan data<br>
let nama = "Budi";<br>
let umur = 25;<br>
<br>
// Fungsi untuk menampilkan pesan<br>
function sapaPengguna() {{<br>
&nbsp;&nbsp;&nbsp;&nbsp;alert("Halo, " + nama + "! Umur Anda " + umur + " tahun.");<br>
}}<br>
<br>
// Event listener untuk tombol<br>
document.getElementById("tombolSapa").addEventListener("click", sapaPengguna);
                </div>

                <button class="demo-button" id="tombolSapa" onclick="sapaPengguna()">Klik untuk sapa!</button>

                <h2>Konsep Dasar JavaScript:</h2>
                <ul>
                    <li><strong>Variabel:</strong> let, const, var untuk menyimpan data</li>
                    <li><strong>Fungsi:</strong> function namaFungsi() {{ ... }} untuk mengelompokkan kode</li>
                    <li><strong>Event:</strong> onclick, onload, dll untuk menangani interaksi user</li>
                    <li><strong>DOM:</strong> Document Object Model untuk mengubah HTML</li>
                    <li><strong>Conditional:</strong> if, else untuk logika percabangan</li>
                    <li><strong>Loop:</strong> for, while untuk perulangan</li>
                </ul>

                <div class="quiz">
                    <h3>🧠 Quiz: Keyword mana yang digunakan untuk mendeklarasikan variabel yang bisa diubah?</h3>
                    <div class="options">
                        <label class="option">
                            <input type="radio" name="js_quiz" value="A"> A) const
                        </label>
                        <label class="option">
                            <input type="radio" name="js_quiz" value="B"> B) let
                        </label>
                        <label class="option">
                            <input type="radio" name="js_quiz" value="C"> C) function
                        </label>
                    </div>
                    <button class="btn" onclick="checkAnswer()">Periksa Jawaban</button>
                    <div id="result" class="result"></div>
                </div>

                <div style="text-align: center; margin-top: 30px;">
                    <a href="/create_js" class="btn">📝 Buat File JavaScript Contoh</a>
                    <a href="/" class="btn btn-success">🏠 Kembali ke Menu</a>
                </div>
            </div>
        </div>

        <script>
            function sapaPengguna() {{
                let nama = prompt("Siapa nama Anda?");
                if (nama) {{
                    alert("Halo, " + nama + "! Selamat belajar JavaScript!");
                }}
            }}

            function checkAnswer() {{
                const selected = document.querySelector('input[name="js_quiz"]:checked');
                const result = document.getElementById('result');

                if (!selected) {{
                    result.innerHTML = 'Silakan pilih jawaban terlebih dahulu!';
                    result.className = 'result wrong';
                    result.style.display = 'block';
                    return;
                }}

                if (selected.value === 'B') {{
                    result.innerHTML = '🎉 Benar! \'let\' digunakan untuk variabel yang bisa diubah nilainya.';
                    result.className = 'result correct';
                    // Update progress via AJAX
                    fetch('/update_progress/javascript', {{method: 'POST'}});
                }} else {{
                    result.innerHTML = '❌ Salah. Jawaban yang benar adalah B) let.';
                    result.className = 'result wrong';
                }}

                result.style.display = 'block';
            }}
        </script>
    </body>
    </html>
    """
    return html

@app.route('/create_js')
def create_js():
    """Route untuk membuat file JavaScript contoh"""
    content = """
// Contoh JavaScript untuk interaktivitas web

// Fungsi untuk mengubah teks
function ubahTeks() {
    document.getElementById('demo-text').innerText = 'Teks telah diubah!';
}

// Fungsi untuk menghitung
function hitung() {
    let angka1 = parseInt(document.getElementById('angka1').value);
    let angka2 = parseInt(document.getElementById('angka2').value);
    let hasil = angka1 + angka2;
    document.getElementById('hasil').innerText = 'Hasil: ' + hasil;
}

// Event listener saat halaman dimuat
document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript berhasil dimuat!');

    // Tambahkan event listener ke tombol
    document.getElementById('ubah-btn').addEventListener('click', ubahTeks);
    document.getElementById('hitung-btn').addEventListener('click', hitung);
});
"""

    filename = create_file_example("js", "contoh_js.js", "JavaScript Contoh", content)

    html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File JavaScript Dibuat - AI Tutor</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                color: #333;
                text-align: center;
            }}

            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}

            h1 {{
                color: #2c3e50;
                margin-bottom: 20px;
            }}

            .success {{
                background: #d4edda;
                color: #155724;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                border: 1px solid #c3e6cb;
            }}

            .btn {{
                background: #3498db;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
                margin: 10px;
                text-decoration: none;
                display: inline-block;
                transition: background 0.3s;
            }}

            .btn:hover {{
                background: #2980b9;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✅ File JavaScript Berhasil Dibuat!</h1>

            <div class="success">
                <h3>🎉 Berhasil!</h3>
                <p>File JavaScript contoh telah dibuat dengan nama: <strong>{filename}</strong></p>
                <p>Buka file tersebut untuk melihat kode JavaScript yang telah dibuat!</p>
            </div>

            <a href="/javascript" class="btn">📖 Kembali ke Pelajaran JavaScript</a>
            <a href="/" class="btn">🏠 Kembali ke Menu Utama</a>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/chat')
def chat():
    """Route untuk AI Chat"""
    html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🤖 AI Chat - AI Tutor</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                color: #333;
            }}

            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}

            h1 {{
                color: #2c3e50;
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5em;
            }}

            .chat-container {{
                border: 1px solid #ddd;
                border-radius: 10px;
                height: 400px;
                padding: 20px;
                overflow-y: auto;
                background: #f8f9fa;
                margin-bottom: 20px;
            }}

            .message {{
                margin-bottom: 15px;
                padding: 10px;
                border-radius: 8px;
            }}

            .user-message {{
                background: #3498db;
                color: white;
                text-align: right;
            }}

            .ai-message {{
                background: #ecf0f1;
                color: #333;
            }}

            .input-container {{
                display: flex;
                gap: 10px;
            }}

            .input-container input {{
                flex: 1;
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 16px;
            }}

            .btn {{
                background: #3498db;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
                transition: background 0.3s;
            }}

            .btn:hover {{
                background: #2980b9;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 AI Chat</h1>
            <p>Tanyakan apa saja tentang programming! Saya adalah AI tutor yang siap membantu Anda belajar.</p>

            <div class="chat-container" id="chatContainer">
                <div class="message ai-message">
                    <strong>AI Tutor:</strong> Halo! Saya adalah AI tutor programming. Apa yang ingin Anda pelajari hari ini? (HTML, CSS, JavaScript, Python, dll.)
                </div>
            </div>

            <div class="input-container">
                <input type="text" id="userInput" placeholder="Ketik pertanyaan Anda di sini..." onkeypress="handleKeyPress(event)">
                <button class="btn" onclick="sendMessage()">Kirim</button>
            </div>

            <div style="text-align: center; margin-top: 20px;">
                <a href="/" class="btn">🏠 Kembali ke Menu Utama</a>
            </div>
        </div>

        <script>
            // Fungsi keamanan: Sanitasi input untuk mencegah XSS
            function bersihkanInput(input) {{
                const map = {{
                    '&': '&amp;',
                    '<': '<',
                    '>': '>',
                    '"': '"',
                    "'": '&#x27;',
                    "/": '&#x2F;'
                }};
                const reg = /[&<>"'/]/ig;
                return input.replace(reg, (match) => map[match]);
            }}

            // Fungsi keamanan: Tampilkan teks dengan aman
            function tampilkanDiWeb(elementId, pesanDariDatabase) {{
                const element = document.getElementById(elementId);
                if (element) {{
                    element.textContent = pesanDariDatabase;
                }}
            }}

            function sendMessage() {{
                const input = document.getElementById('userInput');
                const message = input.value.trim();
                if (!message) return;

                // Sanitasi input user
                const sanitizedMessage = bersihkanInput(message);

                // Add user message
                addMessage(sanitizedMessage, 'user');

                // Simulate AI response
                setTimeout(() => {{
                    const response = getAIResponse(message);
                    addMessage(response, 'ai');
                }}, 1000);

                input.value = '';
            }}

            function handleKeyPress(event) {{
                if (event.key === 'Enter') {{
                    sendMessage();
                }}
            }}

            function addMessage(text, type) {{
                const container = document.getElementById('chatContainer');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${{type}}-message`;
                // Gunakan textContent untuk keamanan
                messageDiv.innerHTML = `<strong>${{type === 'user' ? 'Anda' : 'AI Tutor'}}:</strong> `;
                const textSpan = document.createElement('span');
                textSpan.textContent = text;
                messageDiv.appendChild(textSpan);
                container.appendChild(messageDiv);
                container.scrollTop = container.scrollHeight;
            }}

            function getAIResponse(question) {{
                const responses = {{
                    'html': 'HTML adalah bahasa markup untuk membuat struktur halaman web. Elemen dasar: <h1>, <p>, <a>, <div>.',
                    'css': 'CSS digunakan untuk styling. Properti seperti color, background, margin, padding.',
                    'javascript': 'JavaScript membuat web interaktif. Konsep: variabel, fungsi, event, DOM.',
                    'python': 'Python mudah dipelajari. Konsep: variabel, loop, function, class.',
                    'halo': 'Halo! Ada yang bisa saya bantu?',
                    'hi': 'Hi! Apa yang ingin Anda pelajari?',
                    'default': 'Itu pertanyaan menarik! Saya bisa membantu dengan HTML, CSS, JavaScript, dan Python. Apa spesifik yang ingin Anda tanyakan?'
                }};

                const lowerQuestion = question.toLowerCase();
                for (const key in responses) {{
                    if (lowerQuestion.includes(key)) {{
                        return responses[key];
                    }}
                }}
                return responses['default'];
            }}
        </script>
    </body>
    </html>
    """
    return html

# Jalankan aplikasi jika file ini dieksekusi langsung
if __name__ == "__main__":
    print("🤖 AI Tutor Web - Starting Flask server...")
    print("Buka browser ke: http://localhost:5000")
    print("Tekan Ctrl+C untuk menghentikan server")
    app.run(debug=True, host='0.0.0.0', port=5000)
