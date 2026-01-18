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

# F1 Puan Tablosu
F1_POINTS = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# --- STATE YÖNETİMİ ---
if 'all_votes' not in st.session_state: st.session_state.all_votes = []
if 'competitor_data' not in st.session_state: st.session_state.competitor_data = {}

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Ekip Paneli")
    new_item = st.text_input("Yarışmacı Adı:")
    new_photo = st.file_uploader("Fotoğraf Yükle:", type=['jpg', 'jpeg', 'png'], key="uploader")
    if st.button("Listeye Ekle") and new_item:
        st.session_state.competitor_data[new_item] = new_photo
        st.success(f"{new_item} listeye alındı!")
    st.divider()
    if st.button("Hafızayı Temizle"):
        st.session_state.all_votes = []
        st.session_state.competitor_data = {}
        st.rerun()

# ANA BAŞLIK
st.markdown('<div class="main-title">YTÜ CİNGEN DÜĞÜN ORGANİZASYONLARI EKİBİ OYLUYOR</div>', unsafe_allow_html=True)

# --- OYLAMA ---
with st.expander("📝 Gizli Oylama Girişi"):
    voter = st.text_input("Jüri Adı:", key="voter_name")
    items = list(st.session_state.competitor_data.keys())
    if items:
        order = st.multiselect("Favoriden Sona Sırala:", items, default=items, key="vote_order")
        if st.button("Oyu Kaydet"):
            if voter and len(order) == len(items):
                st.session_state.all_votes.append({"voter": voter, "order": order})
                st.success("Oyun mahzene eklendi!")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("Lütfen adını yaz ve tüm yarışmacıları listeye ekle!")
    else:
        st.info("Önce sol taraftan yarışmacı eklemelisin.")

# --- SEREMONİ (Hata Korumalı) ---
if st.button("🔥 SEREMONİYİ BAŞLAT"):
    if not st.session_state.all_votes:
        st.error("Henüz kimse oy vermedi!")
    elif not st.session_state.competitor_data:
        st.error("Ortada yarışmacı yok!")
    else:
        reveal_list = list(st.session_state.competitor_data.keys())
        random.shuffle(reveal_list)
        leaderboard = []
        
        st.divider()
        display_area = st.empty()

        for current_item in reveal_list:
            total_score = 0
            rank_list = []
            jury_feedback = []
            
            # Puanları Hesapla
            for v_data in st.session_state.all_votes:
                if current_item in v_data['order']:
                    rank_num = v_data['order'].index(current_item) + 1
                    pts = F1_POINTS.get(rank_num, 0)
                else:
                    rank_num = 99
                    pts = 0
                
                total_score += pts
                rank_list.append(rank_num)
                jury_feedback.append(f"{v_data['voter']}: **+{pts} Puan**")
            
            # Liderlik Tablosunu Güncelle
            avg_rank = sum(rank_list) / len(rank_list) if rank_list else 99
            leaderboard.append({"İsim": current_item, "Puan": total_score, "Ort. Sıra": round(avg_rank, 2)})
            
            # DataFrame'i oluştur ve sırala
            current_leaderboard_df = pd.DataFrame(leaderboard).sort_values(
                by=["Puan", "Ort. Sıra"], ascending=[False, True]
            ).reset_index(drop=True)
            current_leaderboard_df.index += 1
            
            # Anlık konumu bul
            current_pos = current_leaderboard_df[current_leaderboard_df['İsim'] == current_item].index[0]

            # EKRANA BAS (77. Satır Civarındaki Hataları Önleyen Dinamik Yapı)
            with display_area.container():
                c1, c2, c3 = st.columns(
