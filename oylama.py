import streamlit as st
import pandas as pd
import time
import random

# --- SAYFA AYARLARI VE CSS ---
st.set_page_config(page_title="YTÜ Cingen Oylama", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    
    .main-title {
        color: #e63946; text-align: center; font-family: 'Arial Black', sans-serif;
        font-size: 42px !important; font-weight: 900; margin-bottom: 25px;
        text-transform: uppercase; text-shadow: 2px 2px 8px rgba(230, 57, 70, 0.5);
    }

    /* Görsel Boyutu */
    .competitor-img {
        border-radius: 15px; border: 3px solid #e63946;
        margin-bottom: 10px; max-width: 100%;
    }

    .item-header { 
        color: #e63946; font-size: 32px; font-weight: bold; 
        text-transform: uppercase; margin-bottom: 15px;
    }

    /* Puan Durumu Tablosu Stili */
    .stTable { font-size: 18px !important; }
    th { background-color: #e63946 !important; color: white !important; }
    
    /* Jüri Yazıları */
    .jury-text {
        font-size: 20px; font-weight: bold; margin-bottom: 8px;
        border-left: 4px solid #e63946; padding-left: 10px;
    }
    
    /* Canlı Sıralama Bilgisi */
    .live-rank {
        background-color: #e63946; color: white; padding: 10px;
        border-radius: 10px; text-align: center; font-size: 24px;
        font-weight: 900; margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# F1 Puanlama Sistemi
F1_POINTS = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# --- HAFIZA YÖNETİMİ ---
if 'all_votes' not in st.session_state: st.session_state.all_votes = []
if 'competitor_data' not in st.session_state: st.session_state.competitor_data = {}

# --- SIDEBAR ---
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

# DEV ANA BAŞLIK
st.markdown('<div class="main-title">YTÜ CİNGEN DÜĞÜN ORGANİZASYONLARI EKİBİ OYLUYOR</div>', unsafe_allow_html=True)

# --- 1. GİZLİ OYLAMA ---
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

# --- 2. SEREMONİ (YENİ 3'LÜ DÜZEN) ---
if st.button("🔥 SEREMONİYİ BAŞLAT"):
    if not st.session_state.all_votes:
        st.error("Henüz oy yok!")
    else:
        reveal_order = list(st.session_state.competitor_data.keys())
        random.shuffle(reveal_order)
        leaderboard = []

        # Sabit Puan Durumu Alanı Oluşturma
        st.divider()
        main_container = st.empty()

        for item in reveal_order:
            # Puan ve Sıralama Hesaplama
            total_p = 0
            ranks = []
            jury_details = []
            
            for vote in st.session_state.all_votes:
                r = vote['order'].index(item) + 1
                p = F1_POINTS.get(r, 0)
                total_p += p
                ranks.append(r)
                jury_details.append(f"{vote['voter']}: **+{p} Puan**")
            
            avg_r = sum(ranks) / len(ranks)
            leaderboard.append({"İsim": item, "Toplam Puan": total_p, "Ort. Sıra": round(avg_r, 2)})
            
            # Tabloyu Sırala
            current_df = pd.
