# Analisis Sentimen BSI 
## Outline 
Merupakan project magang Ludy Hasby di BSI untuk periode 10 Juni - 23 Agustus 2024. Project ini meliputi 2 analisis utama. Diantaranya, 
- Analisis Sentimen dengan Algoritma Artificial Neural Network (dengan LSTM Bidirectional, sebagai hidden layer utama)
- Analisis LDA (Latent Dirichlet Allocation)
- Explorasi Permasalahan Umum LDA 2
## Summary Excecutive
- Pemodelan Sentimen dengan menggunakan Algoritma Artificial Neural Network dengan Bidirectional Long Short Term Memory (LSTM) sebagai hidden layer utama menghasilkan prediksi sentimen yang relatif baik, dimana akurasi yang didapat untuk data latih, data uji, dan data validasi sebesar 99.8%, 92.35%, dan 100%. 
- Sentimen pelanggan atas BSI Mobile pada 1 Februari 2021 - 18 Juli 2024 didominasi oleh sentimen positif, Play Store (65.8% | ulasan = 106350) dan Apps Store (74.8% | ulasan = 3120)
- Berdasar LDA, topik yang sering dibicarakan oleh pengulas diantaranya fitur lengkap dan kemudahan transaksi (20.8%), Kenyamanan BSI Mobile (19.6%), BSI Mobile Susah digunakan dan sering error (19.5%),  BSI lancar digunakan (14%), dan permasalahan pada BSI Mobile (Kode Aktivasi dan Rekening) (12.5%). 
- Permasalahan yang umum dihadapi di BSI Mobile diantaranya,
    1. Tidak Bisa Login, 
    2. Susah digunakan, 
    3. Gangguan Transfer,
    4. Gangguan Transaksi,
    5. Gangguan Update,
    6. Gangguan Deteksi Wajah,
    7. Kehabisan Waktu,
    8. Lambat Saat Digunakan, dan 
    9. Force Close
## Hyperlink penting 
- sentimen_5.h5 adalah model NN dengan format tensorflow 
- Notebook pemodelan LDA 1 yang menghasilkan 7 topik yang umum dibahas oleh pengulas di BSI Mobile dapat diakses di https://colab.research.google.com/drive/1H668jkm8jFWQqkwW1uz8p24E7waLdvLY?usp=sharing
- Notebook pemodelan LDA 2 yang menghasilkan permasalahan umum yang dihadapi oleh BSI Mobile dapat diakses di https://colab.research.google.com/drive/14-m2ST7iNaHeoYuYXJB1ggn-8FYf-QlZ?usp=sharing
- Analisis Sentimen Ulasan BSI Mobile dengan Algoritma Artificial Neural Network.pdf adalah laporan proyek analisis sentimen. 