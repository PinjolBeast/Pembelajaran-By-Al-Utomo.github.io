/**
 * PEMBELAJARAN LOGIKA KUIS INTERAKTIF
 * -----------------------------------
 * Modul 'readline' digunakan untuk membaca input dari keyboard (terminal).
 */
const readline = require('readline');

// Membuat interface input (apa yang kita ketik) dan output (apa yang muncul di layar)
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

/**
 * STRUKTUR DATA (ARRAY OF OBJECTS)
 * q = question (pertanyaan)
 * a = answer (kunci jawaban)
 */
const bankSoal = [
    // --- MATERI KELAS 10 ---
    { q: "1. Hasil dari 2^3 * 2^2? (Sifat Eksponen: pangkat dijumlahkan)", a: "32" },
    { q: "2. Nilai dari 5^0? (Semua angka pangkat 0 hasilnya satu)", a: "1" },
    { q: "3. Akar x^2 - 5x + 6 = 0 adalah 2 dan...? (Cari angka yang kalau dikali jadi 6)", a: "3" },
    { q: "4. Nilai dari log100 (basis 10)? (10 pangkat berapa jadi 100?)", a: "2" },
    { q: "5. Nilai dari 3^log9 (basis 3)?", a: "2" },
    { q: "6. Jika f(x) = 2x + 3, maka f(5) adalah? (Ganti x dengan angka 5)", a: "13" },
    { q: "7. Bentuk sederhana dari (a^5)/(a^2)? (Pangkat dikurangi)", a: "a^3" },
    { q: "8. Nilai x dari 2x + 5 = 11?", a: "3" },
    { q: "9. Suku ke-n barisan 2, 5, 8... Berapa bedanya (b)? (Selisih antar angka)", a: "3" },
    { q: "10. Nilai sin 30 derajat?", a: "0.5" },

    // --- MATERI KELAS 11 ---
    { q: "11. Barisan geometri: 2, 4, 8... Berapa rasionya (r)? (Pengalinya)", a: "2" },
    { q: "12. Determinan matriks [[1,2],[3,4]]? (Rumus: ad - bc)", a: "-2" },
    { q: "13. Jika A=[2] dan B=[3], maka A+B?", a: "5" },
    { q: "14. Pusat lingkaran (x-2)^2 + (y+3)^2 = 25? (Ambil lawan tandanya)", a: "-3" },
    { q: "15. Jari-jari lingkaran x^2 + y^2 = 49? (Akar dari 49)", a: "7" },
    { q: "16. Nilai tan 45 derajat?", a: "1" },
    { q: "17. Banyak cara susun angka 1,2,3? (3! = 3x2x1)", a: "6" },
    { q: "18. S3 aritmetika jika a=2, b=2? (2 + 4 + 6)", a: "12" },
    { q: "19. Nilai cos 0 derajat?", a: "1" },
    { q: "20. Bayangan (1,2) dicerminkan sumbu X? (y berubah tanda)", a: "(1,-2)" },
    { q: "21. Gradien garis y = 3x + 5? (Angka di depan x)", a: "3" },
    { q: "22. Limit x->3 dari 2x? (Langsung substitusi)", a: "6" },
    { q: "23. Turunan x^2? (Pangkat turun jadi pengali, lalu pangkat kurangi 1)", a: "2x" },
    { q: "24. Integral dari 2x dx? (Kebalikan turunan)", a: "x^2" },
    { q: "25. Peluang angka pada satu koin? (1 dari 2 sisi)", a: "0.5" },
    { q: "26. Titik sampel 2 dadu? (6 pangkat 2)", a: "36" },
    { q: "27. Nilai dari 4! (4 faktorial: 4x3x2x1)?", a: "24" },
    { q: "28. Hasil dari 5P2 (Permutasi)?", a: "20" },
    { q: "29. Hasil dari 5C2 (Kombinasi)?", a: "10" },
    { q: "30. Suku ke-5 barisan 1, 3, 5, 7...?", a: "9" },

    // --- MATERI KELAS 12 ---
    { q: "31. Mean dari 2, 4, 6? (Rata-rata: jumlahkan lalu bagi 3)", a: "4" },
    { q: "32. Median dari 1, 3, 5, 7, 9? (Nilai tengah)", a: "5" },
    { q: "33. Modus dari 2,2,3,4,4,4,5? (Paling sering muncul)", a: "4" },
    { q: "34. Banyak rusuk pada kubus?", a: "12" },
    { q: "35. Banyak titik sudut limas segi empat? (4 di bawah + 1 puncak)", a: "5" },
    { q: "36. Turunan dari sin(x)?", a: "cos(x)" },
    { q: "37. Turunan dari cos(x)?", a: "-sin(x)" },
    { q: "38. Integral sin(x) dx?", a: "-cos(x)" },
    { q: "39. Turunan 5x^2 + 3x?", a: "10x+3" },
    { q: "40. Limit x->0 dari sinx/x? (Teorema limit trigonometri)", a: "1" },
    { q: "41. Luas permukaan kubus rusuk 2 cm? (6 * r^2)", a: "24" },
    { q: "42. Volume kubus rusuk 3 cm? (r^3)", a: "27" },
    { q: "43. Simpangan baku jika semua nilai sama?", a: "0" },
    { q: "44. Turunan kedua dari x^3? (Turunkan dua kali)", a: "6x" },
    { q: "45. Integral dari 3x^2 dx?", a: "x^3" },
    { q: "46. Jarak (0,0) ke (3,4)? (Rumus Pythagoras: akar 3^2 + 4^2)", a: "5" },
    { q: "47. Nilai cos 60 derajat?", a: "0.5" },
    { q: "48. Nilai log 1000 (basis 10)?", a: "3" },
    { q: "49. Turunan dari 7x?", a: "7" },
    { q: "50. Hasil dari 2 + 3 * 4? (Operasi perkalian didahulukan)", a: "14" }
];

// Variabel untuk melacak progres kuis
let index = 0; // Mulai dari soal pertama (index 0)
let score = 0; // Skor awal nol

console.log("\x1b[36m%s\x1b[0m", "========================================");
console.log("\x1b[36m%s\x1b[0m", "   BELAJAR MATEMATIKA SMA 2026          ");
console.log("\x1b[36m%s\x1b[0m", "========================================\n");

/**
 * FUNGSI REKURSIF 'ask'
 * Fungsi ini memanggil dirinya sendiri sampai soal habis.
 */
function ask() {
    // Mengecek apakah masih ada soal yang tersisa
    if (index < bankSoal.length) {
        rl.question(`[Soal ${index + 1}/50] ${bankSoal[index].q}\nJawab: `, (input) => {
            
            // PROSES NORMALISASI JAWABAN:
            // .trim() = hapus spasi di awal/akhir
            // .toLowerCase() = ubah jadi huruf kecil semua
            // .replace(/\s+/g, '') = hapus semua spasi di tengah (agar '2x + 3' dianggap sama dengan '2x+3')
            let ans = input.trim().toLowerCase().replace(/\s+/g, '');
            let key = bankSoal[index].a.toLowerCase().replace(/\s+/g, '');

            // Logika pengecekan jawaban
            if (ans === key) {
                console.log("\x1b[32m%s\x1b[0m", "✔ BENAR! Bagus sekali.\n");
                score++; // Tambah skor jika benar
            } else {
                console.log("\x1b[31m%s\x1b[0m", `✘ SALAH! Belajar lagi ya. Kunci: ${bankSoal[index].a}\n`);
            }

            index++; // Pindah ke nomor soal berikutnya
            ask();   // Panggil fungsi ask() lagi untuk soal selanjutnya
        });
    } else {
        // TAMPILAN AKHIR (Jika semua soal sudah dijawab)
        console.log("\x1b[33m%s\x1b[0m", "=== KUIS SELESAI ===");
        console.log(`Total Skor Benar: ${score} dari ${bankSoal.length} soal.`);
        console.log(`Nilai Akhir: ${(score / bankSoal.length) * 100}`);
        
        // Menutup interface agar program berhenti
        rl.close();
    }
}

// Menjalankan fungsi ask untuk pertama kalinya
ask();
