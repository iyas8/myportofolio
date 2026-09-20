# Portfolio Website

## Deskripsi Proyek
Proyek ini adalah sebuah website portofolio pribadi interaktif yang dibangun menggunakan framework web Django. Website ini dirancang untuk menampilkan profil, pengalaman, serta riwayat pendidikan secara dinamis menggunakan arsitektur Model-View-Template (MVT).

## Cara Menjalankan Proyek (Setup)
1. Pastikan Python sudah terinstal di komputer.
2. Buka terminal dan aktifkan *virtual environment* (misal di Windows: `env\Scripts\activate`).
3. Instal semua dependensi dengan menjalankan: `pip install -r requirements.txt`.
4. Terapkan migrasi database dengan perintah: `python manage.py migrate`.
5. Jalankan server lokal dengan mengetik: `python manage.py runserver`.
6. Buka `http://localhost:8000/` di browser.

---

### Tugas 3

1. `ModelForm` memungkinkan efisiensi kode dengan menggenerasi elemen form HTML secara otomatis berdasarkan struktur tipe data pada model Django, lengkap dengan validasi bawaan. Penggunaan `{% csrf_token %}` diwajibkan untuk keamanan guna mencegah *Cross-Site Request Forgery*, yakni eksploitasi di mana pihak ketiga memalsukan aksi *POST* seolah-olah berasal dari pengguna terautentikasi.

2. JSON lebih dominan pada pengembangan web modern karena strukturnya yang ringan, mudah dibaca, dan tidak menggunakan tag pembuka/penutup yang kompleks seperti XML. JSON juga merupakan bagian integral dari JavaScript, sehingga data dapat langsung diparsing dan dimanipulasi pada antarmuka frontend tanpa overhead tambahan

3. Saat user melakukan request ke URL API, fungsi view mengambil data dari database berupa himpunan QuerySet (objek Python). Data mentah ini belum dapat ditransmisikan melalui protokol HTTP, sehingga memerlukan serialization untuk menerjemahkannya menjadi representasi string berformat JSON yang dapat dipahami oleh browser.

### AI Disclosure
Tool yang Digunakan: Gemini

Konteks Penggunaan: Saya menggunakan AI untuk membantu menrapikan tata letak elemen antarmuka (CSS) serta menyusun kerangka penjelasan konsep *serialization* dan *ModelForm* 