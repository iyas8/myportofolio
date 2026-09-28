# Portfolio Website

## Deskripsi Proyek
Proyek ini adalah sebuah website portofolio pribadi interaktif yang dibangun menggunakan framework web Django. Website ini dirancang untuk menampilkan profil, pengalaman, serta riwayat pendidikan secara dinamis menggunakan arsitektur Model-View-Template (MVT). Website ini juga dilengkapi fitur registrasi, login, dan logout, serta pembatasan hak akses data riwayat pendidikan berdasarkan peran pengguna.

## Cara Menjalankan Proyek (Setup)
1. Pastikan Python sudah terinstal di komputer.
2. Buka terminal dan aktifkan *virtual environment* (misal di Windows: `env\Scripts\activate`).
3. Instal semua dependensi dengan menjalankan: `pip install -r requirements.txt`.
4. Terapkan migrasi database dengan perintah: `python manage.py migrate`.
5. Buat akun pemilik portofolio (superuser) dengan perintah: `python manage.py createsuperuser`.
6. Jalankan server lokal dengan mengetik: `python manage.py runserver`.
7. Buka `http://localhost:8000/` di browser.
8. Untuk mencoba peran Editor, buka `http://localhost:8000/admin/` dan login sebagai superuser. Buat *Group* baru bernama `Editor` (nama harus persis sama), lalu masukkan akun pengguna biasa ke grup tersebut lewat halaman Users.

## Peran Pengguna
- **Pengunjung (belum login):** dapat melihat data. Jika mencoba memberi star atau membuka halaman ubah data, akan diarahkan ke halaman login.
- **Pengguna biasa:** dapat melihat data serta memberi atau membatalkan star. Tidak dapat menambah, mengubah, maupun menghapus data (HTTP 403).
- **Editor:** memiliki hak pengguna biasa dan dapat mengubah data. Tidak dapat menambah atau menghapus data (HTTP 403).
- **Pemilik portofolio (superuser):** dapat menambah, mengubah, dan menghapus data, serta memberi star.

---

### Tugas 4
Tidak ada pertanyaan reflektif untuk pekan ini dihilangkan.

### AI Disclosure
Tool yang Digunakan: Gemini

Konteks Penggunaan: Saya menggunakan AI untuk membantu menghubung rangka kerja logika otorisasi (role-based access control) antara Superuser dan Editor di file `views.py`. AI juga membantu saya memilih cara paling efisien untuk menyembunyikan elemen UI di *template* menggunakan *tags conditional* dari Django tanpa harus menulis ulang struktur HTML

---

### Tugas 3

1. `ModelForm` memungkinkan efisiensi kode dengan menggenerasi elemen form HTML secara otomatis berdasarkan struktur tipe data pada model Django, lengkap dengan validasi bawaan. Penggunaan `{% csrf_token %}` diwajibkan untuk keamanan guna mencegah *Cross-Site Request Forgery*, yakni eksploitasi di mana pihak ketiga memalsukan aksi *POST* seolah-olah berasal dari pengguna terautentikasi.

2. JSON lebih dominan pada pengembangan web modern karena strukturnya yang ringan, mudah dibaca, dan tidak menggunakan tag pembuka/penutup yang kompleks seperti XML. JSON juga merupakan bagian integral dari JavaScript, sehingga data dapat langsung diparsing dan dimanipulasi pada antarmuka frontend tanpa overhead tambahan

3. Saat user melakukan request ke URL API, fungsi view mengambil data dari database berupa himpunan QuerySet (objek Python). Data mentah ini belum dapat ditransmisikan melalui protokol HTTP, sehingga memerlukan serialization untuk menerjemahkannya menjadi representasi string berformat JSON yang dapat dipahami oleh browser.

### AI Disclosure
Tool yang Digunakan: Gemini

Konteks Penggunaan: Saya menggunakan AI untuk membantu menrapikan tata letak elemen antarmuka (CSS) serta menyusun kerangka penjelasan konsep *serialization* dan *ModelForm* 

---

### Tugas 2

1. Saat user buka halaman `education`, requestnya masuk ke `urls.py` utama di proyek, lalu diteruskan ke `urls.py` di aplikasi `main`. Di situ URL dipetakan ke fungsi `show_education` di file `views.py`. view akan meminta data ke model `Education` untuk mengambil semua data pendidikan dari database. Datanya dimasukan ke context dan dikirim ke template `education.html`. Di template, datanya dirender jadi HTML yang rapi dan dikirim balik untuk ditampilkan di browser

2. Menyimpan data di model membuat aplikasi lebih mudah dikelola. Kalau nanti mau tambah riwayat pendidikan baru, kita tinggal input datanya ke database dan otomatis langsung muncul di web karena pakai looping di template. Kalau ditulis langsung atau dihardcode di template, tiap mau nambah data harus buka dan edit kode HTMLnya lagi satu per satu, yang mana kodenya akan makin panjang dan rawan typo merusak struktur tagnya.

3. Fungsi `makemigrations` seperti membuat catatan instruksi perubahan berdasarkan kode yang ada di `models.py`. Sedangkan `migrate` fungsinya untuk menjalankan instruksi dari `makemigrations` tadi ke database sungguhan. Contohnya saat buat model class `Education` baru, harus menjalankan `makemigrations` dulu untuk mencatat persiapan pembuatan tabelnya, baru run `migrate` agar tabelnya benar benar dibuat di database.

### AI Disclosure
Tool yang Digunakan: Gemini

Saya menggunakan AI untuk membantu saya mengingatkan dan juga menjelaskan tahapan alur MVT di django agar tidak ada langkah yang terlewat dan membantu membuat html education

---

### Tugas 1

1. Ya, elemen tersebut membantu kodenya agar lebih mudah dibaca dengan CSS. Kalau semuanya pake `<div>`, akan jadi lebih bingung saat styling karena tagnya sama semua. Pakai tag `<article>` buat misahin card skills bisa buat struktur halamannya lebih jelas mana pembungkus utamanya dan mana isinya

2. Saat mengatur ukuran card saat dibuka di layar HP tidak berantakan. Di web dekstop, susunan grid 3 kolom sudah kelihatan rapi, tapi saat layarnya dikecilin, kontennya jadi sempit dan teksnya numpuk. Solusinya adalah mengubah tata letak kolomnya pakai @media query jadi 1 kolom penuh ke bawah (1fr). Jadi ukuran teks dan cardnya tetep proporsional dan prioritas utama biar tetap mudah dibaca bisa tercapai

3. Batasannya yaitu pengolahan datanya masih serba manual karena dihardcode langsung di HTML. Jadi kalau nanti mau tambah informasi baru seperti skills atau projek, harus buka dan edit kodenya lagi satu per satu, yang mana rawan typo atau merusak struktur tagnya

### AI Disclosure
Tool yang Digunakan: Gemini
Saya menggunakan AI untuk membantu saya menstruktur langkah-langkah untuk mengerjakan tugas ini dan memberi contoh struktur CSS grid yang rapi untuk 3 kolom dan efek hover