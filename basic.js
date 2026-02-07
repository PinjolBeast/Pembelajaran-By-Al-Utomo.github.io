// ===========================================
// PEMBELAJARAN DASAR JAVASCRIPT
// ===========================================
// Halo teman-teman! Selamat datang di dunia JavaScript!
// JavaScript adalah bahasa pemrograman yang membuat website "hidup".
// Tanpa JS, website cuma seperti buku statis - cantik tapi tidak interaktif.
//
// Pertanyaan untuk Anda: Pernahkah Anda klik tombol di website dan apa-apa terjadi?
// Itu adalah JavaScript yang bekerja! Tanpa JS, tombol itu cuma gambar saja.

// ===========================================
// 1. VARIABEL: PENYIMPANAN DATA
// ===========================================
// Bayangkan variabel seperti kotak penyimpanan. Kita bisa simpan nama, angka, dll.
// Mengapa perlu variabel? Agar kita bisa gunakan data berulang-ulang.

let namaPengguna = "Bimo"; // String - teks
let umur = 25;             // Number - angka
let isStudent = true;      // Boolean - true/false

// Pertanyaan: Apa yang terjadi jika kita ubah nilai variabel?
// Coba ubah namaPengguna di atas dan lihat apa yang berubah di halaman!

console.log("Halo, nama saya " + namaPengguna); // Ini muncul di console browser (F12)

// ===========================================
// 2. FUNGSI: BLOK KODE YANG BISA DIPANGGIL
// ===========================================
// Fungsi seperti resep masak. Kita definisi sekali, panggil kapan saja.
// Mengapa fungsi penting? Agar kode tidak diulang-ulang.

function sapaPengguna() {
    // Ambil nilai dari input HTML
    let namaInput = document.getElementById('namaInput').value;

    // Cek apakah input kosong
    if (namaInput === "") {
        alert("Eh, masukkan nama dulu dong! 😊");
        return; // Stop fungsi jika kosong
    }

    // Tampilkan hasil
    let output = document.getElementById('hasilOutput');
    output.textContent = "Halo " + namaInput + "! Selamat belajar JavaScript! 🎉";

    // Pertanyaan: Apa yang terjadi jika kita hapus 'return' di atas?
    // Coba hapus dan lihat perbedaannya!
}

// ===========================================
// 3. EVENT HANDLING: MENANGANI KLIK DAN INTERAKSI
// ===========================================
// JavaScript bisa "mendengarkan" apa yang user lakukan.
// Ini yang membuat website interaktif!

function ubahWarna() {
    // Ubah background body secara random
    let warna = ['#ff9999', '#99ff99', '#9999ff', '#ffff99', '#ff99ff'];
    let randomWarna = warna[Math.floor(Math.random() * warna.length)];

    document.body.style.backgroundColor = randomWarna;

    // Pertanyaan: Mengapa kita pakai Math.random()?
    // Apa yang terjadi jika kita hapus Math.floor()?
}

function tampilkanAlert() {
    alert("Ini adalah alert dari JavaScript! 📢");

    // Pertanyaan: Apa bedanya alert, confirm, dan prompt?
    // Coba ganti alert dengan confirm dan lihat apa yang berbeda!
}

function hitungAngka() {
    let hasil = 5 + 3;
    alert("5 + 3 = " + hasil);

    // Pertanyaan: Mengapa hasilnya 8? Apa yang terjadi jika kita ubah jadi 5 * 3?
    // Coba ubah operator dan lihat hasilnya!
}

// ===========================================
// 4. DOM MANIPULATION: MENGUBAH HTML DARI JAVASCRIPT
// ===========================================
// DOM = Document Object Model. Bayangkan HTML sebagai pohon, JS bisa ubah daunnya.
// Mengapa penting? Agar konten berubah tanpa reload halaman.

function ubahKonten() {
    let heading = document.querySelector('h1');
    heading.textContent = "JavaScript Telah Mengubah Judul Ini! ✨";

    // Pertanyaan: Apa bedanya getElementById vs querySelector?
    // Coba ganti querySelector('h1') dengan getElementById('judul') dan lihat errornya!
}

// ===========================================
// 5. CONDITIONAL: LOGIKA IF-ELSE
// ===========================================
// Komputer bisa "berpikir" dengan if-else.
// Ini dasar dari semua aplikasi cerdas!

function cekUmur() {
    let umurInput = prompt("Berapa umur Anda?");

    if (umurInput < 18) {
        alert("Anda masih remaja! 🌟");
    } else if (umurInput >= 18 && umurInput < 60) {
        alert("Anda dewasa! 💼");
    } else {
        alert("Anda sudah senior! 👴");
    }

    // Pertanyaan: Apa yang terjadi jika kita hapus '&& umurInput < 60'?
    // Mengapa kita perlu kondisi ganda?
}

// ===========================================
// 6. LOOP: PENGULANGAN
// ===========================================
// Loop seperti conveyor belt - ulangi task berkali-kali.
// Berguna untuk list, array, dll.

function hitungMundur() {
    let output = document.getElementById('hasilOutput');

    output.textContent = "Hitung mundur: ";

    for (let i = 10; i >= 1; i--) {
        output.textContent += i + " ";
    }

    output.textContent += "SELESAI! 🚀";

    // Pertanyaan: Apa bedanya for, while, dan do-while?
    // Coba ubah jadi while loop dan lihat perbedaannya!
}

// ===========================================
// 7. ARRAY: KUMPULAN DATA
// ===========================================
// Array seperti laci penyimpanan banyak item.
// JavaScript array bisa campur tipe data!

let hobi = ["coding", "gaming", "membaca", "olahraga"];
let angka = [1, 2, 3, 5, 8, 13];

function tampilkanArray() {
    let output = document.getElementById('hasilOutput');

    output.textContent = "Hobi saya: " + hobi.join(", ") + "\n";
    output.textContent += "Angka favorit: " + angka.join(" - ");

    // Pertanyaan: Apa fungsi join()? Apa yang terjadi jika kita hapus join?
    // Coba tambah item ke array dengan hobi.push("baru") dan lihat hasilnya!
}

// ===========================================
// 8. OBJECT: DATA KOMPLEKS
// ===========================================
// Object seperti kartu identitas - punya properties.
// Berguna untuk data kompleks seperti user profile.

let profil = {
    nama: "Bimo Prayogo",
    umur: 25,
    kota: "Jakarta",
    hobi: ["coding", "gaming"],
    isStudent: true
};

function tampilkanProfil() {
    let output = document.getElementById('hasilOutput');

    output.textContent = "Nama: " + profil.nama + "\n";
    output.textContent += "Umur: " + profil.umur + "\n";
    output.textContent += "Kota: " + profil.kota + "\n";
    output.textContent += "Hobi: " + profil.hobi.join(", ");

    // Pertanyaan: Apa bedanya array dan object?
    // Kapan kita pakai object vs array?
}

// ===========================================
// KENAPA JAVASCRIPT PENTING?
// ===========================================
// 1. Interaktivitas: Tombol, form, animasi
// 2. Dynamic Content: Konten berubah tanpa reload
// 3. User Experience: Feedback instan ke user
// 4. Modern Web Apps: SPA (Single Page Applications)
//
// Pertanyaan besar: Bayangkan Instagram tanpa JavaScript!
// Bagaimana cara like foto? Scroll infinite? Chat real-time?
//
// Jawaban: Tidak mungkin! JavaScript membuat web modern.
//
// Tantangan untuk Anda:
// 1. Buka console browser (F12) dan coba console.log("Hello World!")
// 2. Ubah fungsi di atas dan lihat apa yang berubah
// 3. Buat fungsi baru sendiri!
// 4. Coba error - sengaja buat kesalahan dan lihat pesan errornya
//
// Ingat: Coding adalah trial and error. Jangan takut salah!

// ===========================================
// TUGAS PRAKTEK:
// ===========================================
// 1. Buat fungsi yang menghitung luas persegi panjang
// 2. Buat array warna dan ubah background secara random
// 3. Buat object "mobil" dengan properties merk, tahun, warna
// 4. Gunakan loop untuk tampilkan 1-100, tapi skip kelipatan 5
//
// Tips: Gunakan console.log() untuk debug!
// Jika stuck, tanya Google atau lihat MDN Web Docs.

// Selamat belajar JavaScript! 🚀
// Setiap programmer pemula pernah bingung, termasuk saya dulu.
// Teruslah eksplorasi dan jangan menyerah!
