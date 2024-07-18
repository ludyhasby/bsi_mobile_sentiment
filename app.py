import streamlit as st 
import pandas as pd
import numpy as np
from PIL import Image
import re # untuk findall
import base64
import requests

# data preparation
logo = Image.open("logo.png")
df = pd.read_csv('dataset_lengkap_belum_dibaca.csv')

# page config
st.set_page_config(
    page_icon="🗺️",
    page_title="Si Petualang"
)
# Use the following line to include your style.css file
st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def render_lottie(url, width, height):
    lottie_html = f"""
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.7.14/lottie.min.js"></script>
    </head>
    <body>
        <div id="lottie-container" style="width: {width}; height: {height};"></div>
        <script>
            var animation = lottie.loadAnimation({{
                container: document.getElementById('lottie-container'),
                renderer: 'svg',
                loop: true,
                autoplay: true,
                path: '{url}'
            }});
            animation.setRendererSettings({{
                preserveAspectRatio: 'xMidYMid slice',
                clearCanvas: true,
                progressiveLoad: false,
                hideOnTransparent: true
            }});
        </script>
    </body>
    </html>
    """
    return lottie_html

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

footer = """
footer{
    visibility:visible;
}
footer:after{
    content:'Copyright © 2024 Ludy Hasby';
    position:relative;
    color:black;
}
"""
lottie_coding = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_abqysclq.json")

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

def social_icons(width=24, height=24, **kwargs):
        icon_template = '''
        <a href="{url}" target="_blank" style="margin-right: 20px;">
            <img src="{icon_src}" alt="{alt_text}" width="{width}" height="{height}">
        </a>
        '''

        icons_html = ""
        for name, url in kwargs.items():
            icon_src = {
                "gmaps": "https://img.icons8.com/ios-filled/100/ff8c00/google-maps.png",
                "email": "https://cdn-icons-png.flaticon.com/512/561/561127.png"
            }.get(name.lower())

            if icon_src:
                icons_html += icon_template.format(url=url, icon_src=icon_src, alt_text=name.capitalize(), width=width, height=height)

        return icons_html
#####################


add_bg_from_local('bg3.png')   
text1, pict1 = st.columns((4,2))
with text1:
    st.title("Si Petualang")
    st.subheader("Formulasi Pembentukan Rute Baca Meter (RBM) Prabayar Berbasis Data Langganan")
with pict1:
    st.image(logo)

col_benar = ['lat', 'lon']
col_salah = ['KOORDINAT_X', 'KOORDINAT_Y']  # corrected the second element
df[col_benar] = df[col_salah]
df = df.drop(col_salah, axis=1)  # corrected to drop columns by their names directly

# # st.map(df[["lat", "lon"]])
# min_lat = df.lat.min()
# min_lon = df.lon.min()

tab1, tab2, tab3 = st.tabs(["Belum Dicari🌍", "Done✅", "Contact👋"])
with tab1:
    st.header("Visualisasi Progress Belum Dikunjungi")
    peran = ("Petugas", "Kordinator")
    option_peran = st.selectbox("Tentukan Peran anda", peran)
    if option_peran == "Petugas":
        st.write("Anda memilih peran Petugas, Silahkan isi Nama Petugas")
        nama_list = df['PETUGAS'].unique()
        option_nama = st.multiselect("Pilihan Nama Petugas", nama_list)
        st.subheader("Misi Anda Mengunjungi Rumah pada Koordinat sebagai berikut")
        dm = df[df["PETUGAS"].isin(option_nama)]
        st.map(dm[["lat", "lon"]], size=4)
        # st.table(dm)
    elif option_peran == "Kordinator":
        st.write("Anda memilih peran Koordinator, Silahkan isi Nama Koordinator")
        nama_list = df['KORDINATOR'].dropna().unique().tolist()
        option_nama = st.multiselect("Pilihan Nama Koordinator", nama_list)
        st.subheader("Pantau Petugas anda pada Koordinat sebagai berikut")
        dm = df[df["KORDINATOR"].isin(option_nama)]
        st.map(dm[["lat", "lon"]], size=4)
    
    st.subheader("Menampilkan Pelanggan Harus Dikunjungi")
    st.write("Data yang akan difilter adalah data sesuai dengan peran dan nama petugas/koordinator")
    dm['Google_Maps_Link'] = 'https://maps.google.com/?q=' + dm['lat'].astype(str) + ',' + dm['lon'].astype(str)
    col_pilih = ["IDPEL", "NAMA", "NAMAPNJ", "PETUGAS", "KORDINATOR", "NOMOR_METER_KWH", "NAMA_GARDU", "Google_Maps_Link", "lat", "lon"]
    col_pilih1 = ["IDPEL", "NAMA", "NAMAPNJ", "PETUGAS", "KORDINATOR", "NOMOR_METER_KWH", "NAMA_GARDU", "Google_Maps_Link"]
    data_tampil = dm[col_pilih]
    
    on = st.toggle('Tampilkan Tabel Sesuai dengan Peran dan Nama Pilihan')
    if on :
        st.write("Karena Data Terlalu besar, akan disajikan 50 Data dengan Indeks Teratas")
        st.table(data_tampil[col_pilih1].head(100))

    st.subheader("Fitur Filtering dan Akses Google Maps")
    filter = ("ID Pelanggan", "Nama Pelanggan", "Alamat", "Nomor Meter KWH", "Nama Gardu")
    filter_selected = st.selectbox("Tentukan Pencarian berdasar", filter)
    if filter_selected == "ID Pelanggan":
        idpel_list = data_tampil['IDPEL'].unique()
        option_idpel = st.multiselect("Pilihan ID Pelanggan", idpel_list)
        ds = data_tampil[data_tampil["IDPEL"].isin(option_idpel)]
    elif filter_selected == "Nama Pelanggan":
        idpel_list = data_tampil['NAMA'].unique()
        option_idpel = st.multiselect("Pilihan Nama Pelanggan", idpel_list)
        ds = data_tampil[data_tampil["NAMA"].isin(option_idpel)]
    elif filter_selected == "Alamat":
        idpel_list = data_tampil['NAMAPNJ'].unique()
        option_idpel = st.multiselect("Pilihan Alamat / Nama PNJ", idpel_list)
        ds = data_tampil[data_tampil["NAMAPNJ"].isin(option_idpel)]
    elif filter_selected == "Nomor Meter KWH":
        idpel_list = data_tampil['NOMOR_METER_KWH'].unique()
        option_idpel = st.multiselect("Pilihan Nomor Meter KWH", idpel_list)
        ds = data_tampil[data_tampil["NOMOR_METER_KWH"].isin(option_idpel)]
    elif filter_selected == "Nama Gardu":
        idpel_list = data_tampil['NAMA_GARDU'].unique()
        option_idpel = st.multiselect("Pilihan Nama Gardu", idpel_list)
        ds = data_tampil[data_tampil["NAMA_GARDU"].isin(option_idpel)]
        ds = ds.head(20)
    st.write("Untuk efisiensi mesin, tidak disarankan menggunakan pilihan nama gardu")
    for i in range(len(ds)):
        col1, col2 = st.columns((1,1))
        with col1:
            idpel = ds["IDPEL"].iloc[i]
            st.subheader(f"ID Pelanggan: {idpel}")
            detail = ds.iloc[i, :-3]
            st.table(detail)
            maps_link = ds["Google_Maps_Link"].iloc[i]
            st.write(f"[Go To Maps]({maps_link})")
            st.markdown(
            social_icons(50, 50, Gmaps = maps_link),
            unsafe_allow_html=True)
        with col2:
            st.write("Gambaran Koordinat")
            columns=['IDPEL','lat', 'lon']
            maps_i = ds[columns].iloc[i]
            maps_i_list = [maps_i] * 2
            maps_i = pd.DataFrame(maps_i_list, columns=['lat', 'lon'])
            st.map(maps_i, size=4)
    
    on_vis = st.toggle('Tampilkan Kompilasi Maps Hasil Filtering')
    if on_vis & len(ds) != 0:
        st.map(ds[["lat", "lon"]], size=4)
    else:
        st.write("Pastikan anda memilih lebih dari satu data")


with tab3:
    st.header("Penemuan Error, Saran, dan kritik 👋")
    st.markdown("Jika menemukan suatu kesalahan, saran, atau kritik silahkan menghubungi  Fauzi Hidayat di [Whatsapp ini](https://wa.me/6285217347978).")
    st.write("Alternatively, Silahkan hubungi saya di email")
    # linkedin_url = "https://www.linkedin.com/in/harrychangjr/"
    # github_url = "https://github.com/harrychangjr"
    email_url = "mailto:ludy.hasby@gmail.com"
    st.markdown(
        social_icons(32, 32, Email=email_url),
        unsafe_allow_html=True)
    st.markdown("")
st.markdown("*Copyright © 2024 Si Petualang*")
