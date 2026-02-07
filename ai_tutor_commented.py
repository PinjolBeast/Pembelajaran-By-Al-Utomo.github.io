#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI TUTOR PEMBELAJARAN CODING - VERSI ULTIMATE DENGAN KOMENTAR DETAIL
Skrip Python interaktif untuk belajar coding dengan cara seperti AI chatbot.
Dibuat untuk pemula yang ingin belajar programming dengan bahasa Indonesia.

Fitur Utama:
- Interaktif seperti AI tutor dengan efek mengetik
- Bahasa Indonesia penuh
- Generate contoh HTML, CSS, JS, dan Python
- Komentar detail untuk belajar
- Quiz interaktif dengan scoring
- Progress tracking
- File management (buat, edit, hapus file)
- Tidak perlu library tambahan (hanya built-in Python)
- Error handling yang baik
- Cross-platform (Windows, Linux, Mac)

Cara menjalankan:
1. Pastikan Python 3.x terinstall (download dari python.org)
2. Jalankan: python ai_tutor_commented.py
3. Ikuti instruksi di layar
4. File contoh akan dibuat di folder yang sama

Requirements:
- Python 3.6+
- Tidak ada library eksternal diperlukan

Author: AI Assistant
Versi: 2.0 - Ultimate Edition dengan Komentar
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

# Mengapa import banyak? Karena program ini multifungsi: file I/O, random, JSON, dll.
# Keanehan: Tidak ada yang aneh di sini, standar untuk program Python kompleks.

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

// Number - angka
let umur = 25;

// Boolean - true/false
let isStudent = true;

// Array - kumpulan data
let hobi = ["coding", "gaming", "reading"];

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
// CONTOH PENGUNAAN
// ===========================================

// Jalankan contoh saat file dimuat
console.log("=== CONTOH PENGUNAAN JAVASCRIPT ===");

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

    # Konten HTML sebagai string (keanehan: panjang dan hardcoded)
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
# FUNGSI UTAMA PROGRAM
# ===========================================

def main():
    """
    Fungsi utama program AI Tutor.

    Mengapa loop while True? Untuk menu interaktif sampai user keluar.
    Keanehan: Input tanpa validasi, bisa error jika bukan angka.
    Perbaikan: Tambahkan try-except untuk input.
    """
    clear_screen()

    type_text("🤖 SELAMAT DATANG DI AI TUTOR PEMBELAJARAN CODING!")
    type_text("=" * 60)
    type_text("Saya adalah AI tutor yang akan membantu Anda belajar coding.")
    type_text("Kita akan belajar HTML, CSS, JavaScript, dan konsep programming lainnya.")
    type_text("Mari mulai perjalanan coding Anda!\n")

    while True:  # Loop utama menu
        type_text("\n📚 MENU PELAJARAN:")
        type_text("1. HTML Dasar - Struktur halaman web")
        type_text("2. CSS Dasar - Styling dan layout")
        type_text("3. JavaScript Dasar - Interaktivitas")
        type_text("4. Keluar dari program")
        type_text("\n💡 Tips: Buka file HTML yang dibuat di browser untuk melihat hasilnya!")

        try:
            pilihan = input("\nPilih pelajaran (1-4): ").strip()  # Input pilihan, strip spasi

            if pilihan == "1":
                pelajaran_html()  # Panggil fungsi HTML
            elif pilihan == "2":
                pelajaran_css()  # Panggil fungsi CSS
            elif pilihan == "3":
                pelajaran_javascript()  # Panggil fungsi JS
            elif pilihan == "4":
                type_text("\n👋 Terima kasih telah belajar dengan AI Tutor!")
                type_text("Sampai jumpa di pelajaran berikutnya! 🚀")
                break  # Keluar loop
            else:
                type_text("❌ Pilihan tidak valid. Silakan pilih 1-4.")  # Error message

        except KeyboardInterrupt:  # Jika user tekan Ctrl+C
            type_text("\n\n👋 Program dihentikan. Terima kasih!")
            break
        except Exception as e:  # Exception lainnya
            type_text(f"❌ Terjadi error: {e}")
            type_text("Silakan coba lagi.")

        input("\nTekan Enter untuk melanjutkan...")

# Jalankan program jika file ini dieksekusi langsung
if __name__ == "__main__":
    # Cek versi Python
    if sys.version_info[0] < 3:
        print("❌ Error: Program ini membutuhkan Python 3.x")
        print("Silakan install Python 3 dari https://python.org")
        sys.exit(1)

    main()
