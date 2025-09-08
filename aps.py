# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from io import BytesIO

# ====== Setup ======
DATA_FILE = "Fix_Dataset.xlsx"

alergi_obat_dict = {0: "Tidak Ada", 2: "amoxicillin, metroklopramid hcl",
3: "asam mefenamat, natrium diclofenac", 4: "cetirizine", 5: "cefixime",
6: "asam mefenamat, eperison", 7: "amoxicillin", 8: "asam mefenamat",
9: "komix, konidin", 10: "ketoconazole", 11: "cefadroxil", 
12: "asam mefenamat, cefadroxil, lansoprazole, penisilin", 13: "sulfa", 
14: "kotrimoxazole", 15: "salbutamol", 16: "ceftriaxone, ketorolac",
17: "ampicillin", 18: "antalgin, mylanta, penisilin",
19: "cefixime, methylprednisolone", 20:"dexa", 21: "antalgin",
22: "ambroxol, amoxicillin", 23: "penisilin", 24: "ketoconazole, penisilin",
25: "antalgin, ketorolac", 26: "avamys", 27: "mefinal", 28: "eritromicin",
29: "eritromicin, metronidazole", 30: "tetra", 31: "piraceta",
32: "cefixime, ciprofloxacin, meloxicam, metampiron, piroxicam",
33: "amoxicillin, bodrexin, contrexin",
34: "cefixime, ciprofloxacin, metampiron, piroxicam",
35: "amoxicillin, cefadroxil",
36: "cetirizine, ibuprofen, ketorolac, metampiron, salbutamol",
37: "paracetamol", 38: "amoxicillin, ciprofloxacin"}

alergi_makanan_dict = {0: "Tidak Ada", 1: "Daging", 2: "Seafood", 3: "Udang"}

treatment_dict = {0: "Tidak Ada", 1: "audiometri, pelayanan poliklinik spesialis",
                  2: "biopsi kecil, ekterpasi masa kecil ditelinga/hidung, pelayanan poliklinik spesialis",
                  3: "bsm, pasang syringpump.", 4: "endoskopi laring, pemeriksaan dokter spesialis pasien baru",
                  5: "evakuasi corpus alenium ringan binatang, pelayanan poliklinik spesialis",
                  6: "evakuasi/pengambilan cerumen/stosel/corpus alienum ringan non binatang/discrge di telinga hidung, pemeriksaan dokter spesialis pasien lama, asuhan keperawatan/kebidanan",
                  7: "gds stik", 8: "irigasi mata", 9: "irigasi sinus post operasi, pemeriksaan dokter spesialis pasien lama",
                  10: "lepas/pasang tampon hidung, pembersihan hidung, pelayanan poliklinik spesialis", 11: "necrotomi",
                  12: "pasang infus, obat oral nifedipin 20 mg, eritromisin 250 tab, cek urin",
                  13: "pasang/lepas tampon daryantule ditelinga/hidung (10cm), pemeriksaan dokter spesialis pasien lama",
                  14: "pd djj", 15: "pelayanan poliklinik spesialis", 16: "pelayanan poliklinik spesialis, alat bantu dengar",
                  17: "pelayanan poliklinik spesialis, angkat jahit/hecting aff &gt;10, perawatan luka besar (&gt;10 cm)",
                  18: "pelayanan poliklinik spesialis, angkat jahit/hecting aff 1-5, perawatan luka sedang (3-10 cm)", 
                  19: "pelayanan poliklinik spesialis, audiometri", 20: "pelayanan poliklinik spesialis, aural toilet",
                  21: "pelayanan poliklinik spesialis, eksplorasi nasopharyng local", 22: "pelayanan poliklinik spesialis, endoskopi laring", 
                  23: "pelayanan poliklinik spesialis, evakuasi corpus alenium ringan binatang", 
                  24: "pelayanan poliklinik spesialis, evakuasi/pengambilan cerumen/stosel/corpus alienum ringan non binatang/discharge di telinga hidung, aural toilet",
                  25: "pelayanan poliklinik spesialis, evakuasi/pengambilan cerumen/stosel/corpus alienum ringan non binatang/discrge di telinga hidung",
                  26: "pelayanan poliklinik spesialis, evakuasi/pengambilan cerumen/stosel/corpus alienum ringan non binatang/discrge di telinga hidung, nasoendoskopi",
                  27 :"pelayanan poliklinik spesialis, irigasi canalis externa", 
                  28: "pelayanan poliklinik spesialis, irigasi canalis externa, pembersihan hidung, evakuasi/pengambilan cerumen/stosel/corpus alienum ringan non binatang/discrge di telinga hidung, check up pendengaran",
                  29 : "pelayanan poliklinik spesialis, irigasi sinus post operasi", 30: "pelayanan poliklinik spesialis, lepas/pasang tampon hidung",
                  31: "pelayanan poliklinik spesialis, parasentetis/aspirasi abses", 32: "pelayanan poliklinik spesialis, pasang/lepas tampon daryantule ditelinga/hidung (10cm)",
                  33: "pelayanan poliklinik spesialis, pasang/lepas tampon daryantule ditelinga/hidung (10cm), angkat jahit/hecting aff 1-5",
                  34: "pelayanan poliklinik spesialis, pasang/lepas tampon daryantule ditelinga/hidung (10cm), evakuasi/pengambilan cerumen/stosel/corpus alienum ringan non binatang/discrge di telinga hidung, aural toilet",
                  35: "pelayanan poliklinik spesialis, pasang/lepas tampon daryantule ditelinga/hidung (10cm), pembersihan hidung",
                  36: "pelayanan poliklinik spesialis, pasang/lepas tampon daryantule ditelinga/hidung (10cm), perawatan luka besar (&gt;10 cm)", 
                  37: "pelayanan poliklinik spesialis, pembersihan hidung, angkat jahit/hecting aff &gt;10",
                  38: "pelayanan poliklinik spesialis, pembersihan hidung, angkat jahit/hecting aff 6-10",
                  39: "pelayanan poliklinik spesialis, pembersihan hidung, evaluasi terapi", 40: "pelayanan poliklinik spesialis, pembersihan hidung, nasal toilet",
                  41: "pelayanan poliklinik spesialis, pembersihan hidung, pasang/lepas tampon daryantule ditelinga/hidung (10cm)", 
                  42: "pelayanan poliklinik spesialis, pembersihan hidung, perawatan luka besar (&gt;10 cm)",
                  43: "pelayanan poliklinik spesialis, pemeriksaan audiometric", 44: "pelayanan poliklinik spesialis, perawatan luka sedang (3-10 cm)",
                  45: "pelayanan poliklinik spesialis, rawat luka", 46: "pemberian paracetamol pes infus",
                  47: "pemeriksaan audiometric, pelayanan poliklinik spesialis", 48: "pemeriksaan audiometric, pemeriksaan dokter spesialis pasien baru",
                  49: "pemeriksaan dokter spesialis pasien baru", 50: "pemeriksaan dokter spesialis pasien baru, evakuasi corpal tenggorok",
                  51: "pemeriksaan dokter spesialis pasien baru, evakuasi corpus alenium ringan binatang", 52: "pemeriksaan dokter spesialis pasien lama",
                  53: "pemeriksaan dokter spesialis pasien lama, aff hecting 3", 54: "pemeriksaan dokter spesialis pasien lama, alat bantu dengar", 
                  55: "pemeriksaan dokter spesialis pasien lama, evakuasi/pengambilan cerumen/stosel/corpus alienum ringan non binatang/discrge di telinga hidung, pembersihan hidung",
                  56: "pemeriksaan dokter spesialis pasien lama, irigasi sinus post operasi",
                  57: "pemeriksaan dokter spesialis pasien lama, lepas tampon hidung", 
                  58: "pemeriksaan dokter spesialis pasien lama, pasang/lepas tampon daryantule ditelinga/hidung (10cm)", 
                  59: "pemeriksaan dokter spesialis pasien lama, pembersihan hidung", 60: "pemeriksaan dokter spesialis pasien lama, pemeriksaan audiometric",
                  61: "pemeriksaan dokter spesialis pasien lama, perawatan luka kecil (&lt;3 cm)", 
                  62: "pemeriksaan dokter spesialis pasien lama, provokasi hidung/pengambilan pus dengan vacuum",
                  63: "pemeriksaan tht", 64: "periksa", 65: "tindakan sedrhana igd ( gds ), observasi, gds stik"}

# Cek apakah file data ada, jika tidak buat file kosong
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=[
        "id", "alergi_obat", "alergi_makanan", "anamnese", 
        "treatment", "diagnose", "pemeriksaan_fisik", "obat", "status"
    ])
    df.to_excel(DATA_FILE, index=False)

# Fungsi untuk load dataset
import os

def load_data():
    try:
        df = pd.read_excel(DATA_FILE, engine="openpyxl")
    except Exception:
        # kalau file tidak ada atau korup → buat DataFrame baru
        df = pd.DataFrame(columns=[
            "id", "alergi_obat", "alergi_makanan",
            "anamnese", "pemeriksaan_fisik", "diagnose",
            "treatment", "rencana", "obat", "status"
        ])
        df.to_excel(DATA_FILE, index=False, engine="openpyxl")
    
    # Pastikan kolom 'status' ada
    if "status" not in df.columns:
        df["status"] = "Aktif"
 
    if "id" in df.columns:
        df["id"] = pd.to_numeric(df["id"], errors="coerce").fillna(0).astype(int)
    
    # Pastikan alergi berupa angka (kalau masih string di Excel)
    if "alergi_obat" in df.columns:
        df["alergi_obat"] = pd.to_numeric(df["alergi_obat"], errors="coerce").fillna(0).astype(int)
        df["alergi_obat_label"] = df["alergi_obat"].map(alergi_obat_dict)

    if "alergi_makanan" in df.columns:
        df["alergi_makanan"] = pd.to_numeric(df["alergi_makanan"], errors="coerce").fillna(0).astype(int)
        df["alergi_makanan_label"] = df["alergi_makanan"].map(alergi_makanan_dict)
    
    if "treatment" in df.columns:
        df["treatment"] = pd.to_numeric(df["treatment"], errors="coerce").fillna(0).astype(int)
        df["treatment_label"] = df["treatment"].map(treatment_dict)
    return df

# Fungsi untuk save dataset
def save_data(df):
    if "id" in df.columns:
        df["id"] = pd.to_numeric(df["id"], errors="coerce").fillna(0).astype(int)
    df.to_excel(DATA_FILE, index=False, engine="openpyxl")  
    
def generate_new_id(df):
    if df.empty:
        return 1
    else:
        return df["id"].max() + 1

# === Helper function ===
def input_with_manual(label, options, key):
    """Pilih dari daftar atau isi manual"""
    selected = st.selectbox(
        label,
        ["--Pilih--"] + options,
        key=f"select_{key}"
    )
    if selected == "--Isi Manual--":
        return st.text_input(f"{label} (Manual)", key=f"manual_{key}")
    elif selected == "--Pilih--":
        return ""
    else:
        return selected

# Helper decode function
def decode_value(value, mapping_dict, default="Tidak Diketahui"):
    try:
        value = int(value)
    except:
        return default
    return mapping_dict.get(value, default)
  

# ====== Sidebar Menu dengan Kotak ======
st.sidebar.title("🏥 Manajemen Data Pasien")

# Simpan state halaman di session_state
if "menu" not in st.session_state:
    st.session_state.menu = "Dashboard"
if "crud_menu" not in st.session_state:
    st.session_state.crud_menu = None

# Menu utama
st.sidebar.subheader("📌 Menu Utama")
if st.sidebar.button("📊 Dashboard", use_container_width=True):
    st.session_state.menu = "Dashboard"
    st.session_state.crud_menu = None   # reset CRUD

if st.sidebar.button("👨‍⚕️ Data Pasien", use_container_width=True):
    st.session_state.menu = "Data Pasien"
    st.session_state.page = "list"      # default ke daftar pasien
    st.session_state.crud_menu = None

if st.sidebar.button("➕ Tambah Pasien", use_container_width=True):
    st.session_state.menu = "Tambah Pasien"
    st.session_state.crud_menu = None

if st.sidebar.button("✏️ Edit Pasien", use_container_width=True):
    st.session_state.menu = "Edit Pasien"
    st.session_state.crud_menu = None
    
if st.sidebar.button("🗑️ Hapus Pasien", use_container_width=True):
    st.session_state.menu = "Hapus Pasien"
    st.session_state.crud_menu = None

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Keterangan")

if st.sidebar.button("ℹ️ Mapping Encode", use_container_width=True):
    st.session_state.menu = "Mapping Encode"
    st.session_state.crud_menu = None    

# Gunakan menu dari session_state
menu = st.session_state.menu

if menu == "Dashboard":
    st.title("📊 Dashboard Data Pasien")

    df = load_data()
    
    # Hitung statistik
    total_pasien = len(df)
    persen_alergi_obat = (df["alergi_obat"].gt(0).mean() * 100).round(2) if total_pasien > 0 else 0
    persen_alergi_makanan = (df["alergi_makanan"].gt(0).mean() * 100).round(2) if total_pasien > 0 else 0
    
    if not df.empty:
        kode_treatment = df["treatment"].mode()[0]
        treatment_terbanyak = treatment_dict.get(kode_treatment, "Tidak Diketahui")
    else:
        treatment_terbanyak = "-"

    # Tampilkan KPI
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Pasien", total_pasien)
    with col2:
        st.metric("Alergi Obat", f"{persen_alergi_obat}%")
    with col3:
        st.metric("Alergi Makanan", f"{persen_alergi_makanan}%")
    with col4:
        st.markdown(f"**Treatment Terbanyak**  \n{treatment_terbanyak}")
        st.caption(f"Kode: {kode_treatment}")

    st.markdown("---")
    
    # ===== Distribusi Alergi Obat & Makanan (Side by Side) =====
    col1, col2 = st.columns(2)

    with col1:
        if "alergi_obat" in df.columns:
            alergi_obat_count = df[df["alergi_obat"] > 0]["alergi_obat_label"].value_counts()
            if not alergi_obat_count.empty:
                fig_obat = px.bar(
                    x=alergi_obat_count.values, 
                    y=alergi_obat_count.index,
                    orientation="h",   # supaya lebih rapi (horizontal bar)
                    title="Distribusi Alergi Obat",
                    labels={"x": "Jumlah", "y": "Jenis Alergi"}
                )
                st.plotly_chart(fig_obat, use_container_width=True)

    with col2:
        if "alergi_makanan" in df.columns:
            # Hanya ambil pasien yang punya alergi makanan (>0)
            alergi_mkn_count = (
                df[df["alergi_makanan"] > 0]["alergi_makanan_label"].value_counts()
            )
            if not alergi_mkn_count.empty:
                fig_pie_mkn = px.pie(
                    values=alergi_mkn_count.values,
                    names=alergi_mkn_count.index,
                    title="Distribusi Alergi Makanan",
                    hole=0.4
                )
                st.plotly_chart(fig_pie_mkn, use_container_width=True)
    st.caption("⚠️ Pasien tanpa alergi tidak ditampilkan dalam grafik.")

    # Bar chart Treatment
    treat_count = df["treatment"].value_counts()
    fig_treat = px.bar(x=treat_count.index, y=treat_count.values,
                        title="Distribusi Treatment",
                        labels={"x": "Kode Treatment", "y": "Jumlah"})
    st.plotly_chart(fig_treat, use_container_width=True)
    st.caption("⚠️ Keterangan kode treatment dapat dilihat pada mapping encode")

    # Tabel Data Pasien
    st.subheader("Daftar Pasien")

    # Ambil salinan data
    df_display = df.copy()

    # Ganti kolom asli dengan label, lalu hapus kolom *_label biar gak tampil dua kali
    if "alergi_obat" in df_display.columns and "alergi_obat_label" in df_display.columns:
        df_display["alergi_obat"] = df_display["alergi_obat_label"]
        df_display.drop(columns=["alergi_obat_label"], inplace=True)

    if "alergi_makanan" in df_display.columns and "alergi_makanan_label" in df_display.columns:
        df_display["alergi_makanan"] = df_display["alergi_makanan_label"]
        df_display.drop(columns=["alergi_makanan_label"], inplace=True)

    if "treatment" in df_display.columns and "treatment_label" in df_display.columns:
        df_display["treatment"] = df_display["treatment_label"]
        df_display.drop(columns=["treatment_label"], inplace=True)

    # Pastikan id tampil rapi
    df_display["id"] = df_display["id"].astype(str)

    # Tampilkan tabel
    st.dataframe(df_display)

# ===== CRUD Pasien =====
elif menu == "Data Pasien":
    st.title("👨‍⚕️ Data Pasien")

    df = load_data()

    # READ
    # Pastikan ada state untuk halaman aktif
    if "page" not in st.session_state:
        st.session_state.page = "list"   # default tampil daftar pasien
    if "selected_id" not in st.session_state:
        st.session_state.selected_id = None

    # === Halaman daftar pasien ===
    if st.session_state.page == "list":
        st.subheader("📋 Daftar Pasien")
        df_display = df[df["status"] == "Aktif"].copy()

        # Mapping label agar user-friendly
        if "alergi_obat" in df_display.columns and "alergi_obat_label" in df_display.columns:
            df_display["alergi_obat"] = df_display["alergi_obat_label"]
            df_display.drop(columns=["alergi_obat_label"], inplace=True)

        if "alergi_makanan" in df_display.columns and "alergi_makanan_label" in df_display.columns:
            df_display["alergi_makanan"] = df_display["alergi_makanan_label"]
            df_display.drop(columns=["alergi_makanan_label"], inplace=True)

        if "treatment" in df_display.columns and "treatment_label" in df_display.columns:
            df_display["treatment"] = df_display["treatment_label"]
            df_display.drop(columns=["treatment_label"], inplace=True)

        df_display["id"] = df_display["id"].astype(str)
        st.dataframe(df_display)

        st.markdown("---")
        st.subheader("🔍 Pilih Pasien")

        with st.form("form_detail"):
            pilihan_id = st.selectbox("Pilih ID Pasien", df_display["id"].astype(str))
            lihat_btn = st.form_submit_button("Lihat Detail")

        if lihat_btn:
            st.session_state.selected_id = pilihan_id
            st.session_state.page = "detail"
            st.rerun()  # pindah ke halaman detail

    # === Halaman detail pasien ===
    elif st.session_state.page == "detail":
        pilihan_id = st.session_state.selected_id
        data_pasien = df[df["id"].astype(str) == pilihan_id].iloc[0]

        # Decode dari kode → label
        alergi_obat_label = alergi_obat_dict.get(data_pasien["alergi_obat"], "Tidak Ada")
        alergi_makanan_label = alergi_makanan_dict.get(data_pasien["alergi_makanan"], "Tidak Ada")
        treatment_label = treatment_dict.get(data_pasien["treatment"], "Tidak Diketahui")

        st.markdown("---")
        st.markdown(
            f"""
            <div style="background-color:#ffffff;padding:20px;border-radius:15px;
                        box-shadow:2px 2px 10px rgba(0,0,0,0.1);font-size:16px;line-height:1.6;">
                <h3 style="margin-top:0; color:#2c3e50;">🩺 Rekam Medis Pasien</h3>
                <p style="color:#000000;"><b>ID:</b> {data_pasien["id"]}</p>
                <p style="color:#000000;"><b>Alergi Obat:</b> {alergi_obat_label}</p>
                <p style="color:#000000;"><b>Alergi Makanan:</b> {alergi_makanan_label}</p>
                <p style="color:#000000;"><b>Anamnese:</b> {data_pasien["anamnese"]}</p>
                <p style="color:#000000;"><b>Pemeriksaan Fisik:</b> {data_pasien["pemeriksaan_fisik"]}</p>
                <p style="color:#000000;"><b>Diagnose:</b> {data_pasien["diagnose"]}</p>
                <p style="color:#000000;"><b>Treatment:</b> {treatment_label}</p>
                <p style="color:#000000;"><b>Rencana:</b> {data_pasien["rencana"]}</p>
                <p style="color:#000000;"><b>Obat:</b> {data_pasien["obat"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")
        if st.button("⬅️ Kembali ke Daftar Pasien"):
            st.session_state.page = "list"
            st.rerun()

# =================== FORM TAMBAH DATA ===================
elif menu == "Tambah Pasien":
    st.title("➕ Tambah Pasien")
    df = load_data()

    with st.form("tambah_pasien"):
        # Input ID Pasien manual, kosong = generate otomatis
        new_id_input = st.text_input("ID Pasien (kosong = generate otomatis)").strip()
        if new_id_input.isdigit():
            new_id = int(new_id_input)
        else:
            new_id = generate_new_id(df)

        # Input alergi & treatment
        alergi_obat = input_with_manual("Alergi Obat", list(alergi_obat_dict.values()), key="alergi_obat")
        alergi_makanan = input_with_manual("Alergi Makanan", list(alergi_makanan_dict.values()), key="alergi_makanan")
        treatment = input_with_manual("Treatment", list(treatment_dict.values()), key="treatment")

        # Input lain
        anamnese = st.text_area("Anamnese")
        pemeriksaan_fisik = st.text_area("Pemeriksaan Fisik")
        diagnose = st.text_area("Diagnose")
        rencana = st.text_area("Rencana")
        obat = st.text_input("Obat")

        # Tombol submit **HARUS di dalam blok form**
        submitted = st.form_submit_button("Simpan Data")

        if submitted:
            # Mapping label kembali ke kode jika ada di dictionary
            alergi_obat_code = next((k for k,v in alergi_obat_dict.items() if v == alergi_obat), 0)
            alergi_makanan_code = next((k for k,v in alergi_makanan_dict.items() if v == alergi_makanan), 0)
            treatment_code = next((k for k,v in treatment_dict.items() if v == treatment), 0)

            # Buat dataframe baru
            new_data = pd.DataFrame([{
                "id": new_id,
                "alergi_obat": alergi_obat_code,
                "alergi_makanan": alergi_makanan_code,
                "anamnese": anamnese,
                "pemeriksaan_fisik": pemeriksaan_fisik,
                "diagnose": diagnose,
                "treatment": treatment_code,
                "rencana": rencana,
                "obat": obat
            }])

            df = pd.concat([df, new_data], ignore_index=True)
            save_data(df)
            st.success(f"✅ Data pasien {new_id} berhasil ditambahkan!")

# =================== FORM EDIT DATA ===================
elif menu == "Edit Pasien":
    st.title("✏️ Edit Pasien")
    df = load_data()
    if df.empty:
        st.warning("Belum ada data pasien.")
    else:
        pilihan_id= st.selectbox("Pilih ID Pasien", df["id"].astype(str))
        pasien = df[df["id"].astype(str) == pilihan_id].iloc[0]

        with st.form("edit_pasien"):
            st.text_input("ID Pasien", value=pilihan_id, disabled=True)

            # === Alergi Obat ===
            obat_options = ["--Pilih--"] + list(alergi_obat_dict.values())
            alergi_obat_value = alergi_obat_dict.get(pasien["alergi_obat"], "Tidak Ada")
            alergi_obat = st.selectbox(
                "Alergi Obat",
                options=obat_options,
                index=obat_options.index(alergi_obat_value) if alergi_obat_value in obat_options else 0
            )

            # === Alergi Makanan ===
            makanan_options = ["--Pilih--"] + list(alergi_makanan_dict.values())
            alergi_makanan_value = alergi_makanan_dict.get(pasien["alergi_makanan"], "Tidak Ada")
            alergi_makanan = st.selectbox(
                "Alergi Makanan",
                options=makanan_options,
                index=makanan_options.index(alergi_makanan_value) if alergi_makanan_value in makanan_options else 0
            )

            # === Treatment ===
            treatment_options = ["--Pilih--"] + list(treatment_dict.values())
            treatment_value = treatment_dict.get(pasien["treatment"], "Tidak Diketahui")
            treatment = st.selectbox(
                "Treatment",
                options=treatment_options,
                index=treatment_options.index(treatment_value) if treatment_value in treatment_options else 0
            )

            # Field teks lain
            anamnese = st.text_input("Anamnese", value=str(pasien["anamnese"]))
            pemeriksaan_fisik = st.text_input("Pemeriksaan Fisik", value=str(pasien["pemeriksaan_fisik"]))
            diagnose = st.text_input("Diagnose", value=str(pasien["diagnose"]))
            rencana = st.text_area("Rencana", value=str(pasien["rencana"]))
            obat = st.text_input("Obat", value=str(pasien["obat"]))

            submitted = st.form_submit_button("💾 Simpan Perubahan")
            if submitted:
                df.loc[df["id"].astype(str) == pilihan_id, [
                    "alergi_obat", "alergi_makanan", "treatment",
                    "anamnese", "pemeriksaan_fisik", "diagnose", "rencana", "obat"
                ]] = [
                    list(alergi_obat_dict.keys())[list(alergi_obat_dict.values()).index(alergi_obat)],
                    list(alergi_makanan_dict.keys())[list(alergi_makanan_dict.values()).index(alergi_makanan)],
                    list(treatment_dict.keys())[list(treatment_dict.values()).index(treatment)],
                    anamnese, pemeriksaan_fisik, diagnose, rencana, obat
                ]
                save_data(df)
                st.success(f"✅ Data pasien {pilihan_id} berhasil diperbarui!")

# DELETE
elif menu == "Hapus Pasien":
    st.title("🗑️ Nonaktifkan / Aktifkan Pasien")
    df = load_data()
    if df.empty:
        st.warning("Belum ada data pasien.")
    else:
        # Pilih mode
        mode = st.selectbox("Pilih Aksi", ["Nonaktifkan Pasien", "Aktifkan Pasien"])

        # === MODE NONAKTIFKAN ===
        if mode == "Nonaktifkan Pasien":
            df_aktif = df[df["status"] == "Aktif"]
            if df_aktif.empty:
                st.info("Tidak ada pasien aktif yang bisa dinonaktifkan.")
            else:
                pilihan = st.selectbox("Pilih ID Pasien", df_aktif["id"].astype(str))
                data_hapus = df_aktif[df_aktif["id"].astype(str) == pilihan].iloc[0]

                st.write("### Detail Pasien yang akan dinonaktifkan")
                st.json({
                    "ID": str(data_hapus["id"]),
                    "Alergi Obat": alergi_obat_dict.get(data_hapus["alergi_obat"], "Tidak Ada"),
                    "Alergi Makanan": alergi_makanan_dict.get(data_hapus["alergi_makanan"], "Tidak Ada"),
                    "Anamnese": data_hapus["anamnese"],
                    "Diagnose": data_hapus["diagnose"],
                    "Pemeriksaan Fisik": data_hapus["pemeriksaan_fisik"],
                    "Rencana": data_hapus["rencana"],
                    "Treatment": treatment_dict.get(data_hapus["treatment"], "Tidak Diketahui"),
                    "Obat": str(data_hapus["obat"])
                })

                if st.button("⚠️ Konfirmasi Nonaktifkan", use_container_width=True, key="btn_nonaktif"):
                    df.loc[df["id"].astype(str) == pilihan, "status"] = "Nonaktif"
                    save_data(df)
                    st.session_state.success_msg = f"Pasien dengan ID {pilihan} berhasil dinonaktifkan ❌"

        # === MODE AKTIFKAN ===
        elif mode == "Aktifkan Pasien":
            df_nonaktif = df[df["status"] == "Nonaktif"]
            if df_nonaktif.empty:
                st.info("Tidak ada pasien nonaktif yang bisa diaktifkan kembali.")
            else:
                pilihan = st.selectbox("Pilih ID Pasien", df_nonaktif["id"].astype(str))
                data_restore = df_nonaktif[df_nonaktif["id"].astype(str) == pilihan].iloc[0]

                st.write("### Detail Pasien yang akan diaktifkan kembali")
                st.json({
                    "ID": str(data_restore["id"]),
                    "Alergi Obat": alergi_obat_dict.get(data_restore["alergi_obat"], "Tidak Ada"),
                    "Alergi Makanan": alergi_makanan_dict.get(data_restore["alergi_makanan"], "Tidak Ada"),
                    "Anamnese": data_restore["anamnese"],
                    "Diagnose": data_restore["diagnose"],
                    "Pemeriksaan Fisik": data_restore["pemeriksaan_fisik"],
                    "Rencana": data_restore["rencana"],
                    "Treatment": treatment_dict.get(data_restore["treatment"], "Tidak Diketahui"),
                    "Obat": str(data_restore["obat"])
                })

                if st.button("✅ Konfirmasi Aktifkan", use_container_width=True, key="btn_aktif"):
                    df.loc[df["id"].astype(str) == pilihan, "status"] = "Aktif"
                    save_data(df)
                    st.session_state.success_msg = f"Pasien dengan ID {pilihan} berhasil diaktifkan kembali ✅"

        # === Notifikasi sukses ===
        if "success_msg" in st.session_state:
            st.success(st.session_state.success_msg)
            st.toast(st.session_state.success_msg)
            del st.session_state.success_msg

        #  === Tabel pasien nonaktif ===
        st.write("### 📋 Daftar Pasien Nonaktif")
        df_nonaktif_all = df[df["status"] == "Nonaktif"]

        if df_nonaktif_all.empty:
            st.info("Belum ada pasien yang dinonaktifkan.")
        else:
            # Buat versi tampilan tanpa kolom encode
            df_tampil = df_nonaktif_all.copy()
            df_tampil["id"] = df_tampil["id"].astype(str)
            df_tampil["Alergi Obat"] = df_tampil["alergi_obat"].map(alergi_obat_dict).fillna("Tidak Ada")
            df_tampil["Alergi Makanan"] = df_tampil["alergi_makanan"].map(alergi_makanan_dict).fillna("Tidak Ada")
            df_tampil["Treatment"] = df_tampil["treatment"].map(treatment_dict).fillna("Tidak Diketahui")

            # Pilih kolom penting saja
            kolom_tampil = ["id", "Alergi Obat", "Alergi Makanan", "Treatment", "anamnese",
                            "diagnose", "pemeriksaan_fisik", "rencana", "obat", "status"]
            st.dataframe(df_tampil[kolom_tampil], use_container_width=True, hide_index=True)

# === Mapping Encode Page ===
elif menu == "Mapping Encode":
    st.title("ℹ️ Keterangan Mapping Encode")
    
    st.info("📌 Halaman ini membantu memahami arti dari setiap kode pada dataset pasien.")

    # CSS agar isi tabel wrap dan terbaca penuh
    st.markdown("""
        <style>
        table td {
            white-space: normal !important;
            word-wrap: break-word !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Alergi Obat
    with st.expander("💊 Mapping Alergi Obat"):
        df_alergi_obat = pd.DataFrame(
            list(alergi_obat_dict.items()), 
            columns=["Kode", "Label"]
        )
        st.table(df_alergi_obat)

    # Alergi Makanan
    with st.expander("🍽️ Mapping Alergi Makanan"):
        df_alergi_makanan = pd.DataFrame(
            list(alergi_makanan_dict.items()), 
            columns=["Kode", "Label"]
        )
        st.table(df_alergi_makanan)

    # Treatment
    with st.expander("🩺 Mapping Treatment"):
        df_treatment = pd.DataFrame(
            list(treatment_dict.items()), 
            columns=["Kode", "Label"]
        )
        st.table(df_treatment)


