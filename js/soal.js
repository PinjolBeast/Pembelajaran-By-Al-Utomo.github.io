/**
 * 1. INISIALISASI MODUL READLINE
 * Modul ini adalah standar Node.js untuk menangani input/output di terminal.
 */
const readline = require('readline');

// Membuat 'interface' agar program bisa membaca ketikan keyboard (stdin) 
// dan menampilkan teks ke terminal (stdout).
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

/**
 * 2. BANK SOAL (DATABASE SEDERHANA)
 * Menggunakan Array of Objects. Memudahkan kita menambah soal tanpa merubah logika coding.
 */
const bankSoal = [
    {
        pertanyaan: "1. Berapakah turunan pertama (dy/dx) dari fungsi y = 3x^2 + 5x?\nJawaban: ",
        kunci: "6x+5"
    },
    {
        pertanyaan: "2. Berapakah hasil dari integral ∫ 2x dx?\nJawaban: ",
        kunci: "x^2"
    },
    {
        pertanyaan: "3. Turunan dari sin(x) adalah...\nJawaban: ",
        kunci: "cos(x)"
    },
    {
        pertanyaan: "4. Lim x->2 dari (x^2 - 4) / (x - 2) adalah...\nJawaban: ",
        kunci: "4"
    }
];

// Variabel pelacak posisi soal dan skor
let soalSekarang = 0;
let skor = 0;

/**
 * 3. TAMPILAN AWAL
 * \x1b[36m adalah kode warna Cyan. %s adalah tempat teks dimasukkan.
 * \x1b[0m adalah perintah untuk mereset warna kembali ke normal.
 */
console.log("\x1b[36m%s\x1b[0m", "=== KUIS KALKULUS INTERAKTIF 2026 ===");
console.log("Ketik jawabanmu (tanpa spasi untuk fungsi) dan tekan Enter.\n");

/**
 * 4. FUNGSI LOGIKA UTAMA (REKURSIF)
 * Fungsi ini memanggil dirinya sendiri (rekursi) agar soal muncul satu per satu
 * setelah user menjawab, karena proses input di Node.js bersifat menunggu (async).
 */
function jalankanKuis() {
    // Mengecek apakah index soalSekarang masih lebih kecil dari total soal yang ada
    if (soalSekarang < bankSoal.length) {
        
        // Mengajukan pertanyaan ke user
        rl.question(bankSoal[soalSekarang].pertanyaan, (jawabanUser) => {
            
            /**
             * 5. NORMALISASI JAWABAN (BAGIAN PALING PENTING)
             * .replace(/\s+/g, '') => Menghapus semua spasi agar '6x + 5' sama dengan '6x+5'.
             * .toLowerCase() => Mengubah semua huruf jadi kecil agar 'COS(x)' sama dengan 'cos(x)'.
             */
            const jawabanBersih = jawabanUser.replace(/\s+/g, '').toLowerCase();
            const kunciBersih = bankSoal[soalSekarang].kunci.toLowerCase();

            // Membandingkan jawaban user dengan kunci
            if (jawabanBersih === kunciBersih) {
                console.log("\x1b[32m%s\x1b[0m", "✔ BENAR!\n"); // Kode 32m untuk warna Hijau
                skor++; // Menambah poin jika benar
            } else {
                console.log("\x1b[31m%s\x1b[0m", `✘ SALAH! Jawaban yang benar adalah: ${bankSoal[soalSekarang].kunci}\n`); // Kode 31m untuk warna Merah
            }
            
            // Increment untuk lanjut ke soal berikutnya
            soalSekarang++;
            
            // Memanggil kembali fungsi ini untuk soal selanjutnya
            jalankanKuis();
        });
    } else {
        /**
         * 6. PENUTUP (KUIS SELESAI)
         * Menampilkan skor akhir dan menutup koneksi terminal.
         */
        console.log("\x1b[33m%s\x1b[0m", "=== KUIS SELESAI ==="); // Kode 33m untuk warna Kuning
        console.log(`Skor Akhir Anda: ${skor} / ${bankSoal.length}`);
        
        // WAJIB: Menutup readline agar terminal tidak 'hang' atau menggantung
        rl.close();
    }
}

/**
 * 7. EKSEKUSI PROGRAM
 * Memulai kuis untuk pertama kalinya.
 */
jalankanKuis();
