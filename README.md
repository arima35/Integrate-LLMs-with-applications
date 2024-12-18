# <h2 align="center"> **Integrasi LLMs ke Aplikasi** </h2>

#### **1. Tuning Model (Opsional)**
- Tuning adalah proses menyesuaikan model untuk meningkatkan kualitas output.
- Tapi, tidak semua proyek membutuhkan langkah ini. Model di watsonx.ai sudah siap digunakan (pre-deployed), jadi tuning hanya diperlukan kalau Anda memodifikasi model.

---

#### **2. Testing dan Integrasi**
Setelah model siap, testing dan integrasi dilakukan melalui:
- **REST API** atau 
- **Python SDK** (Software Development Kit).

**Cara Tes Prompt:**
1. Masuk ke **Prompt Lab** di watsonx.ai.
2. Gunakan prompt berikut untuk menguji model:

   **Contoh Prompt:**  
   _"Please provide top 5 bullet points in the review provided in '''."_  

   **Review Contoh:**  
   ```
   I started my loan process... (isi sesuai ulasan yang diberikan).
   ```

3. Hasil output dari model adalah daftar poin penting dari review tersebut.

**Parameter untuk Tes Prompt:**
- **Decoding Method:** Greedy.
- **Stop Sequence:** “.” (agar model berhenti setelah kalimat lengkap).
- **Token Range:** Minimum 50, maksimum 300.

---

#### **3. Menjalankan Kode**
Setelah prompt diuji:
1. Klik tombol **Generate** untuk menghasilkan hasil.
2. Klik ikon **View Code** untuk melihat kode Python/REST API.
3. Copy kode ini untuk digunakan dalam aplikasi Anda.

**Isi Kode REST API:**
- Kode akan berisi URL model, token autentikasi, prompt, dan parameter model.  
  _(Note: Token autentikasi dikelola melalui IBM Cloud, dan Anda bisa mendapatkannya di sana.)_

---

#### **4. Gunakan Python Notebook**
Di watsonx.ai:
1. Pilih opsi **Work with data and models in Python or R notebooks**.
2. Upload file notebook Python dari repository proyek Anda (misalnya, `TestLLM.ipynb`).
3. Jalankan notebook untuk mengetes LLM langsung dari lingkungan Python.

---

#### **5. Gunakan Python IDE**
Jika ingin langkah lebih lanjut, Anda bisa:
1. Buka file Python dari folder `applications` (misalnya, `demo_wml_api.py`).
2. Install dependensi:  
   ```
   python3 -m pip install -r requirements.txt
   ```
3. Jalankan script di IDE seperti VS Code atau PyCharm.

---

#### **6. Alternatif dengan Streamlit**
Untuk demo yang lebih interaktif, gunakan file `demo_wml_api_with_streamlit.py`. Ini akan memberikan antarmuka web untuk berinteraksi dengan LLM.

---
