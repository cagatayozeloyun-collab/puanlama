import streamlit as st
import pandas as pd
import time
import random

# --- 1. TASARIM VE STİL AYARLARI ---
st.set_page_config(page_title="YTÜ CİNGEN OYLAMA", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0e1117; color: #ffffff; }
    .main-title {
        color: #e63946; text-align: center; font-family: 'Arial Black', sans-serif;
        font-size: 45px !important; font-weight: 900; margin-bottom: 30px;
        text-transform: uppercase; text-shadow: 2px 2px 10px rgba(230, 57, 70, 0.5);
    }
    .item-header { color: #e63946; font-size: 35px; font-weight: bold; text-transform: uppercase; margin-bottom: 15px; }
    .jury-text-box {
        font-size: 18px; font-weight: bold; margin-bottom: 8px;
        border-left: 5px solid #e63946; padding-left: 15px; background: #1a1c24;
        padding-top: 8px; padding-bottom: 8px; border-radius: 5px;
    }
    .live-rank-balon {
        background-color: #e63946; color: white; padding: 20px;
        border-radius: 15px; text-align: center; font-size: 32px;
        font-weight: 900; margin-top: 20px; box-shadow: 0 0 15px rgba(230,57,70,0.6);
        text-transform: uppercase;
    }
    .stTable { font-size: 18px !important; }
    th { background-color: #e63946 !important; color: white !important; font-size: 20px !important; }
    td { font-size: 18px !important; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 12px; background-color: #e63946; color: white; font-weight: bold; height: 3.5em; }
</style>
""", unsafe_allow_html=True)

# F1 PUAN SİSTEMİ
F1_POINTS = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# --- 2. VERİ YÖNETİMİ ---
if 'all_votes' not in st.session_state: st.session_state.all_votes = []
if 'competitor_data' not in st.session_state: st.session_state.competitor_data = {}

# --- 3. YÖNETİM PANELİ (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ ORGANİZASYON PANELİ")
    new_name = st.text_input("YARIŞMACI ADI:", key="sidebar_n_input")
    new_file = st.file_uploader("FOTOĞRAF SEÇ (Cİ
