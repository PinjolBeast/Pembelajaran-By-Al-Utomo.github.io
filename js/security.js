/**
 * MASTER SECURITY PROTOCOL 2026
 * Dibuat untuk tujuan pembelajaran keamanan Front-End tingkat lanjut.
 */

document.addEventListener("DOMContentLoaded", () => {

    /* --- 1. TEKNIK HONEYPOT (Perangkap Bot) ---
       Pembelajaran: Manusia tidak akan bisa melihat atau mengisi input yang 
       disembunyikan secara visual. Namun, bot spammer akan otomatis mengisi 
       semua field input yang ada di dalam struktur kode (DOM).
    */
    const kuisForm = document.getElementById('kuisForm'); // Contoh pada form kuis
    if (kuisForm) {
        kuisForm.addEventListener('submit', function(e) {
            // Mengambil input jebakan dengan nama 'website_url' (nama umum yang disukai bot)
            const botTrap = this.querySelector('input[name="website_url"]').value;
            
            if (botTrap.length > 0) {
                console.error("KEAMANAN: Bot Terdeteksi melalui Honeypot!");
                e.preventDefault(); // Menghentikan pengiriman data
                return;
            }
        });
    }

    /* --- 2. PENYEMBUNYIAN EMAIL DINAMIS ---
       Pembelajaran: Jangan pernah menulis email utuh dalam variabel tunggal.
       Gunakan manipulasi string agar scraper cerdas pun sulit merekonstruksi email.
    */
    const secureMailLink = document.getElementById('secure-mail');
    if (secureMailLink) {
        secureMailLink.addEventListener('click', (e) => {
            e.preventDefault();
            // Data dipecah dan digabung sesaat sebelum eksekusi (Just-In-Time)
            const part1 = "tomi";
            const part2 = "sarwo";
            const provider = "yahoo";
            const tld = "co.id";
            
            window.location.href = `mailto:${part1}.${part2}@${provider}.${tld}`;
        });
    }

    /* --- 3. PENCEGAHAN INJEKSI XSS (SANITASI TINGKAT LANJUT) ---
       Pembelajaran: Saat menampilkan kembali teks dari user (misal di halaman kuis/debat), 
       selalu gunakan 'textContent' atau 'innerText'. 
       HINDARI 'innerHTML' karena bisa mengeksekusi tag <script> jahat.
    */
    window.displaySafeText = function(targetElementId, rawText) {
        const target = document.getElementById(targetElementId);
        if (target) {
            // textContent akan merubah <script> menjadi teks mati yang tidak berbahaya
            target.textContent = rawText; 
        }
    };

    /* --- 4. PROTEKSI JENDELA (TAB-NABBING) ---
       Pembelajaran: Atribut 'rel="noopener"' memutuskan hubungan antara halaman asal 
       dan halaman tujuan. Tanpa ini, halaman tujuan bisa mengubah URL halaman asal 
       Anda menjadi situs penipuan (Phishing).
    */
    const protectAllExternalLinks = () => {
        const allLinks = document.querySelectorAll('a[target="_blank"]');
        allLinks.forEach(link => {
            link.setAttribute('rel', 'noopener noreferrer');
        });
    };
    protectAllExternalLinks();

    /* --- 5. ANTI-STEAL ASSETS (KEAMANAN GAMBAR) ---
       Pembelajaran: Mencegah bot/pengguna mengambil aset gambar dengan klik kanan 
       menggunakan pencegahan 'contextmenu'.
    */
    document.addEventListener('contextmenu', (e) => {
        if (e.target.tagName === 'IMG') {
            e.preventDefault();
            alert("Informasi: Aset visual dilindungi sistem keamanan 2026.");
        }
    });

    /* --- 6. FRAME BUSTING (ANTI-CLICKJACKING) ---
       Pembelajaran: Memastikan website Anda adalah 'Top Level Window'. 
       Mencegah website Anda dibungkus oleh Iframe rahasia di situs judi atau scam 
       untuk mencuri klik mouse Anda.
    */
    if (window.top !== window.self) {
        window.top.location = window.self.location;
    }

});
/**
 * PENCEGAHAN SUPPLY CHAIN ATTACK
 * Pembelajaran: Kita bisa mengecek apakah library luar yang kita pakai 
 * masih memiliki fungsi yang kita butuhkan atau sudah diubah isinya.
 */
function checkLibraryIntegrity() {
    // Contoh: Cek apakah Font Awesome termuat dengan benar
    if (typeof FontAwesome === 'undefined' && document.querySelector('.fa')) {
        console.error("KEAMANAN: Library Font Awesome hilang atau dimodifikasi!");
        // Tindakan: Hapus ikon dari layar agar tidak disalahgunakan
        document.querySelectorAll('.fa').forEach(el => el.remove());
    }
}
window.onload = checkLibraryIntegrity;

/**
 * RINGKASAN PEMBELAJARAN:
 * 1. Honeypot: Menjebak bot pengisi form otomatis.
 * 2. Obfuscation: Menyamarkan data sensitif (Email/HP).
 * 3. Sanitasi: Mencegah eksekusi script jahat (XSS).
 * 4. Rel Security: Melindungi tab dari pembajakan (Tab-nabbing).
 * 5. Asset Protection: Melindungi hak cipta gambar produk.
 * 6. Frame Busting: Mencegah website dibajak dalam Iframe.
 */
