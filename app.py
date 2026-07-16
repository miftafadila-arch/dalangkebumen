# IMPORT LIBRARY
# ==============
import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# FUNGSI MENGUBAH GAMBAR KE BASE
# ==============================
def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

background = get_base64("bg/logometro-removebg-preview.png")

# PENGATURAN HALAMAN
# ==================
st.set_page_config(
    page_title="DALANG KEBUMEN",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS SEDERHANA
# =============
st.markdown(f"""
<style>

/* Background Dashboard (Watermark) */
.stApp {{
    background-color: #F5F7FA;
}}

.stApp::before {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url("data:image/png;base64,{background}") center center no-repeat;
    background-size: 250px;
    opacity: 0.04;
    z-index: -1;
    pointer-events: none;
}}

/* Sembunyikan menu Streamlit */
#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

/* Hilangkan padding atas */
.block-container {{
    padding-top: 2rem;
    padding-bottom: 1rem;
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background-color: white;
}}

/* Turunkan isi sidebar */
section[data-testid="stSidebar"] > div:first-child {{
    padding-top: 60px;
}}

/* Judul Sidebar */
section[data-testid="stSidebar"] h2 {{
    color: #0F4C81;
}}

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

<div style="
display:flex;
align-items:center;
justify-content:space-between;
">

<!-- Logo Kiri -->
<div style="
width:90px;
display:flex;
justify-content:flex-start;
">
<img src="https://raw.githubusercontent.com/miftafadila-arch/dalangkebumen/main/logo.png"
    width="90">
</div>

<!-- Judul Tengah -->
<div style="
flex:1;
text-align:center;
">

<h1 style="
margin:0;
color:white;
font-size:40px;
font-weight:bold;
">
DALANG KEBUMEN
</h1>

<p style="
margin:2px 0;
font-size:25px;
color:white;
">
Dashboard Pelayanan Tera / Tera Ulang
</p>

<p style="
margin:2px 0 0 0;
font-size:20px;
color:#EEF5FF;
">
UPTD Metrologi Legal Kabupaten Kebumen
</p>

</div>

<!-- Logo Kanan -->
<div style="
width:90px;
display:flex;
justify-content:flex-end;
">
<img src="https://raw.githubusercontent.com/miftafadila-arch/dalangkebumen/main/logometro-removebg-preview.png"
    width="170">
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
    linecolor="black",
    tickfont=dict(
        color="black",
        size=12
    )
)

fig.update_yaxes(
    showline=True,
    linewidth=1,
    linecolor="black",
    tickfont=dict(
        color="black",
        size=12
    )
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
    
    xaxis_title_font=dict(
        color="black",
        size=16
    ),

    yaxis_title_font=dict(
        color="black",
        size=16
    ),

    legend_title="Jenis UTTP",

    legend=dict(
        title_font=dict(
            color="black",
            size=16
        ),
        font=dict(
            color="black",
            size=12
        ),
        orientation="v",
        y=1,
        yanchor="top",
        x=1.02,
        xanchor="left",
        bgcolor="rgba(0,0,0,0)",
        bordercolor="black",
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
