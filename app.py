import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Konfigurasi halaman
st.set_page_config(page_title="Aplikasi Matematika Industri", layout="wide")
st.title("📊 Aplikasi Model Matematika Industri")

# Sidebar
st.sidebar.title("Navigasi Model")
menu = st.sidebar.radio("Pilih Model", [
    "Optimisasi Produksi (Linear Programming)",
    "Model Persediaan (EOQ)",
    "Model Antrian (M/M/1)",
    "Model Tambahan: Prediksi Permintaan"
])

# -----------------------------
# 1. Linear Programming
# -----------------------------
if menu == "Optimisasi Produksi (Linear Programming)":
    st.header("Optimisasi Produksi dengan Linear Programming")
    st.markdown("""
    **Studi Kasus:**
    Sebuah pabrik memproduksi dua jenis produk: A dan B. 
    - Produk A memberi keuntungan Rp3/unit dan membutuhkan 2 jam kerja dan 3 bahan baku.
    - Produk B memberi keuntungan Rp5/unit dan membutuhkan 1 jam kerja dan 1 bahan baku.
    - Total waktu kerja tersedia: 8 jam
    - Total bahan baku tersedia: 4 unit
    Tujuan: Maksimalkan keuntungan.
    """)

    c = [-3, -5]  # Koefisien fungsi objektif
    A = [[2, 3], [1, 1]]  # Matriks kendala
    b = [8, 4]  # RHS kendala

    res = linprog(c, A_ub=A, b_ub=b)
    if res.success:
        st.success(f"Solusi Optimal:\nProduk A = {res.x[0]:.2f} unit, Produk B = {res.x[1]:.2f} unit\nTotal Keuntungan = Rp{-res.fun:.2f}")
    else:
        st.error("Solusi tidak ditemukan.")

    st.subheader("Visualisasi Area Solusi")
    x = np.linspace(0, 5, 200)
    y1 = (8 - 2 * x) / 3
    y2 = 4 - x
    
    fig, ax = plt.subplots()
    ax.plot(x, y1, label="2x + 3y ≤ 8")
    ax.plot(x, y2, label="x + y ≤ 4")
    ax.set_xlim((0, 5))
    ax.set_ylim((0, 5))
    ax.fill_between(x, 0, np.minimum(y1, y2), where=(np.minimum(y1, y2) >= 0), color='yellow', alpha=0.3)
    ax.set_xlabel("Produk A")
    ax.set_ylabel("Produk B")
    ax.legend()
    st.pyplot(fig)

# -----------------------------
# 2. EOQ Model
# -----------------------------
elif menu == "Model Persediaan (EOQ)":
    st.header("Model Persediaan EOQ")
    st.markdown("""
    **Studi Kasus:**
    Sebuah toko menjual 10.000 unit barang per tahun.
    - Biaya pemesanan per pesanan: Rp500
    - Biaya penyimpanan per unit per tahun: Rp2
    Tujuan: Hitung Economic Order Quantity (EOQ).
    """)

    D = st.number_input("Permintaan Tahunan (D)", value=10000)
    S = st.number_input("Biaya Pemesanan (S)", value=500)
    H = st.number_input("Biaya Penyimpanan per unit (H)", value=2.0)

    EOQ = np.sqrt((2 * D * S) / H)
    st.success(f"EOQ: {EOQ:.2f} unit")

    st.subheader("Visualisasi EOQ")
    Q = np.linspace(100, 1000, 100)
    TC = (D / Q) * S + (Q / 2) * H
    fig, ax = plt.subplots()
    ax.plot(Q, TC, label='Total Cost')
    ax.axvline(EOQ, color='r', linestyle='--', label=f'EOQ = {EOQ:.0f}')
    ax.set_xlabel('Kuantitas Pesan')
    ax.set_ylabel('Total Cost')
    ax.legend()
    st.pyplot(fig)

# -----------------------------
# 3. Queue Model (M/M/1)
# -----------------------------
elif menu == "Model Antrian (M/M/1)":
    st.header("Model Antrian M/M/1")
    st.markdown("""
    **Studi Kasus:**
    Suatu loket melayani pelanggan dengan rata-rata 10 pelanggan/jam, dan kedatangan pelanggan rata-rata 7 pelanggan/jam.
    Hitung rata-rata panjang antrian dan waktu tunggu.
    """)

    lam = st.number_input("Laju Kedatangan (λ)", value=7.0)
    mu = st.number_input("Laju Pelayanan (μ)", value=10.0)

    if lam < mu:
        rho = lam / mu
        Lq = (rho**2) / (1 - rho)
        Wq = Lq / lam
        st.success(f"Panjang Antrian Rata-rata (Lq): {Lq:.2f} pelanggan\nWaktu Tunggu Rata-rata (Wq): {Wq:.2f} jam")
    else:
        st.error("Sistem tidak stabil (λ ≥ μ)")

# -----------------------------
# 4. Tambahan: Prediksi Permintaan
# -----------------------------
elif menu == "Model Tambahan: Prediksi Permintaan":
    st.header("Prediksi Permintaan dengan Regresi Linear")
    st.markdown("""
    **Studi Kasus:**
    Diberikan data permintaan 6 bulan terakhir, prediksi permintaan bulan ke-7.
    """)

    months = np.array([1, 2, 3, 4, 5, 6])
    demand = np.array([120, 135, 150, 160, 175, 190])

    coeffs = np.polyfit(months, demand, 1)
    pred = np.polyval(coeffs, 7)

    st.success(f"Prediksi permintaan bulan ke-7: {pred:.2f} unit")

    st.subheader("Visualisasi Data dan Prediksi")
    fig, ax = plt.subplots()
    ax.plot(months, demand, 'bo-', label='Data Historis')
    ax.plot(7, pred, 'ro', label='Prediksi Bulan 7')
    ax.plot(np.append(months, 7), np.polyval(coeffs, np.append(months, 7)), 'g--', label='Garis Regresi')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Permintaan')
    ax.legend()
    st.pyplot(fig)

# Sidebar petunjuk
st.sidebar.markdown("""
**Petunjuk:**
- Pilih model dari menu.
- Masukkan parameter sesuai kasus.
- Lihat hasil perhitungan dan grafik.
""")
