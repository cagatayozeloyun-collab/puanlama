import streamlit as st
import pandas as pd
import time
import random

# --- SAYFA AYARLARI VE GELİŞMİŞ CSS ---
st.set_page_config(page_title="YTÜ Cingen Oylama", layout="wide")

st.markdown("""
    <style>
    /* Genel Arka Plan */
    .main { background-color: #0e1117; color: #ffffff; }
    
    /* DEV BAŞLIK AYARI */
    .main-title {
        color: #e63946;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        font-size: 55px !important;
        font-weight: 900;
        margin-bottom: 30px;
        text-transform: uppercase;
        text-shadow: 3px 3px 10px rgba(230, 57, 70, 0.5);
    }

    /* Buton Tasarımları */
    .stButton>button { 
        width: 100%; border-radius: 12px; background-color: #e63946; 
        color: white; border: none; font-weight: bold; height: 3.8em; 
        font-size: 20px; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #ff4d5a; transform: scale(1.02); }

    /* Yarışmacı/Öğe Başlığı */
    .item-header { 
        color: #e63946; font-size: 55px; text-align: center; 
        font-weight: bold; text-transform: uppercase; margin: 25px 0; 
        border-bottom: 4px solid #e63946; letter-spacing: 3px;
    }

    /* BÜYÜTÜLMÜŞ SIRALAMA BALONU */
    .rank-info { 
        background-color: #1a1c24; padding: 40px; border-radius: 25px; 
        text-align: center; border: 3px solid #e63946; 
        font-size: 42px; font-weight: 900; color: #ffffff;
        margin: 30px 0; box-shadow: 0 0 30px rgba(230, 57, 70, 0.6);
        text-transform: uppercase;
    }
    
    /* Tablo Fontları */
    .stTable { font-size: 26px !important; }
    th { background-color: #e63946 !important; color: white !important; font-size: 28px !important; }
    td { font-size: 24px !important; font-weight: bold; }

    .jury-score-box { 
        background-color: #1a1c24; padding: 25px; border-radius: 15px; 
        border-top: 5px solid #e63946; margin: 10px 0; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# F1 Puanlama Sistemi
F1_POINTS = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# --- HAFIZA YÖNETİMİ ---
if 'all_votes' not in st.session_state: st.session_state.all_votes = []
if 'competitor_data' not in st.session_state:
    st.session_state.competitor_data = {}

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Ekip Paneli")
    new_item = st.text_input("Yarışmacı/Öğe Adı:")
    new_photo = st.text_input("Fotoğraf URL:")
    if st.button("Listeye Ekle") and new_item:
        st.session_
