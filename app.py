# IMPORT LIBRARY
# ==============
import streamlit as st
import pandas as pd
import plotly.express as px

# PENGATURAN HALAMAN
# ==================
st.set_page_config(
    page_title="DALANG KEBUMEN",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS SEDERHANA
# =============
st.markdown("""
<style>

# Sembunyiin menu Streamlit
#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

# Hilangin padding atas
.block-container{
    padding-top:2rem;
    padding-bottom:1rem;
}

# Sidebar
section[data-testid="stSidebar"]{
    background-color:#F5F7FA;
}

# Turunin isi sidebar
section[data-testid="stSidebar"] > div:first-child{
    padding-top:60px;
}

# Judul Sidebar
section[data-testid="stSidebar"] h2{
    color:#0F4C81;
}

</style>
""", unsafe_allow_html=True)

# DASHBOARD
# =========
st.markdown("""
<div style="
background: linear-gradient(90deg, #1565C0 0%, #1E88E5 100%);
padding:14px 28px;
border-radius:15px;
box-shadow:0 4px 10px rgba(0,0,0,0.15);
margin-bottom:25px;
">

<div style="display:flex;justify-content:space-between;align-items:center;">
<div>

<h1 style="
margin:0;
color:white;
font-size:28px;
font-weight:bold;
">
📊 DALANG KEBUMEN
</h1>

<p style="
margin:4px 0;
font-size:17px;
color:white;
">
Dashboard Pelayanan Tera / Tera Ulang
</p>

<p style="
margin:0;
font-size:13px;
color:#EEF5FF;
">
UPTD Metrologi Legal Kabupaten Kebumen
</p>

</div>

<div style="
display:flex;
align-items:center;
gap:12px;
">

<img src="https://raw.githubusercontent.com/miftafadila-arch/dalangkebumen/main/logo.png"
         width="30">
<img src="https://raw.githubusercontent.com/miftafadila-arch/dalangkebumen/main/logometro-removebg-preview.png"
         width="40">

</div>

</div>

</div>
""", unsafe_allow_html=True)

# LINK GOOGLE SHEETS
# =====================
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT4IPCTLRaDiBtT1JA9-PhqO8AyCL213SRzUjze0nftzB9AH40bGck1apc5GTgQuVIYniGaWQsjG6VY/pub?output=csv"

# MEMBACA DATA
# ============
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL)
    return df

df = load_data()

# UBAH TIMESTAMP MENJADI DATETIME
# ===============================
df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    dayfirst=True,
    errors="coerce"
)

# HAPUS DATA YANG TIMESTAMP KOSONG (GA VALIDD)
df = df.dropna(subset=["Timestamp"])

# TAHUN
# =====
df["Tahun"] = df["Timestamp"].dt.year

# BULAN
# =====
df["Nomor Bulan"] = df["Timestamp"].dt.month

bulan_dict = {
    1: "Januari",
    2: "Februari",
    3: "Maret",
    4: "April",
    5: "Mei", 
    6: "Juni",
    7: "Juli",
    8: "Agustus",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Desember"
}

df["Bulan"] = df["Nomor Bulan"].map(bulan_dict)

# SIDEBAR
# =======
st.sidebar.markdown("## 📌 Filter")

st.sidebar.divider()

# FILTER TAHUN
# ============
tahun_list = sorted(df["Tahun"].unique())

pilih_tahun = st.sidebar.selectbox(
    "Pilih Tahun",
    tahun_list,
    index=len(tahun_list)-1
)

# FILTER BULAN
# ============
bulan_list = [
    "Semua",
    "Januari",
    "Februari",
    "Maret",
    "April",
    "Mei",
    "Juni",
    "Juli",
    "Agustus",
    "September",
    "Oktober",
    "November",
    "Desember"
]

pilih_bulan = st.sidebar.selectbox(
    "Pilih Bulan",
    bulan_list
)

# FILTER JENIS UTTP
# =================
jenis_list = sorted(
    df["Jenis UTTP"]
    .dropna()
    .unique()
    .tolist()
)

jenis_list.insert(0, "Semua")

pilih_jenis = st.sidebar.selectbox(
    "Jenis UTTP",
    jenis_list
)

# FILTER DATA
# ===========
df_filter = df.copy()

# Filter Tahun
df_filter = df_filter[
    df_filter["Tahun"] == pilih_tahun
]

# Filter Bulan
if pilih_bulan != "Semua":
    df_filter = df_filter[
        df_filter["Bulan"] == pilih_bulan
    ]

# Filter Jenis UTTP
if pilih_jenis != "Semua":
    df_filter = df_filter[
        df_filter["Jenis UTTP"] == pilih_jenis
    ]

# GRAFIK
# ======
grafik = (
    df_filter
    .groupby(
        ["Nomor Bulan", "Bulan", "Jenis UTTP"]
    )
    .size()
    .reset_index(name="Jumlah")
)

grafik = grafik.sort_values("Nomor Bulan")

# TOTAL PER BULAN
# ===============
total_bulan = (
    grafik
    .groupby(["Nomor Bulan", "Bulan"], as_index=False)["Jumlah"]
    .sum()
)

# CEK DATA
# ========
if grafik.empty:
    st.warning("Tidak ada data yang sesuai dengan filter.")
    st.stop()

# GRAFIK
# ======
fig = px.bar(

    grafik,

    x="Bulan",

    y="Jumlah",

    color="Jenis UTTP",

    barmode="stack",

    category_orders={
        "Bulan":[
            "Januari",
            "Februari",
            "Maret",
            "April",
            "Mei",
            "Juni",
            "Juli",
            "Agustus",
            "September",
            "Oktober",
            "November",
            "Desember"
        ]
    },

    color_discrete_sequence=[
    "#1565C0",
    "#42A5F5",
    "#66BB6A",
    "#FFA726",
    "#EF5350",
    "#AB47BC",
    "#26A69A",
    "#8D6E63"
]

)

for _, row in total_bulan.iterrows():

    fig.add_annotation(

        x=row["Bulan"],

        y=row["Jumlah"],

        text=f'{row["Jumlah"]}',

        showarrow=False,

        yshift=8,

        font=dict(
            size=14,
            color="black"
        )

    )

fig.update_xaxes(
    showline=True,
    linewidth=1,
    linecolor="#BDBDBD"
)

fig.update_yaxes(
    showline=True,
    linewidth=1,
    linecolor="#BDBDBD"
)

# ESTETIKA
# ========
fig.update_traces(
    hovertemplate=
    "<b>Bulan</b> : %{x}<br>"
    "<b>Jenis UTTP</b> : %{fullData.name}<br>"
    "<b>Jumlah</b> : %{y} Unit<extra></extra>"
)

fig.update_layout(

    template="plotly_white",

    xaxis_title="Bulan ke-",

    yaxis_title="Jumlah UTTP yang Tertera (Unit)",

    legend_title="Jenis UTTP",

    legend=dict(
    title="Jenis UTTP",
    orientation="v",
    y=1,
    yanchor="top",
    x=1.02,
    xanchor="left",
    bgcolor="rgba(0,0,0,0)",
    bordercolor="#DDDDDD",
    borderwidth=1
    ),

    height=650,

    plot_bgcolor="white",

    paper_bgcolor="white",

    hovermode="closest",

    font=dict(
        color="black",
        size=12
    ),

    margin=dict(
        l=40,
        r=40,
        t=40,
        b=40
    )

)

fig.update_yaxes(

    showgrid=True,

    gridcolor="#E5E5E5",

    zeroline=False

)

fig.update_xaxes(

    showgrid=False

)

st.plotly_chart(

    fig,

    use_container_width=True,

    config={
        "displaylogo":False,
        "responsive":True
    }

)
