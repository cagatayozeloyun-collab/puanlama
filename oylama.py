import streamlit as st
import pandas as pd
import time
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="YTÜ Cingen Oylama", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .main-title {
        color: #e63946; text-align: center; font-family: 'Arial Black', sans-serif;
        font-size: 42px !important; font-weight: 900; margin-bottom: 25px;
        text-transform: uppercase; text-shadow: 2px 2px 8px rgba(230, 57, 70, 0.5);
    }
    .item-header { color: #e63946; font-size: 32px; font-weight: bold; text-transform: uppercase; margin-bottom: 15px; }
    .stTable { font-size: 18px !important; }
    th { background-color: #e63946 !important; color: white !important; }
    .jury-text { font-size: 20px; font-weight: bold; margin-bottom: 8px; border-left: 4px solid #e63946; padding-left: 10px; }
    .live-rank {
        background-color: #e63946; color: white; padding: 10px;
        border-radius: 10px; text-align: center; font-size: 24px;
        font-weight: 900; margin-top: 15px;
    }
    .stButton>button { width: 100%; border-radius: 12px; background-color: #e63946; color: white; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

F1_POINTS = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

if 'all_votes' not in st.session_state: st.session_state.all_votes = []
if 'competitor_data' not in st.session_state: st.session_state.competitor_data = {}

with st.sidebar:
    st.header("⚙️ Ekip Paneli")
    new_item = st.text_input("Yarışmacı Adı:")
    new_photo = st.file_uploader("Fotoğraf Yükle:", type=['jpg', 'jpeg', 'png'])
    if st.button("Listeye Ekle") and new_item:
        st.session_state.competitor_data[new_item] = new_photo
        st.success(f"{new_item} eklendi!")
    st.divider()
    if st.button("Hafızayı Temizle"):
        st.session_state.all_votes = []
        st.session_state.competitor_data = {}
        st.rerun()

st.markdown('<div class="main-title">YTÜ CİNGEN DÜĞÜN ORGANİZASYONLARI EKİBİ OYLUYOR</div>', unsafe_allow_html=True)

with st.expander("📝 Gizli Oylama Girişi"):
    voter = st.text_input("Jüri Adı:")
    items = list(st.session_state.competitor_data.keys())
    order = st.multiselect("Favoriden Sona Sırala:", items, default=items)
    if st.button("Oyu Kaydet"):
        if voter and len(order) == len(items) > 0:
            st.session_state.all_votes.append({"voter": voter, "order": order})
            st.success("Sisteme eklendi!")
            time.sleep(1)
            st.rerun()

if st.button("🔥 SEREMONİYİ BAŞLAT"):
    if not st.session_state.all_votes:
        st.error("Henüz oy yok!")
    else:
        reveal_order = list(st.session_state.competitor_data.keys())
        random.shuffle(reveal_order)
        leaderboard = []
        st.divider()
        main_container = st.empty()

        for item in reveal_order:
            total_p = 0
            ranks = []
            jury_details = []
            
            for vote in st.session_state.all_votes:
                # HATA ÖNLEYİCİ: Eğer item oylama listesinde yoksa 0 puan ver (ValueError engeller
