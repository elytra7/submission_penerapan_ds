# Proyek Akhir: Deteksi Dini Dropout Mahasiswa Jaya Jaya Institut 🎓

## Business Understanding
Jaya Jaya Institut merupakan salah satu institusi pendidikan tinggi yang telah berdiri sejak tahun 2000 dan memiliki reputasi pencetak lulusan terbaik. Namun, belakangan ini institusi menghadapi permasalahan serius: **tingginya angka mahasiswa putus kuliah (*dropout*) yang mencapai 32,1%**.

Tingginya angka *dropout* ini berdampak negatif pada citra institusi dan kelancaran finansial kampus. Oleh karena itu, Jaya Jaya Institut membutuhkan sebuah sistem berbasis data yang dapat mendeteksi sedini mungkin mahasiswa yang berisiko melakukan *dropout* agar kampus dapat memberikan bimbingan khusus secara proaktif.

### Cakupan Proyek
Proyek *Data Science* ini dikerjakan secara *end-to-end* yang meliputi:
1. **Data Preparation & EDA:** Pembersihan data dan analisis faktor-faktor yang memiliki korelasi tertinggi terhadap potensi *dropout*.
2. **Machine Learning Modeling:** Membangun model prediksi klasifikasi menggunakan algoritma *Random Forest* dengan akurasi tinggi.
3. **Business Dashboard:** Pembuatan *dashboard* interaktif menggunakan Metabase untuk pemantauan performa mahasiswa oleh pihak manajemen.
4. **Cloud Deployment:** Pembuatan purwarupa (*prototype*) aplikasi web interaktif menggunakan Streamlit yang di-deploy ke Streamlit Community Cloud.

## Persiapan & Setup Environment

**Sumber Data:** https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/README.md

**Setup Environment - Anaconda:**
```text
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

**Setup Environment - Shell/Terminal (Pipenv):**
```text
pip install pipenv
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Business Dashboard
*Business Dashboard* telah dibuat menggunakan **Metabase** untuk memonitor metrik-metrik krusial mahasiswa. 

**Cara Mengakses Dashboard Lokal:**
1. Pastikan Docker sudah terinstal dan berjalan.
2. Salin file `metabase.db.mv.db` dari repositori ini ke direktori kerja Anda.
3. Jalankan perintah berikut di terminal:
   ```text
   docker run -d -p 3000:3000 --name metabase -u root -v $(pwd):/metabase.db -e "MB_DB_FILE=/metabase.db/metabase.db" metabase/metabase
   ```
4. Buka `http://localhost:3000` di browser.
5. Login menggunakan kredensial berikut:
   * **Email:** root@mail.com
   * **Password:** root123

## Sistem Prediksi Machine Learning (Prototype)
Model *Random Forest* yang telah dilatih diekspor dan diintegrasikan ke dalam antarmuka web interaktif menggunakan Streamlit. Aplikasi ini memungkinkan staf akademik untuk memasukkan profil 10 indikator utama mahasiswa dan mendapatkan skor probabilitas *dropout* secara instan.

 **Akses Streamlit:** https://yvuppits2y3qqijrtsdcvp.streamlit.app/

**Cara Menjalankan Prototype Secara Lokal:**
```text
streamlit run app.py
```

## Kesimpulan (Conclusion)
Proyek ini telah berhasil memetakan profil risiko mahasiswa dan menghasilkan model Machine Learning dengan performa **Akurasi 92.8%** dan tingkat **Recall (deteksi Dropout) 88%**.

**Insight Utama dari Data:**
Berdasarkan Analisis Data Eksploratif (EDA) dan ekstraksi kepentingan fitur (*feature importance*), ditemukan faktor pendorong utama keberhasilan dan kegagalan mahasiswa:
1. **Performa Akademik (Faktor Penyelamat Utama):** Mahasiswa yang memiliki tingkat kelulusan mata kuliah (*Curricular units approved*) dan rata-rata nilai (*Grade*) yang tinggi di Semester 1 dan 2 sangat kecil kemungkinannya untuk *dropout*.
2. **Kesehatan Finansial (Faktor Risiko):** Tunggakan biaya (*Debtor*) dan keterlambatan pembayaran UKT (*Tuition fees not up to date*) adalah prediktor kuat mahasiswa putus kuliah. Sebaliknya, penerima beasiswa (*Scholarship holder*) memiliki tingkat retensi kelulusan yang sangat tinggi.
3. **Faktor Demografi:** Terdapat korelasi positif antara *Age at enrollment* (usia saat mendaftar) dengan risiko *dropout*, di mana mahasiswa yang mendaftar di usia yang lebih tua memiliki probabilitas *dropout* yang lebih tinggi dibandingkan yang mendaftar di usia muda.

## Rekomendasi Action Items
Berdasarkan temuan data, berikut adalah rekomendasi strategis bagi Jaya Jaya Institut:

1. **Intervensi Finansial Proaktif:** Manajemen harus segera menghubungi mahasiswa yang terdeteksi sebagai *Debtor* atau terlambat membayar UKT. Berikan opsi restrukturisasi pembayaran, cicilan, atau bantuan finansial/beasiswa sebelum mereka memutuskan untuk berhenti.
2. **Sistem Peringatan Akademik Dini:** Gunakan nilai rata-rata (*Grade*) dan kelulusan SKS (*Units Approved*) di Semester 1 sebagai indikator wajib. Jika nilai Semester 1 seorang mahasiswa berada di bawah batas aman, wajibkan mereka mengikuti kelas bimbingan/tutorial tambahan sebelum masuk ke Semester 2.
3. **Pendampingan Khusus Mahasiswa Dewasa:** Karena *Age at enrollment* berkorelasi dengan tingginya *dropout*, sediakan program konseling khusus bagi mahasiswa yang mendaftar di usia lebih tua, karena mereka mungkin menghadapi beban ganda (bekerja/berkeluarga) yang mengganggu studi.
4. **Integrasi Sistem:** Mewajibkan dosen wali atau staf akademik untuk menggunakan *Early Warning System* (Aplikasi Streamlit) pada saat masa evaluasi semester untuk merumuskan daftar *watchlist* mahasiswa berisiko tinggi.