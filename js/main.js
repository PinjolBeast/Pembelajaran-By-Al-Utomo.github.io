/**
 * PEMBELAJARAN LOGIKA PEMROGRAMAN: POHON NATAL TERMINAL
 * ----------------------------------------------------
 * Fungsi ini menggunakan teknik manipulasi String dan Perulangan (Looping).
 */

function buatPohonNatal(tinggi) {
    /**
     * 1. DEFINISI WARNA (ANSI ESCAPE CODES)
     * Kode \x1b[...m digunakan untuk memberi warna pada teks di terminal.
     * \x1b[0m berfungsi untuk 'reset' agar warna tidak bocor ke baris bawahnya.
     */
    const bintang = "\x1b[33m*\x1b[0m"; // Kuning (Gold)
    const daun = "\x1b[32m#\x1b[0m";   // Hijau (Green)
    const batang = "\x1b[33m| |\x1b[0m"; // Cokelat/Kuning (Brownish)
    const hiasan = ["\x1b[31mo\x1b[0m", "\x1b[35m*\x1b[0m"]; // Merah & Ungu (Lampu hias)

    console.log("\n      --- POHON NATAL TERMINAL 2026 ---\n");

    /**
     * 2. PUNCAK BINTANG
     * .repeat(tinggi) digunakan untuk membuat spasi agar bintang berada di tengah.
     */
    console.log(" ".repeat(tinggi) + bintang);

    /**
     * 3. LOGIKA PERULANGAN DAUN (NESTED LOOP)
     * Loop luar (i) untuk membuat baris baru (dari atas ke bawah).
     * Loop dalam (j) untuk mengisi karakter di dalam setiap baris.
     */
    for (let i = 1; i <= tinggi; i++) {
        // Mengatur spasi di kiri agar bentuk pohon jadi segitiga (piramida)
        let baris = " ".repeat(tinggi - i);
        let isiDaun = "";
        
        // Menghitung jumlah karakter daun per baris (Rumus: 2 * baris - 1)
        for (let j = 0; j < (2 * i - 1); j++) {
            /**
             * LOGIKA RANDOM (PROBABILITAS)
             * Math.random() > 0.8 artinya ada peluang 20% hiasan muncul secara acak
             * di antara karakter daun (#).
             */
            if (Math.random() > 0.8) {
                // Mengambil hiasan secara acak dari array 'hiasan'
                isiDaun += hiasan[Math.floor(Math.random() * hiasan.length)];
            } else {
                isiDaun += daun; // Jika tidak ada hiasan, isi dengan daun hijau (#)
            }
        }
        // Mencetak baris yang sudah dirakit ke terminal
        console.log(baris + isiDaun);
    }

    /**
     * 4. BATANG POHON
     * Menggunakan dua baris statis agar batang terlihat lebih tinggi.
     */
    console.log(" ".repeat(tinggi - 1) + batang);
    console.log(" ".repeat(tinggi - 1) + batang);
    
    console.log("\n   Selamat Menikmati Liburan, Naufal!\n");
}

/**
 * 5. EKSEKUSI FUNGSI
 * Memanggil fungsi dengan parameter angka 10 untuk menentukan tinggi pohon.
 */
buatPohonNatal(10);

/**
 * KEAMANAN LINKS - MENGHINDARI SPAM BOTS
 * Menambahkan event listener untuk semua link agar tidak terlihat di HTML dan menghindari spam bots.
 */
document.addEventListener('DOMContentLoaded', () => {
    // Email link
    const emailBtn = document.querySelector('.btn.email');
    if (emailBtn) {
        emailBtn.addEventListener('click', (e) => {
            e.preventDefault();
            window.location.href = 'jendelapintugt@gmail.com';
        });
    }

    // Instagram link
    const instagramBtn = document.querySelector('.btn.instagram');
    if (instagramBtn) {
        instagramBtn.addEventListener('click', (e) => {
            e.preventDefault();
            window.open('https://www.instagram.com/alutomo1', '_blank');
        });
    }

    // GitHub link
    const githubBtn = document.querySelector('.btn.github');
    if (githubBtn) {
        githubBtn.addEventListener('click', (e) => {
            e.preventDefault();
            window.open('https://github.com/pinjolbeast', '_blank');
        });
    }

    // WhatsApp link
    const whatsappBtn = document.querySelector('.btn.whatsapp');
    if (whatsappBtn) {
        whatsappBtn.addEventListener('click', (e) => {
            e.preventDefault();
            window.open('https://wa.me/6281334404273', '_blank');
        });
    }
});
