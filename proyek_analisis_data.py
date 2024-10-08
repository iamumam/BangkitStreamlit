# -*- coding: utf-8 -*-
"""Proyek Analisis Data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15aA47CW8kuUVNT9-acmoSQUX8FfUJdDJ

# Proyek Analisis Data: E Commerce Public Dataset
- **Nama:** Mohamad Khotibul Umam
- **Email:** umammuhamad22@gmail.com
- **ID Dicoding:** Muhammmad Umam

## Menentukan Pertanyaan Bisnis

- Kapan waktu puncak penggunaan sepeda dalam sehari?
- Apakah hari kerja mempengaruhi jumlah pengguna sepeda dibandingkan dengan akhir pekan?

## Import Semua Packages/Library yang Digunakan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

"""## Data Wrangling

### Gathering Data
"""

df_hour = pd.read_csv('hour.csv')
df_hour.head(10)

df_day = pd.read_csv('day.csv')
df_day.head(10)

"""**Insight:**
- Di awal kita melakukan read file csv terlebih dahulu dengan pd.read_csv, ada dua csv yang kita lakukan read yaitu day.csv dan hour.csv day.csv adalah data peminjamaman sepeda dalam hari dan hour.csv adalah data penggunaan sepeda dalam jam
- Selanjutnya kita tampilkan beberapa isi dari csv tersebut dengan method head, disini saya menampilkan 10 row awal saja

### Assessing Data

#### Menilai tabel df_hour
"""

df_hour.info()

df_hour.isna().sum()

df_hour.duplicated().sum()

df_hour.describe()

"""#### Menilai tabel df_day

"""

df_day.info()

df_day.isna().sum()

df_day.duplicated().sum()

df_day.describe()

"""**Insight:**
- Tidak ada missing value dikedua dataset
- Tidak ada data duplikat

### Cleaning Data

####Membersihkan Tabel df_hour
"""

df_hour.info()

"""#####Mengubah tipe data dteday menjadi datetime"""

datetime_columns = ["dteday"]

for column in datetime_columns:
  df_hour[column] = pd.to_datetime(df_hour[column])

df_hour.dtypes

"""####Membersihkan tabel df_day"""

df_day.info()

datetime_columns = ["dteday"]

for column in datetime_columns:
  df_day[column] = pd.to_datetime(df_day[column])

df_day.dtypes

"""**Insight:**
- Didalam dua file csv ini sudah tidak ada missing values dan duplicate jadi saya, menandakan teknik pengumpulan data yang baik
- Column dteday perlu diubah ke tipe datetime untuk mempermudah analisis

## Exploratory Data Analysis (EDA)

### Explore df_hour
"""

df_hour.sample(10)

df_hour.describe(include="all")

df_hour.groupby(by="hr").agg({
    "cnt": ["max", "min", "mean",]})

"""### Explore df_day"""

df_day.sample(10)

df_day.describe(include="all")

df_day.groupby(by="weekday").agg({
    "cnt": ["max", "min", "mean",]})

"""**Insight:**
- Kita bisa mengetahui di jam berapa sepeda banyak disewa
- Kita bisa mengetahui di hari apa sepeda banyak disewa dan apakah ada hubungan jumlah sepeda yang disewa di weekend dan weekday

## Visualization & Explanatory Analysis

### - Kapan waktu puncak penggunaan sepeda dalam sehari?
"""

hourly_usage = df_hour.groupby('hr')['cnt'].sum()

plt.figure(figsize=(10, 6))
sns.barplot(x=hourly_usage.index, y=hourly_usage.values, palette="plasma")

plt.title('Total Peminjaman Sepeda Berdasarkan Jam', fontsize=16)
plt.xlabel('Jam', fontsize=12)
plt.ylabel('Total Peminjaman Sepeda (cnt)', fontsize=12)
plt.xticks(ticks=range(0, 24))  # Jam dari 0 hingga 23
plt.show()

"""### - Apakah hari kerja mempengaruhi jumlah pengguna sepeda dibandingkan dengan akhir pekan?"""

weekday_usage = df_day.groupby('weekday')['cnt'].mean().reset_index()

weekday_usage['day_type'] = weekday_usage['weekday'].apply(lambda x: 'Akhir Pekan' if x >= 5 else 'Hari Kerja')

day_type_usage = weekday_usage.groupby('day_type')['cnt'].mean().reset_index()

plt.figure(figsize=(8, 5))
sns.barplot(x='day_type', y='cnt', data=day_type_usage, palette="Set2")

plt.title('Rata-rata Penggunaan Sepeda: Hari Kerja vs Akhir Pekan', fontsize=16)
plt.xlabel('Tipe Hari', fontsize=12)
plt.ylabel('Rata-rata Pengguna Sepeda (cnt)', fontsize=12)
plt.show()

"""**Insight:**
- Dari visualisasi chart, bisa dilihat bahwa menjelang sore terjadi peningkatan jumlah penyewaan sepeda dengan jam 18 sebagai puncaknya
- Tidak terjadi perbedaan signifikan jumlah penyewaan sepeda yang terjadi antara Hari kerja dan Akhir pekan

## Analisis Lanjutan (Opsional)
"""

def categorize_time(hr):
    if hr < 6:
        return 'Early Morning'
    elif 6 <= hr < 12:
        return 'Morning'
    elif 12 <= hr < 18:
        return 'Afternoon'
    else:
        return 'Evening'

df_hour['Time Category'] = df_hour['hr'].apply(categorize_time)

time_grouped_data = df_hour.groupby('Time Category').agg({
    'cnt': 'sum',
    'casual': 'sum',
    'registered': 'sum'
}).reset_index()

print(time_grouped_data)

plt.figure(figsize=(10, 6))

sns.barplot(data=time_grouped_data,
            x='Time Category',
            y='cnt',
            palette='viridis',
            ci=None)

plt.title('Total Peminjaman Sepeda Berdasarkan Kategori Waktu', fontsize=16)
plt.xlabel('Kategori Waktu', fontsize=12)
plt.ylabel('Total Peminjaman (cnt)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

"""Bisa dilihat bahwa penggunaan sepeda banyak dilakukan di 'afternoon' atau sore hari, berdasar analisa yang saya lakukan karena waktu tersebut suhu atau temperatur mulai menghangat sehingga nyaman digunakan bersepeda

## Conclusion

- Waktu Puncak Penggunaan Sepeda:
Waktu puncak penggunaan sepeda terjadi pada jam 18 atau sore hari. Hal ini terjadi karena di sore hari suhu dan cuaca mulai menghangat sehingga nyaman digunakan untuk bersepeda.

- Pengaruh Hari Kerja terhadap Penggunaan Sepeda:
Tidak ditemukan perbedaan yang signifikan antara penggunaan sepeda pada hari kerja dan akhir pekan. Bahkan, penggunaan sepeda cenderung lebih tinggi pada akhir pekan, yang mungkin menunjukkan bahwa sepeda lebih sering digunakan untuk kegiatan rekreasi atau santai di luar jam kerja.
Kesimpulan ini mengindikasikan bahwa pola penggunaan sepeda lebih dipengaruhi oleh waktu dalam sehari dibandingkan oleh hari kerja atau akhir pekan, dengan tren yang kuat pada jam pulang kerja.
"""

hourly_usage = df_hour.groupby('hr')['cnt'].sum()

# Setup figure
plt.figure(figsize=(10, 6))
sns.barplot(x=hourly_usage.index, y=hourly_usage.values, palette="plasma")

# Tambahkan judul dan label
plt.title('Total Peminjaman Sepeda Berdasarkan Jam', fontsize=16)
plt.xlabel('Jam', fontsize=12)
plt.ylabel('Total Peminjaman Sepeda (cnt)', fontsize=12)
plt.xticks(ticks=range(0, 24))  # Jam dari 0 hingga 23

# Tampilkan plot di Streamlit
st.pyplot(plt)
