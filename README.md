### Tugas 2

1. Saat user buka halaman `education`, requestnya masuk ke `urls.py` utama di proyek, lalu diteruskan ke `urls.py` di aplikasi `main`. Di situ URL dipetakan ke fungsi `show_education` di file `views.py`. view akan meminta data ke model `Education` untuk mengambil semua data pendidikan dari database. Datanya dimasukan ke context dan dikirim ke template `education.html`. Di template, datanya dirender jadi HTML yang rapi dan dikirim balik untuk ditampilkan di browser

2. Menyimpan data di model membuat aplikasi lebih mudah dikelola. Kalau nanti mau tambah riwayat pendidikan baru, kita tinggal input datanya ke database dan otomatis langsung muncul di web karena pakai looping di template. Kalau ditulis langsung atau dihardcode di template, tiap mau nambah data harus buka dan edit kode HTMLnya lagi satu per satu, yang mana kodenya akan makin panjang dan rawan typo merusak struktur tagnya.

3. Fungsi `makemigrations` seperti membuat catatan instruksi perubahan berdasarkan kode yang ada di `models.py`. Sedangkan `migrate` fungsinya untuk menjalankan instruksi dari `makemigrations` tadi ke database sungguhan. Contohnya saat buat model class `Education` baru, harus menjalankan `makemigrations` dulu untuk mencatat persiapan pembuatan tabelnya, baru run `migrate` agar tabelnya benar benar dibuat di database.

### AI Disclosure
Tool yang Digunakan: Gemini

Saya menggunakan AI untuk membantu saya mengingatkan dan juga menjelaskan tahapan alur MVT di django agar tidak ada langkah yang terlewat dan membantu membuat html education