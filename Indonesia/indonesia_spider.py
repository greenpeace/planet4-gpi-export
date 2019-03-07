#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import scrapy
import logging
import locale
import dateutil.parser
import re
import dateparser
from datetime import datetime, date
import random
import time
import csv
import urllib2

locale.setlocale(locale.LC_ALL, '')

class AllSpider(scrapy.Spider):
    name = 'all'

    custom_settings = {
        'ROBOTSTXT_OBEY': 0,
        'FEED_URI': 'gpind_staging_v2_B3.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v2_final.csv"
    __connector_csv_log_file = "connector_csv_log_v2"

    def start_requests(self):
        # v1
        start_urls = {
            'https://www.greenpeace.org/seasia/id/press/releases/Putusan-Komisi-Informasi-Pusat-Sepakat-Mediasi-KLHK-Membuka-Pintu-untuk-Greenpeace-Telusuri-Informasi-Jual-Beli-Lahan-Sawit-Ilegal/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'https://www.greenpeace.org/seasia/id/press/releases/Bersihkan-Politik-Indonesia-dari-Batu-Bara/':('Siaran Pers','Ciptakan Perubahan','','Iklim','','','article','Migrate'),
            'https://www.greenpeace.org/seasia/id/press/releases/Pemberian-Izin-Lokasi-Reklamasi-di-Teluk-Benoa-Kebijakan-Memunggungi-Laut-dan-Tidak-Peka-Sosial-Lingkungan/':('Siaran Pers','Lindungi','','Laut','','','article','Migrate'),
            'https://www.greenpeace.org/seasia/id/press/releases/Gerakan-Bersihkan-Indonesia-ajak-Pemilih-Milenial-untuk-Menyeberang-ke-Masa-Depan-Energi-yang-Bersih-dan-Berkelanjutan/':('Siaran Pers','Ciptakan Perubahan','','Iklim','EnergiTerbarukan','','article','Migrate'),
            'https://www.greenpeace.org/seasia/id/press/releases/Pengaruh-Elite-Politik-Dalam-Pusaran-Bisnis-Batubara/':('Siaran Pers','Ciptakan Perubahan','','Iklim','','','article','Migrate'),
            'https://www.greenpeace.org/seasia/id/blog/kapal-kapal-greenpeace-akan-berlayar-demi-men/blog/62120/':('Cerita','Ciptakan Perubahan','','Laut','','','news-list','Migrate'),
            'https://www.greenpeace.org/seasia/id/blog/kita-mempunyai-kekuatan-untuk-mendorong-indus/blog/62046/':('Cerita','Ciptakan Perubahan','','Laut','','','news-list','Migrate'),
            'https://www.greenpeace.org/seasia/id/blog/saya-tidak-bisa-untuk-tidak-menangis-ketika-b/blog/62018/':('Cerita','Ciptakan Perubahan','','Hutan','','','news-list','Migrate'),
            'https://www.greenpeace.org/seasia/id/blog/apa-yang-dilakukan-oreo-mondelez-wilmar-terha/blog/62015/':('Cerita','Ciptakan Perubahan','','Hutan','','','news-list','Migrate'),
            'https://www.greenpeace.org/seasia/id/blog/minyak-sawit-apa-yang-perlu-kita-ketahui/blog/61993/':('Cerita','Ciptakan Perubahan','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Menimbang-Urgensi-Transisi-Menuju-Listrik-Energi-Baru-Terbarukan/':('Publikasi','Ciptakan Perubahan','','EnergiTerbarukan','Iklim','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Elite-Politik-Dalam-Pusaran-Bisnis-Batu-bara/':('Publikasi','Ciptakan Perubahan','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Sebuah-Krisis-Kenyamanan/':('Publikasi','Ciptakan Perubahan','','Plastik','','','article','Migrate'),
            'https://www.greenpeace.org/seasia/id/press/reports/Briefer---Matahari-untuk-Bali/':('Publikasi','Ciptakan Perubahan','','Iklim','Udara','','article','Migrate'),
            'https://www.greenpeace.org/seasia/id/press/reports/Laporan-Kerusakan-Terumbu-Karang-Karimunjawa/':('Publikasi','Lindungi','','Iklim','Laut','','article','Migrate')
        }

        start_urls = {
            # B1
            'http://www.greenpeace.org/seasia/id/press/releases/Balada-HGU-Dalam-Pilpres-2019--Informasi-HGU-Jangan-Sekedar-Jadi-Dagangan-Politik-/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Laporan-Terbaru-Menemukan-Seluruh-Siklus-Plastik-Mengancam-Kesehatan-Manusia/':('Siaran Pers','Ciptakan Perubahan','','Plastik','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Debat-Pilpres-Melupakan-Perubahan-Iklim-Permasalahan-Lingkungan-Terbesar-yang-Mengancam-Bumi-dan-Manusia/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Ganti-Rugi-189-Triliun-Terkait-Kasus-Kebakaran-dan-Kerusakan-Hutan-Gagal-Dibayar-Sejumlah-Perusahaan-Pemerintah-Harus-Mengambil-Langkah-Tegas/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Menimbang-Urgensi-Transisi-Menuju-Listrik-Energi-Baru-Terbarukan/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Bersihkan-Politik-Indonesia-dari-Batu-Bara/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Putusan-Komisi-Informasi-Pusat-Sepakat-Mediasi-KLHK-Membuka-Pintu-untuk-Greenpeace-Telusuri-Informasi-Jual-Beli-Lahan-Sawit-Ilegal/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Pemberian-Izin-Lokasi-Reklamasi-di-Teluk-Benoa-Kebijakan-Memunggungi-Laut-dan-Tidak-Peka-Sosial-Lingkungan/':('Siaran Pers','Lindungi','','Laut','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Gerakan-Bersihkan-Indonesia-ajak-Pemilih-Milenial-untuk-Menyeberang-ke-Masa-Depan-Energi-yang-Bersih-dan-Berkelanjutan/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Pengaruh-Elite-Politik-Dalam-Pusaran-Bisnis-Batubara/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Terobosan-baru-Wilmar-agar-para-perusak-hutan-tidak-dapat-bersembunyi/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Peringkat-Pengalengan-Tuna-Greenpeace-Terbaru-Hanya-Lima-Dari-23-Perusahaan-Pengalengan-di-Asia-Tenggara-yang-Naik-Kelas/':('Siaran Pers','Lindungi','','Laut','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Tidak-ada-alasan---iklim-kita-sedang-terbakar-dan-saatnya-bertindak/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Pengiriman-minyak-sawit-menuju-Eropa-tertunda-oleh-Greenpeace-selama-lebih-dari-24-jam/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Enam-aktivis-Greenpeace-ditangkap-saat-beraksi-menduduki-kapal-bermuatan-minyak-sawit-kotor-Wilmar-menuju-Eropa/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Perusahaan-biskuit-Oreo-masih-menggunakan-minyak-sawit-yang-berasal-dari-perusakan-habitat-orangutan-di-Indonesia/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Seni-jalanan-karya-20-seniman-di-berbagai-kota-besar-dunia-sebagai-pesan-untuk-mengakhiri-deforestasi-akibat-kelapa-sawit/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Coca-Cola-Nestle-Danone-Mars-Pepsi-dan-Unilever-menandatangani-komitmen-plastik-global-tetapi-masih-belum-memprioritaskan-pengurangan/':('Siaran Pers','Ciptakan Perubahan','','Plastik','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Survei-global-mengungkap-kontribusi-perusahaan-FMCG-terhadap-krisis-polusi-plastik-di-masa-depan/':('Siaran Pers','Ciptakan Perubahan','','Plastik','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Lebih-dari-90-merek-garam-yang-disampel-secara-global-ditemukan-mengandung-mikroplastik/':('Siaran Pers','Ciptakan Perubahan','','Plastik','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Greenpeace-dan-CoalSwarm-menunjukkan-penghapusan-batubara-global-untuk-penurunan-15--C-adalah-sesuatu-yang-realistis-dan-dapat-dicapai/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Kegiatan-bersih-bersih-dan-audit-merek-global-menemukan-Coca-Cola-PepsiCo-dan-Nestle-sebagai-pencemar-plastik-terburuk-di-seluruh-dunia/':('Siaran Pers','Ciptakan Perubahan','','Plastik','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Greenpeace-Indonesia-Konferensi-ICBE-harus-memastikan-komitmen-pembangunan-yang-sejalan-dengan-semangat-konservasi-hutan-tropis-di-Tanah-Papua/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/-Greenpeace-Rencana-Aksi-terbaru-Wilmar-tidak-akan-memperbaiki-masalah-deforestasi---/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Greenpeace-Menemukan-Lebih-Dari-700-Merek-Sampah-Plastik-Dari-Tiga-Lokasi--/':('Siaran Pers','Ciptakan Perubahan','','Plastik','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Aktivis-Greenpeace-dan-personel-grup-band-musik-Boomerang-memblokade-kapal-minyak-sawit-dari-hasil-perusakan-hutan/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/-Greenpeace-Ini-waktunya-mengeluarkan-larangan-deforestasi-kelapa-sawit-bukan-hanya-moratorium/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Investigasi-Greenpeace-memaparkan-bagaimana-perusahaan-merek-merek-terbesar-dunia-masih-terkait-dengan-perusakan-hutan-di-Indonesia/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Kebakaran-Lahan-Terjadi-di-Areal-Pemasok-Sawit-untuk-Perusahaan-Merek-Ternama-Dunia/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Koalisi-Masyarakat-Sipil-Upaya-kasasi-akan-merugikan-masyarakat-pemerintah-diminta-menjalankan-putusan-pengadilan-demi-korban-asap-kebakaran-hutan/':('Siaran Pers','Lindungi','','Hutan','Udara','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Polusi-Jakarta-Masih-Terus-Diabaikan-Ini-Saran-Greenpeace/':('Siaran Pers','Lindungi','','Udara','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Setahun-Lebih-Pemerintah-Mengabaikan-Putusan-Mahkamah-Agung-Koalisi-Masyarakat-Sipil-Menganugerahkan-Trofi-Kepada-ATRBPN-Sebagai-Lembaga-Yang-Tidak-Transparan/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Hari-Orangutan-Sedunia-Klaim-Pemerintah-Soal-Peningkatan-Jumlah-Orangutan-Dibantah-Ilmuwan/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Jelang-HUT-RI-ke-73-Majelis-Hakim-PTUN-Denpasar-Hadiahkan-Asap-Hitam-PLTU-Batubara-bagi-Warga-Celukan-Bawang-dan-Masyarakat-Bali/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Hutan-Seluas-Dua-Kali-Lipat-Ukuran-Kota-Paris-Dihancurkan-Perusahaan-Kelapa-Sawit-Terbesar-Dunia-/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Indonesia-Butuh-Instalasi-Energi-Bersih-Lebih-Banyak-dan-Lebih-Besar-Lagi/':('Siaran Pers','Ciptakan Perubahan','','EnergiTerbarukan','Iklim','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Cerita-dari-Ruang-Bersih-Mengungkap-Kisah-Kotor-Industri-Elektronik-/':('Siaran Pers','Ciptakan Perubahan','','ElektronikHijau','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Minim-Sosialisasi-Proses-Perizinan-PLTU-Celukan-Bawang-Hanya-Libatkan-23-Warga/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Lebih-Dari-1000-Orangutan-Kembali-Terancam-Oleh-Pengrusakan-Hutan/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Memperingati-Hari-Citarum-Tahun-ke-Tiga--Masa-Depan-Bersih-Hak-Kita-Semua---/':('Siaran Pers','Ciptakan Perubahan','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Greenpeace-Putuskan-Hubungan-Setelah-APPSinar-Mas-Terkait-Kembali-Praktik-Deforestasi/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Rainbow-Warrior-Mendukung-Perjuangan-Warga-Pulau-Pari/':('Siaran Pers','Lindungi','','Kapal','Aktivisme','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Greenpeace-Mengungkap-Harga-Batubara-Sebenarnya-di-Konferensi-Industri-Batubara-di-Bali/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/-Jelang-Pertemuan-Pemimpin-Industri-Batubara-Dunia-di-Bali-Greenpeace-Menghalau-Keluar-Tongkang-Batubara-dari-Taman-Nasional/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Kapal-Rainbow-Warrior-Tiba-di-Jakarta-Mendukung-Energi-Bersih-untuk-Udara-Bersih-Bagi-Warga-Ibukota/':('Siaran Pers','Ciptakan Perubahan','','Kapal','Aktivisme','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Jelang-peringatan-Hari-Bumi-lebih-dari-1-juta-orang-menuntut-korporasi-mengurangi-plastik-sekali-pakai/':('Siaran Pers','Ciptakan Perubahan','','Plastik','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Dukung-Perjuangan-Masyarakat-Rainbow-Warrior-Singgah-di-Celukan-Bawang/':('Siaran Pers','Ciptakan Perubahan','','Kapal','Aktivisme','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Salah-satu-pantai-favorit-di-Bali-dan-Taman-Nasional-Bali-Barat-Berada-dalam-Ancaman-PLTU-Batubara---/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Rainbow-Warrior-di-Benoa-Soroti-Persoalan-Lingkungan-Bali/':('Siaran Pers','Ciptakan Perubahan','','Aktivisme','Kapal','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/RUPTL-2018-2027-Telah-Disahkan-PLTU-Celukan-Bawang-2x330-MW-Tetap-Menjadi-Proyek-Siluman/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Upaya-Pemerintah-Menurunkan-Ketimpangan-Penguasaan-Hutan-Belum-Sepenuhnya-Memihak-Masyarakat/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Perusahaan-Ritel-Inggris-Menghentikan-Penggunaan-Bahan-Baku-Minyak-Sawit-Pada-Produknya-Akibat-Sistem-Bisnis-Kelapa-Sawit-Masih-Merusak-Hutan/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Mengurangi-Konsumsi-Kemasan-Plastik-Sekali-Pakai-Adalah-Kunci/':('Siaran Pers','Ciptakan Perubahan','','Plastik','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Laporan-baru-Selama-dua-tahun-berturut-turut-tren-pembangunan-pembangkit-listrik-batubara-anjlok-di-seluruh-dunia/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Sejumlah-Merek-Global-Masih-Enggan-Transparan-Soal-Rantai-Pasok-Sawit/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Debu-Kotor-Batubara-Masih-Menyelimuti-RUPTL-2018-2027/':('Siaran Pers','Lindungi','','Iklim','Udara','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Kapal-Greenpeace-Rainbow-Warrior-Berlayar-Ke-Papua-Mendukung-Hutan-Adat---/':('Siaran Pers','Lindungi','','Hutan','Kapal','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Pengiriman-Kayu-Ilegal-Papua-Terbongkar-Namun-Masih-Banyak-Yang-Belum-Terungkap/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Kedatangan-Rainbow-Warrior-Merajut-Asa-Untuk-Memulihkan-Alam-Indonesia/':('Siaran Pers','Lindungi','','Aktivisme','Kapal','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Asian-Games-Jangan-Sampai-Kalah-Dengan-Kabut-Asap/':('Siaran Pers','Lindungi','','Udara','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Tanggapan-Revisi-Permen-21-2008/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Tanggapan-Greenpeace-Indonesia-terhadap-Draft-Revisi-PermenLH-212008/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Koalisi-internasional-meminta-bank-bank-Singapura-untuk-mengakhiri-pendanaan-batubara/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Masyarakat-Ajukan-Gugatan-Tolak-Pengembangan-PLTU-Batu-Bara-Celukan-Bawang-di-Buleleng-Bali1/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/-Inpres-Moratorium-Izin-Perkebunan-Sawit-Harus-Memuat-Dua-Hal-Ini/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),

            # B2
            'http://www.greenpeace.org/seasia/id/press/releases/Peruntukan-Pengelolaan-Dana-Sawit-Untuk-Subsidi-Biofuel-Tidak-Tepat/':('Siaran Pers','Lindungi','','Hutan','Iklim','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Masyarakat-Ajukan-Gugatan-Tolak-Pengembangan-PLTU-Batu-Bara-Celukan-Bawang-di-Buleleng-Bali/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Sengatan-Kerugian-Proyek-PLTU-PLTU-Batubara-yang-Merugikan-Uang-Rakyat/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Upaya-Pengaktifan-Izin-Tambang-PT-MMP-Bukti-Pemerintah-Kangkangi-Hukum/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Memulihkan-Citarum-Mulai-Dari-Limbah-Industri/':('Siaran Pers','Ciptakan Perubahan','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/-Greenpeace-Desak-Perlindungan-Tuna-yang-Lebih-Kuat-di-WCPFC/':('Siaran Pers','Lindungi','','Laut','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Laporan-Greenpeace-International-Hutan-Indonesia-Masih-Dalam-Ancaman-Industri-Kelapa-Sawit/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Tanggapan-Greenpeace--Presiden-Jokowi-Seharusnya-Menyadari-Deforestasi-Masih-Terjadi-di-Bisnis-Sawit/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Belum-Tampak-Kemajuan-Nyata-Indonesia-Sejak-Kesepakatan-Paris/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Tanggapan-Greenpeace-Indonesia-Mengenai-Rencana-PLN-dan-Kementerian-ESDM-Untuk-Menyeragamkan-Daya-Listrik-Rumah-Tangga/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Keberlangsungan-Hidup-Spesies-Baru-Orangutan-Terancam/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Pengadangan-Tim-Utusan-Presiden-di-Pulau-Bangka-Negara-Jangan-Takluk-Menghadapi-Korporasi-Tambang/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Mengatasi-Polusi-Udara-dengan-Pembatasan-Kendaraan-Bermotor-Tidaklah-Cukup/':('Siaran Pers','Lindungi','','Udara','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/RAPP-Harus-Taat-Aturan-Agar-Bencana-Asap-Tak-Terulang-Kembali/':('Siaran Pers','Lindungi','','Hutan','Udara','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Jakarta-Dikepung-Emisi-Batubara/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/23-negara-dan-negara-bagian-akan--meninggalkan--industri-batubara-dengan--kapital-senilai-432-juta-USD/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Koalisi-Break-Free-From-Coal-Desak-Presiden-Jokowi--Menghapus-PLTU-Batubara-dari-Revisi-Proyek-Setrum-35000-Megawatt/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Hasil-Audit-Sampah-Plastik/':('Siaran Pers','Ciptakan Perubahan','','Plastik','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Pemerintah-dan-Parlemen-Saatnya-Perkuat-Standar-Polusi-Udara-Kita/':('Siaran Pers','Lindungi','','Udara','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Polusi-Udara-Ancam-Kesehatan-Masyarakat/':('Siaran Pers','Lindungi','','Udara','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Krisis-Keuangan-PLN-Pembangunan-PLTU-Batubara-Baru-di-Jawa-Bali-Adalah-Kerugian-Ekonomi-yang-Nyata---/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Keterbukaan-Informasi-Publik-Masih-Sekadar-Wacana/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/-Tidak-Ada-Konsistensi-Dalam-Melindungi-Gambut/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Pemerintah-Belum-Cukup-Melindungi-Hutan-dan-Gambut/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Penanam-kelapa-sawit-terbesar-di-dunia-dipaksauntuk-memperbaiki-lebih-dari-1000-hektar-hutan-hujan/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Pemerintah-Tidak-Serius-Melindungi-Orangutan/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Masyarakat-Pesisir-Labuan-Menuntut-Pemulihan-Ekosistem-Laut-yang-Rusak/':('Siaran Pers','Lindungi','','Laut','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Kualitas-Udara-Jabodetabek-Jauh-Melebihi-Standar-WHO-Selama-Semester-Pertama/':('Siaran Pers','Lindungi','','Udara','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Greenpeace-Kebakaran-dan-Kabut-Asap-Meningkat-Ujian-bagi-Komitmen-Presiden-untuk-Perlindungan-Hutan-dan-Gambut/':('Siaran Pers','Lindungi','','Hutan','Udara','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Greenpeace-Mendorong-Bisnis-daripada-Perlindungan-Hutan-adalah-Pilihan-Buruk-bagi-Indonesia/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Thai-Union-Berjanji-Seafood-yang-Lebih-Berkelanjutan-Bertanggung-Jawab-Secara-Sosial--Kampanye-Greenpeace-berhasil-menghasilkan-perubahan-positif-pada-industri-seafood/':('Siaran Pers','Lindungi','','Laut','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Surat-Greenpeace-untuk-Presiden-Joko-Widodo/':('Siaran Pers','Ciptakan Perubahan','','Aktivisme','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Greenpeace-Indonesia-Sesalkan-Langkah-Mundur-Trump/':('Siaran Pers','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/19-Tahun-Reformasi-Keterbukaan-Informasi-Belum-Terwujud/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/releases/Enam-Tahun-Moratorium-Berapa-Luas-Hutan-Terlindungi/':('Siaran Pers','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Elite-Politik-Dalam-Pusaran-Bisnis-Batu-bara/':('Publikasi','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Sebuah-Krisis-Kenyamanan/':('Publikasi','Ciptakan Perubahan','','Plastik','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Briefer---Matahari-untuk-Bali/':('Publikasi','Ciptakan Perubahan','','EnergiTerbarukan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Laporan-Kerusakan-Terumbu-Karang-Karimunjawa/':('Publikasi','Lindungi','','Iklim','Laut','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/PLTU-Celukan-Bawang-Meracuni-Pulau-Dewata/':('Publikasi','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Merekam-Perkembangan-Pembangkit-Tenaga-Batu-bara-di-Dunia/':('Publikasi','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/saatnya-kebenaran-disuarakan/':('Publikasi','Lindungi','','Hutan','Iklim','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/dampak-pembangkit-batubara-sekitar-jakarta/':('Publikasi','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Briefing-Paper---Kualitas-Udara-yang-Buruk-di-Jabodetabek/':('Publikasi','Lindungi','','Udara','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Fakta-mematikan-pasokan-kelapa-sawit-IOI/':('Publikasi','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Internalisasi-Dampak-dan-Biaya-Kesehatan-dari-PLTU-Batubara-di-Indonesia/':('Publikasi','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Perusakan-IOI-Masalah-Mendesak/':('Publikasi','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/valuasi-kerugian-ekonomi-akibat-pencemaran-limbah-industri/':('Publikasi','Ciptakan Perubahan','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/desa-terkepung-tambang-batubara/':('Publikasi','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Peringkat-Pengalengan-Tuna/':('Publikasi','Lindungi','','Laut','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Hasil-Penelitian-Harvard-Ancaman-Maut-PLTU-Batubara-Indonesia/':('Publikasi','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Nol-Deforestasi-dalam-Praktik-Pendekatan-Stok-Karbon-Tinggi/':('Publikasi','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Visi-Misi-Prabowo-Hatta-dan-Jokowi-Kalla-Belum-Maksimal-Dalam-Melindungi-Lingkungan/':('Publikasi','Ciptakan Perubahan','','Aktivisme','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Sumatera-Akan-Tertutup-Dengan-Asap/':('Publikasi','Lindungi','','Hutan','Udara','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Kartu-Merah-untuk-merk-merk-perlengkapan-olahraga/':('Publikasi','Ciptakan Perubahan','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Bagaimana-pertambangan-batubara-melukai-perekonomian-Indonesia/':('Publikasi','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Laporan-Sebuah-Dongeng-Mengenai-Monster-di-Lemari-Pakaianmu/':('Publikasi','Ciptakan Perubahan','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/APP-progress-review/':('Publikasi','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Izin-Untuk-Memusnahkan/':('Publikasi','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/MENUJU-NOL--Bagaimana-Greenpeace-Menghentikan-Deforestasi-di-Indonesia-20032013-dan-selanjutnya/':('Publikasi','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Bank-Dunia-Mempercepat-Pengembangan-Batubara-di-Indonesia/':('Publikasi','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Energy-Revolution-a-sustainable-ASEAN-energy-outlook/':('Publikasi','Lindungi','','Iklim','EnergiTerbarukan','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Laut-Indonesia-Dalam-Krisis/':('Publikasi','Lindungi','','Laut','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Joint-Vision-for-Oceans-of-Indonesia-in-2025/':('Publikasi','Lindungi','','Laut','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Visi-Bersama-Kelautan-Indonesia-2025/':('Publikasi','Lindungi','','Laut','','','article','Migrate'),

            # B3
            'http://www.greenpeace.org/seasia/id/press/reports/Down-to-Zero/':('Publikasi','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Toxic-Threads-Meracuni-Surga/':('Publikasi','Ciptakan Perubahan','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/ringkasan-eksekutif-Loi-indonesia-norwegia-kajian-Greenpeace/':('Publikasi','Lindungi','','Hutan','Iklim','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Bahan-Beracun-Lepas-Kendali/':('Publikasi','Ciptakan Perubahan','','Detox','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Indonesia-Norway-Agreement-to-reduce-greenhouse-gas/':('Publikasi','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Laporan-Keterkaitan-Perusahaan-Sawit-India-Dalam-Kerusakan-Hutan-Indonesia/':('Publikasi','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/campaigns/melindungi-hutan-alam-terakhir/nogood/KFC-Report/':('Publikasi','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Pelajaran-dari-Fukushima/':('Publikasi','Ciptakan Perubahan','','EnergiTerbarukan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Sesat-Pikir-Kebohongan-Para-Promotor-PLTN/':('Publikasi','Ciptakan Perubahan','','EnergiTerbarukan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Uang-Perlindungan/':('Publikasi','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Mengantar-Indonesia-Menuju-Jalur-Pembangunan-Baru/':('Publikasi','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/surat-terbuka-greenpeace-pada-kementerian-luarnegeri/':('Publikasi','Ciptakan Perubahan','','Aktivisme','Kapal','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/Batubara-Mematikan/':('Publikasi','Lindungi','','Iklim','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/platform-bersama-penyelamatan-hutan/':('Publikasi','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/SM_APP/':('Publikasi','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/tertangkap-basah-eskploitasi-minyak-kelapa-sawit-nestle/':('Publikasi','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/kegiatan-ilegal-perusakan-huta/':('Publikasi','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/press/reports/hutan-tropis-indonesia-krisi-iklim/':('Publikasi','Lindungi','','Hutan','','','article','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/kapal-kapal-greenpeace-akan-berlayar-demi-men/blog/62120/':('Cerita','Ciptakan Perubahan','','Aktivisme','Kapal','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/kita-mempunyai-kekuatan-untuk-mendorong-indus/blog/62046/':('Cerita','Lindungi','','Laut','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/saya-tidak-bisa-untuk-tidak-menangis-ketika-b/blog/62018/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/apa-yang-dilakukan-oreo-mondelez-wilmar-terha/blog/62015/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/minyak-sawit-apa-yang-perlu-kita-ketahui/blog/61993/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/ayo-bangun-dan-bergerak-kita-sedang-diserang-/blog/61990/':('Cerita','Ciptakan Perubahan','','Plastik','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/kenangan-masa-lalu-dan-masa-depan-hutan-indon/blog/61904/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/teruntuk-produk-dan-produsen-penghancur-hutan/blog/61890/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/wings-of-paradise-menarik-perhatian-pada-perm/blog/61883/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/bagaimana-sampah-plastik-mengejutkan-saya/blog/61869/':('Cerita','Ciptakan Perubahan','','Plastik','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/kemenangan-lingkungan-terjadi-berkat-anda/blog/61825/':('Cerita','Ciptakan Perubahan','','Aktivisme','TentangKami','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/10-fakta-tentang-orangutan/blog/61798/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/menelusuri-keindahan-hutan-sungai-putri-yang-/blog/61703/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/apakah-kamu-pernah-melihat-mangrove-berwarna-/blog/61412/':('Cerita','Lindungi','','Laut','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/harmoni-hutan-dengan-masyarakat-di-tanah-papu/blog/61368/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/pak-lurah-ada-api-besar-di-laut/blog/61356/':('Cerita','Lindungi','','Iklim','Laut','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/rainbow-warrior-dan-pesan-untuk-masa-depan-ya/blog/61293/':('Cerita','Ciptakan Perubahan','','Aktivisme','Kapal','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/alasan-kenapa-kita-harus-make-smthng-dan-buka/blog/60732/':('Cerita','Ciptakan Perubahan','','Plastik','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/5-hewan-lucu-ini-terancam-perubahan-iklim/blog/60692/':('Cerita','Lindungi','','Iklim','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/para-pemimpin-iklim-waktunya-telah-tiba/blog/60666/':('Cerita','Lindungi','','Iklim','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/sebera-hijaukah-gadgetmu/blog/60507/':('Cerita','Ciptakan Perubahan','','ElektronikHijau','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/jakarta-bebas-sampah-plastik-dambaan-kita/blog/60439/':('Cerita','Ciptakan Perubahan','','Plastik','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/mencegah-dan-memadamkan-demi-hutan-tanpa-api/blog/60233/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/ketika-pltu-dan-perubahan-iklim-membuat-asinn/blog/60019/':('Cerita','Lindungi','','Iklim','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/batubara-dan-hilangnya-sokongan-finansial-glo/blog/59914/':('Cerita','Lindungi','','Iklim','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/hari-bersejarah-di-pbb-senjata-nuklir-sekaran/blog/59833/':('Cerita','Ciptakan Perubahan','','EnergiTerbarukan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/ourvoicesarevital/blog/59678/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/berbelanja-tidak-membuat-kita-bahagia/blog/59400/':('Cerita','Lindungi','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/menjaring-rezeki-memperjuangkan-hidup-di-laut/blog/59347/':('Cerita','Ciptakan Perubahan','','ElektronikHijau','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/apa-arti-10-tahun-penggunaan-ponsel-pintar-ba/blog/58914/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/hsbc-berjanji-untuk-putuskan-hubungan-dengan-/blog/58791/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/perihal-hsbc-dan-hutan-indonesia/blog/58698/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/sayonara-pak-iwan-kami-akan-lanjutkan-perjuan/blog/58685/':('Cerita','Ciptakan Perubahan','','Aktivisme','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/setiap-plastik-yang-pernah-dibuat-itu-masih-a/blog/58552/':('Cerita','Ciptakan Perubahan','','Plastik','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/terungkap-hsbc-ada-di-balik-krisis-deforestas/blog/58524/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/klhk-ajukan-banding-upaya-perlindungan-hutan-/blog/58500/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/delapan-momen-spesial-tahun-2016/blog/58494/':('Cerita','Ciptakan Perubahan','','Aktivisme','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/black-friday-ambil-nafas-dan-rehat-dulu-bumi-/blog/58123/':('Cerita','Ciptakan Perubahan','','Detox','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/dulu-takut-asap-kini-saya-cari-sumbernya/blog/58099/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/samsung-masa-depan-bergantung-pada-ini/blog/58094/':('Cerita','Ciptakan Perubahan','','ElektronikHijau','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/apakah-43-juta-samsung-galaxy-note-7-akan-ber/blog/57920/':('Cerita','Ciptakan Perubahan','','ElektronikHijau','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/rencana-kami-cegah-dan-padamkan-api/blog/57910/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/bukannya-tegas-ioi-malah-ajak-pemasoknya-untu/blog/57676/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/ioi-berhenti-rusak-hutan-gambut-indonesia/blog/57600/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/ioi-perusahaan-sawit-perusak-terlalu-mudah-di/blog/57586/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/asap-hilangkan-91-ribu-jiwa-tanggung-jawab-si/blog/57545/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/urusan-gadget-antara-keinginan-dan-kebutuhan/blog/57530/':('Cerita','Ciptakan Perubahan','','ElektronikHijau','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/tata-kelola-untuk-masa-depan-perikanan-tuna/blog/57493/':('Cerita','Lindungi','','Laut','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/kita-dan-bumi/blog/57445/':('Cerita','Lindungi','','Iklim','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/petani-sawit-mandiri-juga-mampu-menghasilkan-/blog/57424/':('Cerita','Lindungi','','Hutan','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/yuk-dukung-kemerdekaan-hiu-siripnya-tidak-die/blog/57294/':('Cerita','Lindungi','','Laut','','','news-list','Migrate'),
            'http://www.greenpeace.org/seasia/id/blog/penduduk-negara-manakah-yang-paling-banyak-me/blog/57278/':('Cerita','Ciptakan Perubahan','','ElektronikHijau','','','news-list','Migrate'),
        }

        for url,data in start_urls.iteritems():
            p4_post_type, category1, category2, tags1, tags2, tags3, post_type, action = data

            if (post_type == 'article'):
                request = scrapy.Request(url, callback=self.parse_page_type2, dont_filter='true')
            elif (post_type == 'news-list'):
                request = scrapy.Request(url, callback=self.parse_page_type1, dont_filter='true')


            if ( action.lower()=='migrate' ):
                request.meta['status'] = 'publish'
            if ( action.lower()=='archive' ):
                request.meta['status'] = 'draft'
            request.meta['category1'] = category1
            request.meta['category2'] = category2
            request.meta['tags1'] = tags1
            request.meta['tags2'] = tags2
            request.meta['tags3'] = tags3
            request.meta['action'] = action
            request.meta['post_type'] = post_type
            request.meta['p4_post_type'] = p4_post_type
            yield request

        # Migrating authors/thumbnails
        '''
        author_usernames = {
            'greenpeace': 'Greenpeace P4',
            'Keith Stewart': 'p4_username_keith',
            'Miriam Wilson'
        }

        # Read in the file
        with open( 'gpaf_staging_v1.xml', 'r' ) as file :
            filedata = file.read()

        # Replace with correct usernames.
        for p3_author_username, p4_author_username in author_usernames.iteritems():
            filedata = filedata.replace('<author_username>' + p3_author_username, '<author_username>' + p4_author_username)

        # Remove dir="ltr" attributes from elements as requested.
        filedata = filedata.replace('dir="ltr"', '')

        # Write the file out again
        with open('gpaf_staging_v1.xml', 'w') as file:
            file.write(filedata)
        '''

    # Class = 'news-list'
    # pagetypes = blogs,news
    def parse_page_type1(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        imagesA=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//a[img]/@href').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesA_generated.append(image_file)

        imagesB=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img/@src').extract()
        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesB_generated.append(image_file)

        imagesEnlarge=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//a[@class="open-img EnlargeImage"]/@href').extract()
        imagesEnlarge_generated = list()
        for image_file in imagesEnlarge:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesEnlarge_generated.append(image_file)

        pdfFiles=response.css('div.news-list a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/','http://www.greenpeace.org/',1)
            pdf_files_generated.append(pdf_file)

        date_field = response.css('div.news-list .caption::text').re_first(r' - \s*(.*)')
        if date_field:
            date_field = self.filter_month_name(date_field);
            # Filter extra string part from date.
            date_field = date_field.replace(" at", "")  #english
            date_field = date_field.replace(" à", "")
            date_field = date_field.replace(" kl.", "")
            date_field = date_field.replace(" v", "")
            date_field = date_field.replace(" en ", " ") #spanish
            date_field = date_field.replace(" på ", " ") #swedish
            date_field = date_field.replace(" di ", " ") #indonesian
            date_field = dateutil.parser.parse(date_field)

        image_gallery=response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
        p3_image_gallery = 'false'
        if image_gallery:
            p3_image_gallery = 'true'

        body_text = response.css('div.news-list div.post-content').extract_first()
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)

        body_text = self.filter_post_content(body_text)

        images=response.xpath('//*[@class="post-content"]/div/p/a//img[contains(@style, "float:")]').extract()   #img[@style="margin: 9px; float: left;"]
        imagesD_generated = list()
        for image in images:
            imagesD_generated.append(image)

        blockquotes = response.xpath('//*[@id="content"]//blockquote').extract()
        blockquotes_generated = list()
        for blockquote in blockquotes:
            blockquotes_generated.append(blockquote)

        author_username = response.xpath('string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"]/strong/span[@class="green1"]/a/@href)').extract_first()

        if (author_username != 'None'):
            Segments  = author_username.strip().split('/')
            try:                                            #if ( ( len(Segments) == 4 ) and Segments[4] ):
                if ( Segments[4] ):
                    author_username = Segments[4]
            except IndexError:
                try:  # if ( ( len(Segments) == 4 ) and Segments[4] ):
                    if (Segments[3]):
                        author_username = Segments[3]
                except IndexError:
                    author_username = ''

        author_name = response.xpath('string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"]/strong/span[@class="green1"])').extract()[0]
        if ( author_name ):
            author_name = author_name.strip()

        # Get the thumbnail of the post as requested.
        thumbnail = response.xpath('string(head//link[@rel="image_src"]/@href)').extract_first()

        unique_map_id = int(time.time() + random.randint(0, 999))

        # Filter email id image and replace it with email text.
        delete_images = list()
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                # PHP webservice script url.
                api_url = "http://localhosttest/ocr_webservice/email_img_to_text.php"
                end_point_url = api_url + "?url=" + image_file
                emailid = urllib2.urlopen(end_point_url).read(1000)
                # Search replace the \n, <BR>, spaces from email id.
                emailid = emailid.replace('\n', '')
                emailid = emailid.replace('<br>', '')
                emailid = emailid.replace('<BR>', '')
                emailid = emailid.replace(' ', '')
                delete_images.append(image_file)
                # Remove the email images from Post body and replace it with email text.
                body_text = re.sub(
                    '<img[a-zA-Z0-9="\s\_]*src=\"' + image_file + '\"[a-zA-Z0-9="\s]*>',
                    '<a href="mailto:' + emailid.strip() + '" target="_blank">' + emailid.strip() + '</a>', body_text)

        # Remove the email images from list.
        for image_file in delete_images:
            imagesB_generated.remove(image_file)


        # Filter external image from image list and remove them(eg. https://lh4.googleusercontent.com/AG2E...).
        delete_ext_images = list()
        for image_file in imagesB_generated:
            if (".googleusercontent.com/" in image_file):
                delete_ext_images.append(image_file)

        # Remove the external images from list.
        for image_file in delete_ext_images:
            imagesB_generated.remove(image_file)
        # EOD Filter external image

        '''
        #list images urls
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                data = [image_file]
                self.csv_writer(data, "email_images_url_list_fr_story.csv")
        '''

        # list author names
        # data = [author_name,author_username]
        # self.csv_writer(data, "p3_author_list.csv")

        yield {
            'type': response.meta['p4_post_type'],
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.news-list h1::text'),
            #'subtitle': '',
            'author': author_name,
            'author_username': author_username,
            'date': date_field,
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': response.xpath('string(//div[@class="news-list"]/ul/li/div[@class="post-content"]/div//*[self::p or self::h3 or self::h2][1])').extract()[0],
            'category1': response.meta['category1'],
            'category2': response.meta['category2'],
            'text':  body_text,
            'imagesA': imagesA_generated,
            'imagesEnlarge': imagesEnlarge_generated,
            'imagesB': imagesB_generated,
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(), # Galleries (horrible html)
            'imagesD': imagesD_generated,
            'blockquote': blockquotes_generated,
            'pdfFiles': pdf_files_generated,
            'tags1': response.meta['tags1'],
            'tags2': response.meta['tags2'],
            'tags3': response.meta['tags3'],
            'url': response.url,
            'status': response.meta['status'],
            'map_url': '',
            'unique_map_id': unique_map_id,
            'thumbnail': thumbnail,
        }

    # class = 'happen-box article'
    # pagetypes = parse_publication,parse_press,parse_feature
    def parse_page_type2(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        imagesA=response.xpath('//div[@class="post-content"]//a[img]/@href').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesA_generated.append(image_file)

        imagesB=response.xpath('//div[@class="post-content"]//img/@src').extract()
        if len(imagesB) == 0:
            imagesB = response.xpath('//div[@id="content"]//img/@src').extract()

        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            # Custom fix for GPAF only.
            if 'http://assets.pinterest.com/images/PinExt.png' not in image_file:
                imagesB_generated.append(image_file)

        pdfFiles=response.css('div.article a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/','http://www.greenpeace.org/',1)
            pdf_files_generated.append(pdf_file)

        image_gallery=response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
        p3_image_gallery = 'false'
        if image_gallery:
            p3_image_gallery = 'true'

        try:
            lead_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/div/text()').extract()[0]
        except IndexError:
            lead_text = ''

        body_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract()[0]
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = '<div class="leader">' + lead_text + '</div>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

        subtitle = extract_with_css('div.article h2 span::text')
        if subtitle:
            body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        thumbnail = response.xpath('string(head//link[@rel="image_src"]/@href)').extract_first()

        date_field = response.css('div.article div.text span.author::text').re_first(r' - \s*(.*)')
        try:
            date_field = self.filter_month_name(date_field);
            # Filter extra string part from date.
            date_field = date_field.replace(" at", "")  #english
            date_field = date_field.replace(" à", "")
            date_field = date_field.replace(" kl.", "")
            date_field = date_field.replace(" v", "")
            date_field = date_field.replace(" en ", " ") #spanish
            date_field = date_field.replace(" på ", " ") #swedish
            date_field = date_field.replace(" di ", " ") #indonesian
        except IndexError:
            date_field = ""

        if date_field:
            date_field = dateutil.parser.parse(date_field)

        # Filter email id image and replace it with email text.
        delete_images = list()
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                api_url = "http://localhosttest/ocr_webservice/email_img_to_text.php"
                end_point_url = api_url+"?url="+image_file
                emailid = urllib2.urlopen(end_point_url).read(1000)
                # Search replace the \n, <BR>, spaces from email id.
                emailid = emailid.replace('\n', '')
                emailid = emailid.replace('<br>', '')
                emailid = emailid.replace('<BR>', '')
                emailid = emailid.replace(' ', '')
                delete_images.append(image_file)
                # Remove the email images from Post body and replace it with email text.
                body_text = re.sub(
                    '<img[a-zA-Z0-9="\s\_]*src=\"'+image_file+'\"[a-zA-Z0-9="\s]*>',
                    '<a href="mailto:' + emailid.strip() + '" target="_blank">' + emailid.strip() + '</a>', body_text)

        # Remove the email images from list.
        for image_file in delete_images:
            imagesB_generated.remove(image_file)

        # Filter external image from image list and remove them(eg. https://lh4.googleusercontent.com/AG2E...).
        delete_ext_images = list()
        for image_file in imagesB_generated:
            if (".googleusercontent.com/" in image_file):
                delete_ext_images.append(image_file)

        # Remove the external images from list.
        for image_file in delete_ext_images:
            imagesB_generated.remove(image_file)
        # EOD Filter external image

        '''
        #list images urls
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                data = [image_file]
                self.csv_writer(data, "email_images_url_list_fr.csv")
        '''

        # Post data mapping logic start.
        unique_map_id = int(time.time() + random.randint(0, 999))
        map_url = ''
        """
        if "/en/" in response.url:
            # For English language POSTs

            # Check the POST transalation availability
            try:
                map_url = response.xpath('//*[@class="language"]//option[2]/@value').extract()[0]
            except IndexError:
                map_url = ''

            if "/fr/" not in map_url:
                map_url = ''

            if map_url:
                map_url = 'http://www.greenpeace.org' + map_url

                # The Post mapping data added into csv file.
                data = [unique_map_id, response.url, map_url]
                self.csv_writer(data, self.__connector_csv_filename)

                data = [response.url, response.meta['p4_post_type'], response.meta['category1'],response.meta['category2'], response.meta['tags1'], response.meta['tags2'], response.meta['tags3'], response.meta['post_type'], response.meta['action']]
                self.csv_writer(data, "Language_mapping_en_list.csv")
        else:
            # For French language POSTs

            # Check the POST transalation if available
            try:
                map_url = response.xpath('//*[@class="language"]//option[1]/@value').extract()[0]
            except IndexError:
                map_url = ''

            if "/en/" not in map_url:
                map_url = ''

            if map_url:
                map_url = 'http://www.greenpeace.org' + map_url

                with open(self.__connector_csv_filename, "rb") as file_obj:
                    reader = csv.reader(file_obj)
                    for row in reader:
                        if (row[1] == map_url or row[2] == response.url):
                            #print "=======Match found======="
                            unique_map_id = row[0]
                            # Log the details
                            data = ["FR==>", unique_map_id, response.url, map_url,"EN==>", row[0], row[1], row[2]]
                            #print data
                            self.csv_writer(data, self.__connector_csv_log_file)

                            data = [response.url, response.meta['p4_post_type'], response.meta['category1'], response.meta['category2'],
                                    response.meta['tags1'], response.meta['tags2'], response.meta['tags3'],
                                    response.meta['post_type'], response.meta['action']]
                            self.csv_writer(data, "Language_mapping_fr_list.csv")
        # Post data mapping logic ends.
        """

        yield {
            'type': response.meta['p4_post_type'],
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.article h1 span::text'),
            #'subtitle': '',
            'author': 'Greenpeace Indonesia',
            'author_username': 'greenpeace',
            #'date': response.css('#content > div.happen-box.article > div > div.text > span').re_first(r' - \s*(.*)'),
            'date': date_field,
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': extract_with_css('#content > div.happen-box.article > div > div.text > div.leader > div'),
            'category1': response.meta['category1'],
            'category2': response.meta['category2'],
            #'text':  response.css('div.news-list div.post-content').extract_first(),
            'text':  body_text,
            'imagesA': imagesA_generated,
            #'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img[not(ancestor::a)]/@src').extract(), #don't import image if there's an a tag around it
            'imagesB': imagesB_generated,
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(), # Galleries (horrible html)
            'pdfFiles': pdf_files_generated,
            'tags1': response.meta['tags1'],
            'tags2': response.meta['tags2'],
            'tags3': response.meta['tags3'],
            'map_url': map_url,
            'unique_map_id': unique_map_id,
            'url': response.url,
        }

    def filter_post_content(self, post_data):
        # Filter the youtube video and add embed shortcode instead.
        post_data = re.sub(
            '\<object[width\=\"height0-9\s]*data\=\"([https]*\:\/\/www.youtube.com[a-zA-Z0-9\/\=\-\?\_]*)\"[\=\"a-zA-Z\/\-\s0-9]*\>[\\n\s]*(.*)[\\n\s]*\<\/object\>',
            '[embed]\g<1>[/embed]', post_data)

        return post_data

    def filter_month_name(self, month_name):

        month_ind_en = {
            'Januari': 'January',
            'Februari': 'February',
            'Maret': 'March',
            'April': 'April',
            'Mei': 'May',
            'Juni': 'June',
            'Juli': 'July',
            'Agustus': 'August',
            'September': 'September',
            'Oktober': 'October',
            'Nopember': 'November',
            'November': 'November',
            'Desember': 'December',
        }

        # Replace the Indonesian month name with english month name.
        for ind_month, en_month in month_ind_en.iteritems():
            month_name = month_name.replace(ind_month, en_month)

        return month_name;

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
