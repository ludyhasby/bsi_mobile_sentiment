import streamlit as st
import plotly.express as px
from PIL import Image
import pandas as pd
from datetime import timedelta, date
from wordcloud import WordCloud
from streamlit_option_menu import option_menu

# page config
st.set_page_config(
    page_icon="🧩",
    page_title="Latent Dirichlet Analysis BSI Mobile", 
    layout = "wide"
)
## fungsi penting 
# highlight dataframe
def highlight_sentiment(s):
    return ['background-color: #c5e4e2']*len(s) if s.sentiment =="positive" else ['background-color: #ff7f7f']*len(s)
# wordcloud, distribusi sentiment, time series
def detail_topik(topik, nomorTopik, bg, lowerOrUpper, maksWord):
    st.subheader(f"Topik: {topik} \n dalam {PERIOD}")
    topik_df = df[df["Topic"]==topik]
    kolom1, kolom2 = st.columns(2)
    with kolom1:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        word_df = lda_cv[lda_cv["topic_no"]==nomorTopik][['decoding_kata', 'kontribusi']].head(maksWord)
        word_freq = dict(zip(word_df['decoding_kata'], word_df['kontribusi']))
        # text = " ".join(str(topik) for topik in word_cloud)
        if lowerOrUpper == "Lower":
            word_freq = {k.lower(): v for k, v in word_freq.items()}
        else:
            word_freq = {k.upper(): v for k, v in word_freq.items()}

        wc = WordCloud(background_color=bg, max_font_size= 300,  width=1600, 
                       height=800, max_words=maksWord).generate_from_frequencies(word_freq)
        st.image(wc.to_array(), use_column_width=True)
   
    with kolom2:
        sentiment = topik_df.groupby(["sentiment"]).size().reset_index()
        sentiment.columns = ["sentiment", "size"]
        fig = px.pie(sentiment, values='size', names='sentiment', color='sentiment', 
                    title=f'Distribusi Sentiment pada Topik: {topik}', 
                    color_discrete_map= {"negative": "#ff0000", "positive":"#3EA5A1"})
        
        fig.update_traces(textfont=dict(color="black"))

        st.plotly_chart(fig, theme="streamlit")
    
    sentiment_bulan = topik_df.groupby(['tahun_bulan_01', 'sentiment']).size().unstack(fill_value=0).reset_index()
    if 'negative' not in sentiment_bulan.columns:
        sentiment_bulan['negative'] = 0
    if 'positive' not in sentiment_bulan.columns:
        sentiment_bulan['positive'] = 0
    
    sentiment_bulan.rename({'tahun_bulan_01': 'Periode'}, axis=1, inplace=True)
    sentiment_bulan = pd.melt(sentiment_bulan, id_vars=['Periode'], var_name='Sentiment', value_name='Nilai')

    fig = px.bar(sentiment_bulan, x="Periode", y="Nilai",
            title = f"Perkembangan Sentiment pada Topik: {topik}",
            color="Sentiment",
            barmode = 'group', color_discrete_map={'positive':'#3EA5A1', 'negative':'#ff0000'})
    st.plotly_chart(fig, theme="streamlit")

    st.write(f"Ulasan Terbaru Terkait Topik: {topik}")
    contohUlasan = topik_df.sort_values(by = "datetime_baru", ascending=False)[["datetime_baru", "Sentences", "sentiment"]].head(10).reset_index(drop=True)
    contohUlasan.columns = ["timestamp", "ulasan", "sentiment"]
    st.dataframe(contohUlasan.style.apply(highlight_sentiment, axis=1))

def cariKata(kolom_list, key):
    # Check if the key is in the list
    return 1 if key in kolom_list else 0

# data preparation 
logo = Image.open("bsi.png")
lda_cv = pd.read_csv("lda_topics.csv")

df1 = pd.read_csv("dataset_siap_eksplorasi.csv")
df1["sumber"] = "ps"
df2 = pd.read_csv("ios_processing.csv")
df2["sumber"] = "as"
df = pd.concat([df1, df2])
# tambahan
def load_data(id, sheet_name)-> pd.DataFrame:
  url = f'https://docs.google.com/spreadsheets/d/{id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
  return pd.read_csv(url, parse_dates=[0, 1, 2, 3, 4], infer_datetime_format=True)
id = "1oTSMV4_VAoZEvU7-bHJLoKsg-mSGpFhxyFQLSOjl3VI"
sheet_name = "temp"
df1_tambahan = load_data(id, sheet_name)
df1_tambahan["datetime_baru"]= pd.to_datetime(df1_tambahan["datetime_baru"])
df1_tambahan["score"] = df1_tambahan["score"].astype(int)
df = pd.concat([df, df1_tambahan])

df["datetime_baru"] = pd.to_datetime(df["datetime_baru"]) 
df["tahun_bulan"] = df["datetime_baru"].dt.to_period('M')
df["tahun_bulan_01"] = pd.to_datetime(df["tahun_bulan"].astype(str) + "-01")
df["jam"] = df["datetime_baru"].dt.hour
df["bulan"] = df["datetime_baru"].dt.month
df["date_day"] = df["datetime_baru"].dt.day
df["dayNames"] = df["datetime_baru"].dt.day_name()
df["tanggal"] = df["datetime_baru"].dt.date
bsi_date = date.fromisoformat('2021-02-01')
df = df[df["tanggal"] >= bsi_date]

df["tahun"] = df["datetime_baru"].dt.year
minDate = min(df["tanggal"])
maksDate = max(df["tanggal"])

def social_icons(width=24, height=24, **kwargs):
        icon_template = '''
        <a href="{url}" target="_blank" style="margin-right: 20px;">
            <img src="{icon_src}" alt="{alt_text}" width="{width}" height="{height}">
        </a>
        '''

        icons_html = ""
        for name, url in kwargs.items():
            icon_src = {
                "linkedin": "https://img.icons8.com/ios-filled/100/ff8c00/linkedin.png",
                "github": "https://img.icons8.com/ios-filled/100/ff8c00/github--v2.png",
                "email": "https://img.icons8.com/ios-filled/100/ff8c00/filled-message.png"
            }.get(name.lower())

            if icon_src:
                icons_html += icon_template.format(url=url, icon_src=icon_src, alt_text=name.capitalize(), width=width, height=height)

        return icons_html
#####################
def penampilan_gangguan(nama_gangguan, bulan_hari, jumlah_data):
    if bulan_hari == "Bulanan":
        range_time = 'tahun_bulan_01'
    else:
        range_time = 'tanggal'
    if nama_gangguan == "Tidak Bisa Login":
        data = df_tidak_buka
        st.write("Note: Diterapkan jika timeout maka pasti tidak bisa login, dan tidak sebaliknya")
    elif nama_gangguan == "Susah digunakan":
        data = df_susah
    elif nama_gangguan == "Gangguan Transfer":
        data = df_transfer
    elif nama_gangguan == "Gangguan Update":
        data = df_update
    elif nama_gangguan == "Gangguan Transaksi":
        data = df_transaksi
    elif nama_gangguan == "Kehabisan Waktu":
        data = df_kehabisan_waktu
    elif nama_gangguan == "Gangguan Deteksi Wajah":
        data = df_wajah
    elif nama_gangguan == "Lambat Saat Digunakan":
        data = df_lambat
    elif nama_gangguan == "Force Close":
        data = df_fc
    
    # tampilkan time series nya 
    ts = data.groupby([f'{range_time}']).size().reset_index()
    ts.rename({f'{range_time}': 'Waktu Diskrit', 0:'Jumlah Ulasan'}, axis=1, inplace=True)
    fig = px.line(ts, x ='Waktu Diskrit', y=["Jumlah Ulasan"], title=f'Perkembangan Gangguan {nama_gangguan} dalam {PERIOD}', 
                    color_discrete_sequence=['#ff0000'])
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, theme="streamlit")
    # tampilkan contohnya 
    st.write(f"Contoh {jumlah_data} Data {nama_gangguan}")
    st.dataframe(data.head(jumlah_data)["Sentences"].reset_index(drop=True))


text1, pict1 = st.columns((4,2))
with text1:
    st.title("Latent Dirichlet Analysis")
    st.title("BSI Mobile")
    st.write(f"(Update {maksDate})")
with pict1:
    st.image(logo)
    st.write("Ludy Hasby Aulia - nMLE")

with st.sidebar:
    # with st.container():
    #     l, m, r= st.columns((1,3,1))
    #     with l:
    #          st.empty()
    #     with m:
    #          st.image(img_lh, width)
     choose = option_menu(
                        "Outline",
                        ["Distribusi Topik yang Sering Muncul", 
                         "Perkembangan Topik pada Ulasan BSI Mobile", 
                         "Detail Topik: Fitur Lengkap dan Memudahkan Transaksi",
                         "Detail Topik: Kenyamanan pada BSI Mobile",
                         "Detail Topik: BSI Mobile Susah digunakan dan Sering Eror", 
                         "Detail Topik: BSI Mobile Keren dan Lancar Digunakan",
                         "Detail Topik: Permasalahan pada BSI Mobile (Kode Aktivasi, Rekening)", 
                         "Detail Topik: Transaksi Nasabah pada BSI Mobile", 
                         "Detail Topik: Aplikasi Berguna tapi Ribet"],
                        icons =    ['bi bi-pie-chart', 
                                    'bi bi-bar-chart-line-fill', 
                                    'bi bi-emoji-laughing',
                                    'bi bi-check-circle', 
                                    'bi bi-bug', 
                                    'bi bi-emoji-sunglasses', 
                                    'bi bi-exclamation-diamond-fill',
                                    'bi bi-cash-coin',
                                    'bi bi-gear-wide-connected'],
                        menu_icon="mortadboard",
                        default_index=0,
                        styles={
        "container": {"padding": "0!important", "background-color": "#839E9E"},
        "icon": {"color": "darkorange", "font-size": "20px"}, 
        "nav-link": {"font-size": "17px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#5B6464"},
    }
    )
     st.write(":red[Note]: Mohon maaf Outline diatas tidak akan over anda ke halaman, hanya sebagai petunjuk ketersediaan fitur pada tab ini.")
     linkedin_url = "https://www.linkedin.com/in/ludy-hasby/"
     github_url = "https://github.com/ludyhasby"
     email_url = "mailto:ludy.hasby@gmail.com"

     with st.container():
        l, m, r = st.columns((0.11,2,0.1))
        with l:
            st.empty()
        with m:
            st.markdown(
                social_icons(30, 30, LinkedIn=linkedin_url, GitHub=github_url, Email=email_url),
                unsafe_allow_html=True)
        with r:
            st.empty()
        
        if choose == "Test":
            js = """
            <script>
            window.location.href = 'http://localhost:8501/#distribusi-rating-bsi-mobile';
            </script>
            """
            st.markdown(js, unsafe_allow_html=True)
PERIOD = st.selectbox("Filter Berdasar Waktu", options=["All Times", "2024", "Minggu Terakhir", "Custom Date", "Pilih Bulan"], index=0)
if PERIOD == "2024":
    df = df[df["datetime_baru"].dt.year==2024]
elif PERIOD == "Minggu Terakhir":
    BatasMinggu = maksDate - timedelta(days=7)
    df = df[(df["tanggal"]>=BatasMinggu) & (df["tanggal"]<=maksDate)]
    PERIOD = str(BatasMinggu) + " - "+ str(maksDate)
elif PERIOD == "Custom Date":
    start_date, end_date = st.date_input("For Custome Date, Pick a Date Please", (minDate, maksDate),min_value=minDate, max_value=maksDate)
    df = df[(df["tanggal"]>=start_date) & (df["tanggal"]<=end_date)]
    PERIOD = str(start_date) + " - "+ str(end_date)
elif PERIOD == "Pilih Bulan":
    bulan = st.multiselect("Pilih Nomor Bulan", options= sorted(df["bulan"].unique()), default=sorted(df["bulan"].unique()))
    st.caption("Notes: 1 = Januari, 12 = Desember, dst.")
    df = df[df["bulan"].isin(bulan)]
elif PERIOD == "All Times":
    PERIOD = PERIOD + " (" + str(minDate) + " - "+ str(maksDate) + ")"
tab1, tab2 = st.tabs(["Eksplorasi LDA Result🌍", "Permasalahan Umum pada BSI Mobile 🏫"])
with tab1:
    st.header("Topik Yang Sering Muncul berdasar LDA")
    kol1, kol2 = st.columns(2)
    with kol1:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.markdown("""
        - Transaksi Nasabah pada BSI Mobile \n
        - BSI Mobile Keren dan Lancar Digunakan \n
        - Kenyamanan pada BSI Mobile\n
        - BSI Mobile Susah digunakan dan Sering Eror\n
        - Aplikasi Berguna tapi Ribet\n
        - Permasalahan pada BSI Mobile (Kode Aktivasi, Rekening)\n
        - Fitur Lengkap dan Memudahkan Transaksi\n
""")
    with kol2:
        topic = df.groupby(["Topic"]).size().reset_index()
        topic.columns = ["topic_label", "jumlah"]
        fig = px.pie(topic, values='jumlah', names='topic_label', color='topic_label', 
                    title=f'Distribusi Topik BSI Mobile {PERIOD}')
        fig.update_traces(textfont=dict(color="black"))
        st.plotly_chart(fig, theme="streamlit")
    
    st.header(f"Perkembangan Topik pada BSI Mobile {PERIOD}")
    topik_bulan = df.groupby(['tahun_bulan_01', 'Topic']).size().unstack(fill_value=0).reset_index()
    topik_bulan.rename({'tahun_bulan_01': 'Periode'}, axis=1, inplace=True)
    topik_bulan = pd.melt(topik_bulan, id_vars=['Periode'], var_name='Topik', value_name='Nilai')
    fig = px.line(topik_bulan, x='Periode', y='Nilai', 
                        color='Topik')
    st.plotly_chart(fig)

    st.header("WordCloud dan Perkembangan Setiap Topik")
    cola, colb, colc = st.columns((2, 1, 1))
    with cola:
        maks_kata = st.select_slider("Jumlah Maksimum Kata", options=range(1, 100), value=25)
    with colb:
        lowerOrUpper = st.selectbox("Kapitalisasi Kata", options=["Lower", "Upper"])
    with colc:
        background = st.color_picker("Background Warna", value="#C5F5F0")

    # Fitur Lengkap dan Memudahkan Transaksi
    detail_topik("Fitur Lengkap dan Memudahkan Transaksi", 6, background, lowerOrUpper, maks_kata)
    # Kenyamanan pada BSI Mobile
    detail_topik("Kenyamanan pada BSI Mobile", 2, background, lowerOrUpper, maks_kata)
    # BSI Mobile Susah digunakan dan Sering Eror
    detail_topik("BSI Mobile Susah digunakan dan Sering Eror", 3, background, lowerOrUpper, maks_kata)
    # BSI Mobile Keren dan Lancar Digunakan
    detail_topik("BSI Mobile Keren dan Lancar Digunakan", 1, background, lowerOrUpper, maks_kata)
    # Permasalahan pada BSI Mobile (Kode Aktivasi, Rekening)
    detail_topik("Permasalahan pada BSI Mobile (Kode Aktivasi, Rekening)", 5, background, lowerOrUpper, maks_kata)
    # Transaksi Nasabah pada BSI Mobile
    detail_topik("Transaksi Nasabah pada BSI Mobile", 0, background, lowerOrUpper, maks_kata)
    # Aplikasi Berguna tapi Ribet
    detail_topik("Aplikasi Berguna tapi Ribet", 4, background, lowerOrUpper, maks_kata)

with tab2:
    st.title("Permasalahan Umum pada BSI Mobile")
    dict_gangguan={}
    ## Permintaan Kehabisan Waktu
    p_kw = r"\b(waktu|time|kehabisan)\w*"
    df_kehabisan_waktu = df[(df["Preprocess_Sentences"].str.contains(p_kw, regex=True, na=False)) & (df["sentiment"]=="negative")]
    dict_gangguan["Kehabisan Waktu"] = len(df_kehabisan_waktu)
    ## Tidak bisa Login 
    st.write("Catatan: Jika Timeout pasti tidak bisa login, namun tidak pasti sebaliknya")
    p_tidak_buka = r"\b(buka|bisa buka|login|masuk|waktu|time|kehabisan)\w*"
    df_tidak_buka = df[(df["Preprocess_Sentences"].str.contains(p_tidak_buka, regex=True, na=False)) & (df["sentiment"]=="negative")]
    dict_gangguan["Tidak Bisa Login"] = len(df_tidak_buka)
    ## Force Close 
    p_fc = r"\b(force|close|tutup paksa)\w*"
    df_fc = df[(df["Preprocess_Sentences"].str.contains(p_fc, regex=True, na=False)) & (df["sentiment"]=="negative")]
    dict_gangguan["Force Close"] = len(df_fc)
    ## Lambat, lemot
    p_lambat = r'\b(lambat|lemot|macet|lelet|pending|panding|lag|leg|bug)\w*'
    df_lambat = df[df["Preprocess_Sentences"].str.contains(p_lambat, regex=True, na=False) & (df["sentiment"] == "negative")]
    dict_gangguan["Lambat Saat Digunakan"] = len(df_lambat)
    ## Gangguan Deteksi Wajah, Verifikasi, Senyum
    p_wajah = r'\b(wajah|deteksi|verifikasi|senyum)\w*'
    df_wajah = df[df["Preprocess_Sentences"].str.contains(p_wajah, regex=True, na=False) & (df["sentiment"] == "negative")]
    dict_gangguan["Gangguan Deteksi Wajah"] = len(df_wajah)
    ## Sulit, Susah, Ribet
    p_susah = r"\b(sulit|susah|ribet)\w*"
    df_susah = df[df["Preprocess_Sentences"].str.contains(p_susah, regex=True, na=False) & (df["sentiment"]=="negative")]
    dict_gangguan["Susah digunakan"] = len(df_susah)
    ## gangguan transfer
    df_transfer = df[(df["Preprocess_Sentences"].str.contains(r"\btransfer\w*", regex=True, na=False)) & (df["sentiment"]=="negative")]
    dict_gangguan["Gangguan Transfer"] = len(df_transfer)
    ## gangguan Transaksi
    df_transaksi = df[df["Preprocess_Sentences"].str.contains(r"\btransaksi\w*", regex=True, na=False) & (df["sentiment"]=="negative")]
    dict_gangguan["Gangguan Transaksi"] = len(df_transaksi)
    ## Gangguan update, upgrade 
    p_update = r"\b(update|upgrade|pembaruan|upd)\w*"
    df_update = df[(df["Preprocess_Sentences"].str.contains(p_update, regex=True, na=False)) & (df["sentiment"]=="negative")]
    dict_gangguan["Gangguan Update"] = len(df_update)

    df_gangguan = pd.DataFrame(list(dict_gangguan.items()), columns=['Jenis Gangguan', 'Jumlah Ulasan'])
    st.dataframe(df_gangguan.sort_values("Jumlah Ulasan", ascending=False).reset_index(drop=True))
    k1, k2, k3 = st.columns(3)
    with k1:
        jenis_gangguan = st.selectbox(label="Jenis Gangguan", options=df_gangguan['Jenis Gangguan'].unique(), index=0)
    with k2:
        rentang_waktu = st.selectbox(label="Rentang Waktu", options=["Bulanan", "Harian"], index=0)
    with k3:
        banyak_contoh_data = st.number_input("Banyak contoh data untuk ditampilkan", value=15)
    penampilan_gangguan(jenis_gangguan, rentang_waktu, banyak_contoh_data)



st.markdown("*Copyright © 2024 Ludy Hasby Aulia*")