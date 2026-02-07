# Penjelasan Perbaikan Error pada bersihkanInput dan tampilkanDiWeb

## Pendahuluan
Dalam proyek ini, terdapat error pada fungsi `bersihkanInput` dan `tampilkanDiWeb` yang terdeteksi oleh sistem VSCode. Error ini berkaitan dengan keamanan XSS (Cross-Site Scripting) dan konfigurasi TypeScript. Berikut adalah penjelasan lengkap mengenai error, perbaikan yang dilakukan, dan alasan penambahan file/konfigurasi.

## Error yang Ditemukan
### 1. Error pada `bersihkanInput` di `js/main.js`
- **Deskripsi Error**: Fungsi `bersihkanInput` memiliki mapping HTML entity yang salah. Alih-alih mengubah karakter berbahaya menjadi entity HTML yang aman, fungsi ini hanya mengembalikan karakter asli, sehingga tidak mencegah serangan XSS.
- **Kode Bermasalah**:
  ```javascript
  const map = {
    '&': '&amp;',
    '<': '<',  // Salah: harus '<'
    '>': '>',  // Salah: harus '>'
    '"': '"',  // Salah: harus '"'
    "'": '&#x27;',
    "/": '&#x2F;',
  };
  ```
- **Dampak**: Input seperti `<script>alert('hack')</script>` tidak akan disanitasi dengan benar, sehingga bisa menimbulkan kerentanan keamanan.

### 2. Error pada `tampilkanDiWeb` di `js/main.js`
- **Deskripsi Error**: Fungsi ini menggunakan `innerHTML` yang berbahaya untuk menampilkan konten dinamis, yang bisa menyebabkan XSS jika data dari database tidak disanitasi dengan benar.
- **Kode Bermasalah**:
  ```javascript
  element.innerHTML = pesanDariDatabase; // Berbahaya!
  ```
- **Dampak**: Meskipun `bersihkanInput` diperbaiki, penggunaan `innerHTML` tetap berisiko jika ada kesalahan dalam sanitasi.

### 3. Error Deteksi VSCode pada `ts/protect.ts`
- **Deskripsi Error**: VSCode mendeteksi error karena fungsi `bersihkanInput`, `tampilkanDiWeb`, dan `kirimKomentar` tidak diekspor (export), sehingga dianggap tidak digunakan. Selain itu, TypeScript strict mode menandai variabel yang tidak digunakan.
- **Dampak**: Meskipun kode berfungsi, VSCode menampilkan peringatan merah yang mengganggu pengembangan.

## Perbaikan yang Dilakukan
### 1. Perbaikan `bersihkanInput` di `js/main.js`
- **Perubahan**: Mengubah mapping karakter ke entity HTML yang benar.
- **Kode Setelah Perbaikan**:
  ```javascript
  function bersihkanInput(input) {
    const map = {
      '&': '&amp;',
      '<': '<',  // Benar: mengubah < menjadi <
      '>': '>',  // Benar: mengubah > menjadi >
      '"': '"', // Benar: mengubah " menjadi "
      "'": '&#x27;',
      "/": '&#x2F;',
    };
    const reg = /[&<>"'/]/ig;
    return input.replace(reg, (match) => map[match]);
  }
  ```
- **Penjelasan**:
  - `map`: Objek yang memetakan karakter berbahaya ke entity HTML aman. Misalnya, `<` diubah menjadi `<` agar tidak diinterpretasikan sebagai tag HTML.
  - `reg`: Regular expression dengan flag `i` (case insensitive) dan `g` (global) untuk mencocokkan semua karakter berbahaya.
  - `replace`: Mengganti setiap kecocokan dengan entity dari `map`.
- **Alasan**: Ini mencegah XSS dengan mengubah karakter HTML menjadi teks biasa yang aman ditampilkan.

### 2. Perbaikan `tampilkanDiWeb` di `js/main.js`
- **Perubahan**: Mengubah `innerHTML` menjadi `textContent` untuk keamanan.
- **Kode Setelah Perbaikan**:
  ```javascript
  function tampilkanDiWeb(pesanDariDatabase, elementId) {
    const element = document.getElementById(elementId);
    if (element) {
      element.textContent = pesanDariDatabase; // Aman: menggunakan textContent
    }
  }
  ```
- **Penjelasan**:
  - `document.getElementById(elementId)`: Mencari elemen HTML berdasarkan ID.
  - `element.textContent = pesanDariDatabase`: Menetapkan teks secara aman tanpa mengeksekusi HTML.
- **Alasan**: `textContent` hanya menampilkan teks biasa, sedangkan `innerHTML` bisa mengeksekusi script jika ada tag HTML dalam data.

### 3. Penambahan Export di `ts/protect.ts`
- **Perubahan**: Menambahkan `export` pada fungsi dan konstanta agar bisa digunakan di tempat lain.
- **Kode Setelah Perbaikan**:
  ```typescript
  export function bersihkanInput(input: string): string {
    // ... kode sanitasi
  }

  export const kirimKomentar = async (teksKomentar: string) => {
    // ... kode pengiriman komentar
  };

  export function tampilkanDiWeb(pesanDariDatabase: string) {
    // ... kode tampilan aman
  }
  ```
- **Penjelasan**:
  - `export`: Membuat fungsi/konstanta dapat diimpor di file lain.
  - `bersihkanInput`: Fungsi untuk sanitasi input.
  - `kirimKomentar`: Fungsi async untuk mengirim komentar ke Firebase setelah sanitasi.
  - `tampilkanDiWeb`: Fungsi untuk menampilkan pesan dari database dengan aman.
- **Alasan**: Export mencegah VSCode menandai sebagai "unused", dan memungkinkan penggunaan modular.

### 4. Penambahan `tsconfig.json`
- **Perubahan**: Membuat file konfigurasi TypeScript.
- **Kode**:
  ```json
  {
    "compilerOptions": {
      "target": "ES2020",
      "module": "ESNext",
      "lib": ["DOM", "ES2020"],
      "strict": true,
      "esModuleInterop": true,
      "skipLibCheck": true,
      "forceConsistentCasingInFileNames": true,
      "noUnusedLocals": false,
      "noUnusedParameters": false
    },
    "include": ["ts/**/*"],
    "exclude": ["node_modules"]
  }
  ```
- **Penjelasan**:
  - `target`: Kompilasi ke ES2020.
  - `module`: Menggunakan modul ESNext.
  - `lib`: Termasuk DOM dan ES2020 untuk browser.
  - `strict`: Mode ketat untuk TypeScript.
  - `noUnusedLocals` dan `noUnusedParameters`: Ditetapkan `false` untuk tidak menandai variabel tidak digunakan sebagai error.
  - `include`: Hanya kompilasi file di folder `ts/`.
- **Alasan**: Mengatur TypeScript agar tidak menampilkan peringatan yang tidak diinginkan, dan memastikan kompilasi yang benar.

## Kesimpulan
Perbaikan ini meningkatkan keamanan aplikasi dengan mencegah XSS melalui sanitasi input yang benar dan tampilan yang aman. Penambahan export dan konfigurasi TypeScript menghilangkan error deteksi VSCode, sehingga kode lebih bersih dan mudah dikembangkan. Pastikan untuk selalu menggunakan `textContent` untuk konten dinamis dan sanitasi input sebelum penyimpanan atau tampilan.
