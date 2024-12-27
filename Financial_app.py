import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Setup
st.title("Dashboard Keuangan - Rafif")

# In-memory DataFrame untuk menyimpan data transaksi
if "transactions" not in st.session_state:
    st.session_state["transactions"] = pd.DataFrame(columns=["Tanggal", "Kategori", "Jenis", "Jumlah", "Keterangan"])

# Fungsi untuk menambah transaksi
def add_transaction(tanggal, kategori, jenis, jumlah, keterangan):
    new_transaction = {
        "Tanggal": tanggal,
        "Kategori": kategori,
        "Jenis": jenis,
        "Jumlah": jumlah,
        "Keterangan": keterangan,
    }
    st.session_state["transactions"] = pd.concat(
        [st.session_state["transactions"], pd.DataFrame([new_transaction])],
        ignore_index=True,
    )

# Sidebar Menu
menu_option = st.sidebar.radio(
    "Navigasi",
    ["Tambah Transaksi", "Data Transaksi", "Ringkasan Keuangan"]
)

# Konten Berdasarkan Menu
if menu_option == "Tambah Transaksi":
    st.header("Tambah Transaksi")
    with st.form("transaction_form"):
        tanggal = st.date_input("Tanggal")
        kategori = st.selectbox("Kategori", ["Pemasukan", "Pengeluaran"])
        jenis = st.selectbox("Jenis", ["Gaji", "Belanja", "Investasi", "Tabungan", "Lainnya"])
        jumlah = st.number_input("Jumlah (Rp)", min_value=0, step=1000)
        keterangan = st.text_input("Keterangan", "")
        submitted = st.form_submit_button("Tambah")

        if submitted:
            add_transaction(tanggal, kategori, jenis, jumlah, keterangan)
            st.success("Transaksi berhasil ditambahkan!")

elif menu_option == "Data Transaksi":
    st.header("Data Transaksi")
    st.dataframe(st.session_state["transactions"])

    # Ekspor Data
    st.header("Ekspor Data")
    if st.download_button(
        "Download Data sebagai Excel",
        data=st.session_state["transactions"].to_csv(index=False),
        file_name="data_keuangan.csv",
        mime="text/csv",
    ):
        st.success("File berhasil diunduh!")

elif menu_option == "Ringkasan Keuangan":
    st.header("Ringkasan Keuangan")
    total_pemasukan = st.session_state["transactions"][st.session_state["transactions"]["Kategori"] == "Pemasukan"]["Jumlah"].sum()
    total_pengeluaran = st.session_state["transactions"][st.session_state["transactions"]["Kategori"] == "Pengeluaran"]["Jumlah"].sum()
    saldo = total_pemasukan - total_pengeluaran

    st.metric("Total Pemasukan", f"Rp {total_pemasukan:,.0f}")
    st.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
    st.metric("Saldo", f"Rp {saldo:,.0f}")

    # Visualisasi
    st.header("Visualisasi Keuangan")
    if not st.session_state["transactions"].empty:
        fig, ax = plt.subplots()
        summary = st.session_state["transactions"].groupby("Kategori")["Jumlah"].sum()
        ax.pie(summary, labels=summary.index, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)
    else:
        st.write("Tidak ada data untuk ditampilkan.")